import requests
import glob
import os
import pandas as pd
import pdb
import csv

dateRange = []

# Gets date range and saves it in global dateRange list
def get_date_range():
    global dateRange

    dateRange = []
    with open("dates", "r") as f:
        for date in f.readlines():
            dateRange.append(date.rstrip())

# Using dates file, requests to download the files we need to data folder.
def getCSVs():
    b_url = "https://spotifycharts.com/regional/global/weekly/"
    index = 0
    with open("dates", "r") as daterange:
        for d in daterange.readlines():
            date = d.rstrip()
            url = b_url + date + "/download"

            r = requests.get(url)
            with open('data/week' + str(index) + str('.csv'), 'wb') as f:
                f.write(r.content)
            index += 1
        daterange.close()


def cleanCSVs():
    get_date_range()
    os.chdir('data')
    path = r'.'
    all_files = glob.glob(os.path.join(path, "*.csv"))

    for i in range(len(all_files)):
        with open(os.path.basename(all_files[i]), 'r', encoding="utf-8") as csvInput:
            with open("week " + str(i) + ".csv", 'w') as csvOutput:
                writer = csv.writer(csvOutput, lineterminator='\n')
                reader = csv.reader(csvInput)
                all = []

                # Header
                skip = next(reader)
                row = next(reader)
                row.append("Week")
                all.append(row)
                ##

                try:
                    for row in reader:
                        row.append(dateRange[i])
                        all.append(row)
                    writer.writerows(all)
                except UnicodeEncodeError as e:
                    pass
                finally:
                    csvOutput.close()
        csvInput.close()


def deleteOldCSV():
    path = r'C:\Users\Alex\Documents\Data Science\Project\data\data'
    all_files = glob.glob(os.path.join(path, "*.csv"))
    for f in all_files:
        fname = os.path.basename(f)
        if " " in fname:
            print(fname)
            os.remove(path + "\\" + fname)
        # if " " not in fname:
        #     print(fname)
        #     os.remove(path + "\\" + fname)


def createBigCSV():
    os.chdir('data')
    path = os.curdir
    all_files = glob.glob(
        os.path.join(path, "*.csv"))
    # pdb.set_trace()
    df_from_each_file = ([pd.read_csv(f, encoding="windows-1252") for f in all_files if " " in os.path.basename(f)])
    print(df_from_each_file)
    concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
    concatenated_df.to_csv(os.path.join(os.pardir, "big.csv"), index=False)


if __name__ == "__main__":
    pass
    #deleteOldCSV()
    #cleanCSVs()
    #createBigCSV()
    # getCSVs()


