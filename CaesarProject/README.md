#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char rotate(char c, int n);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    int key = atoi(argv[1]);

    string text = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0; i < strlen(text); i++)
    {
        printf("%c", rotate(text[i], key));
    }
    printf("\n");
    // rotates the individual characters of the plaintext into a cipher with the function rotate
}
char rotate(char c, int n) // creates a rotaste function that changed the value of the previous
                           // character into a ciphered version
{
    // ci = (pi + k) % 26 p = number, k = key, alphabetical index - used for letters like Y/Z
    int index;
    char newC;
    // alpha char of ascii from 65-122
    // turn char into an int, add the key and mod by 26 to find how much the char needs to increase
    // by, then add the key to the ascii value
    if (!isalpha(c))
    {
        return c;
    }
    else if (isupper(c))
    {
        index = (c - 'A' + n) % 26;
        newC = 'A' + index;
        return newC;
    }
    else if (islower(c))
    {
        index = (c - 'a' + n) % 26;
        newC = 'a' + index;
        return newC;
    }
    return c;
}
