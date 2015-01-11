# Trivia 2

**Question**

>Image represents a randomness from the last night. Help us find the flag hidden behind.
>Trivia-200.png

## Write-up
It’s just a randomly shifted figlet image.

The last two characters are the same. The first one looks like a 1. The entire string appears to be 8 characters long.

Assume that the first row is aligned properly. This is actually pretty important to solving the final string, and we can eliminate all lowercase letters from the sequence.  

Writing a script to interactively shift the lines, we can see the text. The flag is 13378055
