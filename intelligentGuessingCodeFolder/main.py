import string
import pandas as pd
import re

df = pd.read_csv('intelligentGuessingDataSet.csv', encoding="ISO-8859-1")

def analyze(firstname, lastname, firstnames, lastnames, email):
    def nlettercode(n):
        if(n == 1):
            return "<1>"
        else:
            return "<11-f{}l>".format(n)


    codes = {
        "firstname": "<11>",
        "lastname": "<22>",
        "nletters": nlettercode,
        "firstpartlastname": "<20>",
        "lastpartlastname": "<21>",
        "underscore": "_",
        "dot": "."
    }

    matches = {
        "firstname": {
            "status": False,
            "position": None
        },
        "lastname": {
            "status": False,
            "position": None
        },
        "nletters": {
            "status": False,
            "position": 0,
            "n": 0
        },
        "firstpartlastname": {
            "status": False,
            "position": None
        },
        "lastpartlastname": {
            "status": False,
            "position": None
        },
        "underscore": {
            "status": False,
            "position": None
        },
        "dot": {
            "status": False,
            "position": None
        },
    }

    if(not isinstance(firstname, str)):
        firstname = ''

    if(not isinstance(lastname, str)):
        lastname = ''

    current_firstname = firstname.replace("-","")
    current_firstname = current_firstname.replace("ô","o")
    current_firstname = current_firstname.replace("ï", "i")

    current_lastname = lastname.replace("-", "")
    current_lastname = current_lastname.replace("ô", "o")
    current_lastname = current_lastname.replace("ï", "i")

    trimmed_email = re.findall("(^.*)@", email)

    current_email = trimmed_email[0]

    firstname_regex = "^{}".format(current_firstname)
    lastname_regex = "{}$".format(current_lastname)

    x = re.search(firstname_regex, current_email)

    if(x):
        matches["firstname"] = {
            "status": True,
            "position": x.span()[0]
        }

    x = re.search(lastname_regex, current_email)

    if(x):
        matches["lastname"] = {
            "status": True,
            "position": x.span()[0]
        }


    def nletter(x, y):
        n = 0
        position = 0
        for i in range(0, len(x)):
            search = re.search("^{}".format(x[0:i+1]), y)
            if(search):
                n = i+1
                position = search.span()[0]
        return (n, position)


    if(not matches["firstname"]['status']):

        nletter_search = nletter(current_firstname, current_email)

        if(nletter_search[0] > 0):
            matches["nletters"] = {
                "status": True,
                "n": nletter_search[0],
                "position": 0
            }

    lastname_split = current_lastname.split(" ")

    if(len(lastname_split) > 1):
        first_part_regex = "{}".format(lastname_split[0])
        last_part_regex = "{}".format(lastname_split[1])

        x = re.search(first_part_regex, current_email)
        if(x):
            matches["firstpartlastname"] = {
                "status": True,
                "position": x.span()[0]
            }
        x = re.search(last_part_regex, current_email)
        if(x):
            matches["lastpartlastname"] = {
                "status": True,
                "position": x.span()[0]
            }

    underscore_regex = "_"

    x = re.search(underscore_regex, current_email)
    if(x):
        matches["underscore"] = {
            "status": True,
            "position": x.span()[0]
        }


    dot_regex = '.'

    x = re.search(dot_regex, current_email)

    if(x):
        matches["dot"] = {
            "status": True,
            "position": x.span()[0]
        }


    matched_list = []


    def get_position(match_key):
        return matches[match_key]["position"]


    for key in matches:
        if(matches[key]["status"]):
            matched_list.append(key)

    matched_list.sort(key=get_position)

    final_code = ""

    for key in matched_list:

        code = codes[key]
        if(key == "nletters"):
            code = code(matches["nletters"]["n"])

        final_code += code

    return final_code


for i in range(21, 53):
    code = analyze(df["firstname"][i], df["lastname"]
                   [i], [], [], df["email"][i])
    df.loc[i, "Email Pattern"] = code

df.to_csv("problemset1_submission.csv")
