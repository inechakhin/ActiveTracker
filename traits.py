import json
import pandas as pd
import vk
from utils import convert_vk_url_to_vkid, get_id_by_vkid


def max_min_for_types(assessment: list) -> list:
    types_max_min = [{"max": 0, "min": 0} for i in range(5)]
    for task in assessment:
        if task["math"] == "+":
            types_max_min[task["type"]]["max"] += 5
            types_max_min[task["type"]]["min"] += 1
        else:
            types_max_min[task["type"]]["max"] -= 1
            types_max_min[task["type"]]["min"] -= 5
    return types_max_min


def find_question(assessment: list, question: str) -> dict:
    for task in assessment:
        if question == task["question"]:
            return task
    return None


def normalization_types_score(types_score: list, types_max_min: list) -> list:
    for i in range(5):
        min = types_max_min[i]["min"]
        max = types_max_min[i]["max"]
        types_score[i] = (types_score[i] - min) / (max - min)
    return types_score


def build_traits_dataframe(
    df: pd.DataFrame, api: vk.API, assessment: list, types_max_min: list
) -> pd.DataFrame:
    columns = [
        "id",
        "Openness",
        "Conscientiousness",
        "Extraversion",
        "Agreeableness",
        "Neuroticism",
    ]
    t_df = pd.DataFrame(columns=columns)
    for i in range(0, len(df.index)):
        id = None
        types_score = [0 for i in range(5)]
        for col in df.columns:
            if col == "Ссылка на вашу страницу ВКонтакте":
                vkid = convert_vk_url_to_vkid(df.at[i, col])
                id = get_id_by_vkid(api, vkid)
                continue
            task = find_question(assessment, col)
            if task["math"] == "+":
                types_score[task["type"]] += df.at[i, col]
            else:
                types_score[task["type"]] -= df.at[i, col]
        if id:
            types_score = normalization_types_score(types_score, types_max_min)
            values = [id] + types_score
            t_df = pd.concat(
                [pd.DataFrame([values], columns=columns), t_df], ignore_index=True
            )
    return t_df


def main():
    assessment = json.load(open("info/ipip50.json", "r"))
    types_max_min = max_min_for_types(assessment)
   
    con_info = json.load(open("info/connect.json", "r"))
    api = vk.API(access_token=con_info["access_token"], v=con_info["v"])

    df = pd.read_csv("dataset/BIG5.csv")
    df.drop("Отметка времени", axis=1, inplace=True)
    traits_df = build_traits_dataframe(df, api, assessment, types_max_min)
    #print(traits_df)
    traits_df.to_csv("dataset/traits.csv", index=False)


if __name__ == "__main__":
    main()
