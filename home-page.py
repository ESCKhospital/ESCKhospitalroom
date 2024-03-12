import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("ESK hospital room service")

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

#st.dataframe(data_med)

# convert to dataframe
info = pd.DataFrame(data_info)
info.dropna(subset=['รหัสนักเรียน'], inplace=True)

ill_df = pd.DataFrame(data_ill)
ill_df.dropna(subset=["ชื่อโรค"], inplace =True)

med_df = pd.DataFrame(data_med)
med_df.dropna(subset=["ชื่อยา"], inplace=True)

# define list of info
student_info = list(info["รหัสนักเรียน"])
student_name = list(info["ชื่อ-นามสกุล"])
name_ls = list(student_name)
student_class = list(info["ระดับชั้น"])
print(student_class)

# define list of disease
ill_ls =  ill_df["ชื่อโรค"]
print(len(ill_ls))

# define list of pill
pill_ls = list(med_df["ชื่อยา"])
print(len(pill_ls))


with st.form(key="บันทึก"):
    date_time = st.date_input(label="วันที่")
    name_id = st.selectbox("ชื่อ", options=student_name, index=None)

    illness = st.multiselect("โรค", options=ill_ls)
    pill_used = st.multiselect("ยาที่ใช้", options=pill_ls)
    pill_amount = st.text_area(label="ปริมาณยาที่ใช้")
    st.write("ใส่ปริมาณเป็นตัวเลข ไม่ต้องใส่หน่วย ถ้าต้องการกรอกมากกว่า 1 ปริมาณ ให้เว้นวรรค แล้วจึงใส่ปริมาณต่อไป")
    addition = st.text_area(label="หมายเหตุ")

    submit_button = st.form_submit_button(label="บันทึก")

    if(submit_button):
        idx_id = name_ls.index(name_id)
        id_now = student_info[idx_id]
        class_now = student_class[idx_id]
        pill_type = pill_used.copy()
        submit_df = pd.DataFrame([{
            "รหัสนักเรียน" : str(id_now),
            "ห้อง": class_now,
            "ชื่อ": name_id,
            "วันที่": date_time.strftime("%Y-%m-%d"),
            "โรค": ",".join(illness),
            "ยาที่ใช้": ",".join(pill_type),
            "หมายเหตุ": addition
        }])

        # add dataframe
        updated_df = pd.concat([data_stat, submit_df], ignore_index=True)
        #st.dataframe(updated_df)

        #push df
        conn.update(worksheet="บันทึก", data=updated_df)

        # pill stock update
        all_used = pill_amount.split(' ')
        all_used = [float(i.strip()) for i in all_used]

        pill_df = med_df.copy()

        print(pill_used)
        print(pill_ls)
        for j in range(len(pill_used)):
            idx = pill_ls.index(pill_used[j])
            pill_df.loc[idx, "จำนวน"] = float(pill_df.loc[idx, "จำนวน"])-all_used[j]
        
        conn.update(worksheet="ข้อมูลยา", data=pill_df)

        st.success("บันทึกเรียบร้อย")
