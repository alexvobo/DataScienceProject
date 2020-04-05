import csv
import os
import pandas as pd
import lyricsgenius
import pdb

with open(os.path.join(os.pardir, "credentials"), 'r') as creds:
    client_id = creds.readline()
    client_secret = creds.readline()
    client_access = creds.readlines()
    creds.close()

# Now we can process the big csv file and add lyrics and stuff
already_added = []
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

def addlyrics():
    genius = lyricsgenius.Genius(client_access[0])
    genius.verbose = True
    genius.remove_section_headers = True
    testfile = "big.csv"
    with open(testfile, 'r') as csvInput:
        with open("bigout.csv", 'w') as csvOutput:
            writer = csv.writer(csvOutput, lineterminator='\n')
            reader = csv.reader(csvInput)
            all = []
            # Header
            row = next(reader)
            row.append("Lyrics")
            all.append(row)
            appendLimit = 3 #appends x at a time just in case
            ##
            try:
                try:
                    for row in reader:
                        song = row[1]
                        artist = row[2]
                        if str(song + artist) not in already_added:
                            songLyrics = genius.search_song(song, artist)
                            already_added.append(song + artist)
                            # pdb.set_trace()
                            # print(songLyrics.lyrics)
                            # print(already_added)
                            row.append(str(songLyrics.lyrics).replace("\u2005", " ").replace("\n", " "))
                        else:
                            row.append("duplicate")
                        all.append(row)
                        print(len(all)-1)
                except Exception as e:
                    print(e)
                    pass
                finally:
                    writer.writerows(all)
            except UnicodeEncodeError as e:
                pass
            finally:
                csvOutput.close()
        csvInput.close()


if __name__ == "__main__":
    addlyrics()
