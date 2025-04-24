# streamlit run main.py
import pandas as pd
import numpy as np
import json 
import file_manager
import datetime as dt
from datetime import datetime, date
import math

x = file_manager.files_name()

def some_basic_function():
   system_setting = file_manager.load_data(x["system_setting"])

   if "journey_starts" in system_setting:
      check_current_month()

      val = check_holiday()

      if val:
         daily_reward_reset()
         daily_row_add()
         revised_today_update()
         check_phase_change()
         phase_todo_xp()
         update_xp()
         return True

      else:
         return False

def check_holiday():
   habit_data = file_manager.load_data(x["habit_data"])

   today = today_date()

   if today in habit_data["holiday_list"]:
      return False
   
   else:
      return True
   
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
            yes_no_xp_gain()

def habit_update():
   df = file_manager.load_data(x["daily"])
   js = file_manager.load_data(x["habit_data"])

   col = df.columns

   val = file_manager.is_file_empty(x["daily"])

   if val :
      return False
   
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

   if 'phase_target' not in data:
      return False

   else:
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
            "Completed": False,
            "Get XP" : False
        })
      task_id += 1

   file_manager.save_to_csv_append(todolist , x["phases_todos"])

def is_valid_string(s):
    
    if '\n' in s:
        return "Contains multiple lines."
    
    elif ',' in s:
        return "Contains commas."
    
    elif len(s) > 60:
        return "Exceeds 60 characters."
    
    return True

def edit_phase_todo(task , phase , day):

   phases_todo = file_manager.load_data(x["phases_todos"])

   empty = file_manager.is_file_empty(x["phases_todos"])

   if empty:
      task_id = 1

   else:
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
         "Completed" : False,
         "Get XP" : False
      })
   
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

   if difficulty_status == 'Need Practice':
      return math.ceil(current_day + 0 + (review_count**1.3)) , review_count + 1
   
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

   next_review_day , review_count = calculate_next_review_day(difficulty_status , date_to_review , current_day)

   new_row = []

   new_row.append({
      "Unique ID" : unique_id,
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
   
def revised_today_update():
   habit_data = file_manager.load_data(x["habit_data"])
   system_setting = file_manager.load_data(x['system_setting'])
   spaced_repetation = file_manager.load_data(x["spaced_repetition"])

   overall_today = system_setting.get("current", {}).get("overall_current_day", 1)

   uid_list = spaced_repetation[spaced_repetation['Next Revision'] == overall_today]['Unique ID'].tolist()

   if "revised_today" not in habit_data:
      habit_data['revised_today'] = {}

      habit_data['revised_today']['today'] = today_date()
      habit_data['revised_today']['revised_u_id'] = []
      habit_data['revised_today']['need_to_revise_u_id'] = []

      file_manager.save_to_json(habit_data , x["habit_data"])

   if habit_data['revised_today']['today'] != today_date():
      space_repetation_xp()
      not_revised()

      habit_data['revised_today']['today'] = today_date()
      habit_data['revised_today']['revised_u_id'] = []
      habit_data['revised_today']['need_to_revise_u_id'] = uid_list

      file_manager.save_to_json(habit_data , x["habit_data"])

def revise_topic_list():

   spaced_repetition = file_manager.load_data(x["spaced_repetition"])
   habit_data = file_manager.load_data(x["habit_data"])

   if 'revised_today' not in habit_data:
      return False
   
   uid_list = habit_data["revised_today"]['need_to_revise_u_id']
   need_to_revise = habit_data["revised_today"]['revised_u_id']
   filtered_df = spaced_repetition[spaced_repetition['Unique ID'].isin(uid_list)]

   today_topic = dict(zip(
        (filtered_df['Subject'] + " - " + filtered_df['Topic'] + " - " + filtered_df['Sub Topic']).tolist(),
        filtered_df['Unique ID'].tolist()
    ))

   return today_topic , filtered_df , need_to_revise

def spaced_review_changes(df , difficulty_status , next_review_day , reviewed , u_id , note):
   habit_data = file_manager.load_data(x["habit_data"])
   spaced_repetation = file_manager.load_data(x["spaced_repetition"])
   system_setting = file_manager.load_data(x['system_setting'])

   index_row = spaced_repetation.index[spaced_repetation['Unique ID'] == u_id].tolist()
   index_row = index_row[0]

   review_count = df['Review Count'].iloc[0]
   overall_today = system_setting.get("current", {}).get("overall_current_day", 1)
   next_review_day , review_count= calculate_next_review_day(difficulty_status , next_review_day , overall_today , review_count)

   spaced_repetation.at[index_row, 'Difficulty Status'] = difficulty_status
   spaced_repetation.at[index_row, 'Note'] = note
   spaced_repetation.at[index_row, 'Next Revision'] = next_review_day

   if reviewed == "Yes Reviewed":
      if u_id not in habit_data['revised_today']['revised_u_id']:
         habit_data['revised_today']['revised_u_id'].append(u_id)

         file_manager.save_to_json(habit_data , x["habit_data"])
         spaced_repetation.at[index_row, 'Review Count'] = review_count

   file_manager.save_to_csv_update(spaced_repetation , x["spaced_repetition"])

def yes_no_xp_gain():
   system_setting = file_manager.load_data(x["system_setting"])
   daily = file_manager.load_data(x["daily"])
   habit_data = file_manager.load_data(x["habit_data"])
 
   phase = system_setting['current']['current_phase']
   day = system_setting['current']['current_day']
   today = today_date()

   row_to_calculate = daily.iloc[-2]

   val = file_manager.is_file_empty(x["xp_points"])

   if val:
      new_row = []

      new_row.append({
         "Phase" : phase,
         "Day" : day,
         "Date" : today,
         "XP Gained" : 0,
         "XP Used" : 0,
         "Total XP Avl" : 0
      })

      file_manager.save_to_csv_update(new_row , x['xp_points'])

   xp = file_manager.load_data(x["xp_points"])

   if str(xp.iloc[-1]['Date']) != str(today):
      
      today_row = []

      today_row.append({
         "Phase" : phase,
         "Day" : day,
         "Date" : today,
         "XP Gained" : 0,
         "XP Used" :0,
         "Total XP Avl":(xp['XP Gained'].sum()) - (xp['XP Used'].sum())
      })

      file_manager.save_to_csv_append(today_row , x["xp_points"])

   if "journey_starts" in system_setting:
      xp = file_manager.load_data(x["xp_points"])
      yes_no_habits = [key for key, value_type in habit_data['daily_habit'].items() if value_type == 'Yes/No']
      total_yes = (row_to_calculate[yes_no_habits] == 1).sum()

      if phase == 1 and day == 1:
         return False
      
      else:
            total_xp = total_yes * 5

            update_xp(total_xp)

def new_phase_target_completion(habit):
   habit_data = file_manager.load_data(x["habit_data"])

   if "habit_target_completion" not in habit_data:
      habit_data['habit_target_completion'] = {}

   if habit not in habit_data['habit_target_completion']:
      habit_data['habit_target_completion'][habit] = 0

   file_manager.save_to_json(habit_data , x["habit_data"])

def check_phase_change():
   daily = file_manager.load_data(x['daily'])
   system_setting = file_manager.load_data(x["system_setting"])

   if "last_reset_phase" not in system_setting["current"]:
      system_setting["current"]['last_reset_phase'] = 1
      file_manager.save_to_json(system_setting , x["system_setting"])

   else:
      if daily.shape[0] > 1:
         if daily.iloc[-1]['Phase'] != system_setting["current"]['last_reset_phase'] and daily.iloc[-1]['Day'] == 1:
            system_setting["current"]['last_reset_phase'] = system_setting["current"]['current_phase']
            reset_phase_target_completion()
            file_manager.save_to_json(system_setting , x["system_setting"])

def reset_phase_target_completion():
   habit_data = file_manager.load_data(x["habit_data"])

   if "habit_target_completion" in habit_data:
      for habit in habit_data['habit_target_completion']:
         habit_data['habit_target_completion'][habit] = 0

   file_manager.save_to_json(habit_data , x["habit_data"])

def phase_target_xp_gain():
   phase_target = file_manager.load_data(x["phase_target"])
   habit_data = file_manager.load_data(x['habit_data'])

   xp_target_list = phase_target.columns.tolist()[3:]
   last_row = phase_target.iloc[-1]

   total_xp = 0

   val = file_manager.is_file_empty(x["xp_points"])

   if val != True:

      for target in xp_target_list:
         value = last_row[target]
         overall_target = habit_data['phase_target'][target]

         if pd.isna(value):
            value = 0
      
         if overall_target == 0:
            overall_target = 1

         completion = int((value / overall_target) * 100)
         last_completion_rate = habit_data['habit_target_completion'][target]

         if last_completion_rate < 101:
            total_xp += ((completion - last_completion_rate) * 4)

         else:
            total_xp += ((completion - last_completion_rate) * 2)

         habit_data['habit_target_completion'][target] = completion
      file_manager.save_to_json(habit_data , x["habit_data"])

      update_xp(total_xp)

def phase_todo_xp():
   phase_todos = file_manager.load_data(x['phases_todos'])

   task_list = phase_todos[(phase_todos["Completed"] == True) & (phase_todos["Get XP"] == False)]['Task ID'].to_list()

   if len(task_list) > 0:

      for i in task_list:
         phase_todos.loc[phase_todos['Task ID'] == i, 'Get XP'] = True

      total_xp = (len(task_list) * 10)

      update_xp(total_xp)

      file_manager.save_to_csv_update(phase_todos , x["phases_todos"])

def update_xp(total_xp = 0 , used_xp = 0):
   xp = file_manager.load_data(x["xp_points"])
   system_setting = file_manager.load_data(x["system_setting"])

   phase = system_setting['current']['current_phase']
   day = system_setting['current']['current_day']

   val = file_manager.is_file_empty(x["xp_points"])

   if val != True:
      row = xp.iloc[-1]

      new_row = []

      new_row.append({
            "Phase" : int(row['Phase']),
            "Day" : int(row['Day']),
            "Date" : row['Date'],
            "XP Gained" : int(total_xp + row['XP Gained']),
            "XP Used" : int(row['XP Used'] + used_xp),
            "Total XP Avl": int((xp['XP Gained'].sum()) - (xp['XP Used'].sum()))
         })
   
      file_manager.update_last_row_in_csv(x['xp_points'] , new_row[0])

   else: 
      new_row = []

      new_row.append({
            "Phase" : phase,
            "Day" : day,
            "Date" : today_date(),
            "XP Gained" : 0,
            "XP Used" : 0,
            "Total XP Avl": int((xp['XP Gained'].sum()) - (xp['XP Used'].sum()))
         })
   
      file_manager.save_to_csv_append(new_row , x["xp_points"])

def space_repetation_xp():
   habit_data = file_manager.load_data(x["habit_data"])

   total_xp = len(habit_data["revised_today"]["revised_u_id"]) * 15
   update_xp(total_xp)

def not_revised():
   habit_data = file_manager.load_data(x["habit_data"])
   spaced_repetation = file_manager.load_data(x["spaced_repetition"])

   should = habit_data['revised_today']['need_to_revise_u_id']
   revised = habit_data['revised_today']['revised_u_id']

   u_id = np.setdiff1d(should , revised)
   
   if len(u_id) > 0:
      for i in u_id:
            index_row = spaced_repetation.index[spaced_repetation['Unique ID'] == i].tolist()
            index_row = index_row[0]

            spaced_repetation.at[index_row, 'Next Revision'] = (spaced_repetation.at[index_row, 'Next Revision'] + 3)

      total_xp = len(u_id) * (-10)
      update_xp(total_xp)
      file_manager.save_to_csv_update(spaced_repetation , x["spaced_repetition"])

def check_current_month():
   habit_data = file_manager.load_data(x["habit_data"])
   system_setting = file_manager.load_data(x["system_setting"])

   now = datetime.now()
   current_month = now.month

   if "current_month" not in system_setting:
     system_setting["current_month"] = current_month
     habit_data["holiday_list"] = []

     file_manager.save_to_json(system_setting , x['system_setting'])
     file_manager.save_to_json(habit_data , x["habit_data"])

   else:

      if system_setting["current_month"] == current_month:
         return 
      
      else :
         habit_data["holiday_list"] = []
         system_setting["current_month"] = current_month
         file_manager.save_to_json(habit_data , x['habit_data'])
         file_manager.save_to_json(system_setting , x['system_setting'])

def holiday_len():
   habit_data = file_manager.load_data(x['habit_data'])
   xp_points_avl = file_manager.load_data(x["xp_points"])

   if xp_points_avl.shape[0] > 0:
      total_xp = xp_points_avl.iloc[-1]["Total XP Avl"]

   else:
      total_xp = 0
   if 'holiday_list' not in habit_data:
      return False
   
   holiday_list = habit_data["holiday_list"]

   total_length = len(holiday_list)

   length =  4 - len(holiday_list)

   return length , holiday_list , total_xp , total_length

def save_holiday(holiday_list):
   habit_data = file_manager.load_data(x['habit_data'])
  
   holiday_list = [d.isoformat() for d in holiday_list]

   holiday = habit_data["holiday_list"]

   for i in holiday_list:
      holiday.append(i)

   unique_holiday = list(set(holiday))

   habit_data["holiday_list"] = unique_holiday

   file_manager.save_to_json(habit_data , x["habit_data"])

def add_new_reward(reward , reward_xp):
   habit_data = file_manager.load_data(x['habit_data'])

   if "reward" not in habit_data:
      habit_data["reward"] = {}

   
   habit_data["reward"][reward] = {}
   habit_data["reward"][reward]["Claimed"] = False
   habit_data["reward"][reward]["XP"] = reward_xp

   file_manager.save_to_json(habit_data , x["habit_data"])

def daily_reward_reset():
   daily = file_manager.load_data(x["daily"])
   habit_data = file_manager.load_data(x['habit_data'])

   if daily.shape[0] > 1:
      date_to_check = daily.iloc[-1]['Date']

      if date_to_check != today_date():
         for i in habit_data['reward']:
            habit_data['reward'][i]['Claimed'] = False
      
         file_manager.save_to_json(habit_data , x["habit_data"])

      else:
         pass

def unlock_reward_prerequisites():
   habit_data = file_manager.load_data(x["habit_data"])
   xp = file_manager.load_data(x["xp_points"])

   true_list = []
   false_dict = {}

   if 'reward' not in habit_data:
      return False
   
   for i in habit_data['reward']:

      if habit_data['reward'][i]['Claimed'] == True:
         true_list.append(i)

      else:
         false_dict[i] = habit_data['reward'][i]

   if xp.shape[0] > 0:
      total_xp = xp.iloc[-1]["Total XP Avl"]

   else:
      total_xp = 0
   
   if xp.shape[0] >= 2:
      xp_change = int(xp.iloc[-1]["Total XP Avl"]) - int(xp.iloc[-2]["Total XP Avl"])

   else:
      xp_change = 0

   holiday_list = habit_data["holiday_list"]

   return true_list , false_dict , total_xp , holiday_list , xp_change

def unlocked_reward(reward_list):
   habit_data = file_manager.load_data(x["habit_data"])

   for i in reward_list:
      habit_data['reward'][i]['Claimed'] = True

   file_manager.save_to_json(habit_data , x["habit_data"])

def update_reward_xp():
   habit_data = file_manager.load_data(x["habit_data"])

   reward_dict = {}
   if "reward" in habit_data:
      for i in habit_data['reward']:
         reward_dict[i] = habit_data['reward'][i]['XP']

   return reward_dict