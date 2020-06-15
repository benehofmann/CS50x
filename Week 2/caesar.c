#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    //argv[0] ==> ist das erste Wort in der command-line !
    if (argc == 2)
    {


        for (int i = 0, n = strlen(argv[1]); i < n; i++) //check if input is valid
        {

            if (argv[1][i] < 49 || argv[1][i] > 57) //input invalid !
            {
                printf("Usage: ./caesar key");
                return 1;
            }
        }


        int key = atoi(argv[1]);
        string input = get_string("plaintext: ");

        printf("ciphertext: ");

        for (int i = 0, m = strlen(input); i < m ; i++)
        {


            if (isalpha(input[i]) && isupper(input[i]))
            {
                printf("%c", (input[i] - 'A' + key) % ('Z' - '@') + 'A');
            }
            else if (isalpha(input[i]) && islower(input[i]))
            {

                printf("%c", (input[i] - 'a' + key) % ('z' - '`') + 'a');

            }
            else
            {
                printf("%c", input[i]);
            }





        }

        printf("\n");

    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

}