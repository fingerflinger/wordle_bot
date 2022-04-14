import pytest

def extract_five_letter_words(dictionary_file_in, dictionary_file_out):
    with open(dictionary_file_in, 'r') as fh:
        lines = [line.rstrip() for line in fh]
    # Remove all words not 5 letters in length
    five_letter_words = []
    for line in lines:
        if len(line) == 5:
            five_letter_words.append(line)
    with open(dictionary_file_out, 'w') as file_handler:
        for item in five_letter_words:
            file_handler.write("{}\n".format(item))
    print("done!")


def print_pattern(word, pattern):
    print_str = ""        
    for i in range(5):
        if pattern[i] == 0:
            print_str = print_str + '\033[92m'
        elif pattern[i] == 1:
            print_str = print_str + '\033[93m'
        elif pattern[i] == 2:
            print_str = print_str + '\033[0m'
        print_str = print_str + word[i]
    print_str = print_str + '\033[0m'
    print(print_str)


def pattern_from_int(pattern_i):
    pattern = [0]*5 
    digit_magnitudes = [3*3*3*3, 3*3*3, 3*3, 3, 1]
    for i in range(5):
        pattern[i] = int(pattern_i / digit_magnitudes[i])
        pattern_i = pattern_i - pattern[i]*digit_magnitudes[i]
    return pattern 

def pattern_from_guess(check_word, answer):
    pattern = [-1]*5
    # Kludgy but YOLO
    check_word = check_word.lower()
    check_word_digits = [True]*5
    answer = answer.lower()
    answer_digits = [True]*5

    # Need to check in place matches first
    for i in range(5):
        if check_word[i] == answer[i]:
            pattern[i] = 0
            answer_digits[i] = False
            check_word_digits[i] = False
    for i in range(5):
        if check_word_digits[i] == False:
            # pattern is defined by check_word
            continue
        loc = find_idx_in_active_digits(answer, answer_digits, check_word[i])
        if loc == -1:
            pattern[i] = 2
        else:
            pattern[i] = 1
            answer_digits[loc] = False

    return pattern


def int_from_pattern(pattern):
    # Sometimes we want pattern as just an offset
    pattern_int = 0
    for i in range(5):
        pattern_int = pattern_int + pattern[i]*pow(3,4-i)
    return pattern_int


def find_idx_in_active_digits(word, active_digits, letter):
    loc = word.find(letter) # First occurance
    loc_offset = 0
    if loc == -1:
        return -1
    if active_digits[loc] == True:
        return loc
    while(active_digits[loc+loc_offset] == False):
        # How to handle 3-4 occurances of the same letter? Need to update loc
        new_offset = word[(loc+loc_offset+1):].find(letter) # Need to search only active digits
        if new_offset == -1:
            # Eventually we will hit the end of the word and end up here
            return -1
        loc_offset = loc_offset + new_offset + 1 # + 1 here because -1 indicates fail 2 find
    
    # We kick out of the loop once active_digits[loc+locoffset] is True
    return loc+loc_offset

def valid_subset(check_word, pattern, word_list):
    # TODO, there is a bug here that misses some edge cases
    # Return word list subset that conforms to the pattern
    # NOTE: I think there is a way of doing this as a mask operation, but out of expediency, going to loop through
    subset = []
    check_word = check_word.lower()
    for x in word_list:
        x = x.lower()
        good_so_far = True
        active_digits = [True] * 5  # The unresolved digits in x
        # Need to check for in place digits first
        for i in range(5):
            if pattern[i] == 0:
                if check_word[i] != x[i]:
                    good_so_far = False
                    break
                else:
                    active_digits[i] = False

        # Surely there is a more elegant implentation, but who cares
        if good_so_far:
            for i in range(5):
                if pattern[i] == 0:
                    # we already did these
                    continue
                loc = find_idx_in_active_digits(x, active_digits, check_word[i])

                if pattern[i] == 1:
                    if loc == -1 or active_digits[loc] == False or check_word[i] == x[i]:
                        # Letter cannot be in correct location for this condition
                        good_so_far = False
                        break
                    else:
                        active_digits[loc] = False
                elif loc != -1 and active_digits[loc]: # pattern[i] = 2
                    good_so_far = False
                    break 
            # If we never failed a condition then add to subset list
            if good_so_far:
                subset.append(x)
    return subset

def test_valid_subset():
    check_word = "crots"
    pattern = [2, 0, 0, 0, 0]
    word_list = ["trots", "grots", "crots", "motss"]
    subset = valid_subset(check_word, pattern, word_list)
    print(subset)

def calculate_word(word, word_list):
    word = word.lower()
    likelihood = [0] * pow(3,5)
    
    # For input word, calculate all possibilities in the word_list
    for i in range(len(word_list)):
        word_i = word_list[i].lower()
        pattern = pattern_from_guess(word, word_i)
        idx = int_from_pattern(pattern)
        likelihood[idx] = likelihood[idx] + 1
    return likelihood 


def calc_guess_value(likelihood):
    # Expected value of this guess
    total_possibilities = sum(likelihood)
    guess_value = 0
    for x in likelihood:
        guess_value = guess_value + x*x / total_possibilities
    return guess_value


def calc_first_guess(wordlist):
    best_word = ""
    best_word_value = -1
    for test_word in word_list:
        likelihood = calculate_word(test_word, word_list)
        value = calc_guess_value(likelihood)
        if best_word_value < 0 or value < best_word_value:
            best_word = test_word
            best_word_value = value
            print(best_word)
            print(best_word_value)
    return best_word

def calc_guess_n(word_list):
    best_word = ""
    best_word_value = -1
    for test_word in word_list:
        likelihood = calculate_word(test_word, word_list)
        value = calc_guess_value(likelihood)
        if best_word_value < 0 or value < best_word_value:
            best_word = test_word
            best_word_value = value
            print("{} {}".format(best_word, best_word_value))
    return best_word


def do_solve(answer):
    # Guesses are only valid if on word list, so do not have to calculate exhaustive 5 letter sequences
    with open("5letter_dict.txt", 'r') as fh:
        word_list = [line.rstrip().lower() for line in fh]
    answer = answer.lower()
    if answer not in word_list:
        print("Sorry, this word isn't in my vocabulary, I won't be able to solve for it")
        return False
    '''
    Challenges
    Black - runtime? Stuck in a loop?
    Royal - runtime? Stuck in a loop?
    '''
    my_guess = "lares"
    subset = word_list 

    for i in range(5): # 5 guesses after the first
        # Make guess
        print("Guess #{} is {}".format(i+1, my_guess))
        pattern = pattern_from_guess(my_guess, answer)
        print_pattern(my_guess, pattern)
        if int_from_pattern(pattern) == 0:
            print("SUCCESS")
            return my_guess
        subset = valid_subset(my_guess, pattern, subset)
        print("Remaining possible words: {}".format(len(subset)))
        my_guess = calc_guess_n(subset)

    return False


def interactive():
    done = False
    my_guess = 'lares'
    print("Please guess LARES for your first guess and enter the resulting pattern")
    print("0 for green, 1 for yellow, 2 for grey")
    with open("5letter_dict.txt", 'r') as fh:
        subset = [line.rstrip() for line in fh]
    while(done == False):
        # Get pattern from the previous guess
        pattern = input("Please enter the pattern:\n")
        if pattern == "quit":
            done = True
        pattern = list(pattern)
        # print out next guess
        subset = valid_subset(my_guess, pattern, subset)
        my_guess = calc_guess_n(subset)
        print("Here is my new guess, enter it {}".format(my_guess))
   
def test_find_idx_in_active_digits():
    find_idx_in_active_digits('spear', [False, True, True, True, True], 'e')

def test_pattern_from_guess():
    print(pattern_from_guess_2('lares', 'black'))
    print(pattern_from_guess_2('lares', 'royal'))


def main():
    #test_valid_subset()
    #test_pattern_from_guess()
    #test_find_idx_in_active_digits()
    interactive()
         
    
if __name__ == "__main__":
    main()
