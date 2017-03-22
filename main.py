from functools import reduce


# 0-1 Knapsack Problem w/ the famous O(nW) time but using only O(W) space; n = # of items, W = max weight.
# A is a list of tuples (weight, value), W is a non-negative integer representing max weight.
# We let the partial array be size W+1, since we index the items with 1-indexing -> 0th index is the case.
# Returns the max value attainable of A given W.
def knapsack(A, W) -> int:
    partial_results = [0] * (W+1)
    for i in range(0, len(A)):
        for j in range(W, 0, -1):
            # Update right to left, since we don't want to use new values from earlier in the array for the later part.
            # If we can add the ith item + its better to take its value, add it on.
            # In all other cases given this 1D array implementation, do nothing as we already have the best value.
            if A[i][0] <= j and partial_results[j - A[i][0]] + A[i][1] > partial_results[j]:
                partial_results[j] = partial_results[j - A[i][0]] + A[i][1]
    return partial_results[W]


# Given an array of int A, return B such that
# B[i] = A[j], j is the earliest value where j > i and A[i] >= A[j].
# e.g. A = [5, 4, 6] -> B[0] = A[1] = 4.
# A DP-like solution that identifies B[i] = B[i+1] | A[i+1] | 0.
# Takes O(n) time (and O(n) space to simply create the array returned).
def earliest_lesser(A) -> "array of int":
    B = [0] * len(A)
    for i in range (len(A)-1, -1, -1):
        if i == len(A)-1 or (i == len(A)-2 and A[i] < A[i+1]):
            # If we're filling the last element or the last element is greater than the second to last.
            B[i] = 0
        elif A[i] > A[i+1]:
            # If the next element in A is less than the current, it's the best answer.
            B[i] = A[i+1]
        elif A[i] > B[i+1]:
            # Otherwise, if the best element comes from past i+1.
            B[i] = B[i+1]
        else:
            # Otherwise, we've proven there is no element to the right that is lesser than our current.
            B[i] = 0
    return B


# EPI Page 184, Find the duplicate and missing elements.
# Given an array of ints in the range [0, n-1], return the duplicate and missing elements.
# That is, if the array is perfect it is exactly [0, n-1] w/ no duplicates.
# If it isn't, the duplicated element takes the slot of what is now the missing element.
# Returns a tuple of int (duplicate, missing).
def find_dupe_and_missing(A) -> "tuple of int":
    B = [i for i in range(0, len(A))]
    C = A + B
    xored_answers = reduce(lambda x, y: x ^ y, C)
    differing_bit = xored_answers & ~(xored_answers - 1)

    # If the result is 0, then there were no duplicate/missing elements.
    if differing_bit == 0:
        return (-1, -1)

    unknown_answer = reduce(lambda x, y: x ^ y, [x for x in C if x & differing_bit])
    duplicate = -1

    # Traverse the whole array to find our unknown answer - if we've found it, we know it's not the missing element.
    for x in A:
        if x == unknown_answer:
            duplicate = unknown_answer
            break

    if duplicate == -1:
        return (xored_answers ^ unknown_answer, unknown_answer)
    return (duplicate, xored_answers ^ duplicate)


# EPI Page 295, The Pretty Printing Problem.
# Given a set of words representing a sentence/excerpt, return the minimum messiness out of all the
# configurations possible that the excerpt can be split into as lines.
# The messiness is defined as the sum of (blanks in a given line) ** 2 over all lines.
def pretty_printing(words, L, return_array = True) -> "array of int":
    # Default initialize the DP list.
    # line_separators[i] = the last line has words[j, i].
    min_messiness = [-1] * len(words)
    line_separators = [-1] * len(words)
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
            line_separators[i] = j

    if return_array:
        return min_messiness
    # TODO - Return one example decomposition if it exists, None otherwise.


# EPI Page 288, The BedBathAndBeyond.com problem.
# Given a phrase and a dictionary of words, determine whether a decomposition of the phrase into a subset of
# the dictionary exists; if it does, return 1 such decomposition.
def bbb(phrase, dict) -> "array of int":
    last_word_length = [-1] * len(phrase)
    for i in range(0, len(phrase)):
        # If this substring is an actual string in the dict, set it as a valid decomposition.
        if dict.count(phrase[0:i+1]):
            last_word_length[i] = i + 1

        # Otherwise, this substring is a decomposition of a smaller decomposition + dict word or not at all.
        if last_word_length[i] == -1:
            for j in range(0, i):
                if last_word_length[j] != -1 and dict.count(phrase[j+1:i+1]):
                    last_word_length[i] = i - j
                    break

    return last_word_length

ks_items = [(2, 3), (3, 4), (4, 5), (5, 6)]
el = [5, 1, 3, 4, 6, 2]
mm_array = [0, 1, 3, 2, 6, 4, 7, 1]
pp_s = ['aaa', 'bbb', 'c', 'd', 'ee', 'ff', 'ggggggg']
bbb_d = ['a', 'am', 'an', 'man', 'plan', 'canal']
bbb_str = "amanaplanacanal"
pp_length = 11

print(knapsack(ks_items, 5))
print(earliest_lesser(el))
print(find_dupe_and_missing(mm_array))
print(pretty_printing(pp_s, pp_length))
print(bbb(bbb_str, bbb_d))