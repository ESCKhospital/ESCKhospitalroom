import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("เพิ่มข้อมูล")

conn = st.connection("gsheets", type=GSheetsConnection)

data_med = conn.read(worksheet="ข้อมูลยา", ttl=5)
data_med  = data_med.dropna(how="all")

data_ill = conn.read(worksheet="ข้อมูลโรค", ttl=5)
data_ill = data_ill.dropna(how="all")

with st.form(key="ข้อมูลยา"):
    name_pill = st.text_area(label="ชื่อยา")
    unit_pill = st.text_area(label="หน่วยนับ")
    n_pill = st.text_area(label="จำนวน")

    pill_submit_but = st.form_submit_button(label="บันทึกข้อมูลยา")

    if(pill_submit_but):
        pill_df = pd.DataFrame([{
            "ชื่อยา": name_pill,
            "หน่วยนับ": unit_pill,
            "จำนวน": int(n_pill)
        }])

        updated_pill_df = pd.concat([data_med, pill_df], ignore_index=True)
        conn.update(worksheet="ข้อมูลยา", data=updated_pill_df)
        
        st.success("บันทึกข้อมูลยาเรียบร้อย")

with st.form(key="ข้อมูลโรค"):
    type_ls = list(set(data_ill["ข้อมูลกลุ่มโรค"]))
    typo = st.selectbox("กลุ่มโรค", options=type_ls)
    name_ill = st.text_area(label="ชื่อโรค")

    ill_submit_but = st.form_submit_button(label="บันทึกข้อมูลโรค")

    if(ill_submit_but):
        ill_submit_df = pd.DataFrame([{
            "ข้อมูลกลุ่มโรค": typo,
            "ชื่อโรค": name_ill
        }])

        updated_ill_df = pd.concat([data_ill, ill_submit_df], ignore_index=True)
        conn.update(worksheet="ข้อมูลโรค", data=updated_ill_df)

        st.success("บันทึกข้อมูลโรคเรียบร้อย")
