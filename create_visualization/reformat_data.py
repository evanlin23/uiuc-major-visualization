import json
import random
from colour import Color

darkgreen = Color("darkgreen")
colors = list(darkgreen.range_to(Color("yellow"), 200))
# print(colors)


f = open("sample.json")

data = json.load(f)

dictionary = {"nodes": [], "links": []}
dictionary_major_nodes = {"nodes": [], "links": []}
max_salary = 93500
min_salary = 29304

idStart = 0

print("Nodes")
for item in data["majors_list"]:
    salary = data["majors_information"][item]["data"]["post_graduation_success"][
        "average_salary"
    ]
    if (
        salary
        != "Insufficient survey data is available for average starting annual income."
    ):
        color_num = round((salary - min_salary) / (max_salary - min_salary) * 199)
    else:
        color_num = 999
    # print(colors[color_num])
    # print(salary)
    hex = ""
    label = ""
    college = data["majors_information"][item]["data"]["college"]
    desc = data["majors_information"][item]["data"]["description"]
    if color_num == 999:
        hex = "#4C4E52"
        label = "Not Enough Data"
    else:
        hex = colors[color_num].hex
        label = salary
    size = random.randint(7, 27)
    dictionary_major_nodes["nodes"].append(
        {
            "id": idStart,
            "label": item,
            "level": 1,
            "color": hex,
            "salary": label,
            "college": college,
            "description": desc,
            "size": size,
        }
    )
    dictionary["nodes"].append(
        {
            "id": idStart,
            "label": item,
            "level": 1,
            "color": hex,
            "salary": label,
            "college": college,
            "description": desc,
            "size": size,
        }
    )
    idStart += 1

for item in data["grad_school_list"]:
    dictionary["nodes"].append({"id": item.lower(), "label": item, "level": 2})

for item in data["employer_list"]:
    dictionary["nodes"].append({"id": item.lower(), "label": item, "level": 3})

print("links major-major")
for item in data["majors_list"]:
    for item2 in data["majors_list"]:
        if item2 in data["majors_information"][item]["data"]["related_majors"]:
            dictionary["links"].append(
                {"target": item2.lower(), "source": item.lower(), "strength": 0.1}
            )
            start_id = 0
            for item3 in dictionary_major_nodes["nodes"]:
                if item3["label"] == item:
                    start_id = item3["id"]
            end_id = 0
            for item3 in dictionary_major_nodes["nodes"]:
                if item3["label"] == item2:
                    end_id = item3["id"]

            dictionary_major_nodes["links"].append(
                {
                    "target": end_id,
                    "source": start_id,
                    "strength": 0.1,
                }
            )

print("links - employers, grad")
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


# Serializing json
json_object = json.dumps(dictionary, indent=4)

with open("nodes.json", "w") as outfile:
    outfile.write(json_object)

json_object_nodes = json.dumps(dictionary_major_nodes, indent=4)

with open("nodes_majors.json", "w") as outfile:
    outfile.write(json_object_nodes)
