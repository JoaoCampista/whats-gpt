import json
import weaviate
from weaviate.util import generate_uuid5

def load(fname):
    with open(fname, "r") as f:
        return json.load(f) 

embeddings = load("embeddings.json")

client = weaviate.Client("http://localhost:8000")

# Configure a batch process
client.batch.configure(
  batch_size=100, 
  dynamic=True,
  timeout_retries=3,
  callback=None,
)

# Batch import all Publications
for text in embeddings:
#   print("importing publication: ", publication["name"])

  properties = {
    "doc": text
  }
  id = generate_uuid5(properties, 'Doc')
  client.batch.add_data_object(properties, "Doc", id, embeddings[text])

# Flush the remaining buffer to make sure all objects are imported
client.batch.flush()
