import io
import pinyin
import codecs
import sys
import csv
import unicodedata


sys.stdout.reconfigure(encoding='utf-8')

class CE_Dictionary:
    def __init__(self, surnames = False):
        self.list_of_dicts = self.parseDictionary()
        self.list_of_dicts = self.remove_surnames(self.list_of_dicts)
        print("Parsed dictionary entries: " + str(len(self.list_of_dicts)))
        
    def remove_surnames(self, list_of_dicts):
        for x in range(len(list_of_dicts)-1, -1, -1):
            if "surname " in list_of_dicts[x]['english']:
                if list_of_dicts[x]['traditional'] == list_of_dicts[x+1]['traditional']:
                    list_of_dicts.pop(x)
        return list_of_dicts
        
    #parsed_dict looks like: [{'traditional': '21三體綜合症', 'simplified': '21三体综合症', 'pinyin': 'er4 shi2 yi1 san1 ti3 zong1 he2 zheng4', 'english': 'trisomy'}]        
    def parseDictionary(self):
        list_of_dicts = []
        with io.open('cedict_ts.u8', "r", encoding="utf-8") as file:
            text = file.read()
            lines = text.split('\n')
            #dict_lines = list(lines)[32:33]
            dict_lines = list(lines)[32:]
        
        for line in dict_lines:
            list_of_dicts.append(self.parse_line(line))

        # print(list_of_dicts)
        return list_of_dicts
    
    def parse_line(self, line):
        parsed = {}
        if line == '':
            dict_lines.remove(line)
            return 0
        line = line.rstrip('/')
        line = line.split('/')
        if len(line) <= 1:
            return 0
        english = line[1]
        char_and_pinyin = line[0].split('[')
        characters = char_and_pinyin[0]
        characters = characters.split()
        traditional = characters[0]
        simplified = characters[1]
        try:
            pinyin = char_and_pinyin[1]
        except IndexError:
            pinyin = 'No Pinyin Found'        
        pinyin = pinyin.rstrip()
        pinyin = pinyin.rstrip("]")
        parsed['traditional'] = traditional
        parsed['simplified'] = simplified
        parsed['pinyin'] = pinyin
        parsed['english'] = english
        return parsed
        
    #Get a list of keys from dictionary which has the given value
    def findByEnglish(self, search_term):
        matches = []
        for item  in self.list_of_dicts:
            if search_term in item['english']:
                matches.append(item)
        return matches
        
    #Get a list of keys from dictionary which has the given value
    def findByChinese(self, search_term):
        search_term = unicodedata.normalize('NFC',search_term)
        matches = []
        for item  in self.list_of_dicts:
            item_simplified_characters =  unicodedata.normalize('NFC',item['simplified'])
            if search_term in item_simplified_characters:
                matches.append(item)
        return  matches    
        
