from bs4 import BeautifulSoup
import json

dictionary = {
    "majors_list": [],
    "grad_school_list": [],
    "employer_list": [],
    "majors_information": {},
}
output = open("out.txt", "w")

with open("index.html", "r") as input:
    contents = input.read()
    soup = BeautifulSoup(contents, "html.parser")
    grad_school_list_new = []
    employer_list_new = []
    for tag in soup.find_all("div", attrs={"class": "programItem"}):
        new_grad_schools = []
        current_page = tag.find(
            "a", attrs={"class": "addToCart btn btn-outline-secondary"}
        )["data"]
        file = "./grad_school_data/" + current_page
        with open(file, "r") as page:
            current_page_soup = BeautifulSoup(page, "html.parser")
            for item in current_page_soup.find_all("li"):
                new_grad_schools.append(item.get_text())

        if new_grad_schools == []:
            new_grad_schools.append(
                "Insufficient survey data is available for sample grad school destinations."
            )

        new_employers = []

        file2 = "./employer_data/" + current_page
        with open(file2, "r") as page:
            current_page_soup = BeautifulSoup(page, "html.parser")
            for item in current_page_soup.find_all("li"):
                new_employers.append(item.get_text())
        if new_employers == []:
            new_employers.append(
                "Insufficient survey data is available for sample employer destinations."
            )

        # add to totals
        for item in new_grad_schools:
            if item not in grad_school_list_new:
                grad_school_list_new.append(item)
        for item in new_employers:
            if item not in employer_list_new:
                employer_list_new.append(item)

        # career options
        options = []
        for i in range(len(tag.div.ul.contents)):
            if tag.div.ul.contents[i].get_text() != "\n":
                option = tag.div.ul.contents[i].get_text().replace(", ", "").strip()
                # if option.startswith("&"):
                #     option = option[2:]
                # if option.startswith("and"):
                #     option = option[4:]
                options.append(
                    tag.div.ul.contents[i]
                    .get_text()
                    .replace(", ", "")
                    .replace(",", "")
                    .strip()
                    .capitalize()
                )

        related_majors_elem = tag.find("div", class_="relatedMajors section")
        related_majors = []
        if related_majors_elem:
            # print(related_majors_elem)
            for item in related_majors_elem.find_all(
                "a", class_="data-description major-link"
            ):
                # print(item.get_text().split(" - ")[0])
                related_majors.append(item.get_text().split(" - ")[0])
        # print(related_majors)

        post_graduation_elem = tag.find("div", class_="programPercentJob")
        if post_graduation_elem:
            # employed_or_continuing_education = post_graduation_elem.find(
            #     "span", class_="number"
            # ).get_text()

            # employed_after_graduation_elem = post_graduation_elem.find_all(
            #     "span", class_="number"
            # )

            # attending_graduate_school_elem = post_graduation_elem.find_all(
            #     "span", class_="number"
            # )

            # employed_after_graduation = (
            #     employed_after_graduation_elem[0].get_text()
            #     if employed_after_graduation_elem
            #     else ""
            # )
            # attending_graduate_school = ""
            # if len(employed_after_graduation_elem) > 1:
            #     attending_graduate_school = employed_after_graduation_elem[1].get_text()

            average_salary_elem = tag.find("div", class_="programAnnualSalary")
            average_salary = (
                average_salary_elem.find("span", class_="number").get_text()
                if average_salary_elem
                else ""
            )

        else:
            employed_or_continuing_education = ""
            employed_after_graduation = ""
            attending_graduate_school = ""
            average_salary = "Insufficient survey data is available for average starting annual income."
            employer_destinations = [
                "Insufficient survey data is available for sample employer destinations."
            ]
            grad_school_destinations = [
                "Insufficient survey data is available for sample grad school destinations."
            ]
        dictionary["majors_list"].append(
            tag.div.div.h2.contents[0]
            .get_text()
            .replace("What is ", "")
            .replace("?", "")
        )
        dictionary["majors_information"].update(
            {
                tag.div.div.h2.contents[0]
                .get_text()
                .replace("What is ", "")
                .replace("?", ""): {
                    "data": {
                        "description": tag.div.div.p.contents[0].get_text().strip(),
                        "career_options": options,
                        "college": tag.p.a.contents[0].get_text(),
                        "related_majors": related_majors,
                        "post_graduation_success": {
                            # "employed_or_continuing_education": employed_or_continuing_education,
                            # "employed_after_graduation": employed_after_graduation,
                            # "attending_graduate_school": attending_graduate_school,
                            "average_salary": average_salary,
                            "employer_destinations": new_employers,
                            "grad_school_destinations": new_grad_schools,
                        },
                    }
                }
            }
        )
    grad_school_list_new.sort()
    employer_list_new.sort()
    dictionary["grad_school_list"] = grad_school_list_new
    dictionary["employer_list"] = employer_list_new

#     majors.append(tag.get_text())
# for tag in soup.find_all("div", attrs={"class": "programAnnualSalary"}):
#     print(tag.p.get_text())
#     salaries.append(tag.p.get_text())
# for i in range(len(majors)):
#     print(majors[i] + ": " + salaries[i])
# div class = programItem
# major: class=major-h1
# career examples: class=programCareerExamples
# class=programPercentJob
# programAnnualSalary
# programJobDestinations
# programGradSchoolDestinations

# Serializing json
json_object = json.dumps(dictionary, indent=4)

# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)
