# Word Search

A word search is a rectangular grid of letters. Words (such as english words, or otherwise) may appear in any of 8 directions (forward, backward, up, down, and any way diagonally). This is a simple word search algorithm for finding words within that grid. It uses a hash table of 2-character prefixes for fast lookup. The most time is spend building the hash table, thus this is most efficient for finding long lists of words in a word search.


## Usage
To run:

```
wordsearch.py [input file]
```

## Input

The input file must be of the following form: 
```
N M
N rows of M letters
"WRAP" or "NO_WRAP"
P
P words with 1 word per line
```

## Output

If a word is found, the program will output the starting and ending coordinates for the word. If a word is not found, the program outputs `NOT FOUND` on the line corresponding to that word.

## Example

The file `WS_input_B.txt` contains

```
4 3
ABC
DEF
GHI
JKL
WRAP
5
FED
CAB
AEIJBFG
LGEC
HIGH
```

When we run the program on it, it outputs: 
```
(1, 2) (1, 0)
(0, 2) (0, 1)
(0, 0) (2, 0)
(3, 2) (0, 2)
(2, 1) (2, 1)
```
