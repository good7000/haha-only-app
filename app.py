import streamlit as st
from supabase import create_client, Client
import hashlib
from datetime import datetime
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Ha Ha only 🤣", page_icon="🤣", layout="wide")

LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiByeD0iMTAwIiBmaWxsPSIjRkZEMzAwIi8+Cjx0ZXh0IHg9IjUwJSIgeT0iNjAlIiBmb250LXNpemU9IjI4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZpbGw9ImJsYWNrIj7wn6SjPC90ZXh0Pgo8L3N2Zz4="

# --- 2. SUPABASE CONNECTION ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except:
    st.error("Config missing in Secrets!")
    st.stop()

@st.cache_resource
def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

# --- 3. UI/CSS/SOUND ---
st.markdown(f"""
    <style>
    #splash-screen {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #FFD300; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 100000;
        animation: fadeOutSplash 2.5s forwards;
    }}
    @keyframes fadeOutSplash {{ 0% {{ opacity: 1; }} 80% {{ opacity: 1; }} 100% {{ opacity: 0; visibility: hidden; }} }}
    .floating-emoji {{ position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 120px; z-index: 9999; animation: fadeOutEmoji 0.8s ease-out forwards; pointer-events: none; }}
    @keyframes fadeOutEmoji {{ 0% {{ opacity: 0; scale: 0.3; }} 30% {{ opacity: 1; scale: 1.2; }} 100% {{ opacity: 0; scale: 2.5; }} }}
    </style>
    <div id="splash-screen"><img src="{LOGO_SVG}" style="width: 120px; border-radius: 20px;"><h1>Ha Ha only</h1></div>
    <audio id="haha-sound" src="https://www.soundjay.com/human/laughter-2.mp3" preload="auto"></audio>
    <script>function playHaha() {{ var sound = document.getElementById("haha-sound"); sound.currentTime = 0; sound.play(); }}</script>
    """, unsafe_allow_html=True)

# --- 4. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'show_emoji' not in st.session_state: st.session_state.show_emoji = False

def hash_pw(pw): return hashlib.sha256(str.encode(pw)).hexdigest()

# --- 5. SIDEBAR (User Area) ---
with st.sidebar:
    st.image(LOGO_SVG, width=100)
    st.title("User Zone")
    
    if not st.session_state.logged_in:
        mode = st.radio("Account", ["Login", "Sign Up"])
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Go"):
            if mode == "Sign Up":
                try:
                    supabase.table("users").insert({"username": u, "password": hash_pw(p)}).execute()
                    st.success("Account created! Logging you in...")
                    st.session_state.logged_in, st.session_state.username = True, u
                    st.rerun()
                except: st.error("Error creating account.")
            else:
                res = supabase.table("users").select("*").eq("username", u).eq("password", hash_pw(p)).execute()
                if res.data:
                    st.session_state.logged_in, st.session_state.username = True, u
                    st.rerun()
                else: st.error("Wrong login info!")
    else:
        st.success(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

# --- 6. MAIN CONTENT (Open for everyone) ---
if st.session_state.show_emoji:
    st.markdown('<div class="floating-emoji">🤣</div>', unsafe_allow_html=True)
    st.session_state.show_emoji = False

st.title("🎬 Live Joy Feed")

# التبويبات الرئيسية
tab1, tab2 = st.tabs(["🔥 Global Feed", "📤 Upload Joy"])

with tab1:
    vids = supabase.table("videos").select("*").order("id", desc=True).execute().data
    if not vids:
        st.info("No laughs yet. Be the first!")
    for v in vids:
        with st.container():
            st.subheader(v['title'])
            st.video(v['url'])
            c1, c2 = st.columns([3, 1])
            c1.caption(f"By: @{v['uploader_name'] or 'Guest'} | 🤣 {v['haha_count']} laughs")
            if c2.button(f"🤣 Ha Ha", key=v['id']):
                st.components.v1.html("<script>window.parent.playHaha();</script>", height=0)
                st.session_state.show_emoji = True
                supabase.table("videos").update({"haha_count": v['haha_count']+1}).eq("id", v['id']).execute()
                time.sleep(0.4)
                st.rerun()
        st.divider()

with tab2:
    if not st.session_state.logged_in:
        st.warning("⚠️ You must Login from the sidebar to upload your own videos!")
    else:
        with st.form("upload"):
            title = st.text_input("Title")
            url = st.text_input("Video URL (.mp4)")
            if st.form_submit_button("Post"):
                supabase.table("videos").insert({
                    "title": title, "url": url, 
                    "uploader_name": st.session_state.username
                }).execute()
                st.success("Shared!")
                time.sleep(1)
                st.rerun()
