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

    st.markdown(
     f"""
     <style>
     .stApp {{
         background-image: url("https://images.pexels.com/photos/2008145/pexels-photo-2008145.jpeg?auto=compress&cs=tinysrgb&w=1600");
         background-attachment: fixed;
         background-size: cover
     }}
     </style>
     """,
     unsafe_allow_html=True
     )

    
    
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

    st.markdown(
     f"""
     <style>
     .stApp {{
         background-image: url("data:image/jpeg;base64,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");
         background-attachment: fixed;
         background-size: cover
     }}
     </style>
     """,
     unsafe_allow_html=True
     )


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

    col1,col2 = st.columns([5,5])
    if selected=="History":
        col1,col2=st.columns(2)

        with col1:
            url=local_host+'todo/?type=fetch_total'
            headers = {'Authorization': f'Bearer {token}'}
            params={
                "username":username
            }
            response=requests.get(url,headers=headers,params=params)
            if response.status_code==200:
                task_history=response.json()
                st.header("Total Tasks")
                df = pd.DataFrame(task_history)
                df.index = [i+1 for i in range(len(df))]
                df.index.name = 'S.No'
                st.write(df, height=350)

        with col2:
            params={
                "username":username,
            }     
        
            url = local_host + "todo/?type=fetch_done"
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(url,headers=headers,params=params)
            
            if response.status_code == 200:
                record = response.json()
                tasks = record['tasks']
                files = record['files']
                description = record['description']
                st.header("Finished Tasks")
                for i in range(len(tasks)):
                    done_task = st.button(f'{i+1}.{tasks[i]}')
                    button_style = """
                        <style>
                        .stButton>button {
                            background: none;
                            border: none;
                            padding: 0;
                            margin: 0;
                            font-size: inherit;
                            font-family: inherit;
                            cursor: pointer;
                            outline: inherit;
                        }
                        </style>
                    """
                    st.markdown(button_style, unsafe_allow_html=True)
                    if done_task:
                        st.write("Description:", description[i])                        
                        st.write("Click the link to download the file:", files[i])         
            else:
                st.error("Unable to fetch the data")   