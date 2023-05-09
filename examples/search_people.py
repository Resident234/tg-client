import json

from conf import DEFAULT_PROFILE_PUBLIC_ID, START_PROFILE_PUBLIC_IDS
from linkedin_api import Linkedin

"""
Поиск всех пользоваталей в Linkedin
"""

if __name__ == "__main__":
    with open("../credentials.json", "r") as f:
        credentials = json.load(f)

    if credentials:
        limit = 1000
        offset = 0
        linkedin = Linkedin(credentials["username"], credentials["password"], debug=False)

        while True:
            peoples = linkedin.search_people(keywords='php', offset=offset)#TODO: вскопать внутренности и разобраться как ускорить
            if not len(peoples) or offset >= limit:
                break
            print(len(peoples), peoples)
            offset += len(peoples)
