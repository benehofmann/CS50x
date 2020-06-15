from cs50 import get_string
# 0.0588 * L - 0.296 * S - 15.8 is the formula
# where L is the average number of letters per 100 words in the text
# S is the average number of sentences per 100 words in the text.


def main():
    userinput = get_string("Text: ")

    letters = countletters(userinput)
    words = countwords(userinput)
    sentences = countsentences(userinput)

    l = letters / words * 100
    s = sentences / words * 100

    index = round(0.0588 * l - 0.296 * s - 15.8)

    if index < 0:
        print("Before Grade 1\n")
    elif index >= 16:
        print("Grade 16+\n")
    elif index >= 0 or index <= 16:
        print("Grade " + str(index) + "\n")


def countletters(text):
    counter = 0
    for i in range(len(text)):
        if text[i].isalpha():
            counter +=1

    return counter


def countwords(text):
    return len(text.split())


def countsentences(text):
    return text.count('.') + text.count('?') + text.count('!')


main()
