import json

f = open("sample.json")

data = json.load(f)

dictionary = {"nodes": [], "links": []}

for item in data["majors_list"]:
    dictionary["nodes"].append({"id": item.lower(), "label": item, "level": 1})

for item in data["grad_school_list"]:
    dictionary["nodes"].append({"id": item.lower(), "label": item, "level": 2})

for item in data["employer_list"]:
    dictionary["nodes"].append({"id": item.lower(), "label": item, "level": 3})

for item in data["majors_list"]:
    for item2 in data["majors_list"]:
        dictionary["links"].append(
            {"target": item.lower(), "source": item2.lower(), "strength": 0.1}
        )

for key in data["majors_information"]:
    for item in data["majors_information"][key]["data"]["post_graduation_success"][
        "employer_destinations"
    ]:
        if (
            item
            != "Insufficient survey data is available for sample employer destinations."
        ):
            dictionary["links"].append(
                {"target": item.lower(), "source": key.lower(), "strength": 0.1}
            )
    for item in data["majors_information"][key]["data"]["post_graduation_success"][
        "grad_school_destinations"
    ]:
        if (
            item
            != "Insufficient survey data is available for sample grad school destinations."
        ):
            dictionary["links"].append(
                {"target": item.lower(), "source": key.lower(), "strength": 0.1}
            )


# print(dictionary)
# var links = [
# 	{ target: "mammal", source: "dog" , strength: 0.7 },
# 	{ target: "mammal", source: "cat" , strength: 0.7 },
#   { target: "mammal", source: "fox" , strength: 0.7 },
#   { target: "mammal", source: "elk" , strength: 0.7 },
#   { target: "insect", source: "ant" , strength: 0.7 },
#   { target: "insect", source: "bee" , strength: 0.7 },
#   { target: "fish"  , source: "carp", strength: 0.7 },
#   { target: "fish"  , source: "pike", strength: 0.7 },
#   { target: "cat"   , source: "elk" , strength: 0.1 },
#   { target: "carp"  , source: "ant" , strength: 0.1 },
#   { target: "elk"   , source: "bee" , strength: 0.1 },
#   { target: "dog"   , source: "cat" , strength: 0.1 },
#   { target: "fox"   , source: "ant" , strength: 0.1 },
# 	{ target: "pike"  , source: "cat" , strength: 0.1 }
# ]
# Serializing json
json_object = json.dumps(dictionary, indent=4)

with open("nodes.json", "w") as outfile:
    outfile.write(json_object)
