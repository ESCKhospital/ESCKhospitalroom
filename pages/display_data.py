import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# gg sheet connection
conn = st.connection("gsheets", type=GSheetsConnection)

# page connecting 
data_med = conn.read(worksheet="ข้อมูลยา", ttl=5)
data_med  = data_med.dropna(how="all")
data_info = conn.read(worksheet="รายชื่อนักเรียนหอพัก", ttl=5)
data_info = data_info.dropna(how="all")
data_ill = conn.read(worksheet="ข้อมูลโรค", ttl=5)
data_ill = data_ill.dropna(how="all")
data_stat = conn.read(worksheet="บันทึก", ttl=5)
data_stat = data_stat.dropna(how="all")

ls_op = ["รายชื่อนักเรียน", "ข้อมูลโรค", "ข้อมูลยา", "บันทึก"]

with st.form(key="dataframey"):
    opt = st.selectbox("เลือกรายการ", options=ls_op, index=None)
    data_sub_df = st.form_submit_button(label="เลือก")

    if(data_sub_df):
        if(opt==ls_op[0]):
            st.dataframe(data_info)
        elif(opt==ls_op[1]):
            st.dataframe(data_ill)
        elif(opt==ls_op[2]):
            st.dataframe(data_med)
        else:
            st.dataframe(data_stat)