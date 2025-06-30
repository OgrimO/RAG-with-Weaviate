import weaviate, os
from weaviate import EmbeddedOptions
import openai
import json
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ.get("OPENAI_API_KEY", "")
url=os.environ.get("WEAVIATE_URL_VERBA", "")
openai.api_base=os.environ.get("OPENAI_BASE_URL", "")
print(openai.api_key)
print(openai.api_base)
# print(url)
client = weaviate.Client(
    # embedded_options=EmbeddedOptions(),
    url=url,
    additional_headers={
        "X-OpenAI-Api-BaseURL": openai.api_base, # Missing base URL can not using ada002
        "X-OpenAI-Api-Key": openai.api_key  # Replace this with your actual key
    }
)

# print(f"Client created? {client.is_ready()}")
def json_print(data):
    print(json.dumps(data, ensure_ascii=False,indent=2))
json_print(client.get_meta())
    # reminder for the data structure


# resetting the schema. CAUTION: This will delete your collection 
if client.schema.exists("SignalMatrix"):
    print("exist SignalMatrix")
    client.schema.delete_class("SignalMatrix")
    
    
class_obj = {
    "class": "SignalMatrix",
    "vectorizer": "text2vec-openai",  # Use OpenAI as the vectorizer
    "moduleConfig": {
        "text2vec-openai": {
            "model": "ada",
            "modelVersion": "002",
            "type": "text",
        }
    }
}
client.schema.create_class(class_obj)


import json

# Read the JSON data from the text file
with open('data.json', 'r', encoding='utf-8') as file:
    json_data = file.read()

# Convert the JSON data to a Python object
data = json.loads(json_data)
print(type(data), len(data))
# Print the Python object to verify the content
print(data[0]['参数'])
for i, d in enumerate(data):  # Batch import data
        
        # print(f"importing question: {i+1}")
        object_uuid = client.data_object.create(
        data_object={
            "name": d["名称"],
            "signal": d["信号名"],
            "parameters": d["参数"],
        },
        class_name="SignalMatrix"
 )

        # print(object_uuid)
# write a query to extract the vector for a question
count = client.query.aggregate("SignalMatrix").with_meta_count().do()
json_print(count)



data_object = client.data_object.get_by_id(object_uuid, class_name="SignalMatrix",with_vector=True)
json_print(data_object)



