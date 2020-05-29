from cs50 import get_float
from math import floor

while True:
    dollars = get_float("Change owed: ")
    if dollars >= 0.01:
        cents = floor(dollars * 100)
        break

while True:
    quarters = cents // 25
    dimes = (cents % 25) // 10
    penny = ((cents % 25) % 10) // 5
    cents = (((cents % 25) % 10) % 5) // 1
    break
change = quarters + dimes + penny + cents
print(change)