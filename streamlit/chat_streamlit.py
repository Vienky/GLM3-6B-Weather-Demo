import os
import openai
import json
import requests
openai.api_key = 'xxxx'
openai.api_base = "http://api.com/v1" #your own api url
import streamlit as st 
from pathlib import Path
from function_weather import run_conversation

st.title("Chat & Functionality Demo")

if "history" not in st.session_state:
    st.session_state.history = []

buttonClean = st.sidebar.button("清理会话历史", key="clean")
if buttonClean:
    st.session_state.history = []

for i, message in enumerate(st.session_state.history):
    if message["role"] == "user":
        st.info(message["content"], icon="👤")
    else:
        st.success(message["content"], icon="🤖")

user_input = st.text_input("请输入您的问题", key="user_input")

if st.button("提交"):
    # 调用run_conversation函数处理用户输入，并获取最终结果
    final_message = run_conversation(user_input)
    
    # 更新会话历史
    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.history.append({"role": "assistant", "content": final_message})

    # 重新加载页面以显示更新的会话历史
    st.experimental_rerun()
