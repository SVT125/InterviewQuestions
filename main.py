# Page 295, The Pretty Printing Problem.
# Given a set of words representing a sentence/excerpt, return the minimum messiness out of all the
# configurations possible that the excerpt can be split into as lines.
# The messiness is defined as the sum of (blanks in a given line) ** 2 over all lines.
def f(words, L)-> int:
    # Default initialize the DP list.
    min_messiness = [-1] * len(words)
    min_messiness[0] = (L - len(words[0])) ** 2
    for i in range(1, len(words)):
        # Include the ith word.
        space_left = L - len(words[i])
        min_messiness[i] = min_messiness[i-1] + space_left ** 2

        # Now, add words from right to left until the line can fit no more.
        # That is, we split by words[0:j-1] and words[j:i].
        for j in range (i-1, -1, -1):
            # We can't fit any more words into the line.
            if len(words[j]) + 1 > space_left:
                break

            space_left -= len(words[j]) + 1
            # If this is the first word, then the line is empty.
            if j - 1 < 0:
                first_messiness = 0
            else:
                first_messiness = min_messiness[j-1]

            min_messiness[i] = min(min_messiness[i], first_messiness + space_left ** 2)

    return min_messiness

s = ['aaa', 'bbb', 'c', 'd', 'ee', 'ff', 'ggggggg']
length = 11
print(f(s, length))