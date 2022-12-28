def zero_adder_to_number(number, zero_number):
    string = str(number)
    list_of_str = list(string)
    for i in range(0, zero_number - len(list_of_str)):
        list_of_str.insert(0, "0")
    result = "".join(list_of_str)
    print(result)


# zero_adder_to_number(23, 3)

def string_uppercase(string):
    str_list = string.split("-")
    new_list = []
    for i in str_list:
        new_word = i.title()
        new_list.append(new_word)
    return " ".join(new_list)


string_uppercase("fire-fang")
