import spacy
from spacy.training.example import Example

# Create a blank English model
nlp = spacy.blank("en")

# Add a new named entity label "ProgrammingLanguage"
ner = nlp.add_pipe("ner")
ner.add_label("ProgrammingLanguage")

# Prepare training data
training_data = [
    ("Python is a popular programming language.", {"entities": [(0, 6, "ProgrammingLanguage")]}),
    ("Java and JavaScript are widely used in web development.", {"entities": [(0, 4, "ProgrammingLanguage"), (9, 19, "ProgrammingLanguage")]}),
    ("C++ is often used in system programming.", {"entities": [(0, 3, "ProgrammingLanguage")]}),
    ("Ruby is known for its simplicity.", {"entities": [(0, 4, "ProgrammingLanguage")]}),
    ("HTML and CSS are essential for web design.", {"entities": [(0, 4, "ProgrammingLanguage"), (9, 12, "ProgrammingLanguage")]}),
    # Add more examples...
]

# Convert training data to spaCy format
train_examples = []
for text, annotations in training_data:
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, annotations)
    train_examples.append(example)

# Train the model
nlp.begin_training()
for epoch in range(100):  # Increase the number of epochs
    for example in train_examples:
        nlp.update([example], drop=0.5)

# Test the custom model
test_text = "My favourite computer coding tool is Java."
doc = nlp(test_text)
for ent in doc.ents:
    print(ent.text, ent.label_)
