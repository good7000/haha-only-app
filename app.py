import streamlit as st
from supabase import create_client, Client
import hashlib
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Ha Ha only 🤣", page_icon="🤣", layout="wide")

# Logo Branding (Yellow Square with Smile)
LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiByeD0iMTAwIiBmaWxsPSIjRkZEMzAwIi8+Cjx0ZXh0IHg9IjUwJSIgeT0iNjAlIiBmb250LXNpemU9IjI4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZpbGw9ImJsYWNrIj7wn6SjPC90ZXh0Pgo8L3N2Zz4="

# --- 2. DATABASE CONNECTION ---
try:
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(URL, KEY)
except Exception as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

def hash_pw(pw):
    return hashlib.sha256(str.encode(pw)).hexdigest()

# --- 3. CUSTOM STYLING & SPLASH SCREEN ---
st.markdown(f"""
    <style>
    /* Splash Screen Styling */
    #splash-screen {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #FFD300; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 100000;
        animation: fadeOutSplash 2.5s forwards;
    }}
    @keyframes fadeOutSplash {{ 0% {{ opacity: 1; }} 80% {{ opacity: 1; }} 100% {{ opacity: 0; visibility: hidden; }} }}
    
    /* Video & UI Enhancements */
    .stVideo {{ border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
    .stButton>button {{ border-radius: 20px; }}
    </style>
    
    <div id="splash-screen">
        <img src="{LOGO_SVG}" style="width: 120px; border-radius: 25px;">
        <h1 style="color: black; font-family: sans-serif; margin-top: 15px;">Ha Ha only</h1>
        <p style="color: black; font-weight: bold;">Spreading Joy... 🤣</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. SESSION MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- 5. SIDEBAR (AUTHENTICATION) ---
with st.sidebar:
    st.image(LOGO_SVG, width=100)
    st.title("User Zone 👤")
    
    if not st.session_state.logged_in:
        auth_mode = st.radio("Select Action", ["Login", "Sign Up"])
        username = st.text_input("Username").strip()
        
        email_addr = ""
        if auth_mode == "Sign Up":
            email_addr = st.text_input("Email Address").strip()
            
        password = st.text_input("Password", type="password")
        
        if st.button("Submit"):
            if auth_mode == "Sign Up":
                if username and password and email_addr:
                    try:
                        supabase.table("users").insert({
                            "username": username, 
                            "password": hash_pw(password), 
                            "email": email_addr
                        }).execute()
                        st.success("Account created! You can now Login.")
                    except Exception as e:
                        st.error(f"Registration Failed: {e}")
                else:
                    st.warning("Please fill in all fields (Username, Email, and Password).")
            else:
                try:
                    res = supabase.table("users").select("*").eq("username", username).eq("password", hash_pw(password)).execute()
                    if res.data:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.email = res.data[0].get('email', 'N/A')
                        st.rerun()
                    else:
                        st.error("Invalid Username or Password.")
                except Exception as e:
                    st.error(f"Login Error: {e}")
    else:
        st.success(f"Hello, {st.session_state.username}!")
        st.info(f"📧 {st.session_state.email}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

# --- 6. MAIN APP CONTENT ---
st.title("🎬 Global Joy Feed")
watch_tab, upload_tab = st.tabs(["🔥 Watch & Laugh", "📤 Share Joy"])

with watch_tab:
    try:
        # Fetching all videos from database
        video_data = supabase.table("videos").select("*").order("id", desc=True).execute().data
        
        if not video_data:
            st.info("The feed is currently empty. Be the first to share a video! 📤")
        else:
            for video in video_data:
                with st.container():
                    st.subheader(video.get('title', 'Joy Video'))
                    st.video(video['url'])
                    
                    col1, col2 = st.columns([4, 1])
                    col1.caption(f"Uploaded by: @{video.get('uploader_name', 'Guest')} | 🤣 {video.get('haha_count', 0)} laughs")
                    
                    if col2.button(f"🤣 Ha Ha", key=f"btn_{video['id']}"):
                        # Increment Haha count in database
                        new_count = video.get('haha_count', 0) + 1
                        try:
                            supabase.table("videos").update({"haha_count": new_count}).eq("id", video['id']).execute()
                            st.rerun()
                        except:
                            pass
                st.divider()
    except Exception as e:
        st.warning(f"Database connection issue: {e}")

with upload_tab:
    if not st.session_state.logged_in:
        st.warning("⚠️ You must be Logged In to upload videos. Please use the sidebar.")
    else:
        st.subheader("Upload Your Content")
        with st.form("upload_form", clear_on_submit=True):
            video_title = st.text_input("Title (e.g., My Funny Dog)")
            video_url = st.text_input("Video URL (Direct link to .mp4)")
            
            if st.form_submit_button("Post Joy 🚀"):
                if video_title and video_url:
                    try:
                        supabase.table("videos").insert({
                            "title": video_title, 
                            "url": video_url, 
                            "uploader_name": st.session_state.username,
                            "haha_count": 0
                        }).execute()
                        st.success("Successfully posted! Switch to the Watch tab to see it.")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Upload failed: {e}")
                else:
                    st.error("Please provide both a Title and a Video URL.")
