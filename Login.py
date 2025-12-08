import streamlit as st
import sqlite3
import bcrypt
st.set_page_config(page_title="College portal",page_icon="🔐",layout="centered")
if 'page' not in st.session_state:
    st.session_state['page']='login'
if 'logged_in' not in st.session_state:
    st.session_state['logged_in']=False
if 'user_email' not in st.session_state:
    st.session_state['user_email']=None
# DATABASE STORAGE
DB_FILE='users.db'
def create_table():
    conn=sqlite3.connect(DB_FILE)
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS
users (email TEXT PRIMARY KEY,password_hash TEXT NOT NULL)''')
    conn.commit()
    conn.close()
def register_user(email,password):
    conn=sqlite3.connect(DB_FILE)
    c=conn.cursor()
    
    salt=bcrypt.gensalt()
    hashed_password=bcrypt.hashpw(password.encode('utf-8'),salt)

    try:
        c.execute("INSERT INTO users (email,password_hash) VALUES (?,?)",
                  (email,hashed_password.decode('utf-8')))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
def verify_user(email,password):
    conn=sqlite3.connect(DB_FILE)
    c=conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE email=?",(email,))

    result=c.fetchone()
    conn.close()

    if result:
        stored_hash=result[0].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'),stored_hash)
    return False

# LOGIN PAGE CODE
def login_page():
    st.markdown("""
    <style>

        .stApp {
            background-color: #edf6fc; 
            color: #333333;   
            font-family: 'Open Sans', sans-serif  
     }
        .banner-container{
            background-color: #FA8072;
            height: 300px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            color: white;
            padding: 20px;
            margin-bottom: 50px;
        }

        .main-card {
            background-color: black;
            color: black;
            width: 380px;
            margin: auto;
            padding: 30px;
            border-radius: 25px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            text-align: center;
        }

        .title-text {
            color: #000000;
            font-size: 22px;
            font-weight: 600;
            margin-bottom: 20px;
        }

        .stTextInput > div > div > input {
            background-color: #ffffff;
            border-radius: 12px;
            border: 1.5px solid #f7a3b5;
            padding: 10px;
        }
        /*text*/
        .stTextInput>div>div>input {
            background-color:#ffffff;
            border-radius:12px;
            border: 1.5px solid #ffffff;
            padding: 10px;
            color:black !important;
        }

        .stButton>button {
            background-color: #ffffff;
            color: #333333;
            border-radius: 50px; 
            border: none;
            box-shadow: 0 3px 5px rgba(0, 0, 0, 0.15);
            transition: all 0.2s;
            height: 100%; 
            margin-top: 29px; 
            font-weight: bold
        }
        .stButton > button:hover {
            background-color: #d2eef6;
            color: white;
        }

    </style>
    """, unsafe_allow_html=True)
    st.title("Begin Your Journey")
    with st.form(key="login_form"):
        email=st.text_input("📧 Email")
        password=st.text_input("🔒 Password",type="password")
        submit_button=st.form_submit_button("🚀 Start Exploring")
    if submit_button:
        if not email or not password:
            st.warning("⚠ Please fill all fields!") 
        else:
            if verify_user(email,password):
                st.success("Login successful! Redirecting to homepage...")
                st.session_state['logged_in']=True
                st.session_state['user_email']=email
                st.switch_page("pages/01_Home_Page.py")
                st.rerun()
            else:
                st.error("Login failed:Invalid email or password.")
    col1,col2,col3=st.columns([1,4,1])
    with col2:
        if st.button("Don't have an account? Register",key="goto_register"):
            st.session_state['page']='register'
            st.rerun()

# REGISTER PAGE CODE
def register_page():
    st.markdown("""
    <style>

        .stApp {
            background-color: #edf6fc; 
            color: #333333;   
            font-family: 'Open Sans', sans-serif  
        }

        .main-card {
            background: black;
            width: 380px;
            margin: auto;
            padding: 30px;
            border-radius: 25px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            text-align: center;
        }

        .title-text {
            color: #d14f74;
            font-size: 22px;
            font-weight: 600;
            margin-bottom: 20px;
        }

        .stTextInput > div > div > input {
            background-color: #ffffff;
            border-radius: 12px;
            border: 1.5px solid #ffffff;
            padding: 10px;
            color: black !important;
        } 
            
        .stButton>button {
            background-color: #ffffff;
            color: #333333;
            border-radius: 50px; 
            border: none;
            box-shadow: 0 3px 5px rgba(0, 0, 0, 0.15);
            transition: all 0.2s;
            height: 100%; 
            margin-top: 29px; 
            font-weight: bold
        }
        .stButton > button:hover {
            background-color: #d2eef6;
            color: white;
        }

    </style>
    """, unsafe_allow_html=True)
    st.title("Create Your Account")
    st.header("Discover Amazing Places And Create Unforgettable Memories!")
    with st.form(key="register_form"):
        st.subheader("Sign Up")
        email=st.text_input("📧 Email",key="reg_email")
        password=st.text_input("🔒 Password",type="password",key="reg_password")
        confirm_password=st.text_input("🔒 Confirm Password",type="password",key="reg_confirm")
        register_button=st.form_submit_button(label="Register🚀")
        if register_button:
            if not email or not password or not confirm_password:
                st.warning("Please fill all fields!")
            elif password!=confirm_password:
                st.error("Passwords do not match!")
            else:
                if register_user(email,password):
                    st.success("Registration successful! Redirecting to Login...")
                    st.session_state['page']='login'
                    st.rerun()
                else:
                    st.error("This email is already registered.Login")
    st.markdown("---")
    st.write("Already have an account?")
    if st.button("Go to Login",key="goto_login_reg_page_button"):
        st.session_state['page']='login'
        st.rerun()

# MAIN CONTROL FLOW
def main():
    create_table()
    if st.session_state['page']=='login':
        login_page()
    elif st.session_state['page']=='register':
        register_page()
if __name__=='__main__':
    main()