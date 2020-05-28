from util import utils
from speech_converter import speech_to_text
from grammar_rater import rate_spelling
from grammar_rater import rate_unnecessary_fillers
from grammar_rater import rate_grammar
import time
import asyncio

filename = "speech.txt"


async def main():

    speech_to_text(filename)
    loop = asyncio.get_running_loop()
    data = utils.read_file(filename)
    words_count = utils.total_words(data)
    logs = '='*44+'\n'
    logs += "total spoken words                   -> " + str(words_count)+'\n'
    logs += '='*44+'\n'

    fut_speech_fluency = loop.create_future()
    loop.create_task(utils.rate_speech_on_fluency(
        fut_speech_fluency, words_count))
    fluency_rating = await fut_speech_fluency

    spelling_rating = rate_spelling(data, words_count)

    fut_unnecessary_filler = loop.create_future()
    loop.create_task(rate_unnecessary_fillers(fut_unnecessary_filler, data))
    filler_rating = await fut_unnecessary_filler

    grammar_rating = rate_grammar(data)

    logs += '='*44+'\n'
    logs += "fluency rating             (out of 1)-> " + \
        str(fluency_rating)+'\n'
    logs += "spelling rating            (out of 2)-> " + \
        str(spelling_rating)+'\n'
    logs += "unnecessary fillers rating (out of 1)-> " + \
        str(filler_rating)+'\n'
    logs += "grammar rating             (out of 1)-> " + \
        str(grammar_rating) + '\n'

    total_rating = fluency_rating + spelling_rating + filler_rating + grammar_rating

    logs += '='*44+'\n'
    logs += "overall rating             (out of 5)-> " + str(total_rating)+"\n"

    logs += '='*44+'\n'

    f = open("logs.txt", "w")
    f.write(logs)
    f.close
    return total_rating
