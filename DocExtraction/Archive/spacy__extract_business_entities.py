import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_business_entities(text):
    # Process the text using spaCy
    doc = nlp(text)

    # Extract business entities
    business_entities = {
        "company_names": [],
        "locations": [],
        "dates": [],
        "persons": [],
        # Add more entity types as needed
    }

    for ent in doc.ents:
        if ent.label_ == "ORG":
            business_entities["company_names"].append(ent.text)
        elif ent.label_ == "GPE" or ent.label_ == "LOC":
            business_entities["locations"].append(ent.text)
        elif ent.label_ == "DATE":
            business_entities["dates"].append(ent.text)
        elif ent.label_ == "PERSON":
            business_entities["persons"].append(ent.text)

    return business_entities

# Example text
sample_text = "Apple Inc. is headquartered in Cupertino, California. The company was founded on April 1, 1976 by Steve Jobs."

# Extract business entities
result = extract_business_entities(sample_text)

# Display the extracted entities
print("Company Names:", result["company_names"])
print("Locations:", result["locations"])
print("Dates:", result["dates"])
print("Persons:", result["persons"])