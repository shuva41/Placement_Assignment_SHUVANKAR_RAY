# Variables used for string manipulation
words = []
frequency = []
length_of_word = []

# Input String
input_string = input('Please enter the string: ')

list_of_words = input_string.split()
set_of_words = set(list_of_words)

for item in set_of_words:
    if list_of_words.count(item) > 1:
        words.append(item)
        frequency.append(list_of_words.count(item))

freq_set = set(frequency)

if len(freq_set) != len(frequency):
    for item in words:
        length_of_word.append(len(item))
    sorted_length = sorted(length_of_word,reverse=True)
    print(sorted_length[0])

else:
    word_freq = dict(zip(words,frequency))
    sorted_dict_keys = sorted(word_freq,reverse = True)
    print(len(sorted_dict_keys[0]))