import datetime as dt

TEXT_KEY           = "text"
CAPTION_NUMBER_KEY = "caption_number"
CAPTION_START_KEY  = "caption_start"
CAPTION_END_KEY    = "caption_end"

class SrtFile:

    def __init__(self,file_name):

        self.file_name = file_name 
        self.all_captions = []

        self._read_file()

    def __str__(self):

        string = "\n"        

        for caption in self.all_captions:

            string += f'Caption number: {caption[CAPTION_NUMBER_KEY]} \n'
            string += f'Caption start: {caption[CAPTION_START_KEY]} Caption end: {caption[CAPTION_END_KEY]} \n'
            
            string += '\nCaptions: \n'
            for line in caption[TEXT_KEY]:

                string += line + '\n'

            string += '\n'

        return string        
    
    def _read_file(self):

        srt_file = open(self.file_name, 'r')
        file_lines = srt_file.readlines()

        caption_information = {}
        caption_information[TEXT_KEY] = []

        for i in range(len(file_lines)):

            curr_line = file_lines[i].strip()

            if not curr_line:
                self.all_captions.append(caption_information)

            elif curr_line.isnumeric():
                caption_information = {}
                caption_information[TEXT_KEY] = []
                caption_information[CAPTION_NUMBER_KEY] = int(curr_line)

            elif "-->" in curr_line:

                timestamps = curr_line.split(" --> ")
                
                caption_information[CAPTION_START_KEY]  = timestamps[0]
                caption_information[CAPTION_END_KEY]    = timestamps[1]

            else: 

                caption_information[TEXT_KEY].append(curr_line)

        self.all_captions.append(caption_information)

        srt_file.close()

    def save_file(self):

        srt_file = open(self.file_name, 'r+')
        srt_file.truncate(0)

        for caption in self.all_captions:

            srt_file.write(str(caption[CAPTION_NUMBER_KEY]) + "\n")
            srt_file.write(caption[CAPTION_START_KEY] + " --> " + caption[CAPTION_END_KEY] + "\n")

            for line in caption[TEXT_KEY]:
                srt_file.write(line + "\n")

            srt_file.write("\n")

    def change_captions_numeration(self,first_number):

        for caption in self.all_captions:
            caption[CAPTION_NUMBER_KEY] = first_number
            first_number += 1

    def add_time_to_timestamps(self,time):

        for caption in self.all_captions:

            hour1, minute1, second1, milliseconds1 = self._get_time_information(time)
            hour2, minute2, second2, milliseconds2 = self._get_time_information(caption[CAPTION_START_KEY])
            hour3, minute3, second3, milliseconds3 = self._get_time_information(caption[CAPTION_END_KEY])

            d = dt.timedelta(hours=int(hour1), minutes=int(minute1), seconds=int(second1), milliseconds=int(milliseconds1)) + dt.timedelta(hours=int(hour2), minutes=int(minute2), seconds=int(second2), milliseconds=int(milliseconds2))
            d2 = dt.timedelta(hours=int(hour1), minutes=int(minute1), seconds=int(second1), milliseconds=int(milliseconds1)) + dt.timedelta(hours=int(hour3), minutes=int(minute3), seconds=int(second3), milliseconds=int(milliseconds3))

            caption[CAPTION_START_KEY] = self._fix_timestamp(d)
            caption[CAPTION_END_KEY]   = self._fix_timestamp(d2)
    
    def reduce_time_to_timestamps(self,time):

        for caption in self.all_captions:

            hour1, minute1, second1, milliseconds1 = self._get_time_information(time)
            hour2, minute2, second2, milliseconds2 = self._get_time_information(caption[CAPTION_START_KEY])
            hour3, minute3, second3, milliseconds3 = self._get_time_information(caption[CAPTION_END_KEY])

            d = dt.timedelta(hours=int(hour2), minutes=int(minute2), seconds=int(second2), milliseconds=int(milliseconds2)) - dt.timedelta(hours=int(hour1), minutes=int(minute1), seconds=int(second1), milliseconds=int(milliseconds1))
            d2 = dt.timedelta(hours=int(hour3), minutes=int(minute3), seconds=int(second3), milliseconds=int(milliseconds3)) - dt.timedelta(hours=int(hour1), minutes=int(minute1), seconds=int(second1), milliseconds=int(milliseconds1))

            caption[CAPTION_START_KEY] = self._fix_timestamp(d)
            caption[CAPTION_END_KEY]   = self._fix_timestamp(d2)

    def _get_time_information(self,time):
        hour, minute, tmp = time.split(":")
        second            = tmp.split(",")[0]
        milliseconds      = tmp.split(",")[1]

        return [hour, minute, second, milliseconds]

    def _fix_timestamp(self,timestamp):
        return ('0' + str(timestamp)[0:11]).replace(".", ",")