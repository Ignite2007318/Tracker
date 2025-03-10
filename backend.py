import pandas as pd
import numpy as np
import json 
import main
import file_manager

x = file_manager.files_name()

def add_habit_filter(new_habit, day_time, habit_type):

    a = x["morning"]
    b = x["afternoon"]
    c = x["evening"]
    d = x["habit_data"]

    if day_time == 'Morning':
        value = file_manager.add_new_habit(a , d , day_time, new_habit, habit_type)

        if value == False:
            return "Habit already exist"
        
        else :
            return True
        
    elif day_time == 'Afternoon':
        value = file_manager.add_new_habit(b , d , day_time, new_habit, habit_type)

        if value == False:
            return "Habit already exist"
        
        else :
            return True

    elif day_time == 'Evening':
        value = file_manager.add_new_habit(c , d , day_time, new_habit, habit_type)

        if value == False:
            return "Habit already exist"
        
        else :
            return True

    else:
        results = {
            "Morning": file_manager.add_new_habit(a , d , "Morning", new_habit, habit_type),
            "Afternoon": file_manager.add_new_habit(b , d , "Afternoon", new_habit, habit_type),
            "Evening": file_manager.add_new_habit(c , d , "Evening", new_habit, habit_type),
        }

        if all(results.values()):
            return True

        else:
            failed_files = [key for key, value in results.items() if not value]
            return f"Failed to add habit in: {', '.join(failed_files)} (Already exists)"


