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
output = io.open(csv_file.replace(".", "_pinyin."), "w", encoding="utf-8")

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
    editedrow.append(row[0])
    editedrow.append(pinyin.get(row[0]))

    #Check if there's already an english definition
    if not row[2]:
        chinese = row[0]    
        matches = dict.findByChinese(chinese)    
        if len(matches) == 1:
            editedrow.append(matches[0].get("english")) 
        elif len(matches) > 1:
            english_definitions = ""
            for match in matches:
                if not english_definitions:
                    english_definitions += match.get("english")
                else:
                    english_definitions = english_definitions + ", " + match.get("english")
            editedrow.append(english_definitions)
        else:
            editedrow.append(row[2])
    else:
        editedrow.append(row[2])
    all.append(editedrow)

writer.writerows(all)
print("CSV file processed")
print("Result file name: " + csv_file.replace(".", "_pinyin."))