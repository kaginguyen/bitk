import json 
import pandas as pd 

with open("./text.txt", "r") as file: 
    json_dict = json.loads(file.read()) 

data = json_dict.get("data")

sample = data[0]
base_dict = {"id": []}
for attribute in data[0]["attributes"]:
    base_dict[attribute] = []



for store in data: 
    base_dict["id"].append(store["id"])
    for attribute in store["attributes"]:
        base_dict[attribute].append(store["attributes"][attribute])

df = pd.DataFrame.from_dict(base_dict)
df.to_csv("./data.csv", index = False)