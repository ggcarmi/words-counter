import re
from collections import Counter


def parse_words(text):
    """ gets string text --> separate lowercase words without special chars """
    return re.sub('[^a-zA-Z]', ' ', text).lower().split()


def parse_text(text):
    """ return frequencies Counter for words in given text """
    return Counter(parse_words(text))


def parse_lines(lines):
    """ parse multiple lines """
    counter = Counter()
    for line in lines:
        counter += parse_text(line)
    return counter
