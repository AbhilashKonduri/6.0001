import string
import re
from random import randint

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
#    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
#    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

#def get_story_string():
#    """
#    Returns: a story in encrypted text.
#    """
#    f = open("story.txt", "r")
#    story = str(f.read())
#    f.close()
#    return story
#
### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words
    
    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''

        lower_letters = list(string.ascii_lowercase)
        upper_letters = list(string.ascii_uppercase)
        mapping_dict = {}
        for ch in string.ascii_letters:
            if ch in string.ascii_lowercase:
                index = lower_letters.index(ch)
                shift_change = index - shift
                if abs(shift_change) > 26 :
                    shift_change %=26 
                mapping_dict[ch] = lower_letters[shift_change]   
            if ch in string.ascii_uppercase:
                index = upper_letters.index(ch)   
                shift_change = index - shift
                if abs(shift_change) > 26 :
                    shift_change %=26 
                mapping_dict[ch] = upper_letters[shift_change]             
        return mapping_dict
        
    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        original_list = list(self.get_message_text())
        req_list = []
        mapping_dict = self.build_shift_dict(shift)   
        for ch in original_list:
            if ch in string.ascii_letters:
                req_list.append(mapping_dict[ch])
            else:
                req_list.append(ch)
        return(''.join(req_list))
            

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
        self.shift = shift
        self.encryption_dict =  self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.get_encryption_dict
    
    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.get_message_text_encrypted()

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.__init__(self.text, shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
#        print("Entered Class Cipher Message")
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

        

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: decrypted message text
        
        '''
#        print("Entered Class Decrypt Message")
        string_cut = self.get_message_text()
#        print(string_cut)
        words_all = re.findall(r"[\w']+|[.,!?;]+ |[\" @#$%^&*()_+\<\>\!\{\}\'\\\/]",string_cut)
#        while("" in words):
#            words.remove("")
        words= []
        for w in words_all:
            for ch in w:
                if ch in string.ascii_letters:
                    flag = 0
                else:
                    flag = 1
            if flag ==0:
                words.append(w)
#       print(words)
        
        shift_list = []
        for w in words:
            shift = 0
            while (shift<27):
                new_letter = []
                dictionary = self.build_shift_dict(shift)
                for ch in w:
                    new_letter.append(dictionary[ch])
                    new_word= ''.join(new_letter)
                if (is_word(self.valid_words, new_word)):            
                    shift_list.append(shift)
                    break
                else:
                    shift+=1
                    if shift ==27:
                        shift_list.append(0)

#        print(shift_list)
        i= 0
        real_word_list=[]
        for w in words:
#            print(w)
            real_char_list= []
            mapping_dict = self.build_shift_dict(shift_list[i])   
            for ch in w:
                real_char_list.append(mapping_dict[ch])
            real_word = ''.join(real_char_list)
#            print(real_word)
            real_word_list.append(real_word)
            i+=1
#        print(real_word_list)
        
#        print(words_all)
        i=0
        for w in words_all:
            index = words_all.index(w)
            for ch in w:
                if ch in string.ascii_letters:
                    flag = 1
                else:
                    flag = 0
                    break
            if flag ==1:
                words_all[index] = real_word_list[i]
#                print(w)
#                print(real_word_list[i])
#                print("Transfer happening")
                i+=1
#                print(words_all)
        decrypted_string = ''.join(words_all)
        return decrypted_string
    
    def get_multiple(self,word):
        '''
        inputs a dis scrambled word and returns all possible solutions
        '''        
        shift_list = []
        shift = 0
        point =0
        while (shift<26):
            new_letter = []
            dictionary = self.build_shift_dict(shift)
            for ch in word:
                if ch in string.ascii_letters:
                    new_letter.append(dictionary[ch])
            new_word= ''.join(new_letter)
            if (is_word(self.valid_words, new_word)):            
                shift_list.append(shift)
                point +=1
                shift +=1
#                print(shift)
            else:
                shift+=1
#        print(shift_list)
        if point >= 1:        
            real_word = []
            i= 0
            real_char_list= []
            while(i < point):
                mapping_dict = self.build_shift_dict(shift_list[i])   
                for ch in word:
                     if ch in string.ascii_letters:
                         real_char_list.append(mapping_dict[ch])
                real_word.append( ''.join(real_char_list))
                real_char_list= []
                i+=1
            return real_word

if __name__ == '__main__':
        print("Welcome to Caesar Cipher Console")
        inp = input("Enter the console Definition \n 0 :Encrypt the message \n 1: Decrypt the message \n")
        if inp == '0':
                text = input("Enter text to Encrypt")
                text_list = re.findall(r"[\w']+|[.,!?;]+ |[\" @#$%^&*()_+\<\>\!\{\}\'\\\/]", text)
#                print(text_list)
                Encrypted_word = []
                for word in text_list:
                    if word in string.punctuation:
                        Encrypted_word.append(word)
                    else:
                        T = Message(word)
                        shift = randint(1, 25)
                        Encrypted_word.append(T.apply_shift(shift))
                print(''.join(Encrypted_word))
        if inp == '1':
            proceed = 1
            try:
                text = input("Enter Message to decrypt")
                T = CiphertextMessage(text)
                print(T.decrypt_message())
            except:
                proceed =0
                print("The text entered has Encountered an Error.\n Please check the Spellings and input only the valid Words for Encryption as provided in the wordlist.")
            if proceed == 1:
                print("Some Words might have actually found multiple solutions. Would you like to review them? ")
                key = input("0: NO thanks i have found the message! \n1:Yes give me those.The message is not clear!\n")
                if key == '1':
                    text_list = re.findall(r"[\w']+|[.,!?;]+ |[\" @#$%^&*()_+\<\>\!\{\}\'\\\/]", text)
                    for word in text_list:
                        if word not in string.punctuation:
                            if word != " " :
                                print(word + ':',T.get_multiple(word))