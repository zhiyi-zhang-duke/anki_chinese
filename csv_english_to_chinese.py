#Converts a csv with only english (3rd column) to an importable anki csv

import io
import pinyin
import codecs
import sys
import csv
import chinese_dict_final as cdict

sys.stdout.reconfigure(encoding='utf-8')

#Get csv file being appended
print('CSV File:')
csv_file = input()

def predict_encoding(file_path, n_lines=20):
    '''Predict a file's encoding using chardet'''
    import chardet

    # Open the file as binary data
    with open(file_path, 'rb') as f:
        # Join binary lines for specified number of lines
        rawdata = b''.join([f.readline() for _ in range(n_lines)])

    return chardet.detect(rawdata)['encoding']

#Determine encoding
encoding = predict_encoding(csv_file, 10)
if "utf" in encoding:
    print("Input file is in " + encoding + " format")
else:
    print("Encoding of file is problematic.")
    print("Encoding is : " + encoding)
    
rows = io.open(csv_file, "r", encoding="utf-8")
output = io.open(csv_file.replace(".", "_anki."), "w", encoding="utf-8")

writer = csv.writer(output, lineterminator='\n')
reader = csv.reader(rows)

all = []
row = next(reader)
#Append the column names, commented out for anki deck importing
#all.append(row)

dict = cdict.CE_Dictionary(False)

#0=kanji 1=pinyin 2=meaning 3=tag 4=pronunciation
for row in reader:
    editedrow = []
    meaning = row[2].lower().strip()
    matches = dict.findByEnglish(meaning)
    if len(matches) == 0:
        editedrow.append("No matches")
        editedrow.append("No matches")        
    elif len(matches) == 1:
        editrow.append(matches[0].get("simplified"))
        editedrow.append(pinyin.get(row[0]))
    else:
        editedrow.append(matches[0].get("simplified"))
        editedrow.append(pinyin.get(matches[0].get("simplified")))
        for match in matches[1:]:
            editedrow[0] = editedrow[0] + "," + match.get("simplified")
            editedrow[1] = editedrow[1] + "," + pinyin.get(match.get("simplified"))
    editedrow.append(meaning)
    editedrow.append(row[3:])
    all.append(editedrow)

writer.writerows(all)
print("CSV file processed")
print("Result file name: " + csv_file.replace(".", "_anki."))