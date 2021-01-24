from subprocess import call
import os
from colorama import Fore
import dateutil.parser as dp
import unicodedata
import json


def find_str(string, char):
    """
    Return index of first occurance of character char in string string
    :param string: chosen string: "hello"
    :param char: chosen char: "r"
    :return: index where char is found in string. -1 if not found.
    """
    index = 0
    if char in string:
        c = char[0]
        for ch in string:
            if ch == c:
                if string[index:index+len(char)] == char:
                    return index
            index += 1
    return -1



def convert_ISO_time_to_seconds(iso_time_str):
    """
    Convert ISO time to corresponding number of seconds
    :param iso_time_str:
    :return:
    """
    parsed_t = dp.parse(iso_time_str)
    t_in_seconds = parsed_t.strftime('%s')
    return t_in_seconds


def RepresentsInt(s):
    """
    Check whether a given input is an int or not (True/false)
    :param s: input to check
    :return: True/False (int / something else)
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def RepresentsFloat(s):
    """
        Check whether a given input is a float or not (True/false)
        :param s: input to check
        :return: True/False (float / something else)
        """
    try:
        float(s)
        return True
    except ValueError:
        return False


def specify_int_in_range(min, max, message="Your choice ", error=""):
    """
    Ask the user to specify an int between min and max, and will keep asking for the value
    if the user gives an int out of range or not an int at all. If 'error' is set to a value, then
    this function will terminate if the user specifies this value.
    :param min: min value to specify (1)
    :param max: max value to specify (2)
    :param message: a message telling what the different numbers represents. (1. Add song 2. Add artists)
    :param error: This function will end if the user specifies this value ('x')
    :return: -1 if user specifies error, an int in the range between min and max otherwise.
    """
    temp_message = message
    temp_message += "\nYour choice"
    if len(error) > 0:
        temp_message += " ('" + str(error) + "' to exit)"

    temp_message += Fore.WHITE + ": " + Fore.WHITE

    while True:
        search_res = input(temp_message)
        if search_res == error:
            return -1
        temp_message = message + "\n"
        if RepresentsInt(search_res):
            if int(search_res) >= min and int(search_res) <= max:
                return int(search_res)
            temp_message += Fore.LIGHTRED_EX + "Value out of range. Must be between " + str(min) + " and " + str(max) + ". Try again.\n" + Fore.WHITE
        else:
            temp_message += Fore.LIGHTRED_EX + "Must be integer. Try again.\n" + Fore.WHITE

        temp_message += "\nYour choice"
        if len(error) > 0:
            temp_message += " ('" + str(error) + "' to exit)"

        temp_message += ": "
        clear_terminal()


def proceed(message="Do you want to continue?"):
    """
    Ask the user if he or she will proceed with something.
    :param message: Info about what the user could proceed with (Do you want to modify playbeack)
    :return: True / False (want to proceed / dont want to proceed)
    """
    still_do_things = input(message + " y/n: ")
    while still_do_things not in ['y', 'n']:
        still_do_things = input("Wrong input. " + message + " y/n: ")
    if still_do_things == 'y':
        return True
    else:
        return False

def proceed_or_refresh(message="Do you want to continue (r = refresh) ?"):
    """
    Ask the user if he or she will proceed with something.
    :param message: Info about what the user could proceed with (Do you want to modify playbeack)
    :return: True / False (want to proceed / dont want to proceed)
    """
    still_do_things = input(message + " y/n/r: ")
    while still_do_things not in ['y', 'n', 'r']:
        still_do_things = input("Wrong input. " + message + " y/n: ")
    return still_do_things


def convert_list_string_to_sentence(lists):
    """
    Put together a list of string to one single string (sentence) where the last
    two elements get "and" between them.
    ["Coldplay", "Yoste", OTR"] => "Coldplay, Yoste and OTR"
    :param list:
    :return:
    """
    if len(lists) == 1:
        return str(lists[0].capitalize())
    temp_list = lists
    temp_list[0] = temp_list[0].capitalize()
    temp_list.insert(len(temp_list)-1, "and " + temp_list[-1])
    temp_list.remove(temp_list[-1])
    return ', '.join(temp_list)


def convertMillis(millis):
    seconds = (millis / 1000) % 60
    minutes = (millis / (1000 * 60)) % 60
    hours = (millis / (1000 * 60 * 60)) % 24
    start_string = " "
    if hours > 1:
        start_string = str(int(round(hours, 0))) + " hour "
    return seconds, minutes, hours, start_string + str(int(round(minutes, 0))) + " min " + str(int(round(seconds, 0))) + " sec"


def shorten_long_names_count_emojis(info, max_letters=15):
    """
    If a string has length longer than max_letters it will only return the first 'maxletters' number of letters of the string.
    It will also count the number of emojies found in the string, and count how many letters the emoji(s) takes.
    One emoji might for instance take up as much space when printed in terminal as two letters.
    :param info: just a string
    :param max_letters: max number of letters of the info string to be returned
    :return: new short string, number of spaces the emojie(s) takes.
    """
    name = info
    if len(name) > max_letters:
        name = name[:max_letters]

    emoji_len_count = 0
    for letter in name:
        if len('  ' if unicodedata.east_asian_width(letter) == 'W' else ' ') > 1:
            emoji_len_count += len('  ' if unicodedata.east_asian_width(letter) == 'W' else ' ') - 1
    return name, emoji_len_count


def clear_terminal():
    # Clears the terminal (bash command "clear")
    # check and make call for specific operating system
    # _ = call('clear' if os.name == 'posix' else 'cls')
    os.system('cls' if os.name == 'nt' else 'clear')



def convert_song_numbers_to_useful_numbers(string_number, maximum, separators=[':', '-']):
    """
    The purpose of this function is to give the user a lot of options to choose between, where each option is represented
    with a given number. 1. Viva la Vida 2. Fix You 3. Yellow. WIth a given user input, all the desired options are chosen
    by return a list with the desried numbers.
    This function lets the user specify several number smaller than 'maximum' by giving a simple string.
    Two separating values are legal, given by 'separators'. The first element of separators is used separate different
    numbers, the second argument is used to specify a range of numbers.
    3:4:5:9 would return a list with these numbers [3,4,5,9]
    3-5 would return a list with these numbers [3,4,5]
    You can combine and use both the separators.
    3-5:9 would also return the same list as the first example [3,4,5,9]
    3:5-7:6 would return [3, 5, 6, 7, 6] (The same number can appear twice if specified)
    If maximum is 10:
    then 3:9-11 would return -1 (error)
    PLEASE SEE test_convert_song_numbers() FOR MORE EXAMPLES:

    :param string_number: string with desired numbers separated with the separtors (1:3:5-9:3)
    :param maximum: Maximum number to specify
    :param separators: list with length 2. First separate different numbers (:), last specifies a range (-)
    :return: list of desired numbers or -1 if not given correctly. An Error message telling what is wrong with the input.
    """
    for idx, letter in enumerate(string_number):
        if (idx == 0 or idx == len(string_number) - 1) and not RepresentsInt(letter):
            print("First or last value must be int: " + Fore.WHITE + string_number[:idx] + Fore.RED +
                  string_number[idx:idx + 1] + Fore.WHITE + string_number[idx + 1:])
            return -1
        # check if the number is not int or not :, -. Then it is something wrong
        if not (RepresentsInt(letter) or letter in separators):
            print("Input not integer, ':' or '-': " + Fore.WHITE + string_number[:idx] + Fore.RED +
                  string_number[idx:idx + 1] + Fore.WHITE + string_number[idx + 1:])
            return -1
        if letter in separators and idx != 0 and idx != len(string_number) - 1:
            if RepresentsInt(string_number[idx-1])==False or RepresentsInt(string_number[idx+1])==False:
                print("Wrong use of separating signs: " + Fore.WHITE + string_number[:idx] + Fore.RED +
                      string_number[idx:idx+1] + Fore.WHITE + string_number[idx+1:])
                return -1
    nice_numbers = []
    first_split = string_number.split(separators[0])
    for splits in first_split:
        second_split = splits.split(separators[1])
        if len(second_split) == 1:
            num = int(second_split[0])
            if num > maximum or num < 1:
                shady_idx = string_number.find(second_split[0])
                print("Number out of range: ", Fore.WHITE + string_number[:shady_idx] + Fore.RED +
                      string_number[shady_idx:shady_idx+len(str(num))] + Fore.WHITE +
                      string_number[shady_idx+len(str(num)):])
                return -1
            else:
                nice_numbers.append(num)
        else:
            for i in range(len(second_split)-1):
                shady_idx = string_number.find(splits)
                if int(second_split[i]) > int(second_split[i+1]):
                    print("First number must be smaller than next one: ", Fore.WHITE + string_number[:shady_idx]
                          + Fore.RED + string_number[shady_idx:shady_idx + len(str(splits))] + Fore.WHITE +
                          string_number[shady_idx + len(str(splits)):])
                    return -1

            for num in range(int(second_split[0]), int(second_split[-1]) + 1):
                if num <= maximum and num >= 1:
                    nice_numbers.append(num)
                else:
                    shady_idx = string_number.find(second_split[0])
                    print("Number out of range: ", Fore.WHITE + string_number[:shady_idx] + Fore.RED +
                          string_number[shady_idx:shady_idx + len(str(splits))] + Fore.WHITE +
                          string_number[shady_idx + len(str(splits)):])
                    return -1
    return nice_numbers



def test_convert_song_numbers():
    convert_song_numbers_to_useful_numbers("1:2-12:11", maximum=10)
    convert_song_numbers_to_useful_numbers("3:9-11:10", maximum=12)
    convert_song_numbers_to_useful_numbers("1:2-10:11y", maximum=10)
    convert_song_numbers_to_useful_numbers("1:2-1t:11y", maximum=10)
    convert_song_numbers_to_useful_numbers(":1:2-5::y11:", maximum=10)
    convert_song_numbers_to_useful_numbers("1:2-5-11-8", maximum=20)
    convert_song_numbers_to_useful_numbers("1:2-5-11", maximum=20)
    convert_song_numbers_to_useful_numbers("1:6-5:11", maximum=10)
    convert_song_numbers_to_useful_numbers("1:2-5:10-11:12:14:17-20", maximum=19)
    convert_song_numbers_to_useful_numbers("1:2-5:10-11:12:14:17-20", maximum=20)


def check_or_cross(what='check'):
    """
    Return nice cross or check symbol.
    :param what: 'check' or 'cross'
    :return: string which is printed as a green check or a red cross symbol
    """
    if what == 'check':
        return u'\u2713'
    if what == 'cross':
        return u'\u274c'
    return -1


def print_nice_json_format(json_):
    """
    Print a json object on a readable format (oh why didnt I use this earlier haha)
    :param json_: josn object
    :return: nothing a all. It only prints, and you should be happy with that
    """
    print(json.dumps(json_, sort_keys=True, indent=4))


def find_largest_number_in_string(message):
    """
    Find maximum number in a string.
    :param message: message-string ("1. first case \n 2. Second case
    :return: largest number in string, -1 otherwise
    """
    max_num = -1
    for letter in message:
        if RepresentsInt(letter):
            if int(letter) > max_num:
                max_num = int(letter)
    return max_num
