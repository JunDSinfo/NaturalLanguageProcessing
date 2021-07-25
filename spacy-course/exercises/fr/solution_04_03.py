import json
from spacy.matcher import Matcher
from spacy.lang.fr import French

with open("exercises/fr/iphone.json", encoding="utf8") as f:
    TEXTS = json.loads(f.read())

nlp = French()
matcher = Matcher(nlp.vocab)

# Deux tokens dont les formes majuscules correspondent à "iphone" et "x"
pattern1 = [{"LOWER": "iphone"}, {"LOWER": "x"}]

# Tokens dont les formes majuscules correspondent à "iphone" et un nombre
pattern2 = [{"LOWER": "iphone"}, {"IS_DIGIT": True}]

# Ajoute les motifs au matcher et vérifie le résultat
matcher.add("GADGET", None, pattern1, pattern2)
for doc in nlp.pipe(TEXTS):
    print([doc[start:end] for match_id, start, end in matcher(doc)])
