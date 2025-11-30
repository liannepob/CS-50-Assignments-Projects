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
    char word[LENGTH + 1];
    struct node *next;
} node;

// arithmatic: 26 ^ 3
const unsigned int N = 17576;
unsigned int fileSize = 0;
// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);
    // creates a cursor pointer first element of the word in the table
    node *cursor = table[index];

    while (cursor != NULL)
    {
        // checks if the cursor is a the element that needs to be checked

        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        // moves onto the next word if the cursor is not where it needs to be
        cursor = cursor->next;
    }
    return false;
}

// temporary hash function(prob slow) change it so it improves in speed
// change it so it checks the first 2 letters not just the first one
unsigned int hash(const char *word)
{
    int length = strlen(word);
    int hashVal = 0;
    for (int i = 0; i < length; i++)
    {
        hashVal += toupper(word[i]);
        hashVal = (hashVal * toupper(word[i])) % N;
        // multiplies by word[i] to take every char of word's string
    }
    return hashVal;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];
    int index = 0;
    // open dictionary file and checks if it is null
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        return false;
    }

    while (fscanf(source, "%s", word) != EOF)
    {
        // recursively scans the file for the word
        // creates n as a pointer for the new malloc size
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        // checks if the file is null and if not it copies the code into the file
        else
        {
            // makes the next space NULL so that it is clear for the next input
            strcpy(n->word, word);
            n->next = NULL;
            fileSize++;
        }
        // use the hash function to get the index of a string V
        // then the function will return an index V
        // the index will be useed to index into the linked list V
        index = hash(word);
        n->next = table[index];
        table[index] = n;
    }
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return fileSize;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // checks each individual table
    for (int i = 0; i < N; i++)
    {
        // creates temp/cursor to free/move around table
        node *cursor = table[i];
        node *temp = cursor;
        // checks each individual node
        while (temp != NULL)
        {
            cursor = cursor->next;
            free(temp);
            temp = cursor;
        }
    }
    // returns true when it works
    return true;
}
