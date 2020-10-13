from subprocess import call
import os
from colorama import Fore
import dateutil.parser as dp
import unicodedata

def find_str(s, char):
    index = 0
    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index

            index += 1

    return -1




def convert_ISO_time_to_seconds(iso_time_str):
    parsed_t = dp.parse(iso_time_str)
    t_in_seconds = parsed_t.strftime('%s')
    return t_in_seconds




def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def RepresentsFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def specify_int_in_range(min, max, message="Your choice ", error=""):
    temp_message = message
    temp_message += "\n\nYour choice"
    if len(error) > 0:
        temp_message += " ('" + str(error) + "' to exit)"

    temp_message += ": "

    while True:
        search_res = input(temp_message)
        if search_res == error:
            return -1
        temp_message = message + "\n"
        if RepresentsInt(search_res):
            if int(search_res) >= min and int(search_res) <= max:
                return int(search_res)
            temp_message += "Value out of range. Must be between " + str(min) + " and " + str(max) + ". Try again.\n"
        else:
            temp_message += "Must be integer. Try again.\n"

        temp_message += "\nYour choice"
        if len(error) > 0:
            temp_message += " ('" + str(error) + "' to exit)"

        temp_message += ": "
        clear_terminal()


def convert_list_string_to_sentence(list):
    list[0] = list[0].capitalize()
    list.insert(len(list)-1, "and " + list[-1])
    list.remove(list[-1])
    return ', '.join(list)


def convertMillis(millis):
    seconds = (millis / 1000) % 60
    minutes = (millis / (1000 * 60)) % 60
    hours = (millis / (1000 * 60 * 60)) % 24
    start_string = " "
    if hours > 1:
        start_string = str(int(round(hours, 0))) + " hour "
    return seconds, minutes, hours, start_string + str(int(round(minutes, 0))) + " min " + str(int(round(seconds, 0))) + " sec"


def shorten_long_names_count_emojis(info, max_letters=15):
    name = str(info['name'])
    if len(name) > max_letters:
        name = name[:max_letters]

    emoji_len_count = 0
    for letter in name:
        if len('  ' if unicodedata.east_asian_width(letter) == 'W' else ' ') > 1:
            emoji_len_count += len('  ' if unicodedata.east_asian_width(letter) == 'W' else ' ') - 1
    return name, emoji_len_count

def clear_terminal():
    # check and make call for specific operating system
    _ = call('clear' if os.name == 'posix' else 'cls')


def convert_song_numbers_to_useful_numbers(string_number, maximum, seperators=[':', '-']):
    for idx, letter in enumerate(string_number):
        if (idx == 0 or idx == len(string_number) - 1) and not RepresentsInt(letter):
            print("First or last value must be int: " + Fore.WHITE + string_number[:idx] + Fore.RED +
                  string_number[idx:idx + 1] + Fore.WHITE + string_number[idx + 1:])
            return -1
        # check if the number is not int or not :, -. Then it is something wrong
        if not (RepresentsInt(letter) or letter in seperators):
            print("Input not integer, ':' or '-': " + Fore.WHITE + string_number[:idx] + Fore.RED +
                  string_number[idx:idx + 1] + Fore.WHITE + string_number[idx + 1:])
            return -1
        if letter in seperators and idx != 0 and idx != len(string_number) - 1:
            if RepresentsInt(string_number[idx-1])==False or RepresentsInt(string_number[idx+1])==False:
                print("Wrong use of separating signs: " + Fore.WHITE + string_number[:idx] + Fore.RED +
                      string_number[idx:idx+1] + Fore.WHITE + string_number[idx+1:])
                return -1
    nice_numbers = []
    first_split = string_number.split(seperators[0])
    for splits in first_split:
        second_split = splits.split(seperators[1])
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
    convert_song_numbers_to_useful_numbers("1:2-10:11y", maximum=10)
    convert_song_numbers_to_useful_numbers("1:2-1t:11y", maximum=10)
    convert_song_numbers_to_useful_numbers(":1:2-5::y11:", maximum=10)
    convert_song_numbers_to_useful_numbers("1:2-5-11-8", maximum=20)
    convert_song_numbers_to_useful_numbers("1:2-5-11", maximum=20)
    convert_song_numbers_to_useful_numbers("1:6-5:11", maximum=10)
    convert_song_numbers_to_useful_numbers("1:2-5:10-11:12:14:17-20", maximum=19)
    convert_song_numbers_to_useful_numbers("1:2-5:10-11:12:14:17-20", maximum=20)


def check_or_cross(what='check'):
    if what == 'check':
        return u'\u2713'
    if what == 'cross':
        return u'\u274c'
    return -1