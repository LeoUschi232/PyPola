from numpy import array, arange
from random import choice
from re import sub

random_word = "S0"

# First begin by starting the half-string with either a or b
operation = choice([1, 2])
if operation == 1:
    random_word = random_word.replace("S0", "aZ1ASXZ2", 1)
elif operation == 2:
    random_word = random_word.replace("S0", "bZ1BSXZ2", 1)

# Continue creating the half-string by adding a or b
# Use X to count the length of the half-string
while len(random_word) < 40:
    operation = choice([3, 4])
    if operation == 3:
        random_word = random_word.replace("S", "aASX", 1)
    elif operation == 4:
        random_word = random_word.replace("S", "bBSX", 1)
while "S" in random_word:
    operation = choice([3, 4, 5])
    if operation == 3:
        random_word = random_word.replace("S", "aASX", 1)
    elif operation == 4:
        random_word = random_word.replace("S", "bBSX", 1)
    elif operation == 5:
        random_word = random_word.replace("S", "", 1)

# Perform the random permutations of the symbols according to the rules of the grammar
v = ["A", "B", "X"]
operation_indexes = arange(6, 22)
while any(symbol in random_word for symbol in v):
    operation = choice(operation_indexes)
    if operation == 6:
        random_word = random_word.replace("Aa", "aA", 1)
    elif operation == 7:
        random_word = random_word.replace("Ab", "bA", 1)
    elif operation == 8:
        random_word = random_word.replace("Ba", "aB", 1)
    elif operation == 9:
        random_word = random_word.replace("Bb", "bB", 1)
    elif operation == 10:
        random_word = random_word.replace("Z1a", "aZ1", 1)
    elif operation == 11:
        random_word = random_word.replace("Z1b", "bZ1", 1)
    elif operation == 12:
        random_word = random_word.replace("AX", "XA", 1)
    elif operation == 13:
        random_word = random_word.replace("XA", "AX", 1)
    elif operation == 14:
        random_word = random_word.replace("BX", "XB", 1)
    elif operation == 15:
        random_word = random_word.replace("XB", "BX", 1)
    elif operation == 16:
        random_word = random_word.replace("aX", "Xa", 1)
    elif operation == 17:
        random_word = random_word.replace("Xa", "aX", 1)
    elif operation == 18:
        random_word = random_word.replace("bX", "Xb", 1)
    elif operation == 19:
        random_word = random_word.replace("Xb", "bX", 1)
    elif operation == 20:
        random_word = random_word.replace("XBZ2", "Z2b", 1)
    elif operation == 21:
        random_word = random_word.replace("XAZ2", "Z2a", 1)

    if "Z1Z2" in random_word:
        random_word = random_word.replace("Z1Z2", "", 1)
        break

print(random_word)
l = len(random_word)
print(f"Length: {l}")
print(f"{random_word[0:l // 2]}:{random_word[l // 2:l]}")
