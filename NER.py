def NER_getter(TokenizedList):

    from camel_tools.tokenizers.word import simple_word_tokenize
    from camel_tools.ner import NERecognizer

    ner = NERecognizer.pretrained()

    # NERecognizer expects pre-tokenized text
    sentence = TokenizedList

    labels = ner.predict_sentence(sentence)

    # save each token paired with it's NER label
    zipped = list(zip(sentence, labels))

    # Filter and glue named entities into dictionary
    named_entities = {"LOC": [], "ORG": [], "PERS": [], "MISC": []}

    for i, name in enumerate(zipped):
        writer = ""
        x = 1
        if name[1][0] == "B":
            writer = name[0]
            if zipped[i+x][1][0] == "I":
                while zipped[i+x][1][0] == "I":
                    writer += " " + zipped[i+x][0]
                    x += 1
            else:
                pass
            named_entities[zipped[i][1][2:]].append(writer)

    return named_entities
