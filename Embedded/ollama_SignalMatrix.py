import weaviate
import pandas as pd
from weaviate.util import generate_uuid5
# from langchain_community.embeddings import HuggingFaceEmbeddings

import json
class_name = "SignalMatrix"
# --------------------- 连接weaviate --------------------- #
client = weaviate.Client(url='http://10.0.8.147:8080/')

# --------------------- 创建新的class --------------------- #
# client.schema.delete_class(class_name)
schema = client.schema.get()

def json_print(data):
    print(json.dumps(data, ensure_ascii=False,indent=2))

class_names = [s["class"] for s in schema["classes"]]
print(class_names)

class_obj = {
    "class": class_name,
    "vectorizer": "text2vec-ollama",
      "moduleConfig": {
        "text2vec-ollama": {
          "vectorizeClassName": False,
          "apiEndpoint": "http://10.0.8.147:11434", #apiEndpoint后无斜杠！！
          "model": "quentinz/bge-large-zh-v1.5"
        }
      },
    "vectorIndexConfig": {
        "distance": "cosine"  #acceptable variables:["cosine", "dot", "l2-squared", "manhattan","hamming"]
    }
}

if class_name in class_names:
    print(f"class: \"{class_name}\" already exists.")
else:
    print(f"class: \"{class_name}\" does not exist, create the class.")
    client.schema.create_class(class_obj)
    
# --------------------- 加载原始文件 --------------------- #
d = pd.read_json("data.json", encoding="utf-8")
name = d["名称"].tolist()
# print(name)

parameters=d['参数'].tolist()
# print(parameters)

# # --------------------- 加载embedding模型 --------------------- #
# embed_model = HuggingFaceEmbeddings(
#     model_name="bge-large-zh-v1___5",
#     model_kwargs={"device": "cpu"}
# )

# # --------------------- 文本向量化 --------------------- #
# name_embeddings = embed_model.embed_documents(name)
# signal_embeddings = embed_model.embed_documents(signal)
# parameters_embeddings = embed_model.embed_documents(parameters)
# # print(name)

# --------------------- 构造数据集 --------------------- #
data = { "name": d["名称"],
         "parameters": d["参数"]}
df_with_embed = pd.DataFrame(data)
# --------------------- 批量插入数据 --------------------- #
client.batch.configure(batch_size=100)
with client.batch as batch:
    for i in range(df_with_embed.shape[0]):
        properties = {
            "name": df_with_embed.name[i],
            "parameters":df_with_embed.parameters[i],
            }
        # custom_vector = df_with_embed.embeddings[i]
        batch.add_data_object(
            properties,
            class_name=class_name,
            # vector=custom_vector,
            uuid=generate_uuid5(properties),
        )
        
# --------------------- 查询搜索 --------------------- #
# write a query to extract the vector for a question
result = (client.query
          .get(class_name, ["name", "parameters"])
          .with_additional("vector")
          .with_limit(1)
          .do())

# json_print(result)
