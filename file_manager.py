import os
import pandas as pd
import numpy as np
import json

DATA_FOLDER = "data"
FILES = {
    "daily.csv": ["Phase" , "Day" , "Date" ],
    "phase_target.csv": ["Phase", "Day" , 'Date'],
    "xp_points.csv": ["Phase" , "Day" , "Date"],
    "phases_todos.json": {},
    "spaced_repetition.csv": ["Subject" , "Topic", "Sub-Topic", "Hardness", "Last_Revised", "Next_Revision"],
    "habit_data.json" : {},
    "system_setting.json" : {}
}

def check_data_folder():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    check_and_create_files()

def check_and_create_files():
    """Check all required files, create them if missing."""
    for file_name, default_content in FILES.items():
        file_path = os.path.join(DATA_FOLDER, file_name)
        if not os.path.exists(file_path):
            if file_name.endswith(".csv"):
                pd.DataFrame(columns=default_content).to_csv(file_path, index=False)
            elif file_name.endswith(".json"):
                with open(file_path, "w") as f:
                    json.dump(default_content, f)

def files_name():
  d = {}

  for i in FILES:
    x = i
    i = i.split('.')
    d[i[0]] = x 

  return d

def load_data(file_name):
    file_path = os.path.join(DATA_FOLDER , file_name)
    
    if file_name.endswith(".csv"):
        return pd.read_csv(file_path)
    
    if file_name.endswith(".json"):
        with open(file_path, "r") as f:
            return json.load(f)
    
    return None

def add_new_habit(csvfilename, jsonfilename, day_time, newhabit, dtype):
    csv_data = load_data(csvfilename)  
    json_data = load_data(jsonfilename)  

    if day_time not in json_data:
        json_data[day_time] = {}

    if newhabit in csv_data.columns and newhabit in json_data[day_time]:
        return False  

    csv_data[newhabit] = pd.NA

    csv_data.to_csv(os.path.join(DATA_FOLDER, csvfilename), index=False)  

    json_data[day_time][newhabit] = dtype
    with open(os.path.join(DATA_FOLDER, jsonfilename), "w") as f:
        json.dump(json_data, f, indent=4)

    return True

def user_data(user_name, jsonfilename):
    file_path = os.path.join(DATA_FOLDER, jsonfilename)

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            user_info = json.load(f)
    else:
        user_info = {}

    user_info["user_name"] = user_name
    user_info["journey_starts"] = True

    with open(file_path, "w") as f:
        json.dump(user_info, f, indent=4)

def check_journey_start(file_name):
    data = load_data(file_name)
    return "journey_starts" in data and data["journey_starts"] is True


def add_today_if_empty(file_path_csv , file_path_json ,  today):

    df = load_data(file_path_csv)
    data = load_data(file_path_json)

    file_path_csv = os.path.join(DATA_FOLDER, file_path_csv)
    file_path_json = os.path.join(DATA_FOLDER, file_path_json)

    new_row = {col: "NA" for col in df.columns}
    new_row["Date"] = today
    new_row["Phase"] = 1
    new_row["Day"] = 1

    if "current" not in data:
        data["current"] = {}

    data["current"]["start_date"] = today
    data["current"]["current_phase"] = 1
    data["current"]["current_day"] = 1

    with open(file_path_json , "w") as f:
        json.dump(data, f, indent=4)

    df = pd.DataFrame([new_row])
    df.to_csv(file_path_csv, index=False)

def is_file_empty(file_path):
    df = load_data(file_path)
    return df.empty

def daily_file_row_add(csv_file , json_file , today):
    daily_csv = load_data(csv_file)
    setting_json = load_data(json_file)

    file_path_csv = os.path.join(DATA_FOLDER, csv_file)
    file_path_json = os.path.join(DATA_FOLDER, json_file)

    current_phase = setting_json['current']['current_phase']
    current_day = setting_json['current']['current_day']

    current_day += 1 

    if current_day > 10 :
        current_phase += 1 
        current_day = 1

    setting_json["current"]["current_phase"] = current_phase
    setting_json["current"]["current_day"] = current_day

    new_row = {col: "NA" for col in daily_csv.columns}
    new_row["Date"] = today
    new_row["Phase"] = current_phase
    new_row["Day"] = current_day

    with open(file_path_json , "w") as f:
        json.dump(setting_json, f, indent=4)

    updated_csv = pd.concat([daily_csv, pd.DataFrame([new_row])], ignore_index=True)
    updated_csv.fillna("NA", inplace=True)
    updated_csv.to_csv(file_path_csv, index=False)

def replace_na(file_name):
    df = load_data(file_name)

    df = df.astype(str)

    df.replace("nan", "None", inplace=True) 

    file_path = os.path.join(DATA_FOLDER, file_name)
    df.to_csv(file_path, index=False)

def updated_habit_to_csv(new_df, file_path, todaydate):
    daily = load_data(file_path)  

    index_to_replace = daily[daily["Date"] == todaydate].index

    if not index_to_replace.empty:
        daily.loc[index_to_replace] = new_df.values

    else:
        daily = pd.concat([daily, new_df], ignore_index=True)

    file_path = os.path.join(DATA_FOLDER, file_path)
    daily.to_csv(file_path, index=False)
    
    return True


    









