import os
import pandas as pd
import json

DATA_FOLDER = "data"
FILES = {
    "morning.csv": ["Phase" , "Day" , "Date" ],
    "evening.csv": ["Phase" , "Day" , "Date" ],
    "afternoon.csv": ["Phase" , "Day" , "Date" ],
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


