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
    check_word = check_word.lower()
    answer = answer.lower()
    active_digits = [True] * 5 # We can only consider active digits, since position matters
    # Need to check in place matches first
    for i in range(5):
        if check_word[i] == answer[i]:
            pattern[i] = 0
            active_digits[i] = False
    for i in range(5):
        # extract remaining letters
        remaining = []
        remaining_idx = []
        for j in range(5):
            if active_digits[j]:
                remaining.append(answer[j])
                remaining_idx.append(j)
        if pattern[i] < 0:
            # Is this letter in the remaining letters?
            if check_word[i] in remaining:
                loc = remaining.index(check_word[i])
                pattern[i] = 1
                active_digits[loc] = False
            else:
                pattern[i] = 2
    return pattern 


def int_from_pattern(pattern):
    # Sometimes we want pattern as just an offset
    pattern_int = 0
    for i in range(5):
        pattern_int = pattern_int + pattern[i]*pow(3,4-i)
    return pattern_int


def find_idx_in_active_digits(word, active_digits, letter):
    loc = word.find(letter) # Need to search only active digits
    if loc == -1:
        return loc
    while(active_digits[loc] == False):
        import pdb;pdb.set_trace()
        loc = word[(loc+1):].find(letter) # Need to search only active digits
        if loc == -1:
            return loc
    return loc

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
            print(best_word)
            print(best_word_value)
    return best_word


def do_solve():
    # Guesses are only valid if on word list, so do not have to calculate exhaustive 5 letter sequences
    with open("5letter_dict.txt", 'r') as fh:
        word_list = [line.rstrip() for line in fh]
    my_answer = "trots"
    my_guess = "lares"
    subset = word_list 

    for i in range(5): # 5 guesses after the first
        # Make guess
        print("Guess #{}".format(i+1))
        pattern = pattern_from_guess(my_guess, my_answer)
        if int_from_pattern(pattern) == 0:
            print("SUCCESS")
            break
        if i == 1:
            import pdb;pdb.set_trace()
        subset = valid_subset(my_guess, pattern, subset)
        my_guess = calc_guess_n(subset)


def main():
    test_valid_subset()
         
    
if __name__ == "__main__":
    main()
