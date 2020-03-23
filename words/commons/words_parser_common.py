import re
from collections import Counter


def parse_words(text):
    """ gets string text --> separate lowercase words without special chars """
    return re.sub('[^a-zA-Z]', ' ', text).lower().split()


def get_words_frequencies(text):
    """ return frequencies dict for words in given text """
    frequencies_dict = {}
    words = parse_words(text)
    for word in words:
        frequencies_dict[word] = frequencies_dict.get(word, 0) + 1
    return frequencies_dict


def read_line_by_line_with_counter(filename):
    with open(filename) as file:
        return process_lines_with_counter(file)


def process_lines_with_counter(lines):
    counter = Counter()
    for line in lines:
        counter += Counter(parse_words(line))
    return counter
