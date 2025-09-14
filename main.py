#           streamlit run main.py

#           .\setup.bat

import file_manager
import backend
import pandas
import numpy as np
import streamlit as st
from datetime import time , date , timedelta
import time as t
import analysis_graphs as graph


st.set_page_config(page_title="Tracker" , layout="wide")

x = file_manager.files_name()
file_manager.check_data_folder()
holiday_val = backend.some_basic_function()

st.sidebar.title('Tracker')
page = st.sidebar.radio("Navigation", ["Dashboard", "Graphs and Analysis", "Add Habit", "Habit Update", "Phase Target",
                                     "Phase Todo's", "Spaced Repetition", "XP and Reward", "Default"], key="sidebar_radio")


if page == "Dashboard":
    val = backend.check_journey_start()

    if val == False:
        st.warning("Head to the 'Default Page' (last option in the sidebar) and enter your name to begin your journey!")
        st.stop()

    st.header('Dashboard')

    val = backend.check_holiday()
    phase , day , date , total_xp , xp_gained , xp_used , total_xp_change = backend.basic_initials()

    if val == False:
        st.warning("Today's a holiday! 🫡 Rest up!")
        
    col1, col2 , col3 = st.columns(3)

    with col1:
        st.markdown(f"**Phase:** {phase}")
        st.markdown(f"**Day:** {day}")
        st.markdown(f"**Date:** {date}")

    with col2:
        st.metric(label="Total XP", value=total_xp , delta= total_xp_change)
        
    with col3:
        st.markdown(f"**XP Gained Today:** {xp_gained}")
        st.markdown(f"**XP Used Today:** {xp_used}")

    st.markdown('---')

    col1 , col2 , col3 = st.columns(3)

    with col1:
        st.subheader("Today's Tasks")

        task = backend.dashboard_today_todos()
        val = file_manager.is_file_empty(x['phases_todos'])

        if val == True or task.empty:
            st.info("No tasks for today. Go to the Phase Todos page and add some first!")

        else:
             
            updated_completion_status_today = {}
            for index, row in task.iterrows():
                checked = st.checkbox(f"{row['Task Description']}", 
                                        value=row["Completed"], 
                                        key=row["Task ID"])
                updated_completion_status_today[row["Task ID"]] = checked

            if st.button('Save'):
                backend.save_phase_todos(updated_completion_status_today)
                st.success('Saved Successfully')
                t.sleep(1)
                st.rerun()

    with col2:
        st.subheader("Topics to review today")
        today_topic , revised_today , need_to_revise_today = backend.dashboard_spaced_rep()
        val = file_manager.is_file_empty(x['spaced_repetition'])

        if val :
            st.info("No revisions available. Please go to the Spaced Repetition page and add some first.")

        elif len(need_to_revise_today) == 0 :
            st.info('No revision scheduled today')

        else:
            
            data = []
            for topic , id_task in today_topic.items():

                key_unique = f"revise_{id_task}_{topic}"

                if id_task in revised_today:
                    value = True

                else:
                    value = False

                checked = st.checkbox(topic , value = value , key = key_unique)

                if checked :
                    data.append(id_task)
            
            if st.button('Save' , key= 'Space Rep Save'):
                backend.spaced_rep_save(data)
                st.success('Saved')
                t.sleep(1)
                st.rerun()
        
    with col3:
        false_list , true_list = backend.quick_task_list()

        st.subheader('Quick Task')

        if len(false_list) == 0 and len(true_list) == 0:
             st.info('No tasks available. Please add some using the quick task section below.')

        if len(true_list) > 0:
            st.subheader("Completed")

            for i in true_list:
                text = "✅ {}".format(i)
                st.text(text)

        if len(false_list) > 0:
            st.subheader('Incomplete')
            completed_list = []

            counter = 100
            for i in false_list:
                checked = st.checkbox(i , key = counter)
                counter += 1

                if checked:
                    completed_list.append(i)
                
            if st.button('Save' , key = "Save completed"):
                backend.quick_task_save_completed(completed_list)
                st.success('Saved')
                t.sleep(1)
                st.rerun()

        if len(true_list) > 0 and len(false_list) == 0: 
             st.info("No Quick Tasks available or all tasks have been completed for today.")

    st.markdown("---")

    col1 , col2 = st.columns(2)

    with col1:
        st.subheader('Quick Task (Today Only)')

        task = st.text_input("Enter tasks separated by commas:")

        if st.button('Save' , key = "Quick Task Add"):
            if task:
                backend.quick_task_add(task)
                st.success('Saved')
                t.sleep(1)
                st.rerun()

            else:
                st.warning("Empty Task")
                t.sleep(1)
                st.rerun()
                
if page == 'Graphs and Analysis':
    val = backend.check_journey_start()

    if val == False:
        st.warning("Head to the 'Default Page' (last option in the sidebar) and enter your name to begin your journey!")
        st.stop()

    graph_page = st.sidebar.radio("Navigation", ["Default Graphs" , "Customizable Graphs" , "Have Some Fun"] , key = "graphs_sidebar")

    if graph_page == "Default Graphs":
        st.header('Default Graphs')

        col1 , col2 , col3 = st.columns(3)

        phase , day , date , total_xp , xp_gained , xp_used , total_xp_change = backend.basic_initials()
        
        with col1:
            st.markdown(f"**Phase:** {phase}")

        with col2:
            st.markdown(f"**Day:** {day}")

        with col3:
            st.metric(label="Total XP", value=total_xp , delta= total_xp_change)

        fig = graph.avg_study_time_over_the_period()

        st.plotly_chart(fig)

        total_study_graph = graph.total_study_time_line_chart()

        st.plotly_chart(total_study_graph)

        line_chart , avg_xp = graph.total_xp_chart()

        col1 , col2 = st.columns(2)

        with col1:
            st.plotly_chart(line_chart , use_container_width = True)

        with col2:
            st.plotly_chart(avg_xp , use_container_width = True)

        st.markdown("---")

        col1 , col2  = st.columns(2)

        with col1:
            fig1 = graph.yes_no_current_phase_donut()

            st.plotly_chart(fig1 , use_container_width=False)

        with col2:
            fig2 = graph.phase_target_completion_chart()

            if fig2:

                st.plotly_chart(fig2 , use_container_width=False)

            else: 
                st.info("Add Some Phase Target First Too See The Chart")

        st.markdown("---")

        col1 , col2 = st.columns(2)

        with col1:
            bar_chart = graph.average_study_hours_every_phase()

            st.plotly_chart(bar_chart)
    
    if graph_page == "Customizable Graphs":
        st.header("Customizable Graphs")

        habits = backend.fetch_habit()

        col1 , col2 , col3 = st.columns(3)
        with col1:
            graph_type = st.radio("Choose Graph Type", ["Single Habit", "Dual Habit" , "Triple Habit"], key="graph_type")

        with col2:
            if graph_type == "Single Habit":
                st.write("Select a habit and click 'Save' to view the analysis")
                single_selected_habit = st.selectbox("Choose a habit from the list",habits)

                if st.button('Save'):
                    x = backend.save_customize_analysis_habits(single_selected_habit)
                    st.info(x)

                    t.sleep(1)
                    st.rerun()
        
        if graph_type == "Single Habit":
            if backend.check_custom_analysis_exist():
                responce = graph.cust_single_plot_graph()

                for i in responce.values():
                    for j in i.values():
                        st.plotly_chart(j)
            
            else:
                st.info("Please Add some habits first")

        if graph_type == "Dual Habit":
            pass

        if graph_type == "Triple Habit":
            pass

    if graph_page == "Have Some Fun":
        st.header("Have Some Fun")
        st.write("Experiment Area Temporarily")

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

        t.sleep(1)
        st.rerun()

    val = backend.check_journey_start()

    if val == False:
        st.warning("Head to the 'Default Page' (last option in the sidebar) and enter your name to begin your journey!")
        st.stop()

    else:
        st.subheader("Already Added Habits")

        response = backend.fetch_habit()

        response = list(response)

        if len(response):
            for i, item in enumerate(response):
                st.write(int(i) + 1, item)

        else:
            st.info("No habits added yet. Try adding some!")

if page == "Habit Update":
    if holiday_val == False:
        st.warning("Today is a holiday. Habit tracking is disabled.")
        st.stop()

    val = backend.habit_update()

    if val == False:
        st.warning('Go to default and start the journey first')
        st.stop()

    st.title("Habit Update")

    responce = backend.habit_update()
    
    col_time, col_yesno, col_numeric, col_range = st.columns(4)
    user_inputs = {}

    for habit, details in responce.items():
        current_val = details["current_val"]
        habit_type = details["habit_type"]

        if habit_type is None:
            user_inputs[habit] = current_val

        if habit_type == "Numeric value":
            with col_numeric:
                user_inputs[habit] = st.number_input(
                    f"{habit} (Numeric Value)", 
                    value=0.0 if current_val is None else float(current_val), 
                    step=0.1,
                    format="%.2f"
                )

        if habit_type == "Yes/No":
            with col_yesno:
                if current_val == 1:
                    index_val = 0
                else:
                    index_val = 1

                user_choice = st.selectbox(
                    f"{habit} (Yes/No)",
                    options=["Yes", "No"],
                    index=index_val
                )

                user_inputs[habit] = 1 if user_choice == "Yes" else 0

        if habit_type == "Range from 1 to 10":
            with col_range:
                options = list(range(1, 11)) 
        
                if current_val == 0.0 or current_val not in options:
                    default_index = 4 
                else:
                    default_index = options.index(int(current_val)) 

                user_inputs[habit] = st.selectbox(
                    f"{habit} (Range 1-10)", 
                    options=options, 
                    index=default_index
                )


        if habit_type == "Time":
            with col_time:
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
            backend.phase_target_xp_gain()
            st.success("Successfully Added")
    
        t.sleep(1)
        st.rerun()

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

    time_based_habits , numeric_habits = backend.get_phase_target_habit()

    if len(time_based_habits) == 0 and len(numeric_habits) == 0 :
        st.warning('Go to default and start the journey first')
        st.stop()

    page = st.sidebar.radio('Select a Page' , ['Set Phase Target' , 'Update Phase Target'])
    
    if page == 'Set Phase Target':
        st.header("Phase Target")

        current_habit = st.selectbox("Select a Habit",time_based_habits + numeric_habits)

        if current_habit in time_based_habits:
            value =  st.number_input("Time in Hours" , min_value= 1 , step=1)
            st.write("Habit : {} , Target : {} Hours".format(current_habit , value))
            value *= 60

        else :
            value =  st.number_input("Enter a Numeric Value" , min_value= 1.0 , step= 0.1)
            st.write("Habit : {} , Target : {}".format(current_habit , value))

        clicked = st.button("Save")

        if clicked == True:
            value = file_manager.add_new_phase_target(current_habit , value)
            backend.new_phase_target_completion(current_habit)

            if value:
                st.success("Succesfully Added")
            else:
                st.warning("Target Already Exist")

    if page == "Update Phase Target":
        val = backend.update_phase_target_list()

        if val == False:
            st.warning('No phase target to update at this time.')
            st.stop()
    
        st.header("Update Phase Target")

        habit_target , habit_type = backend.update_phase_target_list()

        selected_habit = st.selectbox("Select a Target to Update", options=list(habit_target.keys()))

        value = habit_type[selected_habit]
        default_value = habit_target[selected_habit]
    
        if value == "Time":
            new_input = st.number_input("Enter New Target In Hours(Current Target is Given as default)" , min_value = 1 , step=1 , value=default_value//60)
            st.text("Habit to update : {} | New Target : {} Hours".format(selected_habit , new_input))
            new_input *= 60

        else:
            new_input = st.number_input("Enter New Target(Current Target is Given as default)" , min_value = 1.0 , step=0.1 , value=default_value)
            st.text("Habit to update : {} | New Target : {}".format(selected_habit , new_input))

        clicked = st.button("Save")

        if clicked == True:
            value = file_manager.update_new_phase_target(selected_habit , new_input)

            if value :
                st.success("New Target Updated")

if page == "Phase Todo's":
    system_setting = file_manager.load_data(x["system_setting"])

    if 'current' not in system_setting:
        st.warning('Go to default and start the journey first')
        st.stop()

    current = system_setting['current']['current_phase']

    selected_value = st.sidebar.radio("Select Mode" , ["Phase Mode" , "Edit Mode" , "Update Completed Todo" , "Incomplete Previous Todo"])

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

    if selected_value == "Incomplete Previous Todo":
        st.title('Previous Todo')

        val = backend.previous_phase_incomplete_todo()
        if val == False:
            st.info('No Data Avl')
            st.stop()
        
        df , data = backend.previous_phase_incomplete_todo()

        col1 , col2 = st.columns(2)

        with col1:
            completed_task_id = []

            st.header('Mark as Complete')

            counter = 1000
            for phase in data:
                st.header("Phase {}".format(phase))

                for day in data[phase]:
                    st.subheader("Day {}".format(day))

                    for task_id in data[phase][day]:
                        checked = st.checkbox((df[df['Task ID'] == task_id]['Task Description'].iloc[0]) , key = counter)
                        counter += 1

                        if checked:
                            completed_task_id.append(task_id)
        
            if st.button('Save as completed' , key = 'Previous Task Completed'):
                backend.previous_task_complete(completed_task_id)
                st.success('Marked as Completed')
                t.sleep(1)
                st.rerun()

        with col2:
            forward_task_id = []

            st.header('Carry Forward Pending Tasks to Current Phase')

            counter = 2000
            for phase in data:
                st.header("Phase {}".format(phase))

                for day in data[phase]:
                    st.subheader("Day {}".format(day))

                    for task_id in data[phase][day]:
                        checked = st.checkbox((df[df['Task ID'] == task_id]['Task Description'].iloc[0]) , key = counter)
                        counter += 1

                        if checked:
                            forward_task_id.append(task_id)

            opt = np.arange(1 , 11)
            value = st.selectbox("Select day to forword" , opt )
        
            if st.button('Forward' , key = 'Carry Forword Task'):
                backend.previous_task_forword(forward_task_id , value)
                st.success('Forwarded')
                t.sleep(1)
                st.rerun()

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None

if page == "Spaced Repetition":

    val = backend.check_journey_start()

    if val == False:
        st.warning('Go to default and start the journey first')
        st.stop()

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
        val = backend.revise_topic_list()

        if val == False:
            st.warning('Go to default and start the journey first')
            st.stop()

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

if page == "XP and Reward":
    page = st.sidebar.radio("Sidebar Navigation",["Add Holiday & Reward" , "Unlock Reward"])

    today = date.today()

    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)

    else:
        next_month = today.replace(month=today.month + 1, day=1)

    val = backend.holiday_len()
    if val == False:
        st.warning('Go to default and start the journey first')
        st.stop()
    
    if page == "Add Holiday & Reward":

        length , day_free , total_xp_avl  , total_length = backend.holiday_len()

        col1 , col2 = st.columns(2)

        with col1:
            holiday = []

            if length == 0 or length < 4:
                st.header("Confirmed Holidays")
                for date in day_free:
                    st.text(date)
                st.markdown("---")

            if length > 0:
                st.header('Add Holiday')
                counter = 0

                while counter != length:
                    holiday_date = st.date_input("Select Date",
                                             value= next_month - timedelta(1),
                                             min_value= today.replace(day = 1),
                                             max_value=next_month - timedelta(1),
                                             key = counter)
                    counter += 1
                    holiday.append(holiday_date)

                if st.button('Save'):
                    backend.save_holiday(holiday)
                    st.rerun()

            if total_length == 4 and total_xp_avl > 800:
                st.header("XP Holiday (Need 800 XP)")
                holiday_date = st.date_input("Select Date",
                                             value= next_month - timedelta(1),
                                             min_value= today.replace(day = 1),
                                             max_value=next_month - timedelta(1),
                                             )
                
                if st.button('Save'):
                    backend.save_holiday([holiday_date])
                    backend.update_xp(used_xp=800)
                    st.rerun()

            if total_length == 5 and total_xp_avl > 800:
                st.header("XP Holiday (Need 800 XP)")
                holiday_date = st.date_input("Select Date",
                                             value= next_month - timedelta(1),
                                             min_value= today.replace(day = 1),
                                             max_value=next_month - timedelta(1),
                                             )
                
                if st.button('Save'):
                    backend.save_holiday([holiday_date])
                    backend.update_xp(used_xp=800)
                    st.rerun()
                
        with col2:
            st.subheader('Add Reward')
            reward = st.text_input("Enter Reward")
            reward_xp = st.number_input("Enter XP (>= 100)" , min_value=100 , step=1)

            reward_name = reward.strip()
            clicked = st.button('Save' , disabled = not reward_name ,key=reward_name)

            if clicked:
                backend.add_new_reward(reward , reward_xp)
                st.success('Reward Added')
                t.sleep(1)
                st.rerun()

            st.subheader('Update Reward XP')
            reward_dict = backend.update_reward_xp()

            if len(reward_dict) == 0:
                st.warning('No reward to update')
                st.stop()

            reward = st.selectbox('Select an Reward' , reward_dict.keys())
            new_xp = st.number_input('Enter new XP' , step=1 , value= reward_dict[reward])

            if new_xp >= 100:
                key = f"save_button_{reward}"
                click = st.button('Save', key=key)
    
                if click:
                    backend.add_new_reward(reward, new_xp)
                    st.success('XP Updated')
                    t.sleep(1)
                    st.rerun()

            else:
               st.warning('XP is smaller than 100')

    if page == "Unlock Reward":
        st.header('Unlock Reward')

        val = backend.unlock_reward_prerequisites()

        if val == False:
            st.warning('No Rewards to unlock')
            st.stop()

        true_list , false_dict , total_xp , holiday_list , xp_change = backend.unlock_reward_prerequisites()

        st.metric('Current Total XP' , total_xp , delta=xp_change)

        if len(true_list) > 0:
            st.subheader('Claimed')

            for i in true_list:
                text = "✅ {}".format(i)
                st.text(text)

        if len(false_dict) > 0:
            st.subheader('Claim Your Rewards')
            
            claimed_list = []
            xp_using = 0

            for i in false_dict:
                x = st.checkbox("{} | XP Need : {} ".format(i , false_dict[i]["XP"]), value=False)

                if x :
                    claimed_list.append(i)
                    xp_using += false_dict[i]['XP']

            st.metric("Total XP of Selected Rewards" , xp_using)

            if len(claimed_list) > 0 and xp_using > total_xp:

                extra_xp = xp_using - total_xp
                st.warning("Not Enoughf XP {} more then current total XP".format(extra_xp))

            else:
                if len(claimed_list) == 0 :
                    st.warning('Nothing is selected yet')

                else:
                    if st.button('Save'):
                        backend.update_xp(used_xp= xp_using)
                        backend.unlocked_reward(claimed_list)
                        st.rerun()