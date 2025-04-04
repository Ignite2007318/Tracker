# streamlit run main.py
import file_manager
import backend
import pandas
import numpy as np
import streamlit as st
from datetime import time

st.set_page_config(layout="wide")

x = file_manager.files_name()
file_manager.check_data_folder()
backend.daily_row_add()
backend.revised_today_update()

st.sidebar.title('Tracker')
st.sidebar.header("Navigation")
page = st.sidebar.radio("Pages", ["Add Habit" , "Habit Update" , "Phase Target" , "Default" ,
                                    "Update Phase Target" , "Phase Todo's" , "Spaced Repetition" ] , key = "sidebar_radio")

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

    new_habit = new_habit.strip()
    clicked = st.button("Save Habit", disabled=not new_habit)
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
        
            if isinstance(current_val, (int, float)):
                display_time = time(int(current_val // 60), int(current_val % 60))  
            else:
                display_time = time(0, 0)

            input_time = st.time_input(f"{habit} (Time)", value=display_time)

            user_inputs[habit] = input_time.hour * 60 + input_time.minute

    clicked = st.button("Save")

    if clicked :
        value = backend.updated_habit_js(user_inputs , x['daily'])

        if value == True:
            backend.update_phase_target()
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

if page == "Phase Target":
    st.header("Phase Target")

    time_based_habits , numeric_habits = backend.get_phase_target_habit()

    current_habit = st.selectbox("Select a Habit",time_based_habits + numeric_habits)

    if current_habit in time_based_habits:
       value =  st.number_input("Time in Hours" , min_value= 0 , step=1)
       st.write("Habit : {} , Target : {} Hours".format(current_habit , value))
       value *= 60

    else :
        value =  st.number_input("Enter a Numeric Value" , min_value= 0.0 , step= 0.1)
        st.write("Habit : {} , Target : {}".format(current_habit , value))

    clicked = st.button("Save")

    if clicked == True:
        value = file_manager.add_new_phase_target(current_habit , value)

        if value:
            st.success("Succesfully Added")
        else:
            st.warning("Target Already Exist")

if page == "Update Phase Target":
    st.header("Update Phase Target")

    habit_target , habit_type = backend.update_phase_target_list()

    selected_habit = st.selectbox("Select a Target to Update", options=list(habit_target.keys()))

    value = habit_type[selected_habit]
    default_value = habit_target[selected_habit]
    
    if value == "Time":
        new_input = st.number_input("Enter New Target In Hours(Current Target is Given as default)" , min_value = 0 , step=1 , value=default_value//60)
        st.text("Habit to update : {} | New Target : {} Hours".format(selected_habit , new_input))
        new_input *= 60

    else:
        new_input = st.number_input("Enter New Target(Current Target is Given as default)" , min_value = 0.0 , step=0.1 , value=default_value)
        st.text("Habit to update : {} | New Target : {}".format(selected_habit , new_input))

    clicked = st.button("Save")

    if clicked == True:
        value = file_manager.update_new_phase_target(selected_habit , new_input)

        if value :
            st.success("New Target Updated")

if page == "Phase Todo's":
    system_setting = file_manager.load_data(x["system_setting"])
    current = system_setting['current']['current_phase']


    selected_value = st.sidebar.radio("Select Mode" , ["Phase Mode" , "Edit Mode" , "Update Completed Todo"])

    if selected_value == "Phase Mode":

        st.title('Phase Mode')

        todos = st.text_area("Enter You'r Phase Todos")
        selected_phase = st.radio("Saving For", [f"Current Phase = {current}" , f"For Next Phase = {current+1}"])

        clicked = st.button("Save")

        if clicked:
            x = backend.check_correct_todo_phase(todos , selected_phase)
            if x:
                st.success("Todo's are updated successfully")
            else:
                st.warning("There are not 10 days")
    
    if selected_value == "Edit Mode":

        st.title("Edit Mode")

        col1 , col2 , col3 = st.columns(3)
        
        with col1:
            task = st.text_input("Enter a Task")
        
        with col2:
            selected_phase = st.radio("Saving For", [f"Current Phase = {current}" , f"For Next Phase = {current+1}"])

        with col3:
            array = np.arange(1,11).tolist()
            day = st.selectbox('Select a day' , array)

        x = backend.is_valid_string(task)

        if x != True:
            st.warning(x)

        else:
            clicked = st.button('Save')

            if clicked:
              z = backend.edit_phase_todo(task , selected_phase , day)

              if z:
                 st.success("Added Successfully")

    if selected_value == "Update Completed Todo":

        st.title('Update Phase Todo')
        
        data, unique_days = backend.filter_phase_todo()

        updated_completion_status = {}

        for i in range(0, len(unique_days), 3):
            cols = st.columns(3)
        
            for j in range(3):
                if i + j < len(unique_days):

                    day = unique_days[i + j]
                    task_row = data[data['Day'] == day]

                    with cols[j]:
                        st.subheader(f"Day {day}")

                        for index, row in task_row.iterrows():
                            checked = st.checkbox(f"{row['Task Description']}", 
                                                        value=row["Completed"], 
                                                        key=row["Task ID"])
                            updated_completion_status[row["Task ID"]] = checked

            st.markdown("---")

        clicked = st.button("Save")

        if clicked:
            value = backend.save_phase_todos(updated_completion_status)
            
            if value:
                st.success('Saved Successfully')

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None

if page == "Spaced Repetition":

    selected_value = st.sidebar.radio('Select Page' , ['Add Subject & Topic' , 'Add for review' , "Today's Reviews"])

    if selected_value == 'Add Subject & Topic':

        st.header("Add Subject & Topic")

        col1 , col2  = st.columns(2)

        with col1:
            subject = st.text_input("Enter The Subject")

            clicked = st.button('Save' , key=1)

            if clicked:
                    x = backend.is_valid_topic_subject(subject)

                    if x != True:
                        st.warning(x)

                    else:
                        value = backend.check_subject_exist(subject)

                        if value:
                            st.success("Added")
                        
                        else:
                            st.warning("Subject already exist")

        with col2 :
            subject_list = backend.subject_list()

            if "Independent Topic" in subject_list:
                pass

            else:
                subject_list.insert(0,'Independent Topic')

            subject = st.selectbox("Select a Subject" , subject_list)
        
            topic = st.text_input("Enter The Topic")

            clicked = st.button('Save' , key=2)

            if clicked:
                    x = backend.is_valid_topic_subject(topic)

                    if x != True:
                        st.warning(x)

                    else:
                        value = backend.check_topic_exist(subject , topic)

                        if value:
                            st.success("Added")

                        else:
                            st.warning('Topic alredy exist')
    
    if selected_value == 'Add for review':
        st.header('Add for review')

        col1 , col2 , col3 = st.columns(3)

        value = backend.subject_list()

        if len(value) > 0:
                with col1:
                    subject = st.selectbox("Select a subject" , value)

                with col2:
                    topic_list = backend.topic_list(subject)
                    topic = st.selectbox("Select a topic" , topic_list)

                with col3:
                    opt = ["Need Practice" , "Hard" , "Medium" , "Easy" , "Mastered" , "No need to review again"]
                    difficulty_status = st.selectbox("Select current difficulty status" , opt)

                    if difficulty_status == "Mastered":
                        date_to_review = st.date_input('Enter date to review again')

                    else :
                        date_to_review = 0
                    
                col4 , col5 = st.columns(2)
                
                with col4:
                    sub_topic = st.text_input("Enter sub topic", value = "No Subtopic")

                    valid_subtopic = backend.is_valid_topic_subject(sub_topic)

                    if valid_subtopic != True:
                        st.warning(valid_subtopic)

                    else: 
                        clicked = st.button('Save')
                        
                with col5:
                    note = st.text_area('Additional Notes' , max_chars= 1000)
                
                if clicked :
                    value = backend.add_new_topic_review(subject , topic , difficulty_status , date_to_review , sub_topic , note)

                    st.success('Saved')

        else:
            st.error("No subjects available. Please add a subject first!")

    if selected_value == "Today's Reviews":
        topics , df , revised_list = backend.revise_topic_list()

        if st.session_state.selected_topic:
            u_id = st.session_state.selected_topic
            df = df[df['Unique ID'] == u_id]
            note = df['Note'].iloc[0]
            
            topic_title = next((key for key, value in topics.items() if value == u_id), None)
            
            st.title(f"Review : {topic_title}")

            col1 , col2 , col3 = st.columns(3)

            with col1:
                col4 , col5 = st.columns(2)

                with col4:
                    total_revieww_count = df['Review Count'].iloc[0]
                    st.metric("Review Count" , total_revieww_count)

                with col5:
                    next_review = df['Next Revision'].iloc[0]
                    st.metric("Next Review" , f"Day : {next_review}")
                
            with col2:
                st.subheader("Note")

                if isinstance(note, float) and np.isnan(note):
                       note = ""
                else:
                    note = str(note)

                if "edit_note" not in st.session_state:
                    st.session_state.edit_note = False

                if st.session_state.edit_note:
                    new_note = st.text_area("Edit Note", note, height=150, max_chars=1000)
                    note = new_note
                    
                else:

                    if note.strip() == "":
                        st.info("No notes yet. Click below to add one.")

                    else:
                        st.write(note)

                    if st.button("Edit Note"):
                        st.session_state.edit_note = True
                        st.rerun()

            with col3:
                opt = ["Need Practice" , "Hard" , "Medium" , "Easy" , "Mastered" , "No need to review again"]
                option = ['Yes Reviewed' , 'Not Reviewed']

                val = df[df['Unique ID'] == u_id]['Difficulty Status'].iloc[0]
                index_pos = opt.index(val)

                difficulty_status = st.selectbox('Select current difficulty status' , opt , index = index_pos)

                if difficulty_status == 'Mastered':
                    today = backend.today_date()
                    next_review_day = st.date_input('Enter next review day' , min_value= today)

                else:
                    next_review_day = 0

                if u_id not in revised_list:
                    val = 1

                else :
                    val = 0

                reviewed = st.radio("Reviewed" , option , val)

                if st.button('Save Changes'):
                    backend.spaced_review_changes(df , difficulty_status , next_review_day , reviewed , u_id , note)
                    st.session_state.edit_note = False
                    st.rerun()


            if st.button("Back to Topic List"):
                    st.session_state.selected_topic = None 
                    st.rerun()

        else:
            st.title("Today's Topics to Review")

            for topic in topics:
                num = topics[topic]
                if st.button(topic , key = num):
                    st.session_state.selected_topic = num
                    st.rerun()
