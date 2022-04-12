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


def check_if_possible(word, pattern):
    # pattern 
    pass
   

def pattern_from_int(pattern_i):
    pattern = [0]*5 
    digit_magnitudes = [3*3*3*3, 3*3*3, 3*3, 3, 1]
    for i in range(5):
        pattern[i] = int(pattern_i / digit_magnitudes[i])
        pattern_i = pattern_i - pattern[i]*digit_magnitudes[i]
    return pattern 

def pattern_from_guess(check_word, answer):
    pattern = [0]*5
    check_word = check_word.lower()
    answer = answer.lower()
    active_digits = [1, 1, 1, 1, 1] # We can only consider active digits, since position matters
    for i in range(5):
        if check_word[i] == answer[i]:
            pattern[i] = 0
            active_digits[i] = 0
        elif check_word[i] in answer:
            loc = answer.index(check_word[i])
            pattern[i] = 1
            active_digits[loc] = 0
        else:
            pattern[i] = 2
    return pattern 


def int_from_pattern(pattern):
    # Sometimes we want pattern as just an offset
    pattern_int = 0
    for i in range(5):
        pattern_int = pattern_int + pattern[i]*pow(3,4-i)
    return pattern_int

def find_valid_subset(search_pattern, check_word, word_list):
    # Find patterns for this word against the word_list, and add to search_pattern index to collect metrics for each guess
    # Find word-list subset that matches the search pattern
    # if condition 1 && condition 2 && ..., then add to whitelist
   
    pass


def prune_list(check_word, pattern, word_list):
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
                loc = x.find(check_word[i])
                if pattern[i] == 1:
                    if loc == -1 or active_digits[loc] == False or check_word[i] == x[i]:
                        # Letter cannot be in correct location for this condition
                        break
                        good_so_far = False
                    else:
                        active_digits[loc] = False
                elif loc != -1 and active_digits[loc]: # pattern[i] = 2
                    good_so_far = False
                    break 
            # If we never failed a condition then add to subset list
            if good_so_far:
                subset.append(x)
    return subset

def calculate_word(word, word_list):
    word = word.lower()
    likelihood = [0] * pow(3,5)
    word_space = [0] * pow(3,5)
    
    # For input word, calculate all possibilities in the word_list
    for i in range(len(word_list)):
        word_i = word_list[i].lower()
        pattern = pattern_from_guess(word, word_i)
        idx = int_from_pattern(pattern)
        likelihood[idx] = likelihood[idx] + 1
    
    for i in range(len(word_space)):
        # For each pattern, mask the word list to determine remaining space
        import pdb;pdb.set_trace()
        space = prune_list(word, pattern_from_int(i), word_list)
        word_space[i] = len(space)
        
                
def main():
    #import the word list
    with open("5letter_dict.txt", 'r') as fh:
        word_list = [line.rstrip() for line in fh]
    test_word = "found"
    calculate_word(test_word, word_list)

if __name__ == "__main__":
    main()
