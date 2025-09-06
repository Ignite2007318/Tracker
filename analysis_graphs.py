import pandas as pd
import numpy as np
import json
import file_manager
from datetime import datetime, timedelta
import plotly.express as px
import math

x = file_manager.files_name()

def info_df():

    df = file_manager.load_data(x['daily'])

    df["Overall Day"] = (df["Phase"] - 1) * 10 + df["Day"]

    df["Cumulative Study Time"] = df["Study Time"].fillna(0).cumsum()

    df["Total Study Time (Hours)"] = df["Cumulative Study Time"] / 60

    df["Avg Study Time (min)"] = df["Cumulative Study Time"] / df["Overall Day"]

    df["Avg Study Time Hours"] = (df['Avg Study Time (min)'] / 60).round(2)

    df["Exp Avg Study Time (Hours)"] = (
            df["Study Time"]
            .fillna(0)
            .ewm(span=7, adjust=False)
            .mean() / 60
        ).round(2)

    new_df = df[[
        "Phase",
        "Day",
        "Overall Day",
        "Study Time",
        "Cumulative Study Time",
        "Total Study Time (Hours)",
        "Avg Study Time (min)",
        "Avg Study Time Hours",
        "Exp Avg Study Time (Hours)"
    ]]

    return new_df

def graph_beautify_legend_horizontal(fig, x_title, y_title):

    fig.update_layout(
        title_font_size=24,
        title_font_family="Arial",
        xaxis_title=x_title,
        yaxis_title=y_title,
        xaxis=dict(tickmode="linear", tick0=1, dtick=1),
        font=dict(color="white", size=14),
        hovermode="x unified",
        legend=dict(
            title="",
            orientation="h",
        )
    )
    return fig

def graph_beautify_legend_vertical(fig, x_title, y_title):

    fig.update_layout(
        title_font_size=24,
        title_font_family="Arial",
        xaxis_title=x_title,
        yaxis_title=y_title,
        xaxis=dict(tickmode="linear", tick0=1, dtick=1),
        font=dict(color="white", size=14),
        hovermode="x unified",
        legend=dict(
            title="",
            orientation="v",
        )
    )
    return fig

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

    if yes_no_count == 0:
        yes_no_count = 100

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

    if "habit_target_completion" in habit_data:
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
    
    else :
        return False

def average_study_hours_every_phase():
    daily = file_manager.load_data(x['daily'])

    daily = daily[['Day', 'Study Time']].dropna()

    daily = daily.groupby('Day').mean().reset_index()

    daily['Study Time Num'] = daily['Study Time'].fillna(0)

    daily['Formatted Time'] = daily['Study Time Num'].apply(convert_to_hours_minutes)

    bar_chart = px.bar(
        daily,
        x='Day',
        y='Study Time Num',
        text='Formatted Time',
        title='Average Study Time per Day for all Phase',
        color='Day'
    )
    
    return bar_chart

def convert_to_hours_minutes(mins):
    if pd.isna(mins):
        return "0h 0m"
    hours = int(mins) // 60
    minutes = int(mins) % 60
    return f"{hours}h {minutes}m"

def avg_study_time_over_the_period():

    df_plot = info_df()

    df_melted = df_plot.melt(
        id_vars=["Overall Day"],
        value_vars=["Avg Study Time Hours", "Exp Avg Study Time (Hours)"],
        var_name="Metric",
        value_name="Study Hours"
    )

    fig = px.line(
        df_melted,
        x="Overall Day",
        y="Study Hours",
        color="Metric",
        title="Average vs Exponential Study Time (Hours)",
        markers=True,
        line_shape="spline",
        template="plotly_dark"
    )

    graph = graph_beautify_legend_horizontal(fig , "Days" , "Study Time (Hours)")

    return graph

def total_study_time_line_chart():
    new_df = info_df()

    fig = px.line(new_df,
              "Overall Day",
              "Total Study Time (Hours)",
              title = "Total Study Time",
              markers = True,
              line_shape = "spline",
              template="plotly_dark")
    
    fig = graph_beautify_legend_horizontal(fig , "Days" , "Total Study Time (Hours)")

    return fig

def cust_single_plot_graph():
    habit_data = file_manager.load_data(x['habit_data'])

    single = {}

    for i in habit_data['customize_habits']['single_habit_setup'].values():
        habit = i['habit']
        habit_type = i['type']

        if habit_type == "Time" or habit_type == "Numeric value":
            responce = cust_single_habit_df(habit , habit_type , single)

    return responce

def cust_single_habit_df(habit, habit_type , single):
    daily_df = file_manager.load_data(x['daily'])
    temp_df = daily_df[['Phase', 'Day', habit]].copy()
    temp_df['Overall Day'] = ((temp_df["Phase"] - 1) * 10) + temp_df['Day']

    temp_df['Total Till Day'] = temp_df[habit].fillna(0).cumsum()

    if habit_type == "Time":
        temp_df['Total Till Day'] = temp_df['Total Till Day'] / 60
        temp_df[habit] = temp_df[habit] / 60

    temp_df["Avg"] = (temp_df['Total Till Day'] / temp_df["Overall Day"]).round(2)
    temp_df["Exp Avg"] = (temp_df[habit].ewm(span=7, adjust=False).mean()).round(2)

    response = cust_single_plot_avg_vs_expo(temp_df, habit , habit_type , single)
    return response

def cust_single_plot_avg_vs_expo(temp_df , habit , habit_type , single):

    temp_df_melted = temp_df.melt(id_vars = ['Overall Day'],
                                    value_vars = ["Avg" , "Exp Avg"],
                                    var_name = "Metric",
                                    value_name = "Value"
                    )

    fig1 = px.line(temp_df_melted,
                    x = "Overall Day",
                    y = "Value", color="Metric",
                    title = f"Avg vs Exponential Avg of {habit}",
                    markers=True,
                    line_shape="spline",
                    template="plotly_dark"
            )

    if habit_type == "Time":
        fig1 = graph_beautify_legend_horizontal(fig1,"Days","Hours")

    else:
        fig1 = graph_beautify_legend_horizontal(fig1 , "Days" , f"Avg of {habit}")

    single[habit] = {"Avg vs Expo" : fig1}

    return single