import requests
import glob
import os
import pandas as pd
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
def get_csvs():
    b_url = "https://spotifycharts.com/regional/global/weekly/"

    if not dateRange:
        get_date_range()

    for i, d in enumerate(dateRange):
        url = b_url + d + "/download"

        r = requests.get(url)
        with open('data/week1' + str(i) + str('.csv'), 'wb') as f:
            f.write(r.content)


def clean_csvs():
    if not dateRange:
        get_date_range()

    os.chdir('data')
    path = r'.'
    all_files = glob.glob(os.path.join(path, "*.csv"))

    for i, file in enumerate(all_files):
        with open(os.path.basename(file), 'r', encoding="utf-8") as csvInput:
            with open("week " + str(i) + ".csv", 'w', encoding="utf-8") as csvOutput:
                writer = csv.writer(csvOutput, lineterminator='\n')
                reader = csv.reader(csvInput)
                all = []

                # Header
                next(reader)
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


def delete_old_csv():
    path = r'C:\Users\Alex\Documents\Data Science\Project\data\data'
    all_files = glob.glob(os.path.join(path, "*.csv"))
    for f in all_files:
        fname = os.path.basename(f)
        if " " not in fname:
            print("removing", fname)
            os.remove(path + "\\" + fname)


def create_big_csv():
    os.chdir('data')
    path = os.curdir
    all_files = glob.glob(
        os.path.join(path, "*.csv"))
    df_from_each_file = ([pd.read_csv(f, encoding="windows-1252") for f in all_files if " " in os.path.basename(f)])
    # print(df_from_each_file)
    concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
    concatenated_df.to_csv(os.path.join(os.pardir, "big.csv"), index=False)


if __name__ == "__main__":
    # get_csvs()
    # clean_csvs()
    # delete_old_csv()
    # create_big_csv()
    pass
