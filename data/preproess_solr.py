import json, io

with open('houses.json', 'r') as in_f:
    with io.open('houses_with_id.json', 'w', encoding='utf8') as out_f:
        house_ads = json.load(in_f)
        ad_id = 0
        for house_ad in house_ads:
            house_ad['id'] = ad_id
            if type(house_ad['price']) is unicode:
                house_ad['price'] = -1
            ad_id += 1
        json_str = json.dumps(house_ads, ensure_ascii=False)
        out_f.write(json_str)
