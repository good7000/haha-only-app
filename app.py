import streamlit as st
from supabase import create_client, Client
import hashlib
import time

# --- 1. DIRECT CONNECTION (No Secrets Required) ---
# We put the keys here directly so the app works immediately
URL = "https://bjzievktdyjtnkjghjll.supabase.co"
KEY = "sb_secret_DdkncknmDlgIUvaWAGlpRA_sPXPnjMt"

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(page_title="Ha Ha only 🤣", page_icon="🤣", layout="wide")

LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiByeD0iMTAwIiBmaWxsPSIjRkZEMzAwIi8+Cjx0ZXh0IHg9IjUwJSIgeT0iNjAlIiBmb250LXNpemU9IjI4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZpbGw9ImJsYWNrIj7wn6SjPC90ZXh0Pgo8L3N2Zz4="

@st.cache_resource
def init_db():
    try:
        return create_client(URL, KEY)
    except:
        return None

supabase = init_db()
def hash_pw(pw): return hashlib.sha256(str.encode(pw)).hexdigest()

# --- 3. UI STYLE, ANIMATIONS & SOUND ---
st.markdown(f"""
    <style>
    /* Yellow Splash Screen */
    #splash-screen {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #FFD300; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 100000;
        animation: fadeOut 2.5s forwards;
    }}
    @keyframes fadeOut {{ 0% {{opacity:1}} 80% {{opacity:1}} 100% {{opacity:0; visibility:hidden}} }}
    
    /* Flying Emoji */
    .floating-emoji {{ 
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
        font-size: 150px; z-index: 9999; animation: emojiAnim 1s ease-out forwards; 
        pointer-events: none;
    }}
    @keyframes emojiAnim {{ 0% {{opacity:0; scale:0.5;}} 30% {{opacity:1; scale:1.2;}} 100% {{opacity:0; scale:3;}} }}
    .stVideo {{ border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
    </style>
    
    <div id="splash-screen">
        <img src="{LOGO_SVG}" width="150" style="border-radius: 30px;">
        <h1 style="color: black; margin-top: 20px;">Ha Ha only</h1>
    </div>

    <audio id="laugh-sound" src="https://www.soundjay.com/human/laughter-2.mp3" preload="auto"></audio>
    <script>
    function playLaugh() {{
        var audio = document.getElementById("laugh-sound");
        audio.currentTime = 0; audio.play();
    }}
    </script>
    """, unsafe_allow_html=True)

# --- 4. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'emoji_trigger' not in st.session_state: st.session_state.emoji_trigger = False

# --- 5. SIDEBAR (User System) ---
with st.sidebar:
    st.image(LOGO_SVG, width=100)
    st.title("User Zone")
    if not st.session_state.logged_in:
        mode = st.radio("Action", ["Login", "Sign Up"])
        u = st.text_input("Username").strip()
        em = st.text_input("Email Address").strip() if mode == "Sign Up" else ""
        p = st.text_input("Password", type="password")
        if st.button("Submit"):
            if mode == "Sign Up":
                try:
                    supabase.table("users").insert({"username": u, "password": hash_pw(p), "email": em}).execute()
                    st.success("Success! Now Login.")
                except Exception as e: st.error(f"Error: {e}")
            else:
                res = supabase.table("users").select("*").eq("username", u).eq("password", hash_pw(p)).execute()
                if res.data:
                    st.session_state.logged_in, st.session_state.username = True, u
                    st.session_state.email = res.data[0].get('email', 'User')
                    st.rerun()
                else: st.error("Wrong info!")
    else:
        st.success(f"Hi {st.session_state.username}!")
        st.caption(f"📧 {st.session_state.email}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

# --- 6. FEED ---
if st.session_state.emoji_trigger:
    st.markdown('<div class="floating-emoji">🤣</div>', unsafe_allow_html=True)
    st.session_state.emoji_trigger = False

st.title("🎬 Ha Ha only Feed")
tab1, tab2 = st.tabs(["🔥 Watch & Laugh", "📤 Share Joy"])

with tab1:
    try:
        vids = supabase.table("videos").select("*").order("id", desc=True).execute().data
        if not vids: st.info("No videos yet.")
        for v in vids:
            st.subheader(v.get('title'))
            st.video(v['url'])
            c1, c2 = st.columns([4, 1])
            c1.caption(f"By: @{v.get('uploader_name')} | 🤣 {v.get('haha_count', 0)} laughs")
            if c2.button(f"🤣 Ha Ha", key=f"btn_{v['id']}"):
                st.components.v1.html("<script>window.parent.playLaugh();</script>", height=0)
                st.session_state.emoji_trigger = True
                new_c = v.get('haha_count', 0) + 1
                supabase.table("videos").update({"haha_count": new_c}).eq("id", v['id']).execute()
                time.sleep(0.5); st.rerun()
            st.divider()
    except Exception as e: st.warning("Loading joy...")

with tab2:
    if not st.session_state.logged_in: st.warning("Please Login to upload.")
    else:
        with st.form("up", clear_on_submit=True):
            tit = st.text_input("Title")
            v_url = st.text_input("Video URL (.mp4)")
            if st.form_submit_button("Post Joy 🚀"):
                supabase.table("videos").insert({"title": tit, "url": v_url, "uploader_name": st.session_state.username}).execute()
                st.success("Shared!"); time.sleep(1); st.rerun()
