from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.ner import NERecognizer

ner = NERecognizer.pretrained()

# NERecognizer expects pre-tokenized text
sentence = sample.Tokenized

labels = ner.predict_sentence(sentence)

# save each token paired with it's NER label
zipped = list(zip(sentence, labels))


# Filter and glue named entities into dictionary
named_entities = {"LOC": [], "ORG": [], "PERS": [], "MISC": []}
for i, val in enumerate(zipped):
    if zipped[i][1][0] == "B":
        named_entities[zipped[i][1][2:]].append(zipped[i][0])
    if zipped[i][1][0] == "I":
        named_entities[zipped[i][1][2:]][-1] = named_entities[zipped[i]
                                                              [1][2:]][-1] + " " + zipped[i][0]
named_entities["MISC"]
