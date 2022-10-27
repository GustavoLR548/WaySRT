from curses.ascii import isblank
from srt_file import SrtFile
import sys
from os import system, name as os_name

def clear_terminal():
    system('cls' if os_name == 'nt' else 'clear')

def wait_for_user_input():
    input("Press enter to continue...")
    clear_terminal()

def change_captions_numeration(srt: SrtFile):
    print("Change captions numeration")

    new_enumeration = input("Please enter the new enumeration: ")

    start_enumeration = int(new_enumeration.strip())

    srt.change_captions_numeration(start_enumeration)

def add_time_to_captions_timestamps(srt: SrtFile):
    print("Add time to captions")

    timestamp = input("Please enter the timestamp value\nEx: 00:19:49,300\n-> ")

    srt.add_time_to_timestamps(timestamp)

    print("Time added to captions")

def reduce_time_to_captions_timestamps(srt: SrtFile):
    print("Reduce time to captions")

    timestamp = input("Please enter the timestamp value\nEx: 00:19:49,300\n-> ")

    srt.reduce_time_to_timestamps(timestamp)

    print("Time reduced to captions")

def save_srt_file(srt: SrtFile):
    print("Saving srt file")

    srt.save_file()

    print("Saving process completed!")

def add_caption_at_the_end(srt: SrtFile):
    print("Insert the text")

    texts = []

    string = "0"
    while string:
        string = input()
        texts.append(string)

    texts.pop()

    time = input("Please enter the timestamp value\nEx: 00:19:49,300\n-> ")
    srt.add_caption_at_the_end(texts,time)

def default(_srt):
    print("Invalid command, please try again")

def quit(_srt):
    print("Bye, see you next time")

def main(file_name):
    
    switch = {
        "1": change_captions_numeration,
        "2": add_time_to_captions_timestamps,
        "3": reduce_time_to_captions_timestamps,
        "4": print,
        "5": save_srt_file,
        "6": add_caption_at_the_end,
        "0": quit
    }

    srt = SrtFile(file_name)

    instruction = None

    while instruction != "0":

        print("What do you like to do?")
        print("1 - Change captions numbering")
        print("2 - Add time to captions timestamps")
        print("3 - Reduce time to captions timestamps")
        print("4 - Print file")
        print("5 - Save file")
        print("6 - Add caption at the end")
        print("\n0 - Exit the program")

        instruction = input("Please enter a value: ")

        case = switch.get(instruction.strip(), default)

        case(srt)

        wait_for_user_input()

if __name__ == "__main__":

    if len(sys.argv) < 2: 
        print('Error! Please specify the file')
        sys.exit()

    print(f'Reading the file: {sys.argv[1]}...')

    main(sys.argv[1])