import random
import string
import os
path = "D:\\Programming\\6.0001\\ps2\\ps2\\Hangman"
os.chdir(path)
warning_count =3
life = 6
letterslist =[]
end_game =0
WORDLIST_FILENAME = "words.txt"
def default():
    global warning_count
    global life
    global letterslist
    global end_game
    warning_count =3
    life = 6
    letterslist =[]
    end_game =0
def load_words():
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    print(len(wordlist), "words loaded.")
    return wordlist
def choose_word(wordlist):
    return random.choice(wordlist)
wordlist = load_words()
def is_word_guessed(secret_word, letters_guessed):
   secret_letters = list(secret_word)
   unique_letters = []
   for ch in secret_letters:
       if ch not in unique_letters:
           unique_letters.append(ch)
   for ch in letters_guessed:
       if ch in unique_letters:
           unique_letters.remove(ch)
   if len(unique_letters) == 0:
        return 1
   else:
        return 0        
def get_guessed_word(secret_word, letters_guessed):
    secret_letters = list(secret_word)
    status_word = []
    i = 0
    while i < len(secret_letters):
        status_word.append(' _ ')
        i+=1
    for ch in letters_guessed:
        i = 0
        while i < len(secret_letters):
            if ch == secret_letters[i]:
                status_word[i] = ch
            i+=1
    result_string = ''.join(status_word)
    return result_string            
def get_available_letters(letters_guessed):
    remaining_letters = list(string.ascii_lowercase)
    for ch in letters_guessed:
       remaining_letters.remove(ch)
    result_string = ' '.join(remaining_letters)
    return result_string
def letter_input_list (letters_guessed):
    global letterslist
    letterslist.append(letters_guessed)
    return letterslist
def warning():
    global warning_count 
    warning_count -= 1
    if (warning_count > 0):
        print("The input is incorrect you have  "+ str(warning_count) + "  warnings left")
    else:
        print("Sorry no warnings left you have lost a life for incorrect Input")
        global life
        life-=1
        if(life >1):
               print("You have " + str(life) + " lifes left")
        if life == 1:
               print("You have only " + str(life) + " life left " + " Think Carefully!! dude ")
        if life == 0:
               print ("Sorry you have run out of lives!")
               global end_game
               end_game=1
def letter_presence(secret_word,char):
    secret_letters = list(secret_word)
    unique_letters = []
    for ch in secret_letters:
       if ch not in unique_letters:
           unique_letters.append(ch)
       ch = char
       if ch in  secret_letters:
           return 1
       else:
           print("Sorry there is no letter " + str(char) + " in the word" + '\n' + " You will loose a life")
           global life
           life -=1
           if(life >1):
               print("You have " + str(life) + " lifes left")
           if life == 1:
               print("You have only " + str(life) + " life left " + " Think Carefully!! dude ")
           if life == 0:
               print ("Sorry you have run out of lives!")
               global end_game
               end_game=1
           return 0                          
def hangman(secret_word):
    print("\n"+"Welcome to the Game of Hangman !")
    secret_word = choose_word(wordlist)
    print ("I am thinking of a word that is",len(secret_word),"letter Word")
    for i in range(len(secret_word)):
        print ("__ ", end="")
    print("\n" + "You can type * for hint")
    print( "You have 6 guesses left" + '\n' +  "Your available letters are  -> a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z" +  '\n' + "Lets Begin the game!" + '\n' +  "________________________________________________________________________________________" +  '\n')
    print("\n"+"*************************************************************")            
    deciding_factor = 1    
    while (deciding_factor == 1):       
            ch = input ("Please guess a letter.")
            if ch in list(string.ascii_uppercase):
                print("Please use Lower case letters")
                continue
            if ch in list(string.ascii_lowercase):
                if ch in letterslist:
                    print("The letter is already been guessed")
                else:
                    letter_input_list(ch)
                    letter_presence(secret_word,ch)
                    print("The Updated Model of Your Riddle is :")
                    print(get_guessed_word(secret_word, letterslist))
                    print("You have available letters to guess as:")
                    print(get_available_letters(letterslist))
            elif ch == '*' :
                print("Here your hints :" + "\n")
                print(show_possible_matches(get_guessed_word(secret_word, letterslist)))
                print("\n"+"*************************************************************")            
            else:
                warning()                
            deciding_factor = (is_word_guessed(secret_word, letterslist) == 0) and end_game == 0    
    print("*************************************************************")
    if is_word_guessed(secret_word, letterslist) == 0:
            print("The word is " + secret_word)       
    else:
        print("Congrats!! you made it!")
    print("\n" + "Your Game is Over!"+ "\n" + ' ')
    print("\n"+"*************************************************************")
    print ("\n"+ "Wanna try an another word?" + "\n" + "Type y or N")
    k =input("")
    if k == 'y':
         default()
         secret_word = choose_word(wordlist)
         hangman(secret_word)
    if k == 'Y':
         default()
         secret_word = choose_word(wordlist)
         hangman(secret_word)
    else:
        print('\n'+"Since the input in not Yes Closing the game" + "\n")
        print('\n' +"Thanks for Playing !" + '\n')
        
def get_list (word):
        wordlist = []
        for ch in word:
            if ch != ' ':
                wordlist.append(ch)
        return wordlist
def match_with_gaps(my_word, other_word):        
    my_wordlist = get_list(my_word)
    other_wordlist = get_list(other_word)
    check_status =0
    count =0
    times = 0
    if len(my_wordlist) == len(other_wordlist):
        unique = []
        for ch in my_wordlist:         
            if ch != '_':                
                if ch not in unique:
                    unique.append(ch)
                    ch_index = my_wordlist.index(ch)
                    if ch == other_wordlist[ch_index]:
                        check_status += 1            
                else:
                    indexlist =[]
                    indexlist = [i for i, v in enumerate(my_wordlist) if v == ch]
                    for i in indexlist:
                        if my_wordlist[int(i)] == other_wordlist[int(i)]:
                            times +=1
                    if times == len(indexlist):
                        check_status +=1                              
                times=0
                count +=1
        if count == check_status :
            return 1
        else:
            return 0
    else:
        return 0
def show_possible_matches(my_word):
    possible_matches =[]
    for ch in wordlist:
        chlist = get_list (ch)
        my_word_list = get_list (my_word)
        if len(chlist) == len(my_word_list):
            need = match_with_gaps(my_word, ch)
            if need == 1:
                possible_matches.append(ch)
    return possible_matches
if __name__ == "__main__":    
    secret_word = choose_word(wordlist)
    hangman(secret_word)
