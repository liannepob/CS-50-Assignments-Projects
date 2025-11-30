#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void) // main argument for the function
{
    string text = get_string("Enter the text :D: ");
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    float L = (float) letters / words * 100;
    float S = (float) sentences / words * 100;

    int index = round(0.0588 * (float) L - 0.296 * (float) S - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    int count = 0;
    int n = strlen(text);
    for (int i = 0; i < n; i++)
    {
        if (isalpha(text[i]))
        {
            count++;
        }
        else if (text[i] == '-')
        {
            count++;
        }
    }
    return count;
}

int count_words(string text)
{
    int count = 1;
    int n = strlen(text);
    for (int i = 0; i < n; i++)
    {
        if (text[i] == ' ')
        {
            count++;
        }
    }
    return count;
}
int count_sentences(string text)
{
    int count = 0;
    int n = strlen(text);
    for (int i = 0; i < n; i++)
    {
        if (text[i] == '?')
        {
            count++;
        }
        if (text[i] == '.')
        {
            count++;
        }
        if (text[i] == '!')
        {
            count++;
        }
    }
    return count;
}
