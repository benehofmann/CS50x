#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float dollars;
    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0);
    

    int change = round(dollars * 100);
    int counter = 0;

    int amountLeft = change;

    while (amountLeft >= 25) // subtract quarters
    {
        amountLeft -= 25;
        counter++;
    }
    while (amountLeft >= 10) // subtract dimes
    {
        amountLeft -= 10;
        counter++;
    }
    while (amountLeft >= 5) // subtract nickels
    {
        amountLeft -= 5;
        counter++;
    }
    while (amountLeft >= 1) // subtract pennies
    {
        amountLeft--;
        counter++;
    }    

    printf("%i \n", counter);
}