import spacy

# Load the English model
nlp = spacy.load("en_core_web_md")

# Process a string
doc = nlp(
    "Mumbai is looking at buying a Adani's airport startup for $1 billion in 10 years"
)

# Print entities
for ent in doc.ents:
    print(ent.text, ent.label_)
