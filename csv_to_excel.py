import pandas as pd
import datetime
import re

# Import CSV file
print("Enter CSV path:", end="")
csv_path = input()
if not csv_path:
    csv_path = "input/testfile.csv"
csv_file = pd.read_csv(csv_path)

# Filter data with specific words
filtered_csv = csv_file[
    (
        csv_file["text"].str.contains("ROCKET|SPACE|LAUNCH|LAUNCHING")
        | csv_file["authority"].str.contains("SPACE|LAUNCH|DELTA")
    )
    & ~(
        csv_file["text"].str.contains("SPACE DEBRIS", case=False, regex=False)
        | csv_file["authority"].str.contains("SPACE DEBRIS", case=False, regex=False)
    )
]
index_list = filtered_csv.index.tolist()

rows = []

for index in index_list:
    cd_dict = {}
    cd_data_dict = {}
    text = filtered_csv.loc[index, "text"]
    authority = filtered_csv.loc[index, "authority"]

    if "IN AREAS BOUND BY:" in text:
        cd_pattern = r"IN AREAS BOUND BY:([\s\S]*?)2\. \w+"
        cd_matches = re.findall(cd_pattern, text)
        cd_matches_str = str(cd_matches)[1:-1].replace(" ", "").replace("n", "")
        pattern = r"[A-z]\.\d{2}-\d{2}\.\d{2}"
        characters = re.findall(pattern, cd_matches_str)

        for character in characters:
            char_data = []
            char_pattern = rf"{character}(.*?)(?={chr(ord(character[0]) + 1)}|$)"
            char_matches = (
                str(re.findall(char_pattern, cd_matches_str, re.DOTALL))[1:-1]
                .replace("'", "")
                .replace('"', "")
            )
            cd_matches_list = [
                x.strip() for x in char_matches.split("\\") if x.strip() != ""
            ]
            cd_data_dict[character[0]] = cd_matches_list
        area = ""

    else:
        area = "A"
        cd_pattern = r"IN AREA BOUND BY([\s\S]*?)2\. \w+"
        cd_matches = re.findall(cd_pattern, text)
        cd_matches_list = [
            x.strip() for x in cd_matches[0].split("\n") if x.strip() != ""
        ]

        for i, cd_matches in enumerate(cd_matches_list):
            cd_dict["Cd" + str(i + 1)] = cd_matches

    # Function for extracting data from text field
    def extract_data(pattern):
        matches = re.findall(pattern, text)
        return str(matches)[1:-1].replace("'", "").replace(" THRU ", " ").split(" ")

    effective_start = ""
    effective_end = ""

    # Effective Start, Effective End columns - Pattern 1
    effective_pattern1 = r"(\d{2} THRU \d{2} \w+)"
    matches1 = extract_data(effective_pattern1)

    try:
        if len(matches1) != 1:
            effective_start = f"{matches1[0]}-{matches1[-1]}"
            effective_end = f"{matches1[-2]}-{matches1[-1]}"
    except:
        pass

    # Effective Start, Effective End columns - Pattern 2
    effective_pattern2 = r"(\d{2} \w+ THRU \d{2} \w+)"
    matches2 = extract_data(effective_pattern2)

    try:
        if len(matches1) != 1:
            effective_start = f"{matches2[0]}-{matches2[1]}"
            effective_end = f"{matches2[-2]}-{matches2[-1]}"
    except:
        pass

    # Category column
    category_pattern = r"(\w+ \d{2} THRU|\w+ \d{2} \w+ THRU)"
    category_matches = (
        str(re.findall(category_pattern, text))[1:-1].replace("'", "").split(" ")
    )

    if len(category_matches) == 1:
        category_pattern2 = r"(\d{1}\. NAVIGATION PROHIBITED \w+ )"
        category_matches2 = (
            str(re.findall(category_pattern2, text))[1:-1].replace("'", "").split(" ")
        )
        try:
            category = f"{category_matches2[1]} {category_matches2[2]}"
        except:
            category = f"{category_matches2[0]}"

    else:
        category = category_matches[0]

    # Extract the time start and end and category
    time_pattern = r"(\d{4}Z TO \d{4}Z)"
    time_matches = str(re.findall(time_pattern, text))[1:-1].replace("'", "").split(" ")
    time_start = time_matches[0]
    time_end = time_matches[-1]

    if "ALTERNATE" in text:
        # alternate Category column
        alternate_category_pattern = r"(\d{6}Z TO \d{6}Z \w+, ALTERNATE)"
        alternate_matches = re.findall(alternate_category_pattern, text)
        alternate_list = (
            str(alternate_matches)[1:-1].replace("'", "").replace(",", "").split(" ")
        )

        alternate_category = alternate_list[-1]
        alternate_effective_start = f"{alternate_list[0][:2]}-{alternate_list[3]}"
        alternate_effective_end = f"{alternate_list[2][:2]}-{alternate_list[3]}"
        alternate_time_start = alternate_list[0][2:]
        alternate_time_end = alternate_list[2][2:]

        # create dict for alternate Category data
        if area != "":
            row = {
                "Authority": authority,
                "Effective Start": alternate_effective_start,
                "Effective End": alternate_effective_end,
                "Category": alternate_category,
                "Time Start": alternate_time_start,
                "Time End": alternate_time_end,
            }
            row["Area"] = area
            row.update(cd_dict)
            rows.append(row)

        else:
            for key, value in cd_data_dict.items():
                row = {
                    "Authority": authority,
                    "Effective Start": alternate_effective_start,
                    "Effective End": alternate_effective_end,
                    "Category": alternate_category,
                    "Time Start": alternate_time_start,
                    "Time End": alternate_time_end,
                }

                for i, cd_matches in enumerate(value):
                    cd_dict["Cd" + str(i + 1)] = cd_matches
                row["Area"] = key
                row.update(cd_dict)
                rows.append(row)

    # create dict for data
    if area != "":
        row = {
            "Authority": authority,
            "Effective Start": effective_start,
            "Effective End": effective_end,
            "Category": category,
            "Time Start": time_start,
            "Time End": time_end,
        }
        row["Area"] = area
        row.update(cd_dict)
        rows.append(row)

    else:
        for key, value in cd_data_dict.items():
            row = {
                "Authority": authority,
                "Effective Start": effective_start,
                "Effective End": effective_end,
                "Category": category,
                "Time Start": time_start,
                "Time End": time_end,
            }

            for i, cd_matches in enumerate(value):
                cd_dict["Cd" + str(i + 1)] = cd_matches
            row["Area"] = key
            row.update(cd_dict)
            rows.append(row)


df = pd.DataFrame(rows)
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
writer = pd.ExcelWriter(f"output/data{current_time}.xlsx", engine="xlsxwriter")
df.to_excel(writer, sheet_name="Sheet1", index=False)
writer.close()

print("Task run Successfully!")
