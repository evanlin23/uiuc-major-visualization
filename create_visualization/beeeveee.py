import json

f = open("sample.json")

data = json.load(f)

salary = {}
undeclared = []
for item in data["majors_list"]:
    if "undeclared" in item.lower():
        undeclared.append(item)

for key in data["majors_information"]:
    salary.update(
        {
            key: data["majors_information"][key]["data"]["post_graduation_success"][
                "average_salary"
            ]
        }
    )
    # print(
    #     str(key)
    #     + ": "
    #     + data["majors_information"][key]["data"]["post_graduation_success"][
    #         "average_salary"
    #     ]
    # )

# print(salary)
not_enough_data = 0
sorted_salary = sorted(salary.items(), key=lambda x: x[1])
for item in sorted_salary:
    if (
        item[1]
        == "Insufficient survey data is available for average starting annual income."
    ):
        not_enough_data += 1
    print(str(item) + " " + data["majors_information"][item[0]]["data"]["college"])
print(not_enough_data)
# print(sorted_salary)

# print(len(undeclared))
# print(undeclared)
