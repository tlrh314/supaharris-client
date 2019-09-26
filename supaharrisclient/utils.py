import sys
import json


def response_to_json(response):
    return json.loads(response.content.decode("utf8"))


def print_progressbar(i, N, whitespace=""):
    pbwidth = 42

    progress = float(i)/(N-1)
    block = int(round(pbwidth*progress))
    text = "\r{0}Progress: [{1}] {2:.1f}%".format(whitespace,
        "#"*block + "-"*(pbwidth-block), progress*100)
    sys.stdout.write(text)
    sys.stdout.flush()

    if i == (N-1):
        print(" .. done")
