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
   

def main():
    #import the word list
    with open("5letter_dict.txt", 'r') as fh:
        word_list = [line.rstrip() for line in fh]
    # Remove all words not 5 letters in length
    #populate a graph with 
    print_pattern("hello", [0,1,0,1,2])
if __name__ == "__main__":
    main()
