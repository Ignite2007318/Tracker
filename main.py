import file_manager
import backend
import pandas
import numpy
import streamlit as st

st.set_page_config(layout="wide")

x = file_manager.files_name()
file_manager.check_data_folder()
backend.daily_row_add()
file_manager.replace_na(x["daily"])

st.sidebar.title('Tracker')
st.sidebar.header("Navigation")
page = st.sidebar.radio("Pages", ["Add Habit" , "Habit Update" ,  "Default" , "Phase Target"] , key = "sidebar_radio")

if page == "Add Habit":
    st.title("Add Habit")
    st.write("Welcome : ")

    col1 , col2 , col3 = st.columns(3)
    
    with col1 :
        new_habit = st.text_input(
            'Write new habit' , placeholder="Add a habit to enable the save button"
            )

    with col2:
        habit_type = st.selectbox(
            "Select habit type",
            ('Yes/No' , 'Range from 1 to 10' , 'Numeric value' , 'Time') 
        )

    clicked = st.button("Save Habit" , disabled=not new_habit.strip())
    if clicked:
        x = backend.add_habit_filter(new_habit , habit_type)
        if x == True:
            st.balloons()
            st.success("Habit added successfully!")

        else :
            st.warning(x)

if page == "Habit Update":
    st.title("Habit Update")
    dict = backend.habit_update()

    user_inputs = {}

    for habit, details in dict.items():
        current_val = details["current_val"]
        habit_type = details["habit_type"]

        if habit_type is None:
            st.write(f"**{habit}:** {current_val}")
            user_inputs[habit] = current_val

        elif habit_type == "Numeric value":
            user_inputs[habit] = st.number_input(
                f"{habit} (Numeric Value)", 
                value=0.0 if current_val is None else float(current_val), 
                step=0.1,
                format="%.2f"
            )

        elif habit_type == "Yes/No":
            user_inputs[habit] = st.selectbox(
                f"{habit} (Yes/No)", 
                options=[None, "Yes", "No"], 
                index=0 if current_val is None else ["Yes", "No"].index(current_val) + 1
            )

        elif "Range from 1 to 10" in habit_type:
            user_inputs[habit] = st.selectbox(
                f"{habit} (Range 1-10)", 
                options=[None] + list(range(1, 11)), 
                index=0 if current_val is None else list(range(1, 11)).index(current_val) + 1
            )
        
        elif habit_type == "Time":
            user_inputs[habit] = st.time_input(f"{habit} (Time)", value=current_val)

    col1 , col2 = st.columns(2)

    with col1:
        st.write("### Submitted Data")
        st.json(user_inputs)

    with col2:
        clicked = st.button("Save")

    if clicked :
        value = backend.updated_habit_js(user_inputs , x['daily'])

        if value == True:
            st.success("Successfully Added")


    

if page == "Default":
    user_name = st.text_input("Enter you'r name hare")

    st.header("Some Default Habits")
    col1 , col2 , col3 = st.columns(3)

    with col1:
     st.write("""
- *Wake up time* (Time)
- *Exercise/Workout* (Yes/No)""")
     
    with col2: 
        st.write("""
- Screen Time (Time)
- Study Time (Time)""")
        
    st.write("*These are the default habits for tracking*")

    clicked = st.button('Save Info')

    if clicked :
        backend.add_default(user_name)
        st.balloons()
        st.success(f"Have a wonderful journey, {user_name}")



















