import streamlit as st
from supabase import create_client, Client
import hashlib
import time

# --- 1. PAGE CONFIG & BRANDING ---
st.set_page_config(page_title="Ha Ha only 🤣", page_icon="🤣", layout="wide")

# Embedded Logo (Yellow Square with Smile)
LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiByeD0iMTAwIiBmaWxsPSIjRkZEMzAwIi8+Cjx0ZXh0IHg9IjUwJSIgeT0iNjAlIiBmb250LXNpemU9IjI4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZpbGw9ImJsYWNrIj7wn6SjPC90ZXh0Pgo8L3N2Zz4="

# --- 2. SUPABASE CONNECTION ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("⚠️ Configuration Error: Please check your Streamlit Secrets.")
    st.stop()

def hash_pw(pw): return hashlib.sha256(str.encode(pw)).hexdigest()

# --- 3. UI DESIGN (CSS & ANIMATIONS) ---
st.markdown(f"""
    <style>
    /* Splash Screen Animation */
    #splash-screen {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #FFD300; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 100000;
        animation: fadeOutSplash 2.5s forwards;
    }}
    @keyframes fadeOutSplash {{ 0% {{ opacity: 1; }} 80% {{ opacity: 1; }} 100% {{ opacity: 0; visibility: hidden; }} }}
    
    /* Floating 🤣 Emoji Animation */
    .floating-emoji {{ 
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
        font-size: 120px; z-index: 9999; animation: fadeOutEmoji 0.8s ease-out forwards; 
        pointer-events: none; 
    }}
    @keyframes fadeOutEmoji {{ 
        0% {{ opacity: 0; scale: 0.3; }} 
        30% {{ opacity: 1; scale: 1.2; }} 
        100% {{ opacity: 0; scale: 2.5; }} 
    }}

    /* Global Video Styles */
    .stVideo {{ border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
    </style>
    
    <div id="splash-screen">
        <img src="{LOGO_SVG}" style="width: 130px; border-radius: 25px;">
        <h1 style="color: black; margin-top: 20px; font-family: sans-serif;">Ha Ha only</h1>
        <p style="color: black; font-weight: bold;">Loading Joy... 🤣</p>
    </div>

    <audio id="haha-sound" src="https://www.soundjay.com/human/laughter-2.mp3" preload="auto"></audio>
    <script>
    function playHaha() {{
        var sound = document.getElementById("haha-sound");
        sound.currentTime = 0;
        sound.play();
    }}
    </script>
    """, unsafe_allow_html=True)

# --- 4. SESSION MANAGEMENT ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'show_emoji' not in st.session_state: st.session_state.show_emoji = False

# --- 5. SIDEBAR (User Zone with Email) ---
with st.sidebar:
    st.image(LOGO_SVG, width=100)
    st.title("User Zone 👤")
    
    if not st.session_state.logged_in:
        mode = st.radio("Select Mode", ["Login", "Sign Up"])
        u = st.text_input("Username")
        
        email_val = ""
        if mode == "Sign Up":
            email_val = st.text_input("Email Address")
            
        p = st.text_input("Password", type="password")
        
        if st.button("Go"):
            if mode == "Sign Up":
                if u and p and email_val:
                    try:
                        # Check if username exists
                        check = supabase.table("users").select("username").eq("username", u).execute()
                        if check.data:
                            st.error("Username already taken!")
                        else:
                            supabase.table("users").insert({
                                "username": u, 
                                "password": hash_pw(p), 
                                "email": email_val
                            }).execute()
                            st.success("Account created! Please switch to Login.")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Please fill all fields, including Email.")
            else:
                # Login Logic
                res = supabase.table("users").select("*").eq("username", u).eq("password", hash_pw(p)).execute()
                if res.data:
                    st.session_state.logged_in = True
                    st.session_state.username = res.data[0]['username']
                    st.session_state.email = res.data[0].get('email', 'No email')
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
    else:
        st.success(f"Hello, {st.session_state.username}!")
        st.info(f"📧 {st.session_state.email}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

# --- 6. MAIN CONTENT (PUBLIC FEED) ---
if st.session_state.show_emoji:
    st.markdown('<div class="floating-emoji">🤣</div>', unsafe_allow_html=True)
    st.session_state.show_emoji = False

st.title("🎬 Global Joy Feed")
tab1, tab2 = st.tabs(["🔥 Watch & Laugh", "📤 Share Joy"])

with tab1:
    try:
        # Fetching videos with Try/Except to prevent app crash
        vids_res = supabase.table("videos").select("*").order("id", desc=True).execute()
        vids = vids_res.data if vids_res.data else []
    except Exception:
        st.warning("🔄 Connecting to the joy database... Please wait.")
        vids = []

    if not vids:
        st.info("The feed is empty. Be the first to share joy! 📤")
        
    for v in vids:
        with st.container():
            st.subheader(v.get('title', 'Joy Video'))
            st.video(v['url'])
            c1, c2 = st.columns([3, 1])
            c1.caption(f"Created by: @{v.get('uploader_name', 'Guest')} | 🤣 {v.get('haha_count', 0)} laughs")
            
            if c2.button(f"🤣 Ha Ha", key=f"btn_{v['id']}"):
                # Trigger Laughter Sound & Emoji
                st.components.v1.html("<script>window.parent.playHaha();</script>", height=0)
                st.session_state.show_emoji = True
                
                # Update Haha count in Supabase
                try:
                    new_count = v.get('haha_count', 0) + 1
                    supabase.table("videos").update({"haha_count": new_count}).eq("id", v['id']).execute()
                except:
                    pass
                
                time.sleep(0.4)
                st.rerun()
        st.divider()

with tab2:
    if not st.session_state.logged_in:
        st.warning("⚠️ Access Denied: You must Login from the sidebar to upload videos.")
    else:
        st.subheader("Upload a New Video")
        with st.form("upload_joy", clear_on_submit=True):
            t = st.text_input("Joy Title (e.g. Funny Cat!)")
            url = st.text_input("Direct Video Link (.mp4 only)")
            if st.form_submit_button("Post Joy Now 🚀"):
                if t and url:
                    try:
                        supabase.table("videos").insert({
                            "title": t, 
                            "url": url, 
                            "uploader_name": st.session_state.username
                        }).execute()
                        st.success("Shared successfully! Refresh the feed.")
                        time.sleep(1)
                        st.rerun()
                    except:
                        st.error("Upload failed. Check your connection.")
                else:
                import streamlit as st
from supabase import create_client, Client
import hashlib
import time

# --- 1. CONFIG ---
st.set_page_config(page_title="Ha Ha only 🤣", page_icon="🤣", layout="wide")

# Logo SVG
LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiByeD0iMTAwIiBmaWxsPSIjRkZEMzAwIi8+Cjx0ZXh0IHg9IjUwJSIgeT0iNjAlIiBmb250LXNpemU9IjI4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZpbGw9ImJsYWNrIj7wn6SjPC90ZXh0Pgo8L3N2Zz4="

# --- 2. SECURE CONNECTION ---
try:
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(URL, KEY)
except Exception as e:
    st.error("Connection settings missing. Check Secrets!")
    st.stop()

def hash_pw(pw): return hashlib.sha256(str.encode(pw)).hexdigest()

# --- 3. UI STYLE ---
st.markdown(f"""
    <style>
    #splash-screen {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #FFD300; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 100000;
        animation: fadeOut 2.5s forwards;
    }}
    @keyframes fadeOut {{ 0% {{opacity:1}} 80% {{opacity:1}} 100% {{opacity:0; visibility:hidden}} }}
    </style>
    <div id="splash-screen"><img src="{LOGO_SVG}" width="120"><h1>Ha Ha only</h1></div>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

with st.sidebar:
    st.image(LOGO_SVG, width=100)
    if not st.session_state.logged_in:
        mode = st.radio("Action", ["Login", "Sign Up"])
        u = st.text_input("Username")
        em = st.text_input("Email") if mode == "Sign Up" else ""
        p = st.text_input("Password", type="password")
        if st.button("Submit"):
            if mode == "Sign Up":
                try:
                    supabase.table("users").insert({"username": u, "password": hash_pw(p), "email": em}).execute()
                    st.success("Created! Please Login.")
                except: st.error("User exists or error.")
            else:
                res = supabase.table("users").select("*").eq("username", u).eq("password", hash_pw(p)).execute()
                if res.data:
                    st.session_state.logged_in, st.session_state.username = True, u
                    st.session_state.email = res.data[0].get('email', 'No Email')
                    st.rerun()
                else: st.error("Wrong info.")
    else:
        st.write(f"Logged in as: **{st.session_state.username}**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

# --- 5. GLOBAL FEED ---
st.title("🎬 Global Joy Feed")
try:
    vids = supabase.table("videos").select("*").order("id", desc=True).execute().data
    if not vids:
        st.info("No videos yet. Be the first to share joy! 📤")
    for v in vids:
        st.subheader(v['title'])
        st.video(v['url'])
        st.caption(f"By: @{v['uploader_name']} | 🤣 {v['haha_count']} laughs")
        st.divider()
except:
    st.warning("Connecting to database... please refresh.")
                    st.error("Please provide both a title and a link.")
