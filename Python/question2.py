input_string = input("The input string is: ")


def checking_func(i_s):
    count_of_char = dict()

    list_of_char = list(i_s)
    set_of_char = set(list_of_char)

    for item in set_of_char:
        count = list_of_char.count(item)
        count_of_char[item] = count
    print(count_of_char)
    freq_of_char = count_of_char.values()
    return freq_of_char


result = checking_func(input_string)
if len(set(result)) == 1:
    print('Yes')
else:
    trunc_string = input_string[:-1]
    print(trunc_string)
    result = checking_func(trunc_string)
    if len(set(result)) == 1:
        print('Yes')
    else:
        print('No')

