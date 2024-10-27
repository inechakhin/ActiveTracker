import json
import vk
import pandas as pd
import numpy as np
from keras.models import Sequential
from utils import convert_vk_url_to_vkid, get_features_by_vkid
from features import fill_gaps

def preprocess_input_data(input_data: list, features_df: pd.DataFrame):
    id = input_data[0]
    if not (features_df["id"] == id).any():
        features_df = pd.concat([pd.DataFrame([input_data], columns=features_df.columns), features_df], ignore_index=True)
        features_df = fill_gaps(features_df)
    input_data = features_df.loc[features_df["id"] == id].values.tolist()
    # input_data = (input_data - np.mean(input_data)) / np.std(input_data)
    return [input_data[0][1:]], features_df


def predict_big5(vk_url: str, api: vk.API, features_df: pd.DataFrame, model: Sequential):
    vkid = convert_vk_url_to_vkid(vk_url)
    features = features_df.columns
    values = get_features_by_vkid(api, vkid, features)
    values, features_df = preprocess_input_data(values, features_df)
    pred = model.predict(values)
    return pred, features_df

