import weaviate
import json

#client = weaviate.Client("https://some-endpoint.semi.network/") # <== if you use the WCS
# or
client = weaviate.Client("http://localhost:8000") # <== if you use Docker-compose

# schema = client.schema.get()
# print(json.dumps(schema))


all_objects = client.data_object.get()
print(json.dumps(all_objects))

# print(client.query.get("Doc", ["doc"]).do())