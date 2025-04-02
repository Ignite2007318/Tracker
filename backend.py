# streamlit run main.py
import pandas as pd
import numpy as np
import json 
import file_manager
import datetime as dt
from datetime import datetime, date
import math

x = file_manager.files_name()

def today_date():
 today_date = dt.datetime.today().strftime("%Y-%m-%d")
 return today_date

def add_habit_filter(new_habit, habit_type):
   
   a = x['daily']
   y = x['habit_data']

   value = file_manager.add_new_habit(a , y , 'daily_habit' , new_habit , habit_type )

   if value == True:
      return True
   else :
      return "Habit Alredy Exist"
   
def add_default(user_name):
   
    default_habits = {
     "Wake up Time": "Time",
     "Exercise/Workout": "Yes/No",
     "Screen Time": "Time",
     "Study Time": "Time",
}
    file_path = x["system_setting"]
 
    for habit_name in default_habits:

      habit_type = default_habits[habit_name] 
      add_habit_filter(habit_name , habit_type)

      file_manager.user_data(user_name , file_path )

def daily_row_add():

   value = file_manager.load_data(x["daily"])

   check_value  = file_manager.check_journey_start(x["system_setting"])

   if check_value == True:
      empty = file_manager.is_file_empty(x["daily"])

      if empty :
         file_manager.add_today_if_empty(x["daily"] ,  x["system_setting"] ,today_date())

      else :
         y = value.tail(1)['Date'].values[0] == today_date()

         if y == False:
            file_manager.daily_file_row_add(x["daily"] , x["system_setting"] , today_date())
            update_phase_target()

def habit_update():
   df = file_manager.load_data(x["daily"])
   js = file_manager.load_data(x["habit_data"])

   col = df.columns

   today = df[df['Date'] == today_date()]
   today = today.iloc[0]

   dict = {}

   for i in col :

      currentval = today[i]
      habittype = js["daily_habit"].get(i, None)

      if isinstance(currentval, float) and np.isnan(currentval):
           currentval = None

      dict[i] = {
         "current_val": currentval,
         "habit_type": habittype 
      }
      
   return dict

def updated_habit_js(json_data , file_path):

   if isinstance(json_data, str):
        json_data = json.loads(json_data)

   df = pd.DataFrame([json_data])

   df = df.where(pd.notna(df), "None")

   todaydate = today_date()

   value = file_manager.updated_habit_to_csv(df , file_path , todaydate)

   if value :
      return True
   
def get_phase_target_habit():
    json_file = file_manager.load_data(x["habit_data"])

    daily_habit = json_file.get("daily_habit", {})

    time_based_habits = [key for key, value in daily_habit.items() if value.lower() == "time"]
    numeric_habits = [key for key, value in daily_habit.items() if "numeric value" in value.lower()]

    return time_based_habits, numeric_habits

def update_phase_target_list():
   data = file_manager.load_data(x['habit_data'])

   habit_target = data['phase_target']
   habit_type = data['daily_habit']

   return habit_target , habit_type

def update_phase_target():
   file_manager.phase_target_update_row(today_date())

def check_correct_todo_phase(todo , selected_phase):

   todo = todo.split("\n")
   new_todo = []

   for t in todo:
      t = t.strip()
      if t:
        new_todo.append(t)

   l = len(new_todo)

   if l == 10:
      add_phase_todo(new_todo , selected_phase)
      return True
   
   else:
      return False

   
def add_phase_todo(todos , phase):

   phase = int(phase[-1])

   phases_todo = file_manager.load_data(x["phases_todos"])
   system_setting = file_manager.load_data(x["system_setting"])

   empty = file_manager.is_file_empty(x["phases_todos"])
   current_phase = system_setting['current']['current_phase']
   Phase = 0

   if phase == current_phase:
      Phase = current_phase
   
   else:
      Phase = current_phase + 1

   if empty:
      task_id = 1
      Day = 0

   else:
      last_task = phases_todo.iloc[-1]
      task_id = last_task["Task ID"] + 1
      Day = 0

   todolist = []

   for day in todos:
    Day += 1
    day = day.split(",")

    for task in day:
      task = task.strip()

      if task:
        todolist.append({
            "Phase": Phase,
            "Day": Day,
            "Task ID": task_id, 
            "Task": task,  
            "Completed": False
        })
      task_id += 1

   file_manager.save_to_csv_append(todolist , x["phases_todos"])

def is_valid_string(s):
    
    if '\n' in s:
        return "Contains multiple lines."
    
    elif ',' in s:
        return "Contains commas."
    
    elif len(s) > 20:
        return "Exceeds 20 characters."
    
    return True

def edit_phase_todo(task , phase , day):

   phases_todo = file_manager.load_data(x["phases_todos"])

   last_row = phases_todo.iloc[-1]
   task_id = last_row["Task ID"] + 1

   phase = int(phase[-1])

   tolist = []

   valid = is_valid_string(task)

   if valid:
      task.strip()
      tolist.append({
         "Phase" : phase,
         "Day" : day,
         "Task ID" : task_id,
         "Task Description" : task,
         "Completed" : False })
   
   value = file_manager.save_to_csv_append(tolist , x["phases_todos"])

   return value

def filter_phase_todo():

   df = file_manager.load_data(x["phases_todos"])
   settings = file_manager.load_data(x["system_setting"])

   phase = settings['current']['current_phase']

   data = df[df["Phase"] == phase]

   unique_days = data['Day'].unique()

   return data , unique_days

def save_phase_todos(data):

   df = file_manager.load_data(x["phases_todos"])
   
   for task_id , status in data.items():
        df.loc[df["Task ID"] == task_id, "Completed"] = status

   file_manager.save_to_csv_update(df , x["phases_todos"])

   return True 

def check_subject_exist(subject):
   habit_data = file_manager.load_data(x["habit_data"])

   habit_data.setdefault("subject_data", {})

   if subject in habit_data["subject_data"].keys():
      return False
   
   else: 
      value = save_subject_topic(subject)
      return value
   
def check_topic_exist(subject , topic):
   save_subject_topic(subject)
   habit_data = file_manager.load_data(x["habit_data"])

   if topic in habit_data['subject_data'][subject]:
      return False

   else :
      value = save_subject_topic(subject , topic)
      return value   

def save_subject_topic(new_subject, topics=None):
   habit_data = file_manager.load_data(x["habit_data"])

   habit_data.setdefault("subject_data", {})
   habit_data["subject_data"].setdefault(new_subject, [])

   if topics:
      if isinstance(topics, list):
            habit_data["subject_data"][new_subject].extend(topics)
      else:
            habit_data["subject_data"][new_subject].append(topics)

   file_manager.save_to_json(habit_data, x["habit_data"])

   return True


def subject_list():
   habit_data = file_manager.load_data(x["habit_data"])

   if "subject_data" in habit_data:
        return list(habit_data["subject_data"].keys())

   return []

def is_valid_topic_subject(s):

   if not s.strip():
      return "Cannot be empty."
    
   if '\n' in s:
      return "Contains multiple lines."
    
   if ',' in s:
      return "Contains commas."
    
   if len(s) > 60:
      return "Exceeds 60 characters."
    
   return True

def topic_list(subject):

   habit_data = file_manager.load_data(x["habit_data"])

   topic_list = habit_data['subject_data'][subject]


   if len(topic_list) == 0:
      topic_list.insert(0 , "Independent from topic")
      return topic_list

   else:
      return topic_list 
   
def calculate_next_review_day (difficulty_status , date_to_review , current_day , review_count = 1 ):
   
   if difficulty_status == 'Hard':
      return math.ceil(current_day + 1 + (review_count**1.75)) , review_count + 1

   elif difficulty_status == 'Medium':
      return math.ceil(current_day + 2 + (review_count**1.9)) , review_count + 1

   elif difficulty_status == 'Easy':
      return math.ceil(current_day + 3 + (review_count**2)) , review_count + 1

   elif difficulty_status == "Mastered":
      today = today_date()

      today = datetime.strptime(today, "%Y-%m-%d").date()
      difference = (date_to_review - today).days

      return current_day + difference ,  review_count + 1
   
   else:
      return 0 , review_count

def add_new_topic_review(subject , topic, difficulty_status , date_to_review , sub_topic , note):
   setting = file_manager.load_data(x['system_setting'])
   spaced_repetation = file_manager.load_data(x["spaced_repetition"])

   current_day = setting['current']['overall_current_day']

   empty = file_manager.is_file_empty(x["spaced_repetition"])

   if empty:
      unique_id = 1

   else:
      unique_id = spaced_repetation['Unique ID'].max() + 1

   next_review_day , review_count= calculate_next_review_day(difficulty_status , date_to_review , current_day)

   new_row = []

   new_row.append({
      "Unique ID" : unique_id ,
      "Subject" : subject,
      "Topic" : topic,
      "Sub Topic" : sub_topic,
      "Difficulty Status" : difficulty_status,
      "Next Revision" : next_review_day,
      "Review Count" : review_count,
      "Note" : note
   })

   value = file_manager.save_to_csv_append(new_row , x["spaced_repetition"])

   return value
   
   

