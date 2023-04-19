import weaviate
import json

client = weaviate.Client("http://localhost:8000")

class_obj = {
    "class": "Doc", # <= note the capital "A".
    "description": "A test quest and answer",
    "properties": [
        {
            "dataType": [
                "text"
            ],
            "description": "The text of the document",
            "name": "doc"
        }
    ]
}

# add the schema
client.schema.create_class(class_obj)

# get the schema
schema = client.schema.get()

# print the schema
print(json.dumps(schema, indent=4))
