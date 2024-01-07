from markupsafe import Markup, escape
from flask import Flask, make_response, request
import io
import os
from tika import parser
from A_spacy_functions import extract_and_store_sections, dict_to_xml

A_spacy_flask_WS = Flask(__name__)

# Define a route for the POST method
@A_spacy_flask_WS.route('/DocExtractionPOC', methods=['POST'])
def process_pdf():
    try:
        # Get PDF file from the incoming POST request
        pdf_file = request.files['file']

        # Process the PDF file
        try:
            # Parse PDF content using tika
            parsed_pdf = parser.from_buffer(pdf_file.read())

            # Get the total number of pages
            total_pages = int(parsed_pdf['metadata']['xmpTPg:NPages'])

            # Initialize a dictionary to store text blocks
            text_blocks_dict = {}

            # Extract each page and store its content in the dictionary
            for page_num in range(1, total_pages + 1):
                page_content = parsed_pdf['content'].split('\n\n', page_num)[-1].strip()

                # Split the content into text blocks using new line as separator
                text_blocks = page_content.split('\n\n')

                # Store each section in the dictionary with only the section numbers as keys
                for section_num, text_block in enumerate(text_blocks, start=1):
                    section_key = int(section_num)
                    text_blocks_dict[section_key] = text_block


            # Sort the dictionaries by keys in numeric order
            sorted_sections_dict_test = {k: text_blocks_dict[k] for k in sorted(text_blocks_dict)}


            # Initialize strings to store the merged sections
            merged_sections = {"Header": "", "Item": "", "Footer": ""}

            # State variable to track the current section
            current_section = None

            # Iterate through the dictionary and concatenate each element to the appropriate section
            for key, value in sorted_sections_dict_test.items():
                # Check if the element starts with "Item"
                if value.startswith("Item"):
                    current_section = "Item"
                    merged_sections[current_section] += value + "\n"
                elif "___________" in value:
                    current_section = "Footer"
                    merged_sections[current_section] += value + "\n"
                elif current_section == "Item" or current_section == "Footer":
                    merged_sections[current_section] += value + "\n"
                else:
                    merged_sections["Header"] += value + "\n"

            for key in merged_sections:
                if(key!="Item"):
                    merged_sections[key] = merged_sections[key].replace('\n', ' ',-1)


            # Split the input text into lines
            lines = merged_sections["Item"].split('\n')

            # Create the sub-dictionary dynamically
            sub_dict = {}  # Initialize with the first line as ItemLabels

            # Initialize variables
            current_line = 0
            item_number = 10  # Initial item number

            # Handle the first item separately
            sub_dict["ItemLabels"] = lines[current_line]

            for i, line in enumerate(lines):
                if line.startswith(f"   {item_number}"):
                    # Skip the first iteration
                    if current_line != 0:
                        # Create a new element in the sub-dictionary
                        key = f"ItemNumber#{item_number-10}"  # Generate dynamic key (Element2, Element3, ...)
                        sub_dict[key] = "\n".join(lines[current_line:i])
                    current_line = i
                    item_number += 10  # Increment item number by 10 for the next iteration

            # Handle the last item
            key = f"ItemNumber#{item_number-10}"
            sub_dict[key] = "\n".join(lines[current_line:])

            training_raw_text={"Header":merged_sections["Header"],"Item":sub_dict,"Footer":merged_sections["Footer"]}

            #for key, value in training_raw_text.items():
                #print(f'{key}:\n{value}\n')



            import pickle
            # save the model to disk
            header_model_filename = 'model_header.pkl'
            item_model_filename = 'model_item.pkl'

            nlp_header = pickle.load(open(header_model_filename, 'rb'))
            nlp_item = pickle.load(open(item_model_filename, 'rb'))

            doc_header = nlp_header(training_raw_text["Header"])

            from collections import OrderedDict
            Dict = {}
            Dict = OrderedDict(Dict)

            for ent in doc_header.ents:
                Dict.update({ent.label_: ent.text})

            Dict_dict = {}  # Initialize an empty dictionary to store dictionaries

            for key, value in training_raw_text.get("Item", {}).items():
                if key.startswith('ItemNumber#'):
                    item_number = key.split('#')[1]

                    # Initialize a new sub-dictionary for each line item
                    Dict_Items = {}

                    doc_item = nlp_item(value)

                    for ent in doc_item.ents:
                        # Ensure that the key exists in Dict_Items and update it
                        Dict_Items.setdefault(ent.label_, []).append(ent.text)

                    # Add the sub-dictionary to the dictionary
                    Dict_dict[f"Item{item_number}"] = Dict_Items.copy()

            # 'Dict_dict' will now contain dictionaries, each corresponding to a line item with its associated entities
            Dict['Items'] = Dict_dict

                    
            Dict.update({"FooterText": training_raw_text["Footer"]})

            # Convert dictionary to XML
            root_element = dict_to_xml(Dict)

            # Print the XML
            import xml.etree.ElementTree as ET
            xml_str = ET.tostring(root_element.getroot(), encoding="unicode")


            return make_response(xml_str, 200)
        except Exception as e:
            print(f"Error: {str(e)}")
            return str(e), 500

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    A_spacy_flask_WS.run(host='0.0.0.0', port=5000, debug=True)
    #port = int(os.environ.get('PORT', 5000))
    #A_spacy_flask_WS.run(host='0.0.0.0', port=port)