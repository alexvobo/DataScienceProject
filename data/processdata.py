import os
import sys

import lyricsgenius
import pdb
import numpy as np
import csv
from multiprocessing import Pool
import time
import datetime

with open(os.path.join(os.pardir, "credentials"), 'r') as creds:
    client_id = creds.readline()
    client_secret = creds.readline()
    client_access = creds.readlines()
    creds.close()

# Now we can process the big csv file and add lyrics and stuff
already_added = []
infile = "big.csv"
outfile = "bigout.csv"


# Utility function for hiding text output.
# with HiddenPrints(): ...
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


# #csv file to be read in
# in_csv = '/path/to/read/file.csv'
#
# #csv to write data to
# out_csv = 'path/to/write/file.csv'
#
# #get the number of lines of the csv file to be read
# number_lines = sum(1 for row in (open(in_csv)))
#
# #size of chunks of data to write to the csv
# chunksize = 10
#
# #start looping through data writing it to a new file for each chunk
# for i in range(1,number_lines,chunksize):
#      df = pd.read_csv(in_csv,
#           header=None,
#           nrows = chunksize,#number of rows to read at each loop
#           skiprows = i)#skip rows that have been read
#
#      df.to_csv(out_csv,
#           index=False,
#           header=False,
#           mode='a',#append data to csv file
#           chunksize=chunksize)#size of data to append for each loop
def call_processing_rows_pickably(row):
    return process_row(row)


def process_row(row):
    song = row[1]
    artist = row[2]
    if str(song + artist) not in already_added:
        songLyrics = genius.search_song(song, artist)
        already_added.append(song + artist)
        if songLyrics:
            row.append(str(songLyrics.lyrics).replace("\u2005", " ").replace("\n", " "))
        else:
            row.append("Error fetching lyrics")
    elif str(song + artist) in already_added:
        row.append("duplicate")

    return row


def append_to_csv(file, list_of_rows):
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(list_of_rows)


class process_csv():

    def __init__(self, file_name):
        self.file_name = file_name

    def get_row_count(self):
        with open(self.file_name, encoding="utf-8") as f:
            for i, l in enumerate(f):
                pass
        self.row_count = i

    def select_chunk_size(self):
        self.chunk_size = 20
        return

    def process_rows(self):
        list_de_rows = []
        count = 0
        with open(self.file_name, 'r', encoding='utf-8') as csvIn:
            with open(outfile, "a", encoding='utf-8') as csvOut:
                reader = csv.reader(csvIn)
                next(reader)
                for row in reader:
                    # print(count + 1)
                    list_de_rows.append(row)
                    if len(list_de_rows) == self.chunk_size:
                        append_to_csv(csvOut, p.map(call_processing_rows_pickably, list_de_rows))
                        del list_de_rows[:]
                if list_de_rows:
                    append_to_csv(csvOut, p.map(call_processing_rows_pickably, list_de_rows))

    def start_process(self):
        self.get_row_count()
        self.select_chunk_size()
        self.process_rows()


def addlyrics():
    pass
    # genius = lyricsgenius.Genius(client_access[0])
    # genius.remove_section_headers = True
    # with open(file, 'r') as csvInput:

    # with open("bigout.csv", 'w') as csvOutput:
    #     writer = csv.writer(csvOutput, lineterminator='\n')

    # reader = csv.reader(csvInput)
    # all = []
    # # Header
    # row = next(reader)
    # row.append("Lyrics")
    # all.append(row)
    # appendLimit = 3  # appends x at a time just in case
    ##
    # try:
    #     try:
    #         for row in reader:
    #             song = row[1]
    #             artist = row[2]
    #             if str(song + artist) not in already_added:
    #                 songLyrics = genius.search_song(song, artist)
    #                 already_added.append(song + artist)
    #                 # pdb.set_trace()
    #                 # print(songLyrics.lyrics)
    #                 # print(already_added)
    #                 row.append(str(songLyrics.lyrics).replace("\u2005", " ").replace("\n", " "))
    #             else:
    #                 row.append("duplicate")
    #             all.append(row)
    #             print(len(all) - 1)
    #     except Exception as e:
    #         print(e)
    #         pass
    #         finally:
    #             writer.writerows(all)
    #     except UnicodeEncodeError as e:
    #         pass
    #     finally:
    #         csvOutput.close()
    # csvInput.close()


genius = lyricsgenius.Genius(client_access[0])
genius.remove_section_headers = True
if __name__ == "__main__":
    with open(infile, 'r', encoding='utf-8') as csvInput:
        with open(outfile, 'w') as csvOutput:
            writer = csv.writer(csvOutput, lineterminator='\n')
            reader = csv.reader(csvInput)
            # Header
            row = next(reader)
            row.append("Lyrics")
            writer.writerow(row)
            #
    with HiddenPrints:
        initial = datetime.datetime.now()
        p = Pool()
        ob = process_csv(infile)
        ob.start_process()
        print(ob.row_count)
        final = datetime.datetime.now()
    print(final - initial)

    # addlyrics()
