from spacy.lang.fr import French

nlp = French()

people = ["David Bowie", "Angela Merkel", "Lady Gaga"]

# Crée une liste de motifs pour le PhraseMatcher
patterns = list(nlp.pipe(people))
