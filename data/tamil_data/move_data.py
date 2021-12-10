import csv
import os

with open("covost_v2.ta_en.tsv", newline='\n') as csvf:
    csv_reader = csv.reader(csvf, delimiter='\t')
    fns = []
    header_row = True
    for row in csv_reader:
        if header_row:
            header_row = False
            continue
        fns.append(row[0])

# Now move all files
for fn in fns:
    command_str = "mv " + fn + " cv-corpus-7.0-2021-07-21/ta/clips2/"
    os.system(command_str)

print("moved {} files".format(len(fns)))
