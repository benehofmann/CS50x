#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>

int countletters(string text);
int countwords(string text);
int countsentences(string text);


//index = 0.0588 * L - 0.296 * S - 15.8
//Here, L is the average number of letters per 100 words in the text
// L = Letters / Words  x 100
//and S is the average number of sentences per 100 words in the text.
// S = Sentences / Words x 100

int main(void)
{

    string input = get_string("Text: ");

    int numberOfLetters = countletters(input);
    int numberOfWords = countwords(input);
    int numberOfSentences = countsentences(input);

    float l = (float) numberOfLetters / (float) numberOfWords * 100;
    float s = (float) numberOfSentences / numberOfWords * 100;

    float floatindex = 0.0588 * l - 0.296 * s - 15.8;

    int index = (int) round(floatindex);

    if (index < 0)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }


}

int countletters(string text)
{
    int counter = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {

        if (text[i] >= 'a' && text[i] <= 'z')
        {
            counter++;
        }
        if (text[i] >= 'A' && text[i] <= 'Z')
        {
            counter++;
        }

    }

    return counter;
}

int countwords(string text)
{
    int counter = 0;

    for (int i = 0; text[i] != '\0'; i++)
    {
        if (text[i] == ' ' && text[i + 1] != ' ')
        {
            counter++;
        }

    }

    return counter + 1;

}

int countsentences(string text)
{
    int counter = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == 46 || text[i] == 63 || text[i] == 33)
        {
            counter++;
        }
    }

    return counter;
}