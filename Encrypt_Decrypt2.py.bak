# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations
from random import randint
import re

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
 #   print("  ", len(wordlist), "words loaded.")
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


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
#VOWELS_LOWER = 'aeiou'
#VOWELS_UPPER = 'AEIOU'
#CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
#CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
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
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        letters_list = list(string.ascii_letters)
        vowels_upper = ['A','E','I','O','U']
        vowels_lower = ['a','e','i','o','u']
        vowels_list = vowels_upper + vowels_lower
        permutation_list = list(vowels_permutation)
        transpose_dict ={}
        i=0
        j=0
        for ch in letters_list:
            if ch not in vowels_list:
                transpose_dict[ch] = ch
            if ch in vowels_upper:
                transpose_dict[ch] = permutation_list[i].upper()
                i+=1
            if ch in vowels_lower:
                transpose_dict[ch] = permutation_list[j].lower()
                j+=1
        return transpose_dict
                
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        text = self.get_message_text()
        text_list = list(text)
        encrypt_list =[]
        for ch in text_list:
            if ch in string.ascii_letters:
                encrypt_list.append(transpose_dict[ch])
            else:
                encrypt_list.append(ch)
        encrypted_text = ''.join(encrypt_list)
        return encrypted_text
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)


    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        text = self.message_text
        decrypt_list =[]
        words_all = re.findall(r"[\w']+|[.,!?;]+ |[\" @#$%^&*()_+\<\>\!\{\}\'\\\/]",text)
        for w in words_all:
            key =1
            char_list = list(w)
            for ch in char_list:
                if ch not in string.ascii_letters:
                    key =0
                    break
            if key ==1:
                perm_list = get_permutations("aeiou")
                for p in perm_list:
                    word=[]
                    dictionary = self.build_transpose_dict(p)            
                    for ch in char_list:
                        word.append(dictionary[ch])
                    word_string = ''.join(word)
                    if is_word(self.valid_words, word_string) ==1:
                        decrypt_list.append(word_string)
                        break
            else:
                decrypt_list.append(w)
        decrypt_text = ''.join(decrypt_list)
        return decrypt_text
                    

if __name__ == '__main__':
    print("Welcome to Caesar Cipher Console")
    inp = input("Enter the console Definition \n 0 :Encrypt the message \n 1: Decrypt the message \n")
    if inp == '0':
        text = input("Enter text to Encrypt")
        message = SubMessage(text)
        permutation_txt_list = get_permutations("aeiou")
        list_length = len(permutation_txt_list)
        i = randint(1,list_length)
        permutation_txt = permutation_txt_list[i]
#        print(permutation_txt)
        transpose_dict = message.build_transpose_dict(permutation_txt)
#        print(transpose_dict)
        encrypted_text = message.apply_transpose(transpose_dict)
        print("Your encrypted Message is :"+"\n" + encrypted_text)
    if inp == '1':
        text = input("Enter text to Decrypt")
        message = EncryptedSubMessage(text)
        decrypted_text = message.decrypt_message()
        print("Your decrypted Message is :"+"\n" + decrypted_text)
        print('\n'+ "NOTE: Some words might have multiple decryptions!!")
    