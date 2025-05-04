import pandas as pd
import numpy as np
import json
import file_manager
from datetime import datetime, timedelta
import plotly.express as px
import file_manager
import math

x = file_manager.files_name()

def total_xp_chart():
    xp = file_manager.load_data(x['xp_points'])

    line_chart = px.line(
        xp,
        x = 'Date',
        y = 'Total XP Avl',
        color = 'Phase',
        title= "Total XP",
        text='Day',
        markers=True,
        line_shape='spline')
    
    line_chart.update_traces(textposition = 'bottom center')
    
    grp = xp.groupby('Day')

    grp = grp['XP Gained'].mean().reset_index()
    avg_xp = px.bar(grp,
            x = 'Day',
            y = 'XP Gained',
            color = 'Day',
            title = 'Average XP Gained per Day Across All Phases',
            text_auto=True,
            color_continuous_scale='Viridis')

    return line_chart , avg_xp

def habit_category_devision():
    habit_data = file_manager.load_data(x['habit_data'])

    yes_no = ['Phase', 'Day', 'Date']
    range__habit = ['Phase', 'Day', 'Date']
    time = ['Phase', 'Day', 'Date']
    numeric = ['Phase', 'Day', 'Date']

    for habit, habit_type in habit_data['daily_habit'].items():
        if habit_type == 'Time':
            time.append(habit)

        elif habit_type == 'Yes/No':
            yes_no.append(habit)

        elif habit_type == 'Range from 1 to 10':
            range__habit.append(habit)

        else:
            numeric.append(habit)

    return yes_no , range__habit , time , numeric

def yes_no_current_phase_donut():
    daily = file_manager.load_data(x['daily'])
    system_setting = file_manager.load_data(x['system_setting'])
    yes_no , range__habit , time , numeric = habit_category_devision()

    phase = system_setting['current']['current_phase']

    daily = daily[daily['Phase'] == phase]
    yes_no_df = daily[yes_no]
    yes_no_df_filtered = yes_no_df.drop(columns=['Day', 'Date'])

    yes_no_sum = int(yes_no_df_filtered.groupby('Phase').sum().sum().sum())

    yes_no_count = int(yes_no_df.count().drop(['Phase' , 'Day' , 'Date']).sum())

    labels = ['Yes', 'No']
    values = [yes_no_sum, yes_no_count - yes_no_sum]

    phase_donut = px.pie(
        names=labels,
        values=values,
        hole=0.6,
        title="Yes/No Habit Completion for current Phase",
        color=labels,
        color_discrete_map={'Yes': 'green', 'No': 'red'})
    
    return phase_donut

def phase_target_completion_chart():
    habit_data = file_manager.load_data(x['habit_data'])

    value = 0
    counter = 0

    for i in habit_data['habit_target_completion'].values():
        if i < 101:
            value += i
            counter += 1
        
        else:
            value += 100
            counter += 1
    
    completed = (value/counter)

    labels = ['Completed', 'Left or Not Completed']
    values = [completed, 100 - completed ]

    phase_target_donut = px.pie(
        names=labels,
        values=values,
        hole=0.6,
        title="Target Completion for current phase",
        color=labels,
        color_discrete_map={'Completed': 'green', 'Left or Not Completed': 'red'})
    
    return phase_target_donut

    

