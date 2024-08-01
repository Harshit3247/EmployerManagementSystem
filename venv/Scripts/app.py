import streamlit as st
import mysql.connector
import datetime

# Set page configuration
st.set_page_config(page_title="Employee Management System", page_icon="https://cdn-icons-png.flaticon.com/512/3616/3616930.png")
st.title("Employee Management System")

# Sidebar menu
choice = st.sidebar.selectbox("Menu", ("HOME", "EMPLOYEE", "ADMIN"))

# Home page
if choice == "HOME":
    st.image("https://img.freepik.com/free-vector/hiring-agency-candidates-job-interview_1262-18940.jpg")
    st.write("This application is developed by Harshit Pant.")

# Employee login and actions
elif choice == "EMPLOYEE":
    if "islogin" not in st.session_state:
        st.session_state["islogin"] = False
    eid = st.text_input("Enter Employee ID")
    pwd = st.text_input("Enter Employee Password", type="password")
    btn = st.button("Login")

    if btn:
        mydb = mysql.connector.connect(host="localhost", user="root", password="20553640", database="ems")
        c = mydb.cursor()
        c.execute("SELECT emp_id, emp_pwd FROM employee_details")
        for r in c:
            if r[0] == eid and r[1] == pwd:
                st.session_state["islogin"] = True
                break
        if not st.session_state["islogin"]:
            st.error("Invalid ID or Password")
        else:
            st.success("Login Successful")

    if st.session_state["islogin"]:
        choice2 = st.selectbox("Features", ("None", "Profile Info", "Apply for Leave"))
        if choice2 == "Profile Info":
            mydb = mysql.connector.connect(host="localhost", user="root", password="20553640", database="ems")
            c = mydb.cursor()
            c.execute("SELECT * FROM employee_details WHERE emp_id = %s", (eid,))
            row = c.fetchone()
            if row:
                st.write(f"**Employee ID:** {row[0]}")
                st.write(f"**Name:** {row[2]}")
                st.write(f"**Salary:** {row[3]}")
        elif choice2 == "Apply for Leave":
            reason = st.text_input("Enter the reason for leave")
            btn3 = st.button("Apply")
            if btn3:
                aid = str(datetime.datetime.now())
                mydb = mysql.connector.connect(host="localhost", user="root", password="20553640", database="ems")
                c = mydb.cursor()
                c.execute("INSERT INTO leave_application VALUES (%s, %s, %s)", (aid, eid, reason))
                mydb.commit()
                st.success("Leave Applied Successfully")

# Admin login and actions
elif choice == "ADMIN":
    if "isadminlogin" not in st.session_state:
        st.session_state["isadminlogin"] = False
    admin_id = st.text_input("Enter Admin ID")
    admin_pwd = st.text_input("Enter Admin Password", type="password")
    btn = st.button("Login")

    if btn:
        mydb = mysql.connector.connect(host="localhost", user="root", password="20553640", database="ems")
        c = mydb.cursor()
        c.execute("SELECT admin_id, admin_pwd FROM admins")
        for r in c:
            if r[0] == admin_id and r[1] == admin_pwd:
                st.session_state["isadminlogin"] = True
                break
        if not st.session_state["isadminlogin"]:
            st.error("Invalid ID or Password")
        else:
            st.success("Login Successful")

    if st.session_state["isadminlogin"]:
        choice3 = st.selectbox("Admin Features", ("None", "Mark Attendance", "Add Employee", "Delete Employee", "Update Salary"))
        if choice3 == "Mark Attendance":
            eid = st.text_input("Enter Employee ID")
            status = st.selectbox("Enter Status", ("Present", "Absent", "Half Day"))
            btn4 = st.button("Submit")
            if btn4:
                dt = str(datetime.datetime.now())
                mydb = mysql.connector.connect(host="localhost", user="root", password="20553640", database="ems")
                c = mydb.cursor()
                c.execute("INSERT INTO emp_attendance VALUES (%s, %s, %s)", (dt, eid, status))
                mydb.commit()
                st.success("Attendance Marked Successfully")
        elif choice3 == "Add Employee":
            new_eid = st.text_input("Choose Employee ID")
            new_pwd = st.text_input("Choose Employee Password", type="password")
            name = st.text_input("Enter Employee Name")
            salary = st.text_input("Enter Salary")
            btn5 = st.button("Add Employee")
            if btn5:
                mydb = mysql.connector.connect(host="localhost", user="root", password="20553640", database="ems")
                c = mydb.cursor()
                c.execute("INSERT INTO employee_details VALUES (%s, %s, %s, %s)", (new_eid, new_pwd, name, salary))
                mydb.commit()
                st.success("Employee Added Successfully")
        elif choice3 == "Delete Employee":
            del_eid = st.text_input("Enter Employee ID to Delete")
            btn6 = st.button("Delete Employee")
            if btn6:
                mydb = mysql.connector.connect(host="localhost", user="root", password="20553640", database="ems")
                c = mydb.cursor()
                c.execute("DELETE FROM employee_details WHERE emp_id = %s", (del_eid,))
                mydb.commit()
                st.success("Employee Deleted Successfully")
        elif choice3 == "Update Salary":
            up_eid = st.text_input("Enter Employee ID to Update Salary")
            new_salary = st.text_input("Enter New Salary")
            btn7 = st.button("Update Salary")
            if btn7:
                mydb = mysql.connector.connect(host="localhost", user="root", password="20553640", database="ems")
                c = mydb.cursor()
                c.execute("UPDATE employee_details SET emp_salary = %s WHERE emp_id = %s", (new_salary, up_eid))
                mydb.commit()
                st.success("Salary Updated Successfully")
