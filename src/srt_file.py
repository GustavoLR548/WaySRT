import re
from dataclasses import dataclass
from datetime import timedelta
from typing import List


@dataclass
class Caption():
    index: int
    start_time: timedelta
    end_time: timedelta
    caption: str
    

class SrtFile:

    captions = List[Caption]

    START_TIME = 0
    END_TIME = 1

    CAPTION_TEXT_KEY   = "text"
    CAPTION_NUMBER_KEY = "caption_number"
    CAPTION_START_KEY  = "caption_start"
    CAPTION_END_KEY    = "caption_end"


    _CAPTION_REGEX = re.compile(r"(?<index>:\d+)\s*\n(?<shr>:\d{0,3}):(?<smin>:\d{0,3}):(?<ssec>:\d{0,3}),(?<sml>:\d{0,3})\s+-->\s+(?<ehr>:\d{0,3}):(?<emin>:\d{0,3}):(?<esec>:\d{0,3}),(?<eml>:\d{0,3})(?<content>:(?:[^\n]+)\n)+\n")

    def __init__(self,file_name: str):

        self.file_name = file_name.strip()
        self._read_file()
    

    def parse_str(self, text: str) -> List[Caption]:
        captions = List[Caption]

        for n, m in enumerate(re.findall(self._CAPTION_REGEX, text)):
            captions.append(
                Caption(
                    index=n,
                    start_time=timedelta(
                        hours=m.group("shr"),
                        minutes=m.group("smin"),
                        seconds=m.group("ssec"),
                        milliseconds=m.group("sml")
                    ),
                    end_time=timedelta(
                        hours=m.group("ehr"),
                        minutes=m.group("emin"),
                        seconds=m.group("esec"),
                        milliseconds=m.group("eml")
                    ),
                    caption=m.group("content")
                )
            )
        
        return captions



            

    def _read_file(self):

        with open(self.file_name, 'r') as srt_file:
            file_lines = srt_file.readlines()


            caption_information = {}
            caption_information[SrtFile.CAPTION_TEXT_KEY] = []

            for line in file_lines:

                curr_line = line.strip()

                if not curr_line:
                    self.all_captions.append(caption_information)
                    self.num_of_captions += 1

                elif curr_line.isnumeric():
                    caption_information = {}
                    caption_information[SrtFile.CAPTION_TEXT_KEY] = []
                    caption_information[SrtFile.CAPTION_NUMBER_KEY] = int(curr_line)

                elif "-->" in curr_line:

                    timestamps = curr_line.split(" --> ")
                    
                    if self.__match_time_regex(timestamps[SrtFile.START_TIME]):
                        raise Exception(f"Error! The regex {timestamps[SrtFile.START_TIME]} is not valid for the file {self.file_name} ")

                    if self.__match_time_regex(timestamps[SrtFile.END_TIME]):
                        raise Exception(f"Error! The regex {timestamps[SrtFile.END_TIME]} is not valid for the file {self.file_name} ")

                    caption_information[SrtFile.CAPTION_START_KEY]  = timestamps[SrtFile.START_TIME]
                    caption_information[SrtFile.CAPTION_END_KEY]    = timestamps[SrtFile.END_TIME]

                else: 

                    caption_information[SrtFile.CAPTION_TEXT_KEY].append(curr_line)

            if not caption_information in self.all_captions:
                self.all_captions.append(caption_information)
                self.num_of_captions += 1

    def save_file(self):

        srt_file = open(self.file_name, 'r+')
        srt_file.truncate(0)

        for caption in self.all_captions:

            srt_file.write(f'{caption[SrtFile.CAPTION_NUMBER_KEY]} \n')
            srt_file.write(f'{caption[SrtFile.CAPTION_START_KEY]} --> {caption[SrtFile.CAPTION_END_KEY]} \n')

            for line in caption[SrtFile.CAPTION_TEXT_KEY]:
                srt_file.write(f'{line}\n')

            srt_file.write("\n")

    def change_captions_numeration(self,first_number):

        for caption in self.all_captions:
            caption[SrtFile.CAPTION_NUMBER_KEY] = first_number
            first_number += 1

    def add_time_to_timestamps(self,time):

        if not self.__match_time_regex(time):
            raise Exception("Error! The timestamp specified is not compatible!")

        for caption in self.all_captions:

            time_timedelta          = self._get_time_information(time)
            caption_start_timedelta = self._get_time_information(caption[SrtFile.CAPTION_START_KEY])
            caption_end_timedelta   = self._get_time_information(caption[SrtFile.CAPTION_END_KEY])

            caption[SrtFile.CAPTION_START_KEY] = self._fix_timestamp(caption_start_timedelta + time_timedelta)
            caption[SrtFile.CAPTION_END_KEY]   = self._fix_timestamp(caption_end_timedelta   + time_timedelta)

    def add_caption_at_the_end(self, texts, caption_duration):

        self.num_of_captions += 1
        caption_numeration = self.num_of_captions

        start_time = self.all_captions[-1][SrtFile.CAPTION_END_KEY]

        caption_duration_timedelta = self._get_time_information(caption_duration)

        end_time_timedelta = self._get_time_information(start_time)
        end_time_timedelta += caption_duration_timedelta
        end_time = self._fix_timestamp(end_time_timedelta)

        caption_information = {
            SrtFile.CAPTION_NUMBER_KEY : f'{caption_numeration}',
            SrtFile.CAPTION_START_KEY : f'{start_time}',
            SrtFile.CAPTION_END_KEY : f'{end_time}'
        }

        caption_information[SrtFile.CAPTION_TEXT_KEY] = texts

        self.all_captions.append(caption_information)

    def reduce_time_to_timestamps(self,time):

        for caption in self.all_captions:

            time_timedelta          = self._get_time_information(time)
            caption_start_timedelta = self._get_time_information(caption[SrtFile.CAPTION_START_KEY])
            caption_end_timedelta   = self._get_time_information(caption[SrtFile.CAPTION_END_KEY])

            caption[SrtFile.CAPTION_START_KEY] = self._fix_timestamp(caption_start_timedelta - time_timedelta)
            caption[SrtFile.CAPTION_END_KEY]   = self._fix_timestamp(caption_end_timedelta   - time_timedelta)

    def _get_time_information(self,time):
        hour, minute, tmp = time.split(":")
        second            = tmp.split(",")[0]
        milliseconds      = tmp.split(",")[1]

        return timedelta(hours=int(hour), minutes=int(minute), seconds=int(second), milliseconds=int(milliseconds))

    def _fix_timestamp(self,timestamp: timedelta):
        return ('0' + str(timestamp)[0:11]).replace(".", ",")

    def __match_time_regex(self,time):
        return (not re.findall("(\d{0,3}:\d{0,3}:\d{0,3},\d{0,3})",time))

    def __str__(self) -> str:

        string = "\n"    

        string += f'Number of captions: {self.num_of_captions}\n'    

        for caption in self.all_captions:

            string += f'Caption number: {caption[SrtFile.CAPTION_NUMBER_KEY]} \n'
            string += f'Caption start: {caption[SrtFile.CAPTION_START_KEY]} Caption end: {caption[SrtFile.CAPTION_END_KEY]}'
            
            string += '\nCaptions: \n'
            for line in caption[SrtFile.CAPTION_TEXT_KEY]:

                string += line + '\n'

            string += '\n'

        return string

