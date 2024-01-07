from tika import parser


def extract_and_store_sections(pdf_path):
    # Parse the PDF using Tika
    parsed_pdf = parser.from_file(pdf_path)

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

    return text_blocks_dict


import xml.etree.ElementTree as ET

def dict_to_xml(dictionary, parent=None):
    """
    Convert a dictionary to XML.

    Args:
        dictionary (dict): The input dictionary.
        parent (Element, optional): The parent XML element. Defaults to None.

    Returns:
        Element: The root XML element.
    """
    if parent is None:
        root = ET.Element("MT_PurchaseOrder")
        dict_to_xml(dictionary, root)
        return ET.ElementTree(root)
    
    for key, value in dictionary.items():
        child = ET.SubElement(parent, str(key))
        if isinstance(value, dict):
            dict_to_xml(value, child)
        else:
            child.text = str(value)

    return parent