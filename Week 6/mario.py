from cs50 import get_int

while True:
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        break

if height >= 1 and height <= 8:
    spaces = height - 1
    startblocks = 1
    for i in range(height):
        print(" " * spaces, end="")
        print("#" * startblocks, end="")
        print()
        spaces -= 1
        startblocks += 1

