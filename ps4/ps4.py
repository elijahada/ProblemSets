##ELijah Ada
# 6.00 Problem Set 4
#
# Caesar Cipher Skeleton
#
import string
import random
import copy
import operator

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print "  ", len(wordlist), "words loaded."
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    #>>> is_word(wordlist, 'bat') returns
    True
    #>>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words  
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: -27 < int < 27
    returns: dict

    Example:
    #>>> build_coder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)
    """
    ### TODO.
    original_dict_lower = {
    'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i', 'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r', 's': 's', 't': 't', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y', 'z': 'z', ' ':' '
    }
    original_dict_upper = {
    'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z', ' ': ' '
    }
    sorted_dict_lower = sorted(original_dict_lower.items(), key=operator.itemgetter(0))
    sorted_dict_upper = sorted(original_dict_upper.items(), key=operator.itemgetter(0))
    # print sorted_dict_lower
    new_dict_lower = {}
    new_dict_upper = {}
    # print type(new_dict_lower)
    # print "shift:", shift
    # print "new_dict_lower ", new_dict_lower
    for x in range(0, 27):
        if (x+shift) >= 27:
            over_shift = (x+shift-27)
            new_dict_lower.update({sorted_dict_lower[x][0] : sorted_dict_lower[over_shift][1]})
            new_dict_upper.update({sorted_dict_upper[x][0] : sorted_dict_upper[over_shift][1]})
        elif (x+shift) < 0:
            under_shift = (x+shift+27)
            new_dict_lower.update({sorted_dict_lower[x][0] : sorted_dict_lower[under_shift][1]})
            new_dict_upper.update({sorted_dict_upper[x][0] : sorted_dict_upper[under_shift][1]})
        else:
            new_dict_lower.update({sorted_dict_lower[x][0] : sorted_dict_lower[x+shift][1]})
            new_dict_upper.update({sorted_dict_upper[x][0] : sorted_dict_upper[x+shift][1]})
        # print new_dict_lower
        # x += 1
    final_dict = dict(new_dict_upper, **new_dict_lower)
    # print final_dict
    # for key, value in final_dict .items():
    #     print key, value
    # # print "the new dict is: ", new_dict_lower
    # print "the old dict is ", original_dict_lower
    return final_dict

# print build_coder(3) #used to test above function

def build_encoder(shift):
    """
    Returns a dict that can be used to encode a plain text. For example, you
    could encrypt the plain text by calling the following commands
    # >>>encoder = build_encoder(shift)
    # >>>encrypted_text = apply_coder(plain_text, encoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    # >>> build_encoder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    ### TODO.
    while True:
        if shift >= 0 and shift < 27 :
            break
        else:
            print "That is not a valid input."
            print
    final_dict = build_coder(shift)
    return final_dict

# shift = int(raw_input("Please input a shift (0 <= int < 27): "))
# print build_encoder(shift)


def build_decoder(shift):
    """
    Returns a dict that can be used to decode an encrypted text. For example, you
    could decrypt an encrypted text by calling the following commands
    # >>>encoder = build_encoder(shift)
    # >>>encrypted_text = apply_coder(plain_text, encoder)
    # >>>decrypted_text = apply_coder(plain_text, decoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    # >>> build_decoder(3)
    {' ': 'x', 'A': 'Y', 'C': ' ', 'B': 'Z', 'E': 'B', 'D': 'A', 'G': 'D',
    'F': 'C', 'I': 'F', 'H': 'E', 'K': 'H', 'J': 'G', 'M': 'J', 'L': 'I',
    'O': 'L', 'N': 'K', 'Q': 'N', 'P': 'M', 'S': 'P', 'R': 'O', 'U': 'R',
    'T': 'Q', 'W': 'T', 'V': 'S', 'Y': 'V', 'X': 'U', 'Z': 'W', 'a': 'y',
    'c': ' ', 'b': 'z', 'e': 'b', 'd': 'a', 'g': 'd', 'f': 'c', 'i': 'f',
    'h': 'e', 'k': 'h', 'j': 'g', 'm': 'j', 'l': 'i', 'o': 'l', 'n': 'k',
    'q': 'n', 'p': 'm', 's': 'p', 'r': 'o', 'u': 'r', 't': 'q', 'w': 't',
    'v': 's', 'y': 'v', 'x': 'u', 'z': 'w'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    ### TODO.
    decoder = build_coder(27-shift)
    # print decoder
    return decoder
# print build_decoder(3)

def apply_coder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text

    Example:
    # >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor,czruog!'
    # >>> apply_coder("Khoor,czruog!", build_decoder(3))
    'Hello, world!'
    """
    ## TODO.
    encoded_text = ''
    for letter in text:
        if letter in coder:
            encoded_text += coder[letter]
        else:
            encoded_text += letter
    return encoded_text


def apply_shift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.
    
    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    # >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    ### TODO.
    encoder = build_coder(shift)
    # print encoder
    encoded_text = apply_coder(text, encoder)
    # print "'" + encoded_text + "'"
    return encoded_text

# text = raw_input("Please input text you would like encripted: ")
# shift = int(raw_input("Please input a shift (0 <= int < 27): "))
# encoded_text = apply_shift(text, shift)
# decoder = build_decoder(shift)
# decoded_text = apply_coder(encoded_text, decoder)
# print "'" + decoded_text + "'"
#
# Problem 2: Codebreaking.
#
def find_best_shift(wordlist, text):
    """
    Decrypts the encoded text and returns the plaintext.

    text: string
    returns: 0 <= int 27

    Example:
    # >>> s = apply_coder('Hello, world!', build_encoder(8))
    # >>> s
    'Pmttw,hdwztl!'
    # >>> find_best_shift(wordlist, s) returns
    8
    # >>> apply_coder(s, build_decoder(8)) returns
    'Hello, world!'
    """
    ### TODO
    # possible_shift1 = 0
    # possible_shift2 = 0
    real_words1 = ()
    real_words2 = ()
    round = 0
    for shift in range(0, 27, 2):
        # print "It is currently round", round
        possible_shift1 = apply_shift(text, shift)
        # print "The current possible shift 1 is", str(shift) + " and looks like", str(possible_shift1)
        possible_words1 = possible_shift1.split()
        for word1 in possible_words1:
                if is_word(wordlist, word1) == True:
                    real_words1 += (word1,)
        # print "Possible words from shift 1 are", possible_words1
        # print "The real words in 1 are", real_words1
        if shift < 27:
            possible_shift2 = apply_shift(text, (shift+1))
            # print "The current possible shift 2 is", str(shift+1) + " and looks like", str(possible_shift2)
            possible_words2 = possible_shift2.split()
            for word2 in possible_words2:
                if is_word(wordlist, word2) == True:
                    real_words2 += (word2,)
            # print "Possible words from shift 2 are", possible_words2
            # print "The real words in 2 are", real_words2
        if shift == 0:
            if len(real_words1) > len(real_words2):
                current_guess = shift
                words_in_current_guess = real_words1
                real_words1 = ()
                real_words2 = ()
            elif len(real_words1) == len(real_words2) and len(real_words1) != 0 and len(real_words2) != 0:
                if len(max(real_words1, key=len)) > len(max(real_words2, key=len)):
                    current_guess = shift
                    words_in_current_guess = real_words1
                    real_words1 = ()
                    real_words2 = ()
                else:
                    current_guess = shift+1
                    words_in_current_guess = real_words2
                    real_words1 = ()
                    real_words2 = ()
            else:
                current_guess = shift+1
                words_in_current_guess = real_words2
                real_words1 = ()
                real_words2 = ()
        else:
            if len(words_in_current_guess) < len(real_words1):
                if len(real_words1) < len(real_words2):
                    current_guess = shift+1
                    words_in_current_guess = real_words2
                    real_words1 = ()
                    real_words2 = ()
                else:
                    current_guess = shift
                    words_in_current_guess = real_words1
                    real_words1 = ()
                    real_words2 = ()

            elif len(words_in_current_guess) < len(real_words2):
                if len(real_words2) < len(real_words1):
                    current_guess = shift
                    words_in_current_guess = real_words1
                    real_words1 = ()
                    real_words2 = ()
                else:
                    current_guess = shift+1
                    words_in_current_guess = real_words2
                    real_words1 = ()
                    real_words2 = ()
            else:
                if len(words_in_current_guess) == len(real_words2) and len(words_in_current_guess) != 0 and len(real_words2) != 0:
                    if len(max(words_in_current_guess, key=len)) > len(max(real_words2, key=len)):
                        # print "max(words_in_current_guess, key=len)", max(words_in_current_guess, key=len)
                        # print "max(real_words2, key=len)", max(real_words2, key=len)
                        current_guess = current_guess
                        real_words1 = ()
                        real_words2 = ()
                    else:
                        current_guess = shift+1
                        words_in_current_guess = real_words2
                        real_words1 = ()
                        real_words2 = ()
                elif len(words_in_current_guess) == len(real_words1) and len(words_in_current_guess) != 0 and len(real_words1) != 0:
                    if len(max(words_in_current_guess, key=len)) > len(max(real_words1, key=len)):
                        current_guess = current_guess
                        real_words1 = ()
                        real_words2 = ()
                    else:
                        current_guess = shift
                        words_in_current_guess = real_words1
                        real_words1 = ()
                        real_words2 = ()
                else:
                    current_guess = current_guess
                    real_words1 = ()
                    real_words2 = ()
        round += 1
        # print "The current guess is", current_guess
        # print # empty line for spacing
    true_shift = current_guess
    # print "The True shift is", true_shift
    return true_shift

##-----for testing above
# true_shift = find_best_shift(wordlist, 'Apq hq hiham a.') #This is a test.
# print apply_coder('Apq hq hiham a.', build_decoder(8)) #tests previous function
##---- for testing problem 4
# s = 'eqorqukvqtbmultiform wyy ion'
# true_shift = find_best_shift(wordlist, s)
# print apply_shift(s, 25)


#
# Problem 3: Multi-level encryption.
#
def apply_shifts(text, shifts):
    """
    Applies a sequence of shifts to an input text.

    text: A string to apply the Ceasar shifts to 
    shifts: A list of tuples containing the location each shift should
    begin and the shift offset. Each tuple is of the form (location,
    shift) The shifts are layered: each one is applied from its
    starting position all the way through the end of the string.  
    returns: text after applying the shifts to the appropriate
    positions

    Example:
    # >>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    """
    ### TODO.
    for tuple in shifts:
        print "Text =", text
        print "Tuple", tuple
        print "The first element is:", tuple[0]
        print "The second element is:", tuple[1]
        new_text = text[tuple[0]:]
        print "new_text =", new_text
        old_text = text[:tuple[0]]
        print "old_text =", old_text
        shifted_text = apply_shift(new_text,tuple[1])
        print "shifted_text =", shifted_text
        text = old_text + shifted_text
        print "shifted_string", text
    return text

# test_shifts = [(0,6), (3, 18), (12, 16)]
# print apply_shifts("Do Androids Dream of Electric Sheep?", test_shifts)
## 'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
##Above are for testing above function (Problem 3)

#
# Problem 4: Multi-level decryption.
#

def find_best_shift_for_next_word(wordlist, text): #for problem 4
    real_words1 = ()
    real_words2 = ()
    round = 1
    for shift in range(0, 27, 2):
        possible_words1 = []
        possible_words2 = []
        word1 = ""
        word2 = ""
        # print "It is currently round", round
        possible_shift1 = apply_shift(text, shift)
        # print "The current possible shift 1 is", str(shift) + " and looks like", str(possible_shift1)
        possible_words1 = possible_shift1.split()
        if len(possible_words1) > 0:
            word1 = possible_words1[0]
        else:
            word1 = ""
        if is_word(wordlist, word1) == False:
            word1 = ""
            # print "The real word in 1 is", word1
        if shift < 27:
            possible_shift2 = apply_shift(text, (shift+1))
            # print "The current possible shift 2 is", str(shift+1) + " and looks like", str(possible_shift2)
            possible_words2 = possible_shift2.split()
            if len(possible_words2) >0:
                word2 = possible_words2[0]
            else:
                word2 = ""
            if is_word(wordlist, word2) == False:
                word2 = ""
            # print "The real word in 2 is", word2
        if shift == 0:
            if len(word1) > len(word2):
                current_guess = shift
                current_word_guess = word1
            else:
                current_guess = shift+1
                current_word_guess = word2
        else:
            if len(word1) > len(word2):
                long_word_guess = word1
                long_word_shift = shift
            else:
                long_word_guess = word2
                long_word_shift = shift + 1
            if len(current_word_guess) < len(long_word_guess):
                current_word_guess = long_word_guess
                current_guess = long_word_shift
        round += 1
        # print "The current guess is", current_guess
    true_shift = current_guess
    print "The true shift is", true_shift
    return true_shift


def find_best_shifts(wordlist, text):
    """
    Given a scrambled string, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: Make use of the recursive function
    find_best_shifts_rec(wordlist, text, start)

    wordlist: list of words
    text: scambled text to try to find the words for
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    
    Examples:
    # >>> s = random_scrambled(wordlist, 3)
    # >>> s
    # 'eqorqukvqtbmultiform wyy ion'
    # >>> shifts = find_best_shifts(wordlist, s)
    # >>> shifts
    # [(0, 25), (11, 2), (21, 5)]
    # >>> apply_shifts(s, shifts)
    # 'compositor multiform accents'
    # >>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    # >>> s
    # 'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    # >>> shifts = find_best_shifts(wordlist, s)
    # >>> print apply_shifts(s, shifts)
    Do Androids Dream of Electric Sheep?
    """
    start = 0 # default
    # start = int(raw_input("Please input the starting position: "))
    tuple_of_best_shifts = find_best_shifts_rec(wordlist, text, start)
    return tuple_of_best_shifts

def find_best_shifts_rec(wordlist, text, start):
    """
    Given a scrambled string and a starting position from which
    to decode, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: You will find this function much easier to implement
    if you use recursion.

    wordlist: list of words
    text: scambled text to try to find the words for
    start: where to start looking at shifts
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    """
    ### TODO.
    list_of_best_shifts = []
    decoded_text = text[:start]
    encoded_text = text[start:]
    best_shift = (start, find_best_shift_for_next_word(wordlist, encoded_text))
    # print "best_shift =", best_shift
    list_of_best_shifts.append(best_shift)
    # print "list_of_best_shifts =", list_of_best_shifts
    new_decoded_text = apply_shift(encoded_text,best_shift[1])
    point = new_decoded_text.find(" ")
    # print "point =",point
    if start > len(text):
        return list_of_best_shifts
    else:
        decoded_text = decoded_text + new_decoded_text[:point]
        encoded_text = new_decoded_text[point:]
        text = decoded_text + encoded_text
        # print "(decoded_text =", decoded_text + ") (encoded_text=", encoded_text + ")"
        # print "text =", text
        start = len(decoded_text) + 1
        # print "start =", start
        real_words = ()
        possible_words = []
        list_of_best_shifts.extend(find_best_shifts_rec(wordlist, text, start))
        return list_of_best_shifts
    # if point >= 0:
    #     decoded_text = decoded_text + new_decoded_text[:point]
    #     encoded_text = new_decoded_text[point:]
    #     text = decoded_text + encoded_text
    #     # print "(decoded_text =", decoded_text + ") (encoded_text=", encoded_text + ")"
    #     # print "text =", text
    #     start = len(decoded_text) + 1
    #     # print "start =", start
    #     real_words = ()
    #     possible_words = []
    #     list_of_best_shifts.extend(find_best_shifts_rec(wordlist, text, start))
    #     return list_of_best_shifts
    # else:
    #     # print "We are now in the last layer"
    #     # print "best_shift = ", best_shift
    #     # print "Type of best_shift =", type(best_shift)
    #     return list_of_best_shifts


# s = 'eqorqukvqtbmultiform wyy ion' # 'compositor multiform accents'
# shifts = find_best_shifts(wordlist, s)
# print "shifts =", shifts # [(0, 25), (11, 2), (21, 5)]
# print apply_shifts(s, shifts)
# print apply_shifts(s, [(0, 25), (11, 2), (21, 5)])
#-----
# s = random_scrambled(wordlist, 3)
# print "Returning random scrambled set of words"
# print
# print "The scrambled string is:", s
# print
# shifts = find_best_shifts(wordlist, s)
# print "shifts = ", shifts
# print "The string is ", s
# print apply_shifts(s, shifts)
# #above for testing problem 4
# #----

def decrypt_fable():
    """
    Using the methods you created in this problem set,
    decrypt the fable given by the function get_fable_string().
    Once you decrypt the message, be sure to include as a comment
    at the end of this problem set how the fable relates to your
    education at MIT.

    returns: string - fable in plain text
    """
    ### TODO.
    fable_string = get_fable_string()
    print "fable_string = ", fable_string
    fable_best_shifts = find_best_shifts(wordlist, fable_string)
    print "fable_best_shifts =", fable_best_shifts
    fable_decoded = apply_shifts(fable_string, fable_best_shifts)
    return fable_decoded
fable_decoded = decrypt_fable()
print "The decrypted fable is:", fable_decoded

#What is the moral of the story?
# The smarter man is the one who knows and understands his mistakes so that next time he will be sure to not make them.
# The next time he builds something, it will be more successful than the first.
#
#
#

