import pandas as pd
import json
import vk
from utils import convert_vk_url_to_vkid


def get_vkid_from_vk_list(vk_list: list) -> list:
    vkid_list = []
    for vk_url in vk_list:
        vkid = convert_vk_url_to_vkid(vk_url)
        if vkid:
            vkid_list.append(vkid)
    return vkid_list


def build_features_dataframe(
    api: vk.API, vkid_list: list, columns: list
) -> pd.DataFrame:
    f_df = pd.DataFrame(columns=columns)
    for vkid in vkid_list:
        values = []
        users = api.users.get(
            user_ids=vkid,
            fields=[
                "counters",
                "city",
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
            ],
        )
        if users:
            user = users[0]
            for column in columns:
                parts = column.split(".")
                if len(parts) == 1:
                    if parts[0] in user:
                        values.append(user[parts[0]])
                    else:
                        values.append(None)
                if len(parts) == 2:
                    if parts[0] in user and parts[1] in user[parts[0]]:
                        values.append(user[parts[0]][parts[1]])
                    else:
                        values.append(None)
            f_df = pd.concat(
                [pd.DataFrame([values], columns=columns), f_df], ignore_index=True
            )
    return f_df


def main():
    df = pd.read_csv("dataset/BIG5.csv")
    vk_list = df["Ссылка на вашу страницу ВКонтакте"].to_list()
    vkid_list = get_vkid_from_vk_list(vk_list)

    con_info = json.load(open("connect_info.json", "r"))
    api = vk.API(access_token=con_info["access_token"], v=con_info["v"])

    columns = [
        "id",
        "counters.followers",
        "counters.pages",
        "counters.photos",
        "counters.videos",
        "sex",
        "counters.clips_followers",
        "city.id",
        "occupation.id",
    ]

    features_df = build_features_dataframe(api, vkid_list, columns)
    features_df.to_csv("dataset/features.csv", index=False)


if __name__ == "__main__":
    main()
