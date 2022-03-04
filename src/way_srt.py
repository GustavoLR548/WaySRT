from srt_file import SrtFile
import sys

def change_captions_numeration(srt):
    print("Change captions numeration")

    new_enumeration = input("Please enter the new enumeration: ")

    start_enumeration = int(new_enumeration.strip())

    srt.change_captions_numeration(start_enumeration)

def add_time_to_captions_timestamps(srt):
    print("Add time to captions")

    timestamp = input("Please enter the timestamp value\nEx: 00:19:49,300\n-> ")

    srt.add_time_to_timestamps(timestamp)

def reduce_time_to_captions_timestamps(srt):
    print("Reduce time to captions")

    timestamp = input("Please enter the timestamp value\nEx: 00:19:49,300\n-> ")

    srt.reduce_time_to_timestamps(timestamp)

def save_srt_file(srt):
    print("Saving srt file")

    srt.save_file()

    print("Saving process completed!")

def default(_srt):
    print("Invalid command, please try again")

def main(file_name):
    
    switch = {
        "1": change_captions_numeration,
        "2": add_time_to_captions_timestamps,
        "3": reduce_time_to_captions_timestamps,
        "4": print,
        "5": save_srt_file,
        
    }

    srt = SrtFile(file_name)

    instruction = "0"

    while True:

        print("What do you like to do?")
        print("1 - Change captions numbering")
        print("2 - Add time to captions timestamps")
        print("3 - Reduce time to captions timestamps")
        print("4 - Print file")
        print("5 - Save file")
        print("\n0 - Exit the program")

        instruction = input("Please enter a value: ")

        if "0" in instruction:
            break 

        case = switch.get(instruction.strip(), default)

        case(srt)

    print("Bye, see you next time")

if __name__ == "__main__":

    if len(sys.argv) < 2: 
        print('Error! Please specify the file')
        sys.exit()

    print(f'Reading the file: {sys.argv[1]}...')

    main(sys.argv[1])