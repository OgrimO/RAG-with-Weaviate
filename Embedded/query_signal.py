import weaviate
import pandas as pd
from weaviate.util import generate_uuid5
import json
from translate import Translator
from langchain_community.embeddings import OllamaEmbeddings
import json
embeddings = (
    OllamaEmbeddings(base_url="http://10.0.8.147:11434",model="quentinz/bge-large-zh-v1.5")
)  
class_name='SignalMatrix'

# --------------------- 连接weaviate --------------------- #
client = weaviate.Client(url='http://10.0.8.147:8080/')
schema = client.schema.get()
class_names = [s["class"] for s in schema["classes"]]
# print(class_names)
def json_print(data):
    print(json.dumps(data, indent=2))
# json_print(client.get_meta())
# --------------------- 定义Functions --------------------- #\
def Search(class_name,query):
    count = client.query.aggregate(class_name).with_meta_count().do()
    # json_print(count)
    result_name={}
    result_parameter={}
    for q in query:
        
        nearVector = {"concepts": q}
        response = (
            client.query
            .get(class_name, ["name","parameters"])
            .with_near_text(nearVector)
            .with_limit(3) #expected results
            .with_additional(["distance"])
            .do()
        )
        # print(response)
        # print(class_name)
        l1=[]
        l2=[]
        for data1 in response['data']['Get'][class_name]:
            l1.append(data1['name'])
            l2.append(data1['parameters'])
           
        result_name[query.index(q)+1]=l1
        result_parameter[query.index(q)+1]=l2
    return result_name,result_parameter
            
query=[None for _ in range(3)]
query[0]='''检查信号：
    电源分配状态信号为ON
    PEPS_PowerDistributionStatus=0x3: ON'''

query[1]='''检查信号：
    日间行车灯点亮
    PEPS_PowerDistributionStatus=0x3: ON'''

query[2]='''检查信号：
    日间行车灯关闭"
    ''' 

a,b=Search(class_name,query)
print(a)
print(b)

