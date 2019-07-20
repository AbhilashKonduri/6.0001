import math
import random
import string
VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}
WORDLIST_FILENAME = "words.txt"
def load_words():
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist
def get_frequency_dict(sequence):
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
def get_word_score(word, n):
    word_req = word.lower()
    comp_1 = 0
    for ch  in word_req:
        comp_1 += SCRABBLE_LETTER_VALUES[ch]  
    wordlen = len(word_req)
    comp_2 = (7*wordlen) - 3*(n-wordlen)
    if comp_2 < 1:
        comp_2=1
    score = comp_1* comp_2
    return score
def display_hand(hand):
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')
    print()                              
def deal_hand(n):
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand
def update_hand(hand, word):
    hand_cpy = hand.copy()
    word_req = word.lower()
    for ch in word_req:
        if ch in hand_cpy.keys():
            if hand_cpy[ch] != 0:
                hand_cpy[ch]-=1
    return hand_cpy
def is_valid_word(word, hand, word_list):    
    hand_cpy = hand.copy()
    word_req = word.lower()
    for ch in word_req:
        if ch in hand_cpy:
            hand_cpy[ch] -=1        
            if hand_cpy[ch] <0:
                return 0
        else:
            return 0
    if word_req not in word_list:
        return 0
    else:
        return 1
def calculate_handlen(hand):
    handlen =0
    for i in hand.values():
        handlen +=i
    return handlen
def play_hand(hand, word_list):
    print("Your Hand is.. " + "\n")
    print(hand)
    word = input("Please provide your input word")
    total_score =0
    word = word.lower()
    new_hand = hand.copy()
    while word != "!!" :
        validation = is_valid_word(word, new_hand, word_list)
        new_hand = update_hand(new_hand, word)
        n = calculate_handlen(new_hand)
        if n ==0:
            return total_score
        if validation == 0 :
            print("Entered word is invalid! so no points are awarded to you.")
            score =0
        if validation == 1:
            score = get_word_score(word, n)
            total_score += get_word_score(word, n)
        print("\n"+"Congrats! You earned " + str(score) + "Points")
        print("\n"+"Your Updated Hand is.. " + "\n")
        print(new_hand)
        word = input("Please provide your input word")
    if total_score>0:
        print("Well done !! Your Total Score is .." + str(total_score))
    else:
        print("Sorry! Your points are not worthy for a display :( Try Again")
    return total_score
def substitute_hand(hand, letter):   
    hand_cpy = hand.copy()
    char = letter.lower()
    if char in hand_cpy.keys():
        number = hand_cpy[char]
        del(hand_cpy[char])        
        ch = random.choice(string.ascii_letters)
        while ch in hand_cpy.keys():
            ch = random.choice(string.ascii_letters)
        while ch not in hand_cpy.keys():
            hand_cpy[ch] =number
        return hand_cpy
    else:
        return hand   
def play_game(word_list):
    hand_cnt = int(input("Hello! Welcome to the Game. How many hands Do you wanna Play?"))
    count_replay =1
    count_substitute =1
    n= random.randint(6,7)
    hand = deal_hand(n)
    new_hand = hand.copy()
    print(new_hand)
    game_total_score=0
    while hand_cnt != 0:
        if count_substitute >0:
            yn = (input("Do you want to substitute a letter?")).lower()
            if yn == 'y':
                letter = (input("Enter letter You want to substitute")).lower()
                print("Done!" + "/n" + "Your new hand is..")
                new_hand = substitute_hand(hand, letter)
                print(new_hand)
                count_substitute -=1
        
        print("Lets play !!")
        game_score = play_hand(new_hand, word_list)
        if count_replay >0:
            yn = (input("Do you want to replay the hand?")).lower()
            if yn == 'y':
                game_score=0
                game_score = play_hand(new_hand, word_list)
                count_replay -=1
        game_total_score +=game_score 
        hand_cnt -=1
    print("Well Done! Your Game score is ... "+ str(game_total_score))    
    return game_total_score   
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)