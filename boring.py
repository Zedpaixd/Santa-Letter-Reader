import re
import json
import codecs
import time
from pathlib import Path

start_time = time.time()

secvname = ["My name is ", "I am ", "I'm ","Im"]
secvaddress = ['exp:', 'expeditor:', "Exp:", 'Expeditor:']
secvgifts = ['This year I want ', 'I want to receive ', 'I wish to get ', 'I would like ', 'I would love ',
             'I would like to receive ', 'I wish for ', 'I would like to get ', 'My wish is to receive ']
def find_and_add_name(letter):
    for txt in secvname:
        if re.search(txt, letter) != None:
            x = re.search(txt, letter).span()
            i = x[1]
            if letter[i].isupper():
                n = ''
                while letter[i] != ',' and letter[i] != '.':
                    n = n + letter[i]
                    i += 1
                    if letter[i] == ' ':
                        if letter[i + 1].isupper() == False:
                            break
    
        return n


def find_and_add_address(letter):
    for txt in secvaddress:
        if re.search(txt, letter) != None:
            x = re.search(txt, letter).span()
            i = x[1]
            if letter[i] == " ":
                a = letter[i + 1:len(letter)]
            else:
                a = letter[i:len(letter)]
    if a.find(', nr.'):
        a = a.replace('str. ', '').replace(', nr. ', ',')
    if a.find(' nr.'):
        a = a.replace('str. ', '').replace(' nr. ', ',')
    l = re.split(',', a)
    for i in range(len(l)):
        l[i] = l[i].strip()

        return l
   

def find_and_add_gifts(letter):
    for txt in secvgifts:
        i = letter.rfind(txt)
        if i != -1:
            a = len(txt)
            q = a + i
            g = ""
            while letter[q] not in ['?', '.', '!','\n']:
                g = g + letter[q]
                q += 1
            if re.search(' and', g) != None:
                g = re.sub('and', ',', g)
    g = g.replace('a ', '').replace('the ', '').replace('an ', '')
    l = re.split(',', g)
    for i in range(len(l)):
        l[i] = l[i].strip()

    return l

def find_and_add_color(letter):
    i = letter.find('colour')
    if i != -1:
            a = len('colour')
            q = a + i
            g = ""
            while letter[q] not in ['?', '.', '!','\n',',']:
                g = g + letter[q]
                q += 1
    else:
        return None
    return g.strip()
    
L = []


def dictionary(letter):
    d = {"name": '',
         "address": '',
         "gifts": '',
         "color": None}
    try:
        d['name'] = find_and_add_name(letter)
    except:
        pass
    d['address'] = find_and_add_address(letter)
    d['gifts'] = find_and_add_gifts(letter)
    d['color'] = find_and_add_color(letter)
    return d


a = Path(__file__)
found = 0
i = len(str(a)) - 1
b = str(a)
while found == 0:
    if b[i] != "\\":
        b = b[0:i]
    else:
        found = 1
    i -= 1
b = b + "input"

txt_folder = Path(b).rglob('*.txt')
files = [x for x in txt_folder]

for name in files:
    with codecs.open(name, 'r+',"utf-8") as f:
        l = f.read()
        l=l.replace("\n","").replace("\r","").replace("exp:"," exp: ").replace(" , ",",")
        a=re.split('n\*r=[0-9]+',l)
        while a[0]=='':
            a.pop(0)
            if(a[0]==''):
                print('nu e bine')
        print(a)
        for line in a: 
            L.append(dictionary(line)) 
            pass
out_file = codecs.open('./output.json', 'w+',"utf-8")
json.dump(L, out_file, indent=2)
out_file.close()
print("--- %s seconds ---" % (time.time() - start_time))
##for dicti in L:
  ##  print(dicti)
