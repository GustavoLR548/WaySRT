import re
from dataclasses import dataclass
from datetime import timedelta, datetime
from typing import List


@dataclass
class Caption():
    index: int
    start_time: timedelta
    end_time: timedelta
    caption: str

    def __str__(self) -> str:
        start = datetime.min + self.start_time
        end = datetime.min + self.end_time
        return f"""{self.index}
{start.strftime("%HHH:%MMM:%SSS")},{(start.microsecond/1000)%1000} --> {end.strftime("%HHH:%MMM:%SSS")},{(end.microsecond/1000)%1000}
{self.caption}
        """
    

class SRTParser:


    def __init__(self) -> None:
        self.captions = List[Caption]

    START_TIME = 0
    END_TIME = 1

    CAPTION_TEXT_KEY   = "text"
    CAPTION_NUMBER_KEY = "caption_number"
    CAPTION_START_KEY  = "caption_start"
    CAPTION_END_KEY    = "caption_end"

    _CAPTION_REGEX = re.compile(r"(?P<index>:\d+)\s*\n(?P<shr>:\d{0,3}):(?P<smin>:\d{0,3}):(?P<ssec>:\d{0,3}),(?P<sml>:\d{0,3})\s+-->\s+(?P<ehr>:\d{0,3}):(?P<emin>:\d{0,3}):(?P<esec>:\d{0,3}),(?P<eml>:\d{0,3})(?P<content>:(?:[^\n]+)\n)+\n")

    def __init__(self,file_name: str):

        self.num_of_captions = 0
        self.all_captions = []

        self.file_name = file_name.strip()
        self.open(file_path=file_name)
    

    @classmethod
    def parse_str(cls, text: str) -> List[Caption]:
        captions = List[Caption]

        for n, m in enumerate(re.findall(SRTParser._CAPTION_REGEX, text)):
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



            

    def open(self, file_path: str):

        with open(file_path, 'r') as file:
            self.captions = SRTParser.parse_str(file.read())


    def save_file(self):

        srt_file = open(self.file_name, 'r+')
        srt_file.truncate(0)

        for caption in self.all_captions:

            srt_file.write(f'{caption[SRTParser.CAPTION_NUMBER_KEY]} \n')
            srt_file.write(f'{caption[SRTParser.CAPTION_START_KEY]} --> {caption[SRTParser.CAPTION_END_KEY]} \n')

            for line in caption[SRTParser.CAPTION_TEXT_KEY]:
                srt_file.write(f'{line}\n')

            srt_file.write("\n")

    def change_captions_numeration(self,first_number):

        for caption in self.all_captions:
            caption[SRTParser.CAPTION_NUMBER_KEY] = first_number
            first_number += 1

    def add_time_to_timestamps(self,time):

        if not self.__match_time_regex(time):
            raise Exception("Error! The timestamp specified is not compatible!")

        for caption in self.all_captions:

            time_timedelta          = self._get_time_information(time)
            caption_start_timedelta = self._get_time_information(caption[SRTParser.CAPTION_START_KEY])
            caption_end_timedelta   = self._get_time_information(caption[SRTParser.CAPTION_END_KEY])

            caption[SRTParser.CAPTION_START_KEY] = self._fix_timestamp(caption_start_timedelta + time_timedelta)
            caption[SRTParser.CAPTION_END_KEY]   = self._fix_timestamp(caption_end_timedelta   + time_timedelta)

    def add_caption_at_the_end(self, texts, caption_duration):

        self.num_of_captions += 1
        caption_numeration = self.num_of_captions

        start_time = self.all_captions[-1][SRTParser.CAPTION_END_KEY]

        caption_duration_timedelta = self._get_time_information(caption_duration)

        end_time_timedelta = self._get_time_information(start_time)
        end_time_timedelta += caption_duration_timedelta
        end_time = self._fix_timestamp(end_time_timedelta)

        caption_information = {
            SRTParser.CAPTION_NUMBER_KEY : f'{caption_numeration}',
            SRTParser.CAPTION_START_KEY : f'{start_time}',
            SRTParser.CAPTION_END_KEY : f'{end_time}'
        }

        caption_information[SRTParser.CAPTION_TEXT_KEY] = texts

        self.all_captions.append(caption_information)

    def reduce_time_to_timestamps(self,time):

        for caption in self.all_captions:

            time_timedelta          = self._get_time_information(time)
            caption_start_timedelta = self._get_time_information(caption[SRTParser.CAPTION_START_KEY])
            caption_end_timedelta   = self._get_time_information(caption[SRTParser.CAPTION_END_KEY])

            caption[SRTParser.CAPTION_START_KEY] = self._fix_timestamp(caption_start_timedelta - time_timedelta)
            caption[SRTParser.CAPTION_END_KEY]   = self._fix_timestamp(caption_end_timedelta   - time_timedelta)

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

            string += f'Caption number: {caption[SRTParser.CAPTION_NUMBER_KEY]} \n'
            string += f'Caption start: {caption[SRTParser.CAPTION_START_KEY]} Caption end: {caption[SRTParser.CAPTION_END_KEY]}'
            
            string += '\nCaptions: \n'
            for line in caption[SRTParser.CAPTION_TEXT_KEY]:

                string += line + '\n'

            string += '\n'

        return string

