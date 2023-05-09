import json

from conf import DEFAULT_PROFILE_PUBLIC_ID, START_PROFILE_PUBLIC_IDS
from linkedin_api import Linkedin

"""
TODO: Слишком много операций со структурами данных производится, тут нужно фундаментально другое решение
поискать алгоритмы по обходам графов
"""

if __name__ == "__main__":
    with open("../credentials.json", "r") as f:
        credentials = json.load(f)

    if credentials:
        limit = 1000
        linkedin = Linkedin(credentials["username"], credentials["password"], debug=False)
        profiles_urn_ids_public_ids_map = {}
        profiles_urn_ids_pull = set()
        profiles_urn_ids_viewed = set()
        profiles_public_ids_viewed = set()

        for profile_id in START_PROFILE_PUBLIC_IDS:
            profile = linkedin.get_profile(profile_id)
            profiles_urn_ids_pull.add(profile["urn_id"])
            profiles_urn_ids_public_ids_map[profile["urn_id"]] = profile["public_id"]
        while True:
            if not profiles_urn_ids_pull:
                break
            profile_urn_id = profiles_urn_ids_pull.pop()
            connections = linkedin.get_profile_connections(profile_urn_id)
            profiles_urn_ids_public_ids_map = {**profiles_urn_ids_public_ids_map, **{connection.get('urn_id'): connection.get('public_id') for connection in connections}}
            profiles_urn_ids_pull = profiles_urn_ids_pull | set([connection.get('urn_id') for connection in connections])
            profiles_urn_ids_viewed.add(profile_urn_id)
            profiles_urn_ids_pull = profiles_urn_ids_pull.difference(profiles_urn_ids_viewed)
            print(f'viewed: {len(profiles_urn_ids_viewed)}, pull: {len(profiles_urn_ids_pull)}')
            if len(profiles_urn_ids_viewed) >= limit:
                break
        profiles_public_ids_viewed = set([profiles_urn_ids_public_ids_map.get(urn_id) for urn_id in profiles_urn_ids_viewed])
        print(profiles_public_ids_viewed)
