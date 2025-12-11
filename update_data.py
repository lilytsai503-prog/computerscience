import pandas as pd
from deep_translator import GoogleTranslator
import json
import time
import requests
import io
import os

csv_url = "https://data.fda.gov.tw/opendata/exportDataLinked.do?method=ExportData&InfoId=178&logType=2"

try:
    response = requests.get(csv_url, verify=False)
    response.encoding = 'utf-8-sig'
    df = pd.read_csv(io.StringIO(response.text))
    
    old_data_map = {}
    if os.path.exists('food_database.json'):
        with open('food_database.json', 'r', encoding='utf-8') as f:
            old_list = json.load(f)
            for item in old_list:
                old_data_map[item['zh']] = item
    
    def get_english_name(text):
        try:
            if not text or str(text).isascii(): return text
            return GoogleTranslator(source='zh-TW', target='en').translate(text)
        except:
            return text

    new_database_list = []

    for index, row in df.iterrows():
        zh_name = row.get('樣品名稱', '').strip()
        if pd.isna(zh_name) or zh_name == '': continue
        
        new_cal = str(row.get('熱量', '0')).strip()
        if new_cal == 'nan': new_cal = '0'

        if zh_name in old_data_map:
            old_entry = old_data_map[zh_name]
            old_cal = str(old_entry.get('cal', '0')).strip()

            if old_cal != new_cal:
                old_entry['cal'] = new_cal
            
            new_database_list.append(old_entry)
        
        else:
            en_name = get_english_name(zh_name)
            new_database_list.append({
                "zh": zh_name,
                "en": en_name,
                "cal": new_cal
            })
            time.sleep(0.5)

    filename = 'food_database.json'
    backup_filename = 'food_database.backup.json'

    if os.path.exists(filename):
        if os.path.exists(backup_filename):
            os.remove(backup_filename)
        os.rename(filename, backup_filename)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(new_database_list, f, ensure_ascii=False, indent=4)

    print(f"Update Complete. Total: {len(new_database_list)}")

except Exception as e:
    print(f"Error: {e}")