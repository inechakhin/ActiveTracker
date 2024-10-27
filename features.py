import pandas as pd
import numpy as np
import json
import vk
from utils import convert_vk_url_to_vkid, get_features_by_vkid
from collections import Counter
from sklearn.preprocessing import StandardScaler


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
        values = get_features_by_vkid(api, vkid, columns)
        if values:
            f_df = pd.concat(
                [pd.DataFrame([values], columns=columns), f_df], ignore_index=True
            )
    return f_df


def my_mode(sample):
    count = Counter(sample)
    return [key for key, value in count.items() if value == count.most_common(1)[0][1]]


def fill_gaps(df: pd.DataFrame) -> pd.DataFrame:
    set_all_keys = dict()
    array_all_keys = dict()
    for col in df.columns:
        set_all_keys[col] = set()
        array_all_keys[col] = []

    for col in df.columns:
        for elem in df[col].dropna():
            set_all_keys[col].add(elem)
            array_all_keys[col].append(elem)

    for k, v in set_all_keys.items():
        set_all_keys[k] = len(v)

    res_for_gaps = dict()
    all_value = len(df.index)
    for col in df.columns:
        none_value = df[col].isna().sum()
        if col != "id":
            res_for_gaps[col] = (none_value / all_value) * 100

    for col in df.columns:
        for i in range(0, len(df.index)):
            if col != "id" and res_for_gaps[col] < 40:  ### 30??
                if set_all_keys[col] > 15:
                    if df.at[i, col] is np.nan or df.at[i, col] is None:
                        df.at[i, col] = round(np.mean(array_all_keys[col]), 1)
                else:
                    if df.at[i, col] is np.nan or df.at[i, col] is None:
                        df.at[i, col] = my_mode(array_all_keys[col])[0]
    return df


def main():
    df = pd.read_csv("dataset/BIG5.csv")
    vk_list = df["Ссылка на вашу страницу ВКонтакте"].to_list()
    vkid_list = get_vkid_from_vk_list(vk_list)

    con_info = json.load(open("info/connect.json", "r"))
    api = vk.API(access_token=con_info["access_token"], v=con_info["v"])

    columns = json.load(open("info/features.json", "r"))

    features_df = build_features_dataframe(api, vkid_list, columns)
    features_df = fill_gaps(features_df)
    # scaler = StandardScaler()
    # df_columns = features_df.columns
    # features_df[df_columns[1:]] = scaler.fit_transform(features_df[df_columns[1:]])
    # print(features_df)
    features_df.to_csv("dataset/features.csv", index=False)


if __name__ == "__main__":
    main()
