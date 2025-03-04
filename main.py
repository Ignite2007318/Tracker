import file_manager
import backend
import pandas
import numpy
import streamlit as st
file_manager.check_data_folder()
morning , afternoon , evening , daily , phaseprogress , xprewards , todos , spacedrepetition , habitdata = file_manager.load_files()

st.sidebar.title('Tracker')
st.sidebar.header("Navigation")
page = st.sidebar.radio("Pages", ["Add Habit"], key="sidebar_radio")

if page == "Add Habit":
    st.title("Add Habit")
    st.write("Welcome : ")

    col1 , col2 , col3 = st.columns(3)
    
    with col1 :
        new_habit = st.text_input(
            'Write new habit' , placeholder="Add a habit to enable the save button"
            )

    with col2:
        day_time = st.selectbox(
            "Select you'r preference" ,
            ('Morning' , 'Afternoon' , 'Evening' , 'Full Day')
        )

    with col3:
        habit_type = st.selectbox(
            "Select habit type",
            ('Yes/No' , 'Range from 1 to 10' , 'Numeric value')
        )

    clicked = st.button("Save Habit", disabled=not new_habit.strip())
    if clicked:
        x = backend.add_habit_filter(new_habit , day_time , habit_type)
        if x == True:
            st.success("✅ Habit added successfully!")

        else :
            st.warning(x)


















