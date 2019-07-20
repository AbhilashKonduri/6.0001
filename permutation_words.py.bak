def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    length = len(sequence)
    if length == 1:
        return sequence
    else:
        seq_list = list(sequence)
        char = seq_list[0]
        ret_list = []
        remainder = seq_list[1:length+1]
        rem_seq = list(get_permutations(remainder))
        for word in rem_seq:
            for i in range(length):
                word_list = list(word)
                word_list.insert(i,char)
                string = ''.join(word_list)
                ret_list.append(string)
        return ret_list
    
if __name__ == '__main__':
    
    sequence = input("Enter the Sequence that you want it to have permuted ")
    result = get_permutations(sequence)
    print("\n" + "Here Your Result:")
    print(result)
    print("\n" + "There are " + str(len(result)) + " permutations found")

