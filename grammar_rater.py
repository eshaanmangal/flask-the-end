from enchant.checker import SpellChecker
import nltk
import asyncio


chkr = SpellChecker("en_IN")
VERB_CODES = {
    "VB",  # Verb, base form
    "VBD",  # Verb, past tense
    "VBG",  # Verb, gerund or present participle
    "VBN",  # Verb, past participle
    "VBP",  # Verb, non-3rd person singular present
    "VBZ",  # Verb, 3rd person singular present
}


async def rate_unnecessary_fillers(fut, data):
    # yeah,you know,like
    # I have worked on tech like java, like spring boot like mysql
    words = data.split()
    count = 0
    for word in words:
        if word.lower() == "like".lower():
            count = count + 1
        if word.lower() == "you know".lower():
            count = count + 1
    if count >= 3:
        # return 0
        fut.set_result(0)
    elif count == 2:
        # return 0.6
        fut.set_result(0.6)
    else:
        # return 1
        fut.set_result(1)


def logs_after(a, b):
    print(a, "is not allowed after", b)


def rate_grammar(data):
    words = data.split()
    count = 0
    for i, word in enumerate(words):
        if word == "has" or word == "have":
            if is_true(words[i + 1], "VBD"):
                logs_after(words[i+1], words[i])
                count = count + 1
            if is_true(words[i+1], "VB"):
                logs_after(words[i+1], words[i])
                count = count+1
            if is_true(words[i+1], "NN"):
                logs_after(words[i+1], words[i])
                count = count+1
            if is_true(words[i+1], "VBG"):
                logs_after(words[i+1], words[i])
                count = count+1
        if word == "I":
            if is_true(words[i+1], "VBZ"):
                logs_after(words[i+1], words[i])
                count = count+1

    if count == 0:
        return 1
    if count >= 4:
        return 0
    if count >= 2:
        return 0.5
    if count == 1:
        return 0.7


def is_true(word, code):
    result = nltk.pos_tag(word.split())
    word_code = result[0][1]
    if word_code == code:
        return True
    return False


def rate_spelling(data, total_words):
    chkr.set_text(data)
    misspelled_words = 0
    hindi_words = []
    for err in chkr:
        hindi_words.append(err.word)
        misspelled_words = misspelled_words + 1
    error_per = misspelled_words_percentage(total_words, misspelled_words)
    print("Misspelled words :    ", hindi_words)
    return rate_misspelled_percentage(error_per)


def misspelled_words_percentage(total_words, misspelled_words):
    return round(misspelled_words / total_words * 100, 2)


def rate_misspelled_percentage(error_per):
    if error_per >= 50:
        return 0
    if error_per >= 30 and error_per < 50:
        return 0.5
    if error_per >= 20 and error_per < 30:
        return 1
    if error_per >= 10 and error_per < 20:
        return 1.5
    if error_per >= 5:
        return 1.7
    else:
        return 2
