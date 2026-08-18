import json

# Load existing JSON
with open('src/data/seo_pages.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Translation maps
svc_cn = {
    "end-of-tenancy-cleaning": "退房清洁",
    "professional-carpet-cleaning": "专业地毯清洗",
    "rubbish-waste-clearance": "大件垃圾与杂物清理",
    "deep-cleaning": "全屋深度保洁",
    "move-in-cleaning": "入住前开荒保洁",
    "oven-cleaning": "专业烤箱去重油污",
    "upholstery-cleaning": "沙发除螨清洗",
    "mattress-cleaning": "床垫深度除螨",
    "builders-cleans": "装修后开荒保洁",
    "student-accommodation-cleaning": "留学生公寓特惠保洁"
}
svc_tw = {
    "end-of-tenancy-cleaning": "退房清潔",
    "professional-carpet-cleaning": "專業地毯清洗",
    "rubbish-waste-clearance": "大件垃圾與雜物清理",
    "deep-cleaning": "全屋深度保潔",
    "move-in-cleaning": "入住前開荒保潔",
    "oven-cleaning": "專業烤箱去重油污",
    "upholstery-cleaning": "沙發除蟎清洗",
    "mattress-cleaning": "床墊深度除蟎",
    "builders-cleans": "裝修後開荒保潔",
    "student-accommodation-cleaning": "留學生公寓特惠保潔"
}

city_cn = {
    "Birmingham": "伯明翰", "Manchester": "曼彻斯特", "Glasgow": "格拉斯哥",
    "Leeds": "利兹", "Liverpool": "利物浦", "Newcastle": "纽卡斯尔",
    "Sheffield": "谢菲尔德", "Bristol": "布里斯托", "Nottingham": "诺丁汉",
    "Leicester": "莱斯特", "Edinburgh": "爱丁堡", "Cardiff": "加的夫",
    "Coventry": "考文垂", "Belfast": "贝尔法斯特", "Reading": "雷丁",
    "Southampton": "南安普顿", "London": "伦敦"
}

city_tw = {
    "Birmingham": "伯明罕", "Manchester": "曼徹斯特", "Glasgow": "格拉斯哥",
    "Leeds": "里茲", "Liverpool": "利物浦", "Newcastle": "紐卡斯爾",
    "Sheffield": "雪菲爾", "Bristol": "布里斯托", "Nottingham": "諾丁漢",
    "Leicester": "萊斯特", "Edinburgh": "愛丁堡", "Cardiff": "卡地夫",
    "Coventry": "考文垂", "Belfast": "貝爾法斯特", "Reading": "雷丁",
    "Southampton": "南安普敦", "London": "倫敦"
}

for item in data:
    # Add service translations
    item['service']['name_zh_cn'] = svc_cn.get(item['service']['id'], item['service']['name'])
    item['service']['name_zh_tw'] = svc_tw.get(item['service']['id'], item['service']['name'])
    
    # Add city translations
    orig_city = item['city']['name']
    item['city']['name_zh_cn'] = city_cn.get(orig_city, orig_city)
    item['city']['name_zh_tw'] = city_tw.get(orig_city, orig_city)
    
    # Update H1s and text inside content_zh_cn and content_zh_tw
    # zh-cn
    c_cn = item['city']['name_zh_cn']
    s_cn = item['service']['name_zh_cn']
    item['content_zh_cn']['h1'] = f"{c_cn} {s_cn}团队 (覆盖邮编: {item['city']['postcode']})"
    item['content_zh_cn']['faqs'][0]['question'] = f"在 {c_cn} 你们保证能退回押金吗？"
    item['content_zh_cn']['faqs'][1]['answer'] = f"完全不需要，我们 {c_cn} 的专业团队自带商用级清洁设备和强力环保清洁剂（对中式重油烟特别有效）。"
    
    # zh-tw
    c_tw = item['city']['name_zh_tw']
    s_tw = item['service']['name_zh_tw']
    item['content_zh_tw']['h1'] = f"{c_tw} {s_tw}團隊 (覆蓋郵編: {item['city']['postcode']})"
    item['content_zh_tw']['faqs'][0]['question'] = f"在 {c_tw} 你們保證能退回押金嗎？"
    item['content_zh_tw']['faqs'][1]['answer'] = f"完全不需要，我們 {c_tw} 的專業團隊自帶商用級清潔設備和強力環保清潔劑（對中式重油煙特別有效）。"

with open('src/data/seo_pages.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patched seo_pages.json with translations!")
