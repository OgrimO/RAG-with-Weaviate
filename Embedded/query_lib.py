import weaviate
import pandas as pd
from weaviate.util import generate_uuid5
import json
from translate import Translator
from langchain_community.embeddings import OllamaEmbeddings

embeddings = (
    OllamaEmbeddings(base_url="http://10.0.8.147:11434",model="quentinz/bge-large-zh-v1.5")
)  # by default, uses llama2. Run `ollama pull llama2` to pull down the model

text = "This is a test document."
# from langchain_community.embeddings import HuggingFaceEmbeddings

import json
class_name='Library_bge'
# --------------------- 连接weaviate --------------------- #
client = weaviate.Client(url='http://10.0.8.147:8080/')
schema = client.schema.get()
class_names = [s["class"] for s in schema["classes"]]
print(class_names)
def json_print(data):
    print(json.dumps(data, indent=2))
# json_print(client.get_meta())
# --------------------- 定义Functions --------------------- #\
def Search(class_name,query):
    count = client.query.aggregate(class_name).with_meta_count().do()
    json_print(count)
    result_name={}
    result_parameter={}
    # print(query)
    for q in query:
        embeded_q=embeddings.embed_query(q)
        nearVector = {"vector": embeded_q}
        response = (
            client.query
            .get(class_name, ["name","parameters"])
            .with_near_vector(nearVector)
            .with_limit(3)
            .with_additional(["distance"])
            .do()
        )
        # print(response)
        l1=[]
        l2=[]

        for data1 in response['data']['Get'][class_name]:
            # print('name: ',data1['name'],'\nparameters: ',data1['parameters'],end='\n')
            l1.append(data1['name'])
            l2.append(data1['parameters'])
           
            # print(data1['name'])
            # print(data1['parameters'])
        result_name[query.index(q)+1]=l1
        result_parameter[query.index(q)+1]=l2
    return result_name,result_parameter
            
query=[None for _ in range(3)]
query[0]="设置电源ON"
query[1]='''操作发动机处于运行状态 
EMS_EngineRunningStatue=0x1: on'''
query[2]='''前雾灯点亮''' 

a,b=Search(class_name,query)
print(a)
print(b)

