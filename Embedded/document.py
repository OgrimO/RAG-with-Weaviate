import os,json
def get_filespath(path):
    dict={}
    for filepath,dirnames,filenames in os.walk(fr'{path}'):
        for filename in filenames:
            dict[filename]=os.path.join(filepath,filename).replace('C:/TAE','')
    return dict
path='C:/TAE/library/VV'
output = []

dict=get_filespath(path)
for key,  params in dict.items():
    item = {
    'file': key,
    'filepath': params
    }
    output.append(item)
json_str = json.dumps(output, ensure_ascii=False, indent=4)
with open('document.json','w',encoding='utf-8') as d:
    d.write(json_str)