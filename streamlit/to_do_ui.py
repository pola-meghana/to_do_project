import streamlit as st
import requests
import json
import pandas as pd
from streamlit_option_menu import option_menu


st.set_page_config(layout="wide")

local_host = 'http://localhost:8000/'

session_state = st.session_state

def get_jwt_token(username, password):
    
    url = local_host + 'api/token/'
    data = {
        'username': username,
        'password': password
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token = response.json()
        access_token = token['access']
        return access_token
    else:
        return None
    

def get_data(token):

    url = local_host + 'data/'
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return token
    else:
        return None

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    
    
    st.markdown("<h1 style='text-align: center; '>LOGIN</h1> <br>", unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2 ,col3= st.columns(3)
        with col2:
            login_button = st.button("Login")

    if login_button:
        token = get_jwt_token(username, password)
        
        if token:
            data = get_data(token)
            
            if data:
                st.session_state['logged_in'] = True
                st.session_state['token'] = token
                st.session_state['username']=username
                st.experimental_rerun()
            else:
                 st.write("You do not have permission to access the next page")

        else:
            st.error("Invalid username or password.")

if 'logged_in' in st.session_state and st.session_state['logged_in']:

    token=st.session_state['token']
    username=st.session_state['username']

    selected=option_menu(menu_title="Menu",
        options=["To-Do","Pending","History"],
        orientation="horizontal",)

    if selected=="To-Do":

        task=st.text_input("Task")
        add_button=st.button("Add Task")
        record_data={
            "username":username,
            "task":task,
            "description":"",
            "status":"pending",
        }
        if add_button:
            url=local_host+'todo/?type=insert'
            headers = {'Authorization': f'Bearer {token}'}
            response=requests.post(url,headers=headers,params=record_data)
            if response.status_code==200:
                st.write("Task added successfully")
            
        

    if selected == "Pending":
        url=local_host+'todo/?type=fetch_pending'
        headers = {'Authorization': f'Bearer {token}'}
        params={
            "username":username
        }
        response=requests.get(url,headers=headers,params=params)

        if response.status_code==200:
            record=response.json()
            task=record['tasklist']
            col1,col2 = st.columns([4.5,5.5])
            with col2:
                for item in task:
                    task_button=st.checkbox(item,key=item)
                    if task_button:
                        with st.container():
                            with st.form(key="upload_form",clear_on_submit=True):
                                description = st.text_area("Description")
                                file=st.file_uploader("please choose a file")
                                submit = st.form_submit_button("submit")
                                if description:
                                    if submit:
                                        url=local_host+'todo/?type=update'
                                        headers = {'Authorization': f'Bearer {token}'}
                                        params={
                                            "username":username,
                                            "task":item,
                                            "description":description,
                                            "status":"done",
                                        }
                                        files={
                                            'file':file
                                        }
                                        update_response=requests.post(url,headers=headers,params=params,files=files)
                                        if update_response.status_code==200:
                                            update_message=update_response.json()
                                            st.write(update_message['message'])

    col1,col2 = st.columns([7,3])
    if selected=="History":
        url=local_host+'todo/?type=fetch_total'
        headers = {'Authorization': f'Bearer {token}'}
        params={
            "username":username
        }
        response=requests.get(url,headers=headers,params=params)
        if response.status_code==200:

            task_history=response.json()
            tasklist = task_history['tasklist']
            statuslist = task_history['statuslist']
            task_history={
                'Task': [i for i in tasklist],
                'Status': [i for i in statuslist]
            }
            df = pd.DataFrame(task_history)
            df.index = [i+1 for i in range(len(df))]
            df.index.name = 'S.No'
            with col2:
                st.write(df, height=500)     
