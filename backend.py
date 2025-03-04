import pandas as pd
import numpy as np
import json 
import main
import file_manager


morning_file_path = "data/morning.csv"
evening_file_path = "data/evening.csv"
afternoon_file_path = "data/afternoon.csv"
habit_data_file_path = "data/habit_data.json"



def add_habit_filter(new_habit, day_time, habit_type):
    if day_time == 'Morning':
        value = file_manager.add_new_habit(morning_file_path, habit_data_file_path, day_time, new_habit, habit_type)

        if value == False:
            return "Habit already exist"
        
        else :
            return True
        
    elif day_time == 'Afternoon':
        value = file_manager.add_new_habit(afternoon_file_path, habit_data_file_path, day_time, new_habit, habit_type)

        if value == False:
            return "Habit already exist"
        
        else :
            return True

    elif day_time == 'Evening':
        value = file_manager.add_new_habit(evening_file_path, habit_data_file_path, day_time, new_habit, habit_type)

        if value == False:
            return "Habit already exist"
        
        else :
            return True

    else:
        results = {
            "Morning": file_manager.add_new_habit(morning_file_path, habit_data_file_path, "Morning", new_habit, habit_type),
            "Afternoon": file_manager.add_new_habit(afternoon_file_path, habit_data_file_path, "Afternoon", new_habit, habit_type),
            "Evening": file_manager.add_new_habit(evening_file_path, habit_data_file_path, "Evening", new_habit, habit_type),
        }

        if all(results.values()):
            return True

        else:
            failed_files = [key for key, value in results.items() if not value]
            return f"Failed to add habit in: {', '.join(failed_files)} (Already exists)"


