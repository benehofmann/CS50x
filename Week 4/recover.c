#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <getopt.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    //claring variable
    unsigned char buffer[512];
    int number_of_files = 0;
    File

    //boolean flag
    bool flag = false;


    //invalid arguments
    if (argc > 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    //open Input-File
    FILE *file = fopen(argv[1], "r");

    //Output file
    FILE *img = NULL;

    if (file == NULL)
    {
        fprintf(stderr, "Could not open file\n");
        return 1;
    }

    //reading file until end of card
    while (fread(buffer, 512, 1, file) == 1)
    {
        //is it a jpeg header?
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {

            //If first jpeg
            if (flag == true)
            {
                fclose(img);
            }
            else //JPEG already found
            {
                flag = true;
            }

            //JPEG found now writing to it!
            char filename[8];
            sprintf(filename, "%03i.jpg", number_of_files);
            img = fopen(filename, "a");
            number_of_files++;

        }


        if (flag == true)
        {
            fwrite(&buffer, 512, 1, img);
        }


    }

    //Close all files
    fclose(file);
    fclose(img);


//Success
    return 0;

}
