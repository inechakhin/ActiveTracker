import vk


def convert_vk_url_to_vkid(vk_url: str) -> str:
    if "vk.com" in vk_url or "@" in vk_url:
        vk_url = (
            vk_url.replace("https://", "")
            .replace("m.vk.com/id", "")
            .replace("m.vk.com/", "")
            .replace("vk.com/id", "")
            .replace("vk.com/", "")
        )
        if vk_url[0] == "@":
            vk_url = vk_url[1:]
        return vk_url
    else:
        return None


def get_id_by_vkid(api: vk.API, vkid: str) -> str:
    users = api.users.get(user_ids=vkid)
    if users:
        return users[0]["id"]
    else:
        return None


def get_fields_from_features(features: list) -> list:
    fields = set()
    for feature in features:
        parts = feature.split(".")
        fields.add(parts[0])
    return list(fields)


def get_features_by_vkid(api: vk.API, vkid: str, features: list) -> list:
    fields = get_fields_from_features(features)
    users = api.users.get(user_ids=vkid, fields=fields)
    values = []
    if users:
        user = users[0]
        for feature in features:
            parts = feature.split(".")
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
        return values
    else:
        return None
