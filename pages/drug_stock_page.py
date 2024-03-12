import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("เพิ่ม stock ยา")

# gg sheet connection
conn = st.connection("gsheets", type=GSheetsConnection)

# page connecting 
data_med = conn.read(worksheet="ข้อมูลยา", ttl=5)
data_med  = data_med.dropna(how="all")

med_df = pd.DataFrame(data_med)
pill_ls = list(med_df["ชื่อยา"])

with st.form(key="ข้อมูลยา"):
    pill_type = st.selectbox("ชื่อยา", options=pill_ls, index=None)

    amout = st.text_input('ปริมาณยา')

    pill_add_but = st.form_submit_button(label="เพิ่มจำนวนยา")

    if(pill_add_but):
        amount = float(amout.strip())
        med_up = med_df.copy()
        idx = pill_ls.index(pill_type)
        med_up.loc[idx, "จำนวน"] = float(med_up.loc[idx, "จำนวน"])+amount

        conn.update(worksheet="ข้อมูลยา", data=med_up)

        st.success("อัปเดตข้อมูลยาเรียบร้อย")