# import pandas as pd
# import re

# # Show all Column and Row
# pd.set_option("display.max_rows", 1500)
# pd.set_option("display.max_columns", 150)
# pd.set_option("display.max_colwidth", None)

# # Import CSV file
# csv_file = pd.read_csv("/Users/tl/Documents/subhash_csv/file1.csv")

# # Filter data with specific words
# filtered_csv = csv_file[
#     (csv_file["text"].str.contains("ROCKET|SPACE|LAUNCH|LAUNCHING"))
#     | (csv_file["authority"].str.contains("SPACE|LAUNCH|DELTA"))
# ]
# index_list = filtered_csv.index.tolist()


# rows = []
# for index in index_list:
#     cd_dict = {}
#     cd_data_dict = {}
#     text = filtered_csv.loc[index, "text"]
#     authority = filtered_csv.loc[index, "authority"]

#     if "IN AREAS BOUND BY:" in text:
#         cd_pattern = r"IN AREAS BOUND BY:([\s\S]*?)2\. \w+"
#         cd_matches = re.findall(cd_pattern, text)
#         cd_matches_str = str(cd_matches)[1:-1].replace(" ", "").replace("n", "")
#         pattern = r"[A-z]\.\d{2}"
#         characters = re.findall(pattern, cd_matches_str)

#         for character in characters:
#             char_data = []
#             char_pattern = rf"{character}(.*?)(?={chr(ord(character[0]) + 1)}|$)"
#             char_matches = (
#                 str(re.findall(char_pattern, cd_matches_str, re.DOTALL))[1:-1]
#                 .replace("'", "")
#                 .replace('"', "")
#             )
#             cd_matches_list = [
#                 x.strip() for x in char_matches.split("\\") if x.strip() != ""
#             ]
#             cd_data_dict[character[0]] = cd_matches_list
#         area = ""
#     else:
#         cd_pattern = r"IN AREA BOUND BY([\s\S]*?)2\. \w+"
#         cd_matches = re.findall(cd_pattern, text)
#         cd_matches_list = [
#             x.strip() for x in cd_matches[0].split("\n") if x.strip() != ""
#         ]
#         area = "A"
#         for i, cd_matches in enumerate(cd_matches_list):
#             cd_dict["Cd" + str(i + 1)] = cd_matches

#     # Function for extracting data from text field
#     def extract_data(pattern):
#         matches = re.findall(pattern, text)
#         return str(matches)[1:-1].replace("'", "").replace(" THRU ", " ").split(" ")

#     # Effective Start, Effective End columns - Pattern 1
#     effective_pattern1 = r"(\d{2} THRU \d{2} \w+)"
#     matches1 = extract_data(effective_pattern1)
#     if len(matches1) != 1:
#         effective_start = matches1[0] + " " + matches1[-1]
#         effective_end = matches1[-2] + " " + matches1[-1]

#     # Effective Start, Effective End columns - Pattern 2
#     effective_pattern2 = r"(\d{2} \w+ THRU \d{2} \w+)"
#     matches2 = extract_data(effective_pattern2)
#     if len(matches2) != 1:
#         effective_start = matches2[0] + " " + matches2[1]
#         effective_end = matches2[-2] + " " + matches2[-1]

#     # Function for extracting data from text field
#     def category_and_time_data(pattern):
#         matches = re.findall(pattern, text)
#         return str(matches)[1:-1].replace("'", "").split(" ")

#     # Category column
#     category_pattern = r"(\w+ \d{2} THRU|\w+ \d{2} \w+ THRU)"
#     category_matches = category_and_time_data(category_pattern)
#     category = category_matches[0]

#     # Extract the time start and end and category
#     time_pattern = r"(\d{4}Z TO \d{4}Z)"
#     time_matches = category_and_time_data(time_pattern)
#     time_start = time_matches[0]
#     time_end = time_matches[-1]

#     # if "ALTERNATE" in text:
#     #     # alternate Category column
#     #     alternate_category_pattern = r"(\d{6}Z TO \d{6}Z \w+, ALTERNATE)"
#     #     alternate_matches = re.findall(alternate_category_pattern, text)
#     #     alternate_list = str(alternate_matches)[1:-1].replace("'", "").split(" ")
#     #     alternate_category = alternate_list[-1]

#     #     # create dict for alternate Category data
#     #     if area != "":
#     #         row = {
#     #             "Authority": authority,
#     #             "Effective Start": effective_start,
#     #             "Effective End": effective_end,
#     #             "Category": alternate_category,
#     #             "Time Start": time_start,
#     #             "Time End": time_end,
#     #         }
#     #         row["Area"] = area
#     #         row.update(cd_dict)
#     #         rows.append(row)
#     #     else:
#     #         for key, value in cd_data_dict.items():
#     #             row = {
#     #                 "Authority": authority,
#     #                 "Effective Start": effective_start,
#     #                 "Effective End": effective_end,
#     #                 "Category": alternate_category,
#     #                 "Time Start": time_start,
#     #                 "Time End": time_end,
#     #             }
#     #             for i, cd_matches in enumerate(value):
#     #                 cd_dict["Cd" + str(i + 1)] = cd_matches
#     #             row["Area"] = key
#     #             row.update(cd_dict)
#     #             rows.append(row)

#     # create dict for data
#     alternate_row = {}
#     if area != "":
#         row = {
#             "Authority": authority,
#             "Effective Start": effective_start,
#             "Effective End": effective_end,
#             "Category": category,
#             "Time Start": time_start,
#             "Time End": time_end,
#         }
#         row["Area"] = area
#         row.update(cd_dict)
#         alternate_row.update(row)
#         rows.append(row)
#     else:
#         for key, value in cd_data_dict.items():
#             row = {
#                 "Authority": authority,
#                 "Effective Start": effective_start,
#                 "Effective End": effective_end,
#                 "Category": category,
#                 "Time Start": time_start,
#                 "Time End": time_end,
#             }
#             for i, cd_matches in enumerate(value):
#                 cd_dict["Cd" + str(i + 1)] = cd_matches
#             row["Area"] = key
#             row.update(cd_dict)
#             alternate_row.update(row)
#             rows.append(row)

#     if "ALTERNATE" in text:
#         # alternate Category column
#         alternate_category_pattern = r"(\d{6}Z TO \d{6}Z \w+, ALTERNATE)"
#         alternate_matches = re.findall(alternate_category_pattern, text)
#         alternate_list = str(alternate_matches)[1:-1].replace("'", "").split(" ")
#         alternate_category = alternate_list[-1]
#         alternate_row["Category"] = alternate_category
#         if area != "":
#             rows.append(alternate_row)
#         else:
#             for i, cd_matches in enumerate(value):
#                 cd_dict["Cd" + str(i + 1)] = cd_matches
#                 alternate_row["Area"] = key
#             alternate_row.update(cd_dict)
#             rows.append(alternate_row)

# print(rows)
# df = pd.DataFrame(rows)

# writer = pd.ExcelWriter("data2.xlsx", engine="xlsxwriter")
# df.to_excel(writer, sheet_name="Sheet1", index=False)
# writer.close()


import pandas as pd
import re

# Set display options
pd.set_option("display.max_rows", 1500)
pd.set_option("display.max_columns", 150)
pd.set_option("display.max_colwidth", None)

# Import CSV file
csv_file = pd.read_csv("/Users/tl/Documents/subhash_csv/file1.csv")

# Filter data with specific words
filtered_csv = csv_file[
    (
        csv_file["text"].str.contains(
            "ROCKET|SPACE|LAUNCH|LAUNCHING", na=False, case=False
        )
    )
    | (csv_file["authority"].str.contains("SPACE|LAUNCH|DELTA", na=False, case=False))
]

rows = []
for _, row in filtered_csv.iterrows():
    cd_dict = {}
    cd_data_dict = {}

    text = row["text"]
    authority = row["authority"]

    if "IN AREAS BOUND BY:" in text:
        cd_pattern = r"IN AREAS BOUND BY:([\s\S]*?)2\. \w+"
    else:
        cd_pattern = r"IN AREA BOUND BY([\s\S]*?)2\. \w+"

    cd_matches = re.findall(cd_pattern, text)
    cd_matches_str = "".join(cd_matches).replace(" ", "").replace("\n", "")
    characters = re.findall(r"[A-z]\.\d{2}", cd_matches_str)

    for character in characters:
        char_pattern = rf"{character}(.*?)(?={chr(ord(character[0]) + 1)}|$)"
        char_matches = re.findall(char_pattern, cd_matches_str, re.DOTALL)
        cd_data_dict[character[0]] = [cd.strip() for cd in char_matches]

    area = "" if "IN AREAS BOUND BY:" in text else "A"

    def extract_data(pattern):
        matches = re.findall(pattern, text)
        return str(match.replace("'", "").replace(" THRU ", " ") for match in matches)[
            1:-1
        ].split(" ")

    effective_pattern1 = r"(\d{2} THRU \d{2} \w+)"
    matches1 = extract_data(effective_pattern1)
    effective_start = effective_end = None

    if len(matches1) != 1:
        effective_start = f"{matches1[0]} {matches1[-1]}"
        effective_end = f"{matches1[-2]} {matches1[-1]}"

    effective_pattern2 = r"(\d{2} \w+ THRU \d{2} \w+)"
    matches2 = extract_data(effective_pattern2)

    if len(matches2) != 1:
        effective_start = f"{matches2[0]} {matches2[1]}"
        effective_end = f"{matches2[-2]} {matches2[-1]}"

    category_pattern = r"(\w+ \d{2} THRU|\w+ \d{2} \w+ THRU)"
    category_matches = str(re.findall(category_pattern, text))[1:-1].split(" ")
    category = category_matches[0]

    time_pattern = r"(\d{4}Z TO \d{4}Z)"
    time_matches = str(re.findall(time_pattern, text))[1:-1].split(" ")
    time_start = time_matches[0]
    time_end = time_matches[-1]

    if "ALTERNATE" in text:
        alternate_category_pattern = r"(\d{6}Z TO \d{6}Z \w+, ALTERNATE)"
        alternate_matches = re.findall(alternate_category_pattern, text)
        alternate_list = alternate_matches[0].split(" ")
        alternate_category = alternate_list[-2]

        if area != "":
            row_data = {
                "Authority": authority,
                "Effective Start": effective_start,
                "Effective End": effective_end,
                "Category": alternate_category,
                "Time Start": time_start,
                "Time End": time_end,
                "Area": area,
            }
            row_data.update(cd_dict)
            rows.append(row_data)
        else:
            for key, value in cd_data_dict.items():
                row_data = {
                    "Authority": authority,
                    "Effective Start": effective_start,
                    "Effective End": effective_end,
                    "Category": alternate_category,
                    "Time Start": time_start,
                    "Time End": time_end,
                    "Area": key,
                }
                cd_dict.update(
                    {"Cd" + str(i + 1): cd_match for i, cd_match in enumerate(value)}
                )
                row_data.update(cd_dict)
                rows.append(row_data)

    row_data = {
        "Authority": authority,
        "Effective Start": effective_start,
        "Effective End": effective_end,
        "Category": category,
        "Time Start": time_start,
        "Time End": time_end,
        "Area": area,
    }
    row_data.update(cd_dict)
    rows.append(row_data)

df = pd.DataFrame(rows)
writer = pd.ExcelWriter("data2.xlsx", engine="xlsxwriter")
df.to_excel(writer, sheet_name="Sheet1", index=False)
writer.close()
