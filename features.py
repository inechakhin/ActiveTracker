import pandas as pd


df = pd.read_csv("dataset/BIG5.csv")
vk_list = df["Ссылка на вашу страницу ВКонтакте"].to_list()

vkid_list = []
for vkid in vk_list:
    if "vk.com" in vkid or "@" in vkid:
        vkid = (
            vkid.replace("https://", "")
            .replace("m.vk.com/id", "")
            .replace("m.vk.com/", "")
            .replace("vk.com/id", "")
            .replace("vk.com/", "")
        )
        if vkid[0] == "@": vkid = vkid[1:]
        vkid_list.append(vkid)

print(len(vkid_list))
print(vkid_list)
