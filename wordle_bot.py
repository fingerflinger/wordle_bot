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

def create_pattern(guess, answer):
    pattern = [-1, -1, -1, -1, -1]
    remaining_answer = []
    remaining_guess = []
    # Green 0
    for i in range(5):
        if guess[i] == answer[i]:
            pattern[i] = 0 
        else:
            remaining_answer.append(answer[i])
            remaining_guess.append(guess[i])
        
    # Yellow 1, Grey 2
    for i in range(len(guess)):
        yellow = remaining_guess[i] in remaining_answer
            
        for j in range(5):
            if pattern[j] < 0:
                if yellow:
                    pattern[j] = 1
                else:
                    pattern[i] = 2


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
   

def find_first_guess(wordlist):
    # For each word in the word list, check the possible outcomes vs remaining 
    # search space
    pattern_count = 3*3*3*3*3  # 3 possibilites for each letter
    for i in range(pattern_count):
        check_pattern = pattern_from_int(i)
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
    import pdb;pdb.set_trace()
    
def find_valid_subset(search_pattern, check_word, word_list):
    # Find patterns for this word against the dictionary, and add to search_pattern index to collect metrics for each guess
    # Find word-list subset that matches the search pattern
    # if condition 1 && condition 2 && ..., then add to whitelist
    pass
             
                

def main():
    #import the word list
    with open("5letter_dict.txt", 'r') as fh:
        word_list = [line.rstrip() for line in fh]
    pattern_from_guess("found", "fonde")
    #populate a graph with 

if __name__ == "__main__":
    main()
