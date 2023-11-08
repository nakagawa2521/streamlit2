import streamlit as st
#import pandas as pd
import sqlite3 
import hashlib

conn = sqlite3.connect('database.db')
c = conn.cursor()

if 'select' not in st.session_state: #ビデオ内容の選択変数
	st.session_state.select = ''

path1 = '数学一次方程式01_exported123.mp4'
path2 = '数学文章題_exported_3.mp4'

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False


def create_user():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_user(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def video_play(path):
        video_file = open(path, 'rb') #enter the filename with filepath
        video_bytes = video_file.read() #reading the file
        st.video(video_bytes) #displaying the video

if 'login' not in st.session_state: #の開始
	st.session_state.login= True

if 'video' not in st.session_state: #の開始
	st.session_state.video= False


if st.session_state.login:
        st.markdown("##### ログインテスト")

        username = st.text_input("ユーザー名を入力してください")
        password = st.text_input("パスワードを入力してください",type='password')
        if st.checkbox("ログイン"):
                create_user()
                hashed_pswd = make_hashes(password)

                result = login_user(username,check_hashes(password,hashed_pswd))
                if result:

                        st.success("{}さんでログインしました".format(username))
                        
                        st.session_state.video=True
                        st.session_state.login=False
                else:
                        st.warning("ユーザー名かパスワードが間違っています")

if st.session_state.video:
        st.session_state.select= st.radio(label='###### ビデオ内容の選択', #初期値は「数学一次方程式」
        options=('数学一次方程式', '数学文章題'), 
        index=0,
        horizontal=True,
        )

        if st.session_state.select=='数学一次方程式':
                path=path1
        else:
                path=path2
        
        if st.button('##### video start',key=1,type='primary'):
               video_play(path)
	
