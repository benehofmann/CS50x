#include <cs50.h>
#include <stdio.h>

void printHash(int numberOfHash);
void printSpace(int numberOfDots);

int main(void)
{
    int size;
    do
    {
        size = get_int("Size: ");
    } 
    while (size < 1 || size > 8);

    int counter = 1;
 
    for (int i = 1; i <= size; i++)
    {

        printSpace(size - counter);
        printHash(i);
        counter++;
    
        printf("\n");
    }
}
   
    
    
    
    


void printHash(int numberOfHash) 
//loop to print # : Parameter how many times it should be printed
{
    int i = 0;

    while
    (i != numberOfHash)
    {
        printf("#");
        i++;
    }
   

}
void printSpace(int numberOfDots)
//loop to print white spaces : Parameter how many times it should be printed
{
    int i = 0;

    while (i != numberOfDots) 
    {
        printf(" ");
        i++;
    }
   
}