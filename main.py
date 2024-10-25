import json
import vk
from vk.exceptions import VkAPIError

con_info = open("connect_info.json", "r")
con_data = json.load(con_info)

api = vk.API(access_token=con_data["access_token"], v=con_data["v"])
# user_id = int(input("Enter user_id: "))
name = input("Enter user_id: ")

try:
    user = api.users.get(
        user_ids=name,
        fields=[
            "counters",
            "city",
            "about",
            "activities",
            "education",
            "career",
            "interests",
            "lists",
            "occupation",
            "personal",
            "relatives",
            "relation",
            "schools",
            "sex",
            "status",
            "universities",
            "bdate",
        ],
    )
    print(user)
    print("\n")

    # fr = api.friends.get(user_id=user[0]['id'])
    sub = api.users.getSubscriptions(user_id=user[0]['id'])
    print(sub)

except VkAPIError as e:
    print(e.message)
