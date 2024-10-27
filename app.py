from flask import Flask, request, jsonify
import json
import vk
import pandas as pd
from keras.models import model_from_json
from utils import convert_vk_url_to_vkid, get_fullname_and_photo_by_vkid
from prediction_big5 import predict_big5

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    vk_url = data["vk_url"]
    vkid = convert_vk_url_to_vkid(vk_url)
    if not vkid:
        return jsonify({"error" : "This not vk url!"})
    fn, ln, ph = get_fullname_and_photo_by_vkid(api, vkid)
    if not fn:
        return jsonify({"error" : "User not found!"})
    
    global features_df
    prediction, features_df = predict_big5(vk_url, api, features_df, model)
    big5 = {
        "O": round(prediction[0][0].item(), 3),
        "C": round(prediction[0][1].item(), 3), 
        "E": round(prediction[0][2].item(), 3), 
        "A": round(prediction[0][3].item(), 3), 
        "N": round(prediction[0][4].item(), 3)
    }

    return jsonify({"first_name" : fn, "last_name" : ln, "photo" : ph, "traits" : big5})


if __name__ == "__main__":
    con_info = json.load(open("info/connect.json", "r"))
    api = vk.API(access_token=con_info["access_token"], v=con_info["v"])

    features_df = pd.read_csv("dataset/new_features.csv")

    json_file = open("info/model.json", "r")
    model_info = json_file.read()
    json_file.close()
    model = model_from_json(model_info)
    model.load_weights("info/model.h5")

    app.run(port=8000, debug=True)
    features_df.to_csv("dataset/new_features.csv", index=False)
    
