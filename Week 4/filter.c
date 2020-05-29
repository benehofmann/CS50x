#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float average = 0;

            average = (image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen) / 3.0;

            image[i][j].rgbtRed = roundf(average);
            image[i][j].rgbtBlue = roundf(average);
            image[i][j].rgbtGreen = roundf(average);
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    /*
    sepiaRed = .393 * originalRed + .769 * originalGreen + .189 * originalBlue
    sepiaGreen = .349 * originalRed + .686 * originalGreen + .168 * originalBlue
    sepiaBlue = .272 * originalRed + .534 * originalGreen + .131 * originalBlue

    */

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sr = .393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue;
            float sg = .349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue;
            float sb = .272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue;



            int r = roundf(sr);

            if (r > 255)
            {
                r = 255;
            }
            int g = roundf(sg);

            if (g > 255)
            {
                g = 255;
            }
            int b = round(sb);

            if (b > 255)
            {
                b = 255;
            }
            image[i][j].rgbtRed = r;
            image[i][j].rgbtGreen = g;
            image[i][j].rgbtBlue = b;



        }

    }


    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {

            //buffer the pixel value
            int buffer = 1;
            int rBuffer = image[i][j].rgbtRed;
            int bBuffer = image[i][j].rgbtBlue;
            int gBuffer = image[i][j].rgbtGreen;


            //Swap the red pixels
            image[i][j].rgbtRed = image[i][width - j - buffer].rgbtRed;
            image[i][width - j -  buffer].rgbtRed = rBuffer;

            //Swap the blue pixels
            image[i][j].rgbtBlue = image[i][width - j - buffer].rgbtBlue;
            image[i][width - j - buffer].rgbtBlue = bBuffer;

            //Swap the green pixels
            image[i][j].rgbtGreen = image[i][width - j - buffer].rgbtGreen;
            image[i][width - j -  buffer].rgbtGreen = gBuffer;

        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //saving the original image
    RGBTRIPLE originalImage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            originalImage[i][j] = image[i][j];
        }
    }

    //looping & declaring red, green, blue, and counter
    for (int i = 0, red, green, blue, counter; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            red = green = blue = counter = 0;

            // middle pixel
            if (i >= 0 && j >= 0)
            {
                red += originalImage[i][j].rgbtRed;
                green += originalImage[i][j].rgbtGreen;
                blue += originalImage[i][j].rgbtBlue;
                counter++;
            }

            //Pixel on  the left side
            if (i >= 0 && j - 1 >= 0)
            {
                red += originalImage[i][j - 1].rgbtRed;
                green += originalImage[i][j - 1].rgbtGreen;
                blue += originalImage[i][j - 1].rgbtBlue;
                counter++;
            }

            //Pixel on the right side no edge
            if ((i >= 0 && j + 1 >= 0) && (i >= 0 && j + 1 < width))
            {
                red += originalImage[i][j + 1].rgbtRed;
                green += originalImage[i][j + 1].rgbtGreen;
                blue += originalImage[i][j + 1].rgbtBlue;
                counter++;
            }

            //Pixel above the orginal pixel
            if (i - 1 >= 0 && j >= 0)
            {
                red += originalImage[i - 1][j].rgbtRed;
                green += originalImage[i - 1][j].rgbtGreen;
                blue += originalImage[i - 1][j].rgbtBlue;
                counter++;
            }

            //Pixel left above the original pixel
            if (i - 1 >= 0 && j - 1 >= 0)
            {
                red += originalImage[i - 1][j - 1].rgbtRed;
                green += originalImage[i - 1][j - 1].rgbtGreen;
                blue += originalImage[i - 1][j - 1].rgbtBlue;
                counter++;
            }

            // Pixel right above the original pixel no edge
            if ((i - 1  >= 0 && j + 1 >= 0) && (i - 1 >= 0 && j + 1 < width))
            {
                red += originalImage[i - 1][j + 1].rgbtRed;
                green += originalImage[i - 1][j + 1].rgbtGreen;
                blue += originalImage[i - 1][j + 1].rgbtBlue;
                counter++;
            }

            //Pixel down of the original Pixel
            if ((i + 1  >= 0 && j >= 0) && (i + 1 < height && j >= 0))
            {
                red += originalImage[i + 1][j].rgbtRed;
                green += originalImage[i + 1][j].rgbtGreen;
                blue += originalImage[i + 1][j].rgbtBlue;
                counter++;
            }

            // Pixel down left of the original pixel
            if ((i + 1 >= 0 && j - 1 >= 0) && (i + 1 < height && j - 1 >= 0))
            {
                red += originalImage[i + 1][j - 1].rgbtRed;
                green += originalImage[i + 1][j - 1].rgbtGreen;
                blue += originalImage[i + 1][j - 1].rgbtBlue;
                counter++;
            }

            // Pixel down right of the original pixel
            if ((i + 1 >= 0 && j + 1 >= 0) && (i + 1 < height && j + 1 < width))
            {
                red += originalImage[i + 1][j + 1].rgbtRed;
                green += originalImage[i + 1][j + 1].rgbtGreen;
                blue += originalImage[i + 1][j + 1].rgbtBlue;
                counter++;
            }

            image[i][j].rgbtRed = round(red / (counter * 1.0));
            image[i][j].rgbtBlue = round(blue / (counter * 1.0));
            image[i][j].rgbtGreen = round(green / (counter * 1.0));
        }
    }

    return;
}
