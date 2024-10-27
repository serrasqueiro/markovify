import markovify

learn_txt_fname = "../../markovify/corpus.txt"
text = open(learn_txt_fname, "r").read()
text = text.replace(".", "\n").replace(", ", " ")

#stt = 3
stt = 1
text_model = markovify.NewlineText(text, state_size=stt)
#text_model = markovify.Text(text, state_size=stt)

def generate_new_word(model, max_length=10, min_length=2, ctx=0):
    for idx in range(300):
        sent = model.make_sentence(tries=5000, max_overlap_ratio=0.7, max_overlap_total=15)
        #sent = model.make_sentence(tries=5000)
        words = sent.split(" ")
        res, skp = [], []
        for word in words:
            if (min_length < len(word) <= max_length) and word.isalpha():
                res.append(word)
                continue
            #print(f"Skipped: '{word}'", min_length, len(word), max_length)
            skp.append(word)
        if res:
            return sorted(res), skp
        if ctx > 0:
            print("trying again:", ctx, idx)
            print(words, end="\n---\n")
    return [], skp

def generate_new_words(model, count, max_length=10):
    hist = {}
    for _ in range(count):
        words, _ = generate_new_word(model, max_length, ctx=1)
        for word in words:
            if word in hist:
                hist[word] += 1
            else:
                hist[word] = 1
    # From: https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
    # sorted_footballers_by_goals = sorted(footballers_goals.items(), key=lambda x:x[1])
    #
    # Most popular words upfront:
    res = [ala[0] for ala in sorted(hist.items(), key=lambda x:x[1], reverse=True)]
    return res

def search_at(text, words, debug=0):
    orig_text_words = [
        ala for ala in text.replace("\n", " ").split(" ") if ala
    ]
    txt = list(set(sorted(orig_text_words)))
    for word in words:
        idx = (txt.index(word) + 1) if word in txt else -1
        print("@HIT:" if idx >= 0 else "@NEW:", word)
    if debug <= 0:
        return txt
    for idx, ala in enumerate(txt, 1):
        print("TXT:", idx, ala)
    return txt

# Generate 25 new words with a maximum length of 10 characters
new_words = generate_new_words(text_model, 25, max_length=10)
print(">>>", text.strip() + "\n<<<", end="\n\n")
print(new_words)
search_at(text, new_words)
