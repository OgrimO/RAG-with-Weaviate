import weaviate
import pandas as pd
from weaviate.util import generate_uuid5
from langchain_community.embeddings import HuggingFaceEmbeddings

import json
class_name = "Library_bge"
# --------------------- 连接weaviate --------------------- #
client = weaviate.Client(url='http://10.0.8.147:8080/')
# --------------------- 加载embedding模型 --------------------- #
# 使用本地bge模型
embed_model = HuggingFaceEmbeddings(
    model_name="bge-large-zh-v1___5",
    model_kwargs={"device": "cpu"
}
)

# --------------------- 创建新的class --------------------- #
# client.schema.delete_class('Library_bge')
schema = client.schema.get()

def json_print(data):
    print(json.dumps(data, ensure_ascii=False,indent=2))

class_names = [s["class"] for s in schema["classes"]]
print(class_names)

class_obj = {
    "class": class_name,
    "vectorIndexConfig": {
        "distance": "l2-squared"
    }
}

if class_name in class_names:
    print(f"class: \"{class_name}\" already exists.")
else:
    print(f"class: \"{class_name}\" does not exist, create the class.")
    client.schema.create_class(class_obj)
    
    # --------------------- 加载原始文件 --------------------- #
    df = pd.read_json("document.json", encoding="utf-8")
    file = df["file"].tolist()
    # filepath=df["filepath"].tolist()



    # # --------------------- 文本向量化 --------------------- #
    name_embeddings = embed_model.embed_documents(file)
    # print(name)

    # --------------------- 构造数据集 --------------------- #
    data = { "file": df["file"],
            "filepath": df["filepath"],
            "embeddings":name_embeddings}
    df_with_embed = pd.DataFrame(data)
    # --------------------- 批量插入数据 --------------------- #
    client.batch.configure(batch_size=100)
    with client.batch as batch:
        for i in range(df_with_embed.shape[0]):
            properties = {
                "name": df_with_embed.file[i],
                "parameters":df_with_embed.filepath[i],
                }
            custom_vector = df_with_embed.embeddings[i]
            batch.add_data_object(
                properties,
                class_name=class_name,
                vector=custom_vector,
                uuid=generate_uuid5(properties),
            )
            
# --------------------- 查询搜索 --------------------- #
query=[None for _ in range(4)]
query[0] = embed_model.embed_documents(['操作近光灯点亮\nBLIN_CLS_RQ_LB_ON=0x1: On \n'])[0]


query[1] = embed_model.embed_documents(['2、操作发动机处于运行状态 EMS_EngineRunningStatue=0x1: on \n'])[0]

query[2] = embed_model.embed_documents(['前雾灯点亮 Fog'])[0]

query[3]=embed_model.embed_documents(['近光灯熄灭BLIN_CLS_RQ_LB_ON=0x1: On \n'])[0]
for q in query:
    nearVector = {"vector": q}
    response = (
        client.query
        .get(class_name, ["name","parameters"])
        .with_near_vector(nearVector)
        .with_limit(5)
        .with_additional(["distance"])
        .do()
    )
    # print(response)
    for data1 in response['data']['Get'][class_name]:
                print(data1,end='\n')