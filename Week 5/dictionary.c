// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1]; // +1 wgen nullterminator
    struct node *next;
}
node;

// Number of buckets in hash table 2 ^16
const unsigned int N = 26;

//number of words
unsigned int number_of_words = 0;

// Hash table
node *table[N]; // => size 0f 26 ==> 26 Buckets for each letter

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    // creates a temp variable that stores a lower-cased version of the word
    char temp[LENGTH + 1];
    int len = strlen(word);
    for(int i = 0; i < len; i++)
        temp[i] = tolower(word[i]);
    temp[len] = '\0';

    // find what index of the array the word should be in
    int index = hash(temp);

    // if hashtable is empty at index, return false
    if (table[index] == NULL)
    {
        return false;
    }

    // create cursor to compare to word
    node* cursor = table[index];

    // if hashtable is not empty at index, iterate through words and compare
    while (cursor != NULL)
    {
        if (strcmp(temp, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    // if you don't find the word, return false
    return false;
}



// Hashes word to a number
unsigned int hash(const char *word)
{



    // TODO
    if (word[0] == 'a' || word[0] == 'A')
    {
        return 0;
    }

    //B
    if (word[0] == 'b' || word[0] == 'B')
    {
        return 1;
    }

    //C
    if (word[0] == 'c' || word[0] == 'C')
    {
        return 2;
    }
    //D
    if (word[0] == 'd' || word[0] == 'D')
    {
        return 3;
    }
    //E
    if (word[0] == 'e' || word[0] == 'E')
    {
        return 4;
    }
    //F
    if (word[0] == 'f' || word[0] == 'F')
    {
        return 5;
    }
    //G
    if (word[0] == 'g' || word[0] == 'G')
    {
        return 6;
    }
    //H
    if (word[0] == 'h' || word[0] == 'H')
    {
        return 7;
    }
    //I
    if (word[0] == 'i' || word[0] == 'I')
    {
        return 8;
    }
    //J
    if (word[0] == 'j' || word[0] == 'J')
    {
        return 9;
    }
    //K
    if (word[0] == 'k' || word[0] == 'K')
    {
        return 10;
    }
    //L
    if (word[0] == 'l' || word[0] == 'L')
    {
        return 11;
    }
    //M
    if (word[0] == 'm' || word[0] == 'M')
    {
        return 12;
    }
    //N
    if (word[0] == 'n' || word[0] == 'N')
    {
        return 13;
    }
    //O
    if (word[0] == 'o' || word[0] == 'O')
    {
        return 14;
    }
    //P
    if (word[0] == 'p' || word[0] == 'P')
    {
        return 15;
    }
    //Q
    if (word[0] == 'q' || word[0] == 'Q')
    {
        return 16;
    }
    //R
    if (word[0] == 'r' || word[0] == 'R')
    {
        return 17;
    }
    //S
    if (word[0] == 's' || word[0] == 'S')
    {
        return 18;
    }
    //T
    if (word[0] == 't' || word[0] == 'T')
    {
        return 19;
    }
    //U
    if (word[0] == 'u' || word[0] == 'U')
    {
        return 20;
    }
    //V
    if (word[0] == 'v' || word[0] == 'V')
    {
        return 21;
    }
    //W
    if (word[0] == 'w' || word[0] == 'W')
    {
        return  22;
    }
    //X
    if (word[0] == 'x' || word[0] == 'X')
    {
        return 23;
    }
    //Y
    if (word[0] == 'y' || word[0] == 'Y')
    {
        return 24;
    }
    //Z
    if (word[0] == 'z' || word[0] == 'Z')
    {
        return 25;
    }
    //'
    if (word[0] == 39)
    {
        return
        26;
    }

    return 27;

}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //1. Open up a file with fopen
    char word[LENGTH+1];

    FILE *file = fopen(dictionary, "r");


    if (file == NULL)
    {
        printf("no file loaded");
        return false;
    }

    //2. read all Strings from a file with fscanf


    while (fscanf(file, "%s", word)!=EOF)
    {

        //3. create a new node for the String with malloc, dopy each String into node using strcpy
        node *new_node = malloc(sizeof(node)); //memory allocated
        strcpy(new_node->word, word); //copy the word in the string of the new node
        int hashvalue = hash(word); //hashes the word

        if (new_node == NULL)
        {
            printf("Error while loading");
            unload();
            return false;
        }
        else
        {
            if (table[hashvalue] == NULL)
            {
                table[hashvalue] = new_node; //allocated the node to the right playe e.g. Ben to "B"
                new_node->next = NULL; // set the pointer of the current node there to null
            }
            else
            {
                //add the new node to the front
                new_node->next = table[hashvalue];
                table[hashvalue] = new_node;
            }
            number_of_words++;
        }
    }

    //
    printf("loading completed");
    //close the file
    fclose(file);
    return true;

}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return number_of_words;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *tmp;

    for (int i = 0; i < N; i++)
    {

        tmp = table[i];

        while(table[i] != NULL)
        {
            tmp = table[i];
            table[i] = tmp-> next;
            free(tmp);
        }

    }
    // TODO
    return true;;
}
