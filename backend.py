import pandas as pd
import numpy as np
import json 
import file_manager
import datetime as dt  

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
     "Wake up time": "Numeric value",
     "Sleep Quality": "Range from 1 to 10",
     "Exercise/Workout": "Yes/No",
     "Energy Levels": "Range from 1 to 10",
     "Focus Levels": "Range from 1 to 10",
     "Mental Exhaustion Level": "Range from 1 to 10",
     "Screen Time": "Numeric value",
     "Total Study Time": "Numeric value",
     "Mood": "Range from 1 to 10"
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
         

   
        



