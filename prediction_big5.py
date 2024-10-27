import json
import vk
import numpy as np
from keras.models import Sequential
from utils import convert_vk_url_to_vkid, get_features_by_vkid

def preprocess_input_data(input_data: list):
    input_data = np.where(input_data == None, np.nan, input_data)
    # input_data = (input_data - np.mean(input_data)) / np.std(input_data)
    input_data = input_data.reshape(1, -1)
    return input_data


def predict_big5(vk_url: str, api: vk.API, features: list, model: Sequential):
    vkid = convert_vk_url_to_vkid(vk_url)
    values = get_features_by_vkid(api, vkid, features)
    #print(values)
    values = preprocess_input_data(values[1:])
    #print(values)
    pred = model.predict(values)
    return pred

