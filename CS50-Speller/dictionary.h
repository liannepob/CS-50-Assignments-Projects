// Declares a dictionary's functionality

#ifndef DICTIONARY_H
#define DICTIONARY_H

#include <stdbool.h>
// library for bools

// Maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45
// defines a constant length of 45(not a variable)
// a "find-and-replace" trick

// Prototypes
bool check(const char *word); // char pointer = (string word)
unsigned int hash(const char *word); // char pointer = (string word)
bool load(const char *dictionary); // char pointer = (string dictionary)
// all are declared as constant so the length of the strings remain
unsigned int size(void);
bool unload(void);

#endif // DICTIONARY_H
