# streamlit run main.py
import os
import pandas as pd
import numpy as np
import json

DATA_FOLDER = "data"
FILES = {
    "daily.csv": ["Phase" , "Day" , "Date" ],
    "phase_target.csv": ["Phase", "Day" , 'Date'],
    "xp_points.csv": ["Phase" , "Day" , "Date" , "XP Gained" , "XP Used" , "Total XP Avl"],
    "phases_todos.csv": ["Phase" , "Day" , "Task ID" , "Task Description" , "Completed" , "Get XP"],
    "spaced_repetition.csv": ["Unique ID" , "Subject", "Topic", "Sub Topic",
                               "Difficulty Status", "Next Revision", "Review Count", "Note"],
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

    csv_data[newhabit] = 0.0

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

    new_row = {col: 0.0 for col in df.columns}
    new_row["Date"] = today
    new_row["Phase"] = 1
    new_row["Day"] = 1

    if "current" not in data:
        data["current"] = {}

    data["current"]["start_date"] = today
    data["current"]["current_phase"] = 1
    data["current"]["current_day"] = 1
    data["current"]["overall_current_day"] = 1

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
    setting_json["current"]["overall_current_day"] = ((current_phase - 1) * 10) + current_day

    new_row = {col: 0.0 for col in daily_csv.columns}
    new_row["Date"] = today
    new_row["Phase"] = current_phase
    new_row["Day"] = current_day

    with open(file_path_json , "w") as f:
        json.dump(setting_json, f, indent=4)

    updated_csv = pd.concat([daily_csv, pd.DataFrame([new_row])], ignore_index=True)
    updated_csv.fillna(0.0, inplace=True)
    updated_csv.to_csv(file_path_csv, index=False)


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

def extract_file_names(name):
    x = files_name()
    x = x[name]
    return x

def add_new_phase_target(habit, habit_target):
    phase_target = load_data(extract_file_names("phase_target"))
    habit_data = load_data(extract_file_names("habit_data"))

    if "phase_target" not in habit_data:
        habit_data["phase_target"] = {}

    if habit in habit_data["phase_target"]:
        return False

    phase_target[habit] = pd.NA   

    habit_data["phase_target"][habit] = habit_target

    phase_target_file_path = os.path.join(DATA_FOLDER, extract_file_names('phase_target'))
    habit_data_file_path = os.path.join(DATA_FOLDER, extract_file_names('habit_data'))

    phase_target.to_csv(phase_target_file_path, index=False)

    with open(habit_data_file_path, "w") as f:
        json.dump(habit_data, f, indent=4)

    return True

def update_new_phase_target(habit , new_target):
    data = load_data(extract_file_names('habit_data'))

    data['phase_target'][habit] = new_target

    habit_data_file_path = os.path.join(DATA_FOLDER, extract_file_names('habit_data'))

    with open(habit_data_file_path, "w") as f:
        json.dump(data, f, indent=4)

    return True

def phase_target_update_row(today):
    phase_target = load_data(extract_file_names('phase_target'))
    daily = load_data(extract_file_names('daily'))
    system_setting = load_data(extract_file_names('system_setting'))

    current_phase = system_setting['current']['current_phase']
    current_day = system_setting['current']['current_day']
    current_date = today

    daily = daily[daily['Phase'] == current_phase]

    habit_columns = list(phase_target.columns[3:])

    daily = daily[habit_columns]

    numeric_cols = daily.select_dtypes(include=['number']).columns
    daily_sum = daily[numeric_cols].sum().to_frame().T

    daily_sum.insert(0, 'Phase', current_phase)
    daily_sum.insert(1, 'Day', current_day)
    daily_sum.insert(2, 'Date', current_date)

    existing_entry = (phase_target['Phase'] == current_phase) & (phase_target['Day'] == current_day)
    
    if existing_entry.any():
        phase_target.loc[existing_entry, habit_columns] = daily_sum[habit_columns].values

    else:
        phase_target = pd.concat([phase_target, daily_sum], ignore_index=True)

    phase_target_file_path = os.path.join(DATA_FOLDER, extract_file_names('phase_target'))
    phase_target.to_csv(phase_target_file_path, index=False)

    return True

def save_to_csv_append(data, file_name):
    #appends new row

    data = pd.DataFrame(data)

    file_path = f"data/{file_name}"

    data.to_csv(file_path, mode='a', index=False, header=False)

    return True

def save_to_csv_update(data , file_name):
    # this rewrite the intire file

    df = pd.DataFrame(data)

    file_path = f"data/{file_name}"
    
    df.to_csv(file_path, index=False)

def save_to_json(data , file_path):

    file_path = os.path.join(DATA_FOLDER, file_path)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    return True

def update_last_row_in_csv(file_path, new_row_dict):
    df = load_data(file_path)

    for col in df.columns:
        if col not in new_row_dict:
            new_row_dict[col] = None 

    df.iloc[-1] = pd.Series(new_row_dict)[df.columns]

    file_path = f"data/{file_path}"
    df.to_csv(file_path, index=False)





