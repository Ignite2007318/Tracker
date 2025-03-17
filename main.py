import file_manager
import backend
import pandas
import numpy
import streamlit as st

st.set_page_config(layout="wide")

file_manager.check_data_folder()
backend.daily_row_add()

st.sidebar.title('Tracker')
st.sidebar.header("Navigation")
page = st.sidebar.radio("Pages", ["Add Habit" , "Default"] , key = "sidebar_radio")

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
            ('Yes/No' , 'Range from 1 to 10' , 'Numeric value')
        )

    clicked = st.button("Save Habit", disabled=not new_habit.strip())
    if clicked:
        x = backend.add_habit_filter(new_habit , habit_type)
        if x == True:
            st.balloons()
            st.success("✅ Habit added successfully!")

        else :
            st.warning(x)

if page == "Default":
    user_name = st.text_input("Enter you'r name hare")

    st.header("Some Default Habits")
    col1 , col2 , col3 = st.columns(3)

    with col1:
     st.write("""
- *Wake up time* (Numeric)
- *Sleep Quality* (Range 1-10)
- *Exercise/Workout* (Yes/No)""")
     
    with col2: 
        st.write("""
- *Energy Levels* (Range 1-10)
- *Focus Levels* (Range 1-10)
- *Mental Exhaustion Level* (Range 1-10) """)
         
    with col3:
        st.write("""
- *Screen Time* (Minutes/Hours, Numeric)
- *Total Study Time (minutes)* (Numeric)
- *Mood* (Range 1-10)""")
        
    st.write("💡 *These are the default habits for tracking daily performance and productivity!*")

    clicked = st.button('Save Info')

    if clicked :
        backend.add_default(user_name)
        st.balloons()
        st.success(f"Have a wonderful journey, {user_name}")

















