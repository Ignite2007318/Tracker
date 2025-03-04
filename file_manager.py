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
    "habit_data.json" : {}
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

def load_data(file_name):
    file_path = os.path.join(file_name)
    
    if not os.path.exists(file_path):
        return None
    
    if file_name.endswith(".csv"):
        return pd.read_csv(file_path)
    
    if file_name.endswith(".json"):
        with open(file_path, "r") as f:
            return json.load(f)
    
    return None

def load_files():
   morning = load_data('morning.csv')
   afternoon = load_data('afternoon.csv')
   evening = load_data('evening.csv')
   daily= load_data('daily.csv')
   phaseprogress = load_data('phase_target.csv')
   xprewards = load_data('xp_points.csv')
   todos = load_data('phases_todos.json')
   spacedrepetition= load_data('spaced_repetition.csv')
   habitdata = load_data('habit_data.json')

   return morning , afternoon , evening , daily , phaseprogress , xprewards , todos , spacedrepetition , habitdata

def add_new_habit(csvfilepath, jsonfilepath, day_time, newhabit, dtype):
    csv_data = load_data(csvfilepath)  
    json_data = load_data(jsonfilepath) 

    if day_time not in json_data:
        json_data[day_time] = {}

    if newhabit in csv_data.columns and newhabit in json_data[day_time]:
        return False 

    csv_data[newhabit] = pd.NA  

    csv_data.to_csv(csvfilepath, index=False)

    json_data[day_time][newhabit] = dtype
    with open(jsonfilepath, "w") as f:
        json.dump(json_data, f, indent=4)

    return True

