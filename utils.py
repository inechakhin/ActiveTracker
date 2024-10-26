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