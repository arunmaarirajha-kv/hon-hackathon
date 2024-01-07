import pprint
import pickle

from A_spacy_functions import extract_and_store_sections

if __name__ == "__main__":
    pdf_path1 = '20221216105441_PURCHASE+ORDER+75450989.PDF'

    sections_dict1 = extract_and_store_sections(pdf_path1)

    print('\n')
    print("Tika output: ")
    pprint.pprint(sections_dict1)
    print('\n')

    #Sort the dictionaries by keys in numeric order
    sorted_sections_dict1 = {k: sections_dict1[k] for k in sorted(sections_dict1)}

# Initialize strings to store the merged sections
merged_sections = {"Header": "", "Item": "", "Footer": ""}
print('\n')
pprint.pprint(merged_sections)
print('\n')

# State variable to track the current section
current_section = None

# Iterate through the dictionary and concatenate each element to the appropriate section
for key, value in sorted_sections_dict1.items():
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

print('\n')
print('Header, Item & Footer grouped: ')
pprint.pprint(training_raw_text)
print('\n')

for key, value in training_raw_text.items():
    print(f'{key}:\n{value}\n')







import spacy
from spacy.training.example import Example

# Load a blank English model
nlp_header = spacy.blank("en")

# Declare new NER
ner = nlp_header.add_pipe("ner")
ner.add_label("POnumber")
ner.add_label("Date")
ner.add_label("VendorNumber")
ner.add_label("Currency")
ner.add_label("BillingAddress")
ner.add_label("VendorName")
ner.add_label("VendorAddress")
ner.add_label("VendorContact")
ner.add_label("BuyerName")
ner.add_label("Terms_of_delivery")
ner.add_label("Shipping_Address")
ner.add_label("Terms_of_Payment")

training_data = [
    (training_raw_text["Header"], {"entities": [
    (training_raw_text["Header"].find("75450989"), training_raw_text["Header"].find("75450989")+len("75450989"), "POnumber"),
    (training_raw_text["Header"].find("12.12.2022"), training_raw_text["Header"].find("12.12.2022")+len("12.12.2022"), "Date"), 
    (training_raw_text["Header"].find("10584"), training_raw_text["Header"].find("10584")+len("10584"), "VendorNumber"), 
    (training_raw_text["Header"].find("EUR"), training_raw_text["Header"].find("EUR")+len("EUR"), "Currency"),
    (training_raw_text["Header"].find("Brenntag Nederland B.V. Postbus 79 3300 AB  DORDRECHT NEDERLAND VAT nr: NL001375945B01 Mail: billing@brenntag.nl"), training_raw_text["Header"].find("Brenntag Nederland B.V. Postbus 79 3300 AB  DORDRECHT NEDERLAND VAT nr: NL001375945B01 Mail: billing@brenntag.nl")+len("Brenntag Nederland B.V. Postbus 79 3300 AB  DORDRECHT NEDERLAND VAT nr: NL001375945B01 Mail: billing@brenntag.nl"), "BillingAddress"),
    (training_raw_text["Header"].find("Honeywell Specialty Chem.  GmbH"), training_raw_text["Header"].find("Honeywell Specialty Chem.  GmbH")+len("Honeywell Specialty Chem.  GmbH"), "VendorName"), 
    (training_raw_text["Header"].find("Wunstorferstrasse 40 30926  SEELZE DUITSLAND"), training_raw_text["Header"].find("Wunstorferstrasse 40 30926  SEELZE DUITSLAND")+len("Wunstorferstrasse 40 30926  SEELZE DUITSLAND"), "VendorAddress"), 
    (training_raw_text["Header"].find("Contact: Corina Cosobea Tel.: +4940316306692 Email : Corina.Cosobea@honeywell.com"), training_raw_text["Header"].find("Contact: Corina Cosobea Tel.: +4940316306692 Email : Corina.Cosobea@honeywell.com")+len("Contact: Corina Cosobea Tel.: +4940316306692 Email : Corina.Cosobea@honeywell.com"), "VendorContact"), 
    (training_raw_text["Header"].find("Roy Brust"), training_raw_text["Header"].find("Roy Brust")+len("Roy Brust"), "BuyerName"), 
    (training_raw_text["Header"].find("DDP  Rotterdam-Botlek"), training_raw_text["Header"].find("DDP  Rotterdam-Botlek")+len("DDP  Rotterdam-Botlek"), "Terms_of_delivery"), 
    (training_raw_text["Header"].find("BRENNTAG Rotterdam-Botlek Chemieweg 9 3197 KC  ROTTERDAM-BOTLEK NEDERLAND"), training_raw_text["Header"].find("BRENNTAG Rotterdam-Botlek Chemieweg 9 3197 KC  ROTTERDAM-BOTLEK NEDERLAND")+len("BRENNTAG Rotterdam-Botlek Chemieweg 9 3197 KC  ROTTERDAM-BOTLEK NEDERLAND"), "Shipping_Address"), 
    (training_raw_text["Header"].find("8 DAYS 1,5%"), training_raw_text["Header"].find("8 DAYS 1,5%")+len("8 DAYS 1,5%"), "Terms_of_Payment"), 
    ]}),
    
    # Add more examples...

    (training_raw_text["Header"], {"entities": [
    (training_raw_text["Header"].find("75450989"), training_raw_text["Header"].find("75450989")+len("75450989"), "POnumber"),
    (training_raw_text["Header"].find("12.12.2022"), training_raw_text["Header"].find("12.12.2022")+len("12.12.2022"), "Date"), 
    (training_raw_text["Header"].find("10584"), training_raw_text["Header"].find("10584")+len("10584"), "VendorNumber"), 
    (training_raw_text["Header"].find("EUR"), training_raw_text["Header"].find("EUR")+len("EUR"), "Currency"),
    (training_raw_text["Header"].find("Brenntag Nederland B.V. Postbus 79 3300 AB  DORDRECHT NEDERLAND VAT nr: NL001375945B01 Mail: billing@brenntag.nl"), training_raw_text["Header"].find("Brenntag Nederland B.V. Postbus 79 3300 AB  DORDRECHT NEDERLAND VAT nr: NL001375945B01 Mail: billing@brenntag.nl")+len("Brenntag Nederland B.V. Postbus 79 3300 AB  DORDRECHT NEDERLAND VAT nr: NL001375945B01 Mail: billing@brenntag.nl"), "BillingAddress"),
    (training_raw_text["Header"].find("Honeywell Specialty Chem.  GmbH"), training_raw_text["Header"].find("Honeywell Specialty Chem.  GmbH")+len("Honeywell Specialty Chem.  GmbH"), "VendorName"), 
    (training_raw_text["Header"].find("Wunstorferstrasse 40 30926  SEELZE DUITSLAND"), training_raw_text["Header"].find("Wunstorferstrasse 40 30926  SEELZE DUITSLAND")+len("Wunstorferstrasse 40 30926  SEELZE DUITSLAND"), "VendorAddress"), 
    (training_raw_text["Header"].find("Contact: Corina Cosobea Tel.: +4940316306692 Email : Corina.Cosobea@honeywell.com"), training_raw_text["Header"].find("Contact: Corina Cosobea Tel.: +4940316306692 Email : Corina.Cosobea@honeywell.com")+len("Contact: Corina Cosobea Tel.: +4940316306692 Email : Corina.Cosobea@honeywell.com"), "VendorContact"), 
    (training_raw_text["Header"].find("Roy Brust"), training_raw_text["Header"].find("Roy Brust")+len("Roy Brust"), "BuyerName"), 
    (training_raw_text["Header"].find("DDP  Rotterdam-Botlek"), training_raw_text["Header"].find("DDP  Rotterdam-Botlek")+len("DDP  Rotterdam-Botlek"), "Terms_of_delivery"), 
    (training_raw_text["Header"].find("BRENNTAG Rotterdam-Botlek Chemieweg 9 3197 KC  ROTTERDAM-BOTLEK NEDERLAND"), training_raw_text["Header"].find("BRENNTAG Rotterdam-Botlek Chemieweg 9 3197 KC  ROTTERDAM-BOTLEK NEDERLAND")+len("BRENNTAG Rotterdam-Botlek Chemieweg 9 3197 KC  ROTTERDAM-BOTLEK NEDERLAND"), "Shipping_Address"), 
    (training_raw_text["Header"].find("8 DAYS 1,5%"), training_raw_text["Header"].find("8 DAYS 1,5%")+len("8 DAYS 1,5%"), "Terms_of_Payment"), 
    ]}),

    (training_raw_text["Header"], {"entities": [
    (training_raw_text["Header"].find("75450989"), training_raw_text["Header"].find("75450989")+len("75450989"), "POnumber"),
    (training_raw_text["Header"].find("12.12.2022"), training_raw_text["Header"].find("12.12.2022")+len("12.12.2022"), "Date"), 
    (training_raw_text["Header"].find("10584"), training_raw_text["Header"].find("10584")+len("10584"), "VendorNumber"), 
    (training_raw_text["Header"].find("EUR"), training_raw_text["Header"].find("EUR")+len("EUR"), "Currency"),
    (training_raw_text["Header"].find("Brenntag Nederland B.V. Postbus 79 3300 AB  DORDRECHT NEDERLAND VAT nr: NL001375945B01 Mail: billing@brenntag.nl"), training_raw_text["Header"].find("Brenntag Nederland B.V. Postbus 79 3300 AB  DORDRECHT NEDERLAND VAT nr: NL001375945B01 Mail: billing@brenntag.nl")+len("Brenntag Nederland B.V. Postbus 79 3300 AB  DORDRECHT NEDERLAND VAT nr: NL001375945B01 Mail: billing@brenntag.nl"), "BillingAddress"),
    (training_raw_text["Header"].find("Honeywell Specialty Chem.  GmbH"), training_raw_text["Header"].find("Honeywell Specialty Chem.  GmbH")+len("Honeywell Specialty Chem.  GmbH"), "VendorName"), 
    (training_raw_text["Header"].find("Wunstorferstrasse 40 30926  SEELZE DUITSLAND"), training_raw_text["Header"].find("Wunstorferstrasse 40 30926  SEELZE DUITSLAND")+len("Wunstorferstrasse 40 30926  SEELZE DUITSLAND"), "VendorAddress"), 
    (training_raw_text["Header"].find("Contact: Corina Cosobea Tel.: +4940316306692 Email : Corina.Cosobea@honeywell.com"), training_raw_text["Header"].find("Contact: Corina Cosobea Tel.: +4940316306692 Email : Corina.Cosobea@honeywell.com")+len("Contact: Corina Cosobea Tel.: +4940316306692 Email : Corina.Cosobea@honeywell.com"), "VendorContact"), 
    (training_raw_text["Header"].find("Roy Brust"), training_raw_text["Header"].find("Roy Brust")+len("Roy Brust"), "BuyerName"), 
    (training_raw_text["Header"].find("DDP  Rotterdam-Botlek"), training_raw_text["Header"].find("DDP  Rotterdam-Botlek")+len("DDP  Rotterdam-Botlek"), "Terms_of_delivery"), 
    (training_raw_text["Header"].find("BRENNTAG Rotterdam-Botlek Chemieweg 9 3197 KC  ROTTERDAM-BOTLEK NEDERLAND"), training_raw_text["Header"].find("BRENNTAG Rotterdam-Botlek Chemieweg 9 3197 KC  ROTTERDAM-BOTLEK NEDERLAND")+len("BRENNTAG Rotterdam-Botlek Chemieweg 9 3197 KC  ROTTERDAM-BOTLEK NEDERLAND"), "Shipping_Address"), 
    (training_raw_text["Header"].find("8 DAYS 1,5%"), training_raw_text["Header"].find("8 DAYS 1,5%")+len("8 DAYS 1,5%"), "Terms_of_Payment"), 
    ]}),

    (training_raw_text["Header"], {"entities": [
    (training_raw_text["Header"].find("75450989"), training_raw_text["Header"].find("75450989")+len("75450989"), "POnumber"),
    (training_raw_text["Header"].find("12.12.2022"), training_raw_text["Header"].find("12.12.2022")+len("12.12.2022"), "Date"), 
    (training_raw_text["Header"].find("10584"), training_raw_text["Header"].find("10584")+len("10584"), "VendorNumber"), 
    (training_raw_text["Header"].find("EUR"), training_raw_text["Header"].find("EUR")+len("EUR"), "Currency"),
    (training_raw_text["Header"].find("Brenntag Nederland B.V. Postbus 79 3300 AB  DORDRECHT NEDERLAND VAT nr: NL001375945B01 Mail: billing@brenntag.nl"), training_raw_text["Header"].find("Brenntag Nederland B.V. Postbus 79 3300 AB  DORDRECHT NEDERLAND VAT nr: NL001375945B01 Mail: billing@brenntag.nl")+len("Brenntag Nederland B.V. Postbus 79 3300 AB  DORDRECHT NEDERLAND VAT nr: NL001375945B01 Mail: billing@brenntag.nl"), "BillingAddress"),
    (training_raw_text["Header"].find("Honeywell Specialty Chem.  GmbH"), training_raw_text["Header"].find("Honeywell Specialty Chem.  GmbH")+len("Honeywell Specialty Chem.  GmbH"), "VendorName"), 
    (training_raw_text["Header"].find("Wunstorferstrasse 40 30926  SEELZE DUITSLAND"), training_raw_text["Header"].find("Wunstorferstrasse 40 30926  SEELZE DUITSLAND")+len("Wunstorferstrasse 40 30926  SEELZE DUITSLAND"), "VendorAddress"), 
    (training_raw_text["Header"].find("Contact: Corina Cosobea Tel.: +4940316306692 Email : Corina.Cosobea@honeywell.com"), training_raw_text["Header"].find("Contact: Corina Cosobea Tel.: +4940316306692 Email : Corina.Cosobea@honeywell.com")+len("Contact: Corina Cosobea Tel.: +4940316306692 Email : Corina.Cosobea@honeywell.com"), "VendorContact"), 
    (training_raw_text["Header"].find("Roy Brust"), training_raw_text["Header"].find("Roy Brust")+len("Roy Brust"), "BuyerName"), 
    (training_raw_text["Header"].find("DDP  Rotterdam-Botlek"), training_raw_text["Header"].find("DDP  Rotterdam-Botlek")+len("DDP  Rotterdam-Botlek"), "Terms_of_delivery"), 
    (training_raw_text["Header"].find("BRENNTAG Rotterdam-Botlek Chemieweg 9 3197 KC  ROTTERDAM-BOTLEK NEDERLAND"), training_raw_text["Header"].find("BRENNTAG Rotterdam-Botlek Chemieweg 9 3197 KC  ROTTERDAM-BOTLEK NEDERLAND")+len("BRENNTAG Rotterdam-Botlek Chemieweg 9 3197 KC  ROTTERDAM-BOTLEK NEDERLAND"), "Shipping_Address"), 
    (training_raw_text["Header"].find("8 DAYS 1,5%"), training_raw_text["Header"].find("8 DAYS 1,5%")+len("8 DAYS 1,5%"), "Terms_of_Payment"), 
    ]}),



]

print('\n')
print("Printing header training data\n")
pprint.pprint(training_data)
print('\n')

# Convert training data to spaCy format
train_examples = []
for text, annotations in training_data:
    doc = nlp_header.make_doc(text)
    example = Example.from_dict(doc, annotations)
    train_examples.append(example)

# Train the model
nlp_header.begin_training()
for epoch in range(100):  # Increase the number of epochs
    for example in train_examples:
        nlp_header.update([example], drop=0.5)

# save the model to disk
header_model_filename = 'model_header.pkl'
pickle.dump(nlp_header, open(header_model_filename, 'wb'))


nlp_item = spacy.blank("en")
ner_item = nlp_item.add_pipe("ner")
ner_item.add_label("Item")
ner_item.add_label("Material")
ner_item.add_label("Quantity")
ner_item.add_label("Price")
ner_item.add_label("Net_Amount")
ner_item.add_label("Item_Description")
ner_item.add_label("Additional_Item_Text1")
ner_item.add_label("Additional_Item_Text2")
ner_item.add_label("DeliveryDate")

ner_item.add_label("FooterText")

training_data_item = [
    (training_raw_text["Item"]["ItemNumber#10"], {"entities": [
    (training_raw_text["Item"]["ItemNumber#10"].find("10"), training_raw_text["Item"]["ItemNumber#10"].find("10")+len("10"), "Item"),
    (training_raw_text["Item"]["ItemNumber#10"].find("13081700"), training_raw_text["Item"]["ItemNumber#10"].find("13081700")+len("13081700"), "Material"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("420,00  KG"), training_raw_text["Item"]["ItemNumber#10"].find("420,00  KG")+len("420,00  KG"), "Quantity"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("315,00 /100  KG"), training_raw_text["Item"]["ItemNumber#10"].find("315,00 /100  KG")+len("315,00 /100  KG"), "Price"),
    (training_raw_text["Item"]["ItemNumber#10"].find("1.323,00"), training_raw_text["Item"]["ItemNumber#10"].find("1.323,00")+len("1.323,00"), "Net_Amount"),
    (training_raw_text["Item"]["ItemNumber#10"].find("HYDROGEN PEROXIDE 30% SLSI - DRUM 210KG\nEXPLOSIVES PRECURSOR (Regulation 2019/1148 EU)\n17303-10188775"), training_raw_text["Item"]["ItemNumber#10"].find("HYDROGEN PEROXIDE 30% SLSI - DRUM 210KG\nEXPLOSIVES PRECURSOR (Regulation 2019/1148 EU)\n17303-10188775")+len("HYDROGEN PEROXIDE 30% SLSI - DRUM 210KG\nEXPLOSIVES PRECURSOR (Regulation 2019/1148 EU)\n17303-10188775"), "Item_Description"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("timeslot needs to be booked 24 hours in\nThis can be done by using this link:\nhttps://tms.goramp.eu/app/timeslots/clients/c3200181-dfb1-4bc4-b3a9-98bb7382ec5b"), training_raw_text["Item"]["ItemNumber#10"].find("timeslot needs to be booked 24 hours in\nThis can be done by using this link:\nhttps://tms.goramp.eu/app/timeslots/clients/c3200181-dfb1-4bc4-b3a9-98bb7382ec5b")+len("timeslot needs to be booked 24 hours in\nThis can be done by using this link:\nhttps://tms.goramp.eu/app/timeslots/clients/c3200181-dfb1-4bc4-b3a9-98bb7382ec5b"), "Additional_Item_Text1"),
    (training_raw_text["Item"]["ItemNumber#10"].find("Please one batch per pallet and preferably one batch per order to deliver."), training_raw_text["Item"]["ItemNumber#10"].find("Please one batch per pallet and preferably one batch per order to deliver.")+len("Please one batch per pallet and preferably one batch per order to deliver."), "Additional_Item_Text2"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("15.02.2023 at 00:00"), training_raw_text["Item"]["ItemNumber#10"].find("15.02.2023 at 00:00")+len("15.02.2023 at 00:00"), "DeliveryDate"), 
    ]}),

    (training_raw_text["Item"]["ItemNumber#20"], {"entities": [
    (training_raw_text["Item"]["ItemNumber#20"].find("20"), training_raw_text["Item"]["ItemNumber#20"].find("20")+len("20"), "Item"),
    (training_raw_text["Item"]["ItemNumber#20"].find("16683700"), training_raw_text["Item"]["ItemNumber#20"].find("16683700")+len("16683700"), "Material"), 
    (training_raw_text["Item"]["ItemNumber#20"].find("35,00  KG"), training_raw_text["Item"]["ItemNumber#20"].find("35,00  KG")+len("35,00  KG"), "Quantity"), 
    (training_raw_text["Item"]["ItemNumber#20"].find("691,00 /100  KG"), training_raw_text["Item"]["ItemNumber#20"].find("691,00 /100  KG")+len("691,00 /100  KG"), "Price"),
    (training_raw_text["Item"]["ItemNumber#20"].find("241,85"), training_raw_text["Item"]["ItemNumber#20"].find("241,85")+len("241,85"), "Net_Amount"),
    (training_raw_text["Item"]["ItemNumber#20"].find("TETRAFLUOROBORIC ACID 50% - DRUM 35KG\n01544-10185261"), training_raw_text["Item"]["ItemNumber#20"].find("TETRAFLUOROBORIC ACID 50% - DRUM 35KG\n01544-10185261")+len("TETRAFLUOROBORIC ACID 50% - DRUM 35KG\n01544-10185261"), "Item_Description"), 
    (training_raw_text["Item"]["ItemNumber#20"].find("Please one batch per pallet and preferably one batch per order to deliver."), training_raw_text["Item"]["ItemNumber#20"].find("Please one batch per pallet and preferably one batch per order to deliver.")+len("Please one batch per pallet and preferably one batch per order to deliver."), "Additional_Item_Text1"),
    (training_raw_text["Item"]["ItemNumber#20"].find("22.12.2022 at 00:00"), training_raw_text["Item"]["ItemNumber#20"].find("22.12.2022 at 00:00")+len("22.12.2022 at 00:00"), "DeliveryDate"), 
    ]}),
    
    # Add more examples...

    (training_raw_text["Item"]["ItemNumber#10"], {"entities": [
    (training_raw_text["Item"]["ItemNumber#10"].find("10"), training_raw_text["Item"]["ItemNumber#10"].find("10")+len("10"), "Item"),
    (training_raw_text["Item"]["ItemNumber#10"].find("13081700"), training_raw_text["Item"]["ItemNumber#10"].find("13081700")+len("13081700"), "Material"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("420,00  KG"), training_raw_text["Item"]["ItemNumber#10"].find("420,00  KG")+len("420,00  KG"), "Quantity"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("315,00 /100  KG"), training_raw_text["Item"]["ItemNumber#10"].find("315,00 /100  KG")+len("315,00 /100  KG"), "Price"),
    (training_raw_text["Item"]["ItemNumber#10"].find("1.323,00"), training_raw_text["Item"]["ItemNumber#10"].find("1.323,00")+len("1.323,00"), "Net_Amount"),
    (training_raw_text["Item"]["ItemNumber#10"].find("HYDROGEN PEROXIDE 30% SLSI - DRUM 210KG\nEXPLOSIVES PRECURSOR (Regulation 2019/1148 EU)\n17303-10188775"), training_raw_text["Item"]["ItemNumber#10"].find("HYDROGEN PEROXIDE 30% SLSI - DRUM 210KG\nEXPLOSIVES PRECURSOR (Regulation 2019/1148 EU)\n17303-10188775")+len("HYDROGEN PEROXIDE 30% SLSI - DRUM 210KG\nEXPLOSIVES PRECURSOR (Regulation 2019/1148 EU)\n17303-10188775"), "Item_Description"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("timeslot needs to be booked 24 hours in\nThis can be done by using this link:\nhttps://tms.goramp.eu/app/timeslots/clients/c3200181-dfb1-4bc4-b3a9-98bb7382ec5b"), training_raw_text["Item"]["ItemNumber#10"].find("timeslot needs to be booked 24 hours in\nThis can be done by using this link:\nhttps://tms.goramp.eu/app/timeslots/clients/c3200181-dfb1-4bc4-b3a9-98bb7382ec5b")+len("timeslot needs to be booked 24 hours in\nThis can be done by using this link:\nhttps://tms.goramp.eu/app/timeslots/clients/c3200181-dfb1-4bc4-b3a9-98bb7382ec5b"), "Additional_Item_Text1"),
    (training_raw_text["Item"]["ItemNumber#10"].find("Please one batch per pallet and preferably one batch per order to deliver."), training_raw_text["Item"]["ItemNumber#10"].find("Please one batch per pallet and preferably one batch per order to deliver.")+len("Please one batch per pallet and preferably one batch per order to deliver."), "Additional_Item_Text2"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("15.02.2023 at 00:00"), training_raw_text["Item"]["ItemNumber#10"].find("15.02.2023 at 00:00")+len("15.02.2023 at 00:00"), "DeliveryDate"), 
    ]}),

    (training_raw_text["Item"]["ItemNumber#20"], {"entities": [
    (training_raw_text["Item"]["ItemNumber#20"].find("20"), training_raw_text["Item"]["ItemNumber#20"].find("20")+len("20"), "Item"),
    (training_raw_text["Item"]["ItemNumber#20"].find("16683700"), training_raw_text["Item"]["ItemNumber#20"].find("16683700")+len("16683700"), "Material"), 
    (training_raw_text["Item"]["ItemNumber#20"].find("35,00  KG"), training_raw_text["Item"]["ItemNumber#20"].find("35,00  KG")+len("35,00  KG"), "Quantity"), 
    (training_raw_text["Item"]["ItemNumber#20"].find("691,00 /100  KG"), training_raw_text["Item"]["ItemNumber#20"].find("691,00 /100  KG")+len("691,00 /100  KG"), "Price"),
    (training_raw_text["Item"]["ItemNumber#20"].find("241,85"), training_raw_text["Item"]["ItemNumber#20"].find("241,85")+len("241,85"), "Net_Amount"),
    (training_raw_text["Item"]["ItemNumber#20"].find("TETRAFLUOROBORIC ACID 50% - DRUM 35KG\n01544-10185261"), training_raw_text["Item"]["ItemNumber#20"].find("TETRAFLUOROBORIC ACID 50% - DRUM 35KG\n01544-10185261")+len("TETRAFLUOROBORIC ACID 50% - DRUM 35KG\n01544-10185261"), "Item_Description"), 
    (training_raw_text["Item"]["ItemNumber#20"].find("Please one batch per pallet and preferably one batch per order to deliver."), training_raw_text["Item"]["ItemNumber#20"].find("Please one batch per pallet and preferably one batch per order to deliver.")+len("Please one batch per pallet and preferably one batch per order to deliver."), "Additional_Item_Text1"),
    (training_raw_text["Item"]["ItemNumber#20"].find("22.12.2022 at 00:00"), training_raw_text["Item"]["ItemNumber#20"].find("22.12.2022 at 00:00")+len("22.12.2022 at 00:00"), "DeliveryDate"), 
    ]}),

    (training_raw_text["Item"]["ItemNumber#10"], {"entities": [
    (training_raw_text["Item"]["ItemNumber#10"].find("10"), training_raw_text["Item"]["ItemNumber#10"].find("10")+len("10"), "Item"),
    (training_raw_text["Item"]["ItemNumber#10"].find("13081700"), training_raw_text["Item"]["ItemNumber#10"].find("13081700")+len("13081700"), "Material"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("420,00  KG"), training_raw_text["Item"]["ItemNumber#10"].find("420,00  KG")+len("420,00  KG"), "Quantity"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("315,00 /100  KG"), training_raw_text["Item"]["ItemNumber#10"].find("315,00 /100  KG")+len("315,00 /100  KG"), "Price"),
    (training_raw_text["Item"]["ItemNumber#10"].find("1.323,00"), training_raw_text["Item"]["ItemNumber#10"].find("1.323,00")+len("1.323,00"), "Net_Amount"),
    (training_raw_text["Item"]["ItemNumber#10"].find("HYDROGEN PEROXIDE 30% SLSI - DRUM 210KG\nEXPLOSIVES PRECURSOR (Regulation 2019/1148 EU)\n17303-10188775"), training_raw_text["Item"]["ItemNumber#10"].find("HYDROGEN PEROXIDE 30% SLSI - DRUM 210KG\nEXPLOSIVES PRECURSOR (Regulation 2019/1148 EU)\n17303-10188775")+len("HYDROGEN PEROXIDE 30% SLSI - DRUM 210KG\nEXPLOSIVES PRECURSOR (Regulation 2019/1148 EU)\n17303-10188775"), "Item_Description"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("timeslot needs to be booked 24 hours in\nThis can be done by using this link:\nhttps://tms.goramp.eu/app/timeslots/clients/c3200181-dfb1-4bc4-b3a9-98bb7382ec5b"), training_raw_text["Item"]["ItemNumber#10"].find("timeslot needs to be booked 24 hours in\nThis can be done by using this link:\nhttps://tms.goramp.eu/app/timeslots/clients/c3200181-dfb1-4bc4-b3a9-98bb7382ec5b")+len("timeslot needs to be booked 24 hours in\nThis can be done by using this link:\nhttps://tms.goramp.eu/app/timeslots/clients/c3200181-dfb1-4bc4-b3a9-98bb7382ec5b"), "Additional_Item_Text1"),
    (training_raw_text["Item"]["ItemNumber#10"].find("Please one batch per pallet and preferably one batch per order to deliver."), training_raw_text["Item"]["ItemNumber#10"].find("Please one batch per pallet and preferably one batch per order to deliver.")+len("Please one batch per pallet and preferably one batch per order to deliver."), "Additional_Item_Text2"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("15.02.2023 at 00:00"), training_raw_text["Item"]["ItemNumber#10"].find("15.02.2023 at 00:00")+len("15.02.2023 at 00:00"), "DeliveryDate"), 
    ]}),

    (training_raw_text["Item"]["ItemNumber#20"], {"entities": [
    (training_raw_text["Item"]["ItemNumber#20"].find("20"), training_raw_text["Item"]["ItemNumber#20"].find("20")+len("20"), "Item"),
    (training_raw_text["Item"]["ItemNumber#20"].find("16683700"), training_raw_text["Item"]["ItemNumber#20"].find("16683700")+len("16683700"), "Material"), 
    (training_raw_text["Item"]["ItemNumber#20"].find("35,00  KG"), training_raw_text["Item"]["ItemNumber#20"].find("35,00  KG")+len("35,00  KG"), "Quantity"), 
    (training_raw_text["Item"]["ItemNumber#20"].find("691,00 /100  KG"), training_raw_text["Item"]["ItemNumber#20"].find("691,00 /100  KG")+len("691,00 /100  KG"), "Price"),
    (training_raw_text["Item"]["ItemNumber#20"].find("241,85"), training_raw_text["Item"]["ItemNumber#20"].find("241,85")+len("241,85"), "Net_Amount"),
    (training_raw_text["Item"]["ItemNumber#20"].find("TETRAFLUOROBORIC ACID 50% - DRUM 35KG\n01544-10185261"), training_raw_text["Item"]["ItemNumber#20"].find("TETRAFLUOROBORIC ACID 50% - DRUM 35KG\n01544-10185261")+len("TETRAFLUOROBORIC ACID 50% - DRUM 35KG\n01544-10185261"), "Item_Description"), 
    (training_raw_text["Item"]["ItemNumber#20"].find("Please one batch per pallet and preferably one batch per order to deliver."), training_raw_text["Item"]["ItemNumber#20"].find("Please one batch per pallet and preferably one batch per order to deliver.")+len("Please one batch per pallet and preferably one batch per order to deliver."), "Additional_Item_Text1"),
    (training_raw_text["Item"]["ItemNumber#20"].find("22.12.2022 at 00:00"), training_raw_text["Item"]["ItemNumber#20"].find("22.12.2022 at 00:00")+len("22.12.2022 at 00:00"), "DeliveryDate"), 
    ]}),

    (training_raw_text["Item"]["ItemNumber#10"], {"entities": [
    (training_raw_text["Item"]["ItemNumber#10"].find("10"), training_raw_text["Item"]["ItemNumber#10"].find("10")+len("10"), "Item"),
    (training_raw_text["Item"]["ItemNumber#10"].find("13081700"), training_raw_text["Item"]["ItemNumber#10"].find("13081700")+len("13081700"), "Material"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("420,00  KG"), training_raw_text["Item"]["ItemNumber#10"].find("420,00  KG")+len("420,00  KG"), "Quantity"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("315,00 /100  KG"), training_raw_text["Item"]["ItemNumber#10"].find("315,00 /100  KG")+len("315,00 /100  KG"), "Price"),
    (training_raw_text["Item"]["ItemNumber#10"].find("1.323,00"), training_raw_text["Item"]["ItemNumber#10"].find("1.323,00")+len("1.323,00"), "Net_Amount"),
    (training_raw_text["Item"]["ItemNumber#10"].find("HYDROGEN PEROXIDE 30% SLSI - DRUM 210KG\nEXPLOSIVES PRECURSOR (Regulation 2019/1148 EU)\n17303-10188775"), training_raw_text["Item"]["ItemNumber#10"].find("HYDROGEN PEROXIDE 30% SLSI - DRUM 210KG\nEXPLOSIVES PRECURSOR (Regulation 2019/1148 EU)\n17303-10188775")+len("HYDROGEN PEROXIDE 30% SLSI - DRUM 210KG\nEXPLOSIVES PRECURSOR (Regulation 2019/1148 EU)\n17303-10188775"), "Item_Description"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("timeslot needs to be booked 24 hours in\nThis can be done by using this link:\nhttps://tms.goramp.eu/app/timeslots/clients/c3200181-dfb1-4bc4-b3a9-98bb7382ec5b"), training_raw_text["Item"]["ItemNumber#10"].find("timeslot needs to be booked 24 hours in\nThis can be done by using this link:\nhttps://tms.goramp.eu/app/timeslots/clients/c3200181-dfb1-4bc4-b3a9-98bb7382ec5b")+len("timeslot needs to be booked 24 hours in\nThis can be done by using this link:\nhttps://tms.goramp.eu/app/timeslots/clients/c3200181-dfb1-4bc4-b3a9-98bb7382ec5b"), "Additional_Item_Text1"),
    (training_raw_text["Item"]["ItemNumber#10"].find("Please one batch per pallet and preferably one batch per order to deliver."), training_raw_text["Item"]["ItemNumber#10"].find("Please one batch per pallet and preferably one batch per order to deliver.")+len("Please one batch per pallet and preferably one batch per order to deliver."), "Additional_Item_Text2"), 
    (training_raw_text["Item"]["ItemNumber#10"].find("15.02.2023 at 00:00"), training_raw_text["Item"]["ItemNumber#10"].find("15.02.2023 at 00:00")+len("15.02.2023 at 00:00"), "DeliveryDate"), 
    ]}),

    (training_raw_text["Item"]["ItemNumber#20"], {"entities": [
    (training_raw_text["Item"]["ItemNumber#20"].find("20"), training_raw_text["Item"]["ItemNumber#20"].find("20")+len("20"), "Item"),
    (training_raw_text["Item"]["ItemNumber#20"].find("16683700"), training_raw_text["Item"]["ItemNumber#20"].find("16683700")+len("16683700"), "Material"), 
    (training_raw_text["Item"]["ItemNumber#20"].find("35,00  KG"), training_raw_text["Item"]["ItemNumber#20"].find("35,00  KG")+len("35,00  KG"), "Quantity"), 
    (training_raw_text["Item"]["ItemNumber#20"].find("691,00 /100  KG"), training_raw_text["Item"]["ItemNumber#20"].find("691,00 /100  KG")+len("691,00 /100  KG"), "Price"),
    (training_raw_text["Item"]["ItemNumber#20"].find("241,85"), training_raw_text["Item"]["ItemNumber#20"].find("241,85")+len("241,85"), "Net_Amount"),
    (training_raw_text["Item"]["ItemNumber#20"].find("TETRAFLUOROBORIC ACID 50% - DRUM 35KG\n01544-10185261"), training_raw_text["Item"]["ItemNumber#20"].find("TETRAFLUOROBORIC ACID 50% - DRUM 35KG\n01544-10185261")+len("TETRAFLUOROBORIC ACID 50% - DRUM 35KG\n01544-10185261"), "Item_Description"), 
    (training_raw_text["Item"]["ItemNumber#20"].find("Please one batch per pallet and preferably one batch per order to deliver."), training_raw_text["Item"]["ItemNumber#20"].find("Please one batch per pallet and preferably one batch per order to deliver.")+len("Please one batch per pallet and preferably one batch per order to deliver."), "Additional_Item_Text1"),
    (training_raw_text["Item"]["ItemNumber#20"].find("22.12.2022 at 00:00"), training_raw_text["Item"]["ItemNumber#20"].find("22.12.2022 at 00:00")+len("22.12.2022 at 00:00"), "DeliveryDate"), 
    ]}),


]

print('\n')
print("Printing item training data\n")
pprint.pprint(training_data_item)
print('\n')


# Convert training data to spaCy format
train_examples_item = []
for text, annotations in training_data_item:
    doc = nlp_item.make_doc(text)
    example = Example.from_dict(doc, annotations)
    train_examples_item.append(example)


# Train the model
nlp_item.begin_training()
for epoch in range(100):  # Increase the number of epochs
    for example in train_examples_item:
        nlp_item.update([example], drop=0.5)

# save the model to disk
item_model_filename = 'model_item.pkl'
pickle.dump(nlp_item, open(item_model_filename, 'wb'))
