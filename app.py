import streamlit as st
from supabase import create_client, Client
import hashlib
from datetime import datetime
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Ha Ha only 🤣", page_icon="🤣", layout="wide")

# Logo Icon (Yellow Square with Smile)
LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiByeD0iMTAwIiBmaWxsPSIjRkZEMzAwIi8+Cjx0ZXh0IHg9IjUwJSIgeT0iNjAlIiBmb250LXNpemU9IjI4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZpbGw9ImJsYWNrIj7wn6SjPC90ZXh0Pgo8L3N2Zz4="

# --- 2. SUPABASE CONNECTION ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("⚠️ Configuration Error: Please check your Streamlit Secrets.")
    st.stop()

# --- 3. UI/CSS & ANIMATIONS ---
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
    
    /* Floating Emoji Animation */
    .floating-emoji {{ position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 120px; z-index: 9999; animation: fadeOutEmoji 0.8s ease-out forwards; pointer-events: none; }}
    @keyframes fadeOutEmoji {{ 0% {{ opacity: 0; scale: 0.3; }} 30% {{ opacity: 1; scale: 1.2; }} 100% {{ opacity: 0; scale: 2.5; }} }}
    
    /* Global Styles */
    .stVideo {{ border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
    </style>
    
    <div id="splash-screen">
        <img src="{LOGO_SVG}" style="width: 130px; border-radius: 25px;">
        <h1 style="color: black; margin-top: 20px; font-family: sans-serif;">Ha Ha only</h1>
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

# --- 4. LOGIC FUNCTIONS ---
def hash_pw(pw): return hashlib.sha256(str.encode(pw)).hexdigest()

# --- 5. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'show_emoji' not in st.session_state: st.session_state.show_emoji = False

# --- 6. SIDEBAR (Login/Sign Up) ---
with st.sidebar:
    st.image(LOGO_SVG, width=100)
    st.title("User Zone")
    
    if not st.session_state.logged_in:
        mode = st.radio("Choose Action", ["Login", "Sign Up"])
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Go"):
            if mode == "Sign Up":
                try:
                    supabase.table("users").insert({"username": u, "password": hash_pw(p)}).execute()
                    st.success("Account created! Logging you in...")
                    st.session_state.logged_in, st.session_state.username = True, u
                    st.rerun()
                except: st.error("Error: Try a different username.")
            else:
                res = supabase.table("users").select("*").eq("username", u).eq("password", hash_pw(p)).execute()
                if res.data:
                    st.session_state.logged_in, st.session_state.username = True, u
                    st.rerun()
                else: st.error("Wrong credentials!")
    else:
        st.success(f"Hi, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

# --- 7. MAIN CONTENT (PUBLIC FEED) ---
if st.session_state.show_emoji:
    st.markdown('<div class="floating-emoji">🤣</div>', unsafe_allow_html=True)
    st.session_state.show_emoji = False

st.title("🎬 Global Joy Feed")
tab1, tab2 = st.tabs(["🔥 Watch & Laugh", "📤 Share Joy"])

with tab1:
    try:
        # Secure Data Fetching with Exception Handling
        vids_res = supabase.table("videos").select("*").order("id", desc=True).execute()
        vids = vids_res.data
    except Exception as e:
        st.warning("🔄 Connecting to the joy database... Please wait.")
        vids = []

    if not vids:
        st.info("No videos yet. Be the first to post! 📤")
    
    for v in vids:
        with st.container():
            st.subheader(v.get('title', 'Untitled Joy'))
            st.video(v['url'])
            c1, c2 = st.columns([3, 1])
            c1.caption(f"Creator: @{v.get('uploader_name', 'Guest')} | 🤣 {v.get('haha_count', 0)} Laughs")
            
            if c2.button(f"🤣 Ha Ha", key=f"btn_{v['id']}"):
                # Trigger Sound & Emoji
                st.components.v1.html("<script>window.parent.playHaha();</script>", height=0)
                st.session_state.show_emoji = True
                
                # Update Count in Database
                try:
                    new_count = v.get('haha_count', 0) + 1
                    supabase.table("videos").update({"haha_count": new_count}).eq("id", v['id']).execute()
                except: pass
                
                time.sleep(0.4)
                st.rerun()
        st.divider()

with tab2:
    if not st.session_state.logged_in:
        st.warning("⚠️ Please Login from the sidebar to upload your own videos!")
    else:
        st.subheader("Upload a New Video")
        with st.form("upload_form", clear_on_submit=True):
            t = st.text_input("Title (e.g. Funniest cat ever!)")
            url = st.text_input("Direct Video Link (.mp4 only)")
            if st.form_submit_button("Post to Global Feed 🚀"):
                if t and url:
                    try:
                        supabase.table("videos").insert({
                            "title": t, "url": url, 
                            "uploader_name": st.session_state.username
                        }).execute()
                        st.success("Shared successfully! Go to the Feed to see it.")
                        time.sleep(1)
                        st.rerun()
                    except: st.error("Database connection error.")
                else:
                    st.error("Please fill in both fields.")
