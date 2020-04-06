import os
import sys
import lyricsgenius
import csv
from multiprocessing import Pool
import datetime

with open(os.path.join(os.pardir, "credentials"), 'r') as creds:
    client_id = creds.readline()
    client_secret = creds.readline()
    client_access = creds.readlines()

# Now we can process the big csv file and add lyrics and stuff
already_added = []
infile = "big.csv"
outfile = "bigout2.csv"


# Utility function for hiding text output.
# with HiddenPrints(): ...
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def call_processing_rows_pickably(row):
    return process_row(row)


def process_row(row):
    song, artist = row[1], row[2]
    song_artist = ''.join([song, artist])

    if song_artist not in already_added:
        with HiddenPrints():
            song_lyrics = genius.search_song(song, artist)
            already_added.append(song_artist)
            if song_lyrics:
                row.append(str(song_lyrics.lyrics).replace("\u2005", " ").replace("\n", " "))
            else:
                row.append("Error fetching lyrics")
    elif song_artist in already_added:
        row.append("duplicate")

    return row


def append_to_csv(file, list_of_rows):
    csv.writer(file, lineterminator='\n').writerows(list_of_rows)


class ProcessCsv:

    def __init__(self, file_name):
        self.chunk_size = 20
        self.file_name = file_name
        with open(self.file_name, encoding="utf-8") as f:
            self.row_count = sum(1 for _ in f)

    def process_rows(self):
        list_de_rows = []

        with open(self.file_name, 'r', encoding='utf-8') as csvIn:
            with open(outfile, "a", encoding='utf-8') as csvOut:
                reader = csv.reader(csvIn)
                next(reader)  # skip header
                for row in reader:
                    list_de_rows.append(row)
                    if len(list_de_rows) == self.chunk_size:
                        i = datetime.datetime.now()
                        append_to_csv(csvOut, p.map(call_processing_rows_pickably, list_de_rows))
                        f = datetime.datetime.now()
                        print("per chunk: {0}, per row: {1}".format(f - i, (f - i) / self.chunk_size))
                        del list_de_rows[:]
                if list_de_rows:
                    append_to_csv(csvOut, p.map(call_processing_rows_pickably, list_de_rows))

    def start_process(self):
        self.process_rows()


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

    initial = datetime.datetime.now()
    p = Pool()
    ob = ProcessCsv(infile)
    ob.start_process()
    print(ob.row_count)
    final = datetime.datetime.now()
    print(final - initial)
