import json

mother = dict()

char1 = dict()
char1['strength'] = 10
char1['health'] = 100
char2 = dict(char1)

char1['name'] = 'sprite1'
char2['name'] = 'sprite2'

mother[char1['name']] = char1
mother[char2['name']] = char2


with open('C:/Users/SIWPARK/Desktop/magic-i_python_team/gui_ex_code/src/json/test.json', 'w', encoding='utf-8') as make_file:

    json.dump(mother, make_file, indent="\t")

with open('C:/Users/SIWPARK/Desktop/magic-i_python_team/gui_ex_code/src/json/test.json', 'r') as f:

    json_data = json.load(f)

#print(type(dict(json_data)))
a = dict(json_data)
for i in a : 
    print(i)
    for j in a[i] :
        print('\t' + str(j) + ' : ' + str(a[i][j]))