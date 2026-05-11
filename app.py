import streamlit as st
from supabase import create_client, Client
import hashlib
from datetime import datetime
import time

# --- 1. PAGE CONFIG & BRANDING ---
st.set_page_config(page_title="Ha Ha only 🤣", page_icon="🤣", layout="wide")

# Embedded SVG Logo (Yellow Square with Smile)
LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiByeD0iMTAwIiBmaWxsPSIjRkZEMzAwIi8+Cjx0ZXh0IHg9IjUwJSIgeT0iNjAlIiBmb250LXNpemU9IjI4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZpbGw9ImJsYWNrIj7wn6SjPC90ZXh0Pgo8L3N2Zz4="

# --- 2. SUPABASE CONNECTION (VIA SECRETS) ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except:
    st.error("⚠️ Config Error! Please add SUPABASE_URL and SUPABASE_KEY in Settings > Secrets.")
    st.stop()

@st.cache_resource
def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

# --- 3. UI DESIGN (CSS & JAVASCRIPT) ---
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
    
    /* Floating Emoji Animation */
    @keyframes fadeOutEmoji {{ 
        0% {{ opacity: 0; transform: translate(-50%, -50%) scale(0.3); }} 
        30% {{ opacity: 1; transform: translate(-50%, -50%) scale(1.2); }} 
        100% {{ opacity: 0; transform: translate(-50%, -50%) scale(2.5); }} 
    }}
    .floating-emoji {{ position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 120px; z-index: 9999; animation: fadeOutEmoji 0.8s ease-out forwards; pointer-events: none; }}
    
    /* Golden Support Button */
    .stButton>button:nth-child(1) {{
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: black !important; font-weight: bold !important; border: none !important;
    }}
    </style>
    
    <div id="splash-screen">
        <img src="{LOGO_SVG}" style="width: 150px; border-radius: 30px;">
        <h1 style="color: black; margin-top: 20px; font-family: sans-serif;">Ha Ha only</h1>
        <p style="color: black; font-weight: bold;">Loading Smiles... 🤣</p>
    </div>

    <audio id="haha-sound" src="https://www.soundjay.com/human/laughter-2.mp3" preload="auto"></audio>
    <script>
    function playHaha() {{
        var sound = document.getElementById("haha-sound");
        sound.currentTime = 0; sound.play();
    }}
    </script>
    """, unsafe_allow_html=True)

# --- 4. LOGIC FUNCTIONS ---
def hash_pw(pw): return hashlib.sha256(str.encode(pw)).hexdigest()

def add_notif(target, content):
    now = datetime.now().strftime("%H:%M")
    supabase.table("notifications").insert({"target_user": target, "content": content, "timestamp": now}).execute()

# --- 5. SESSION MANAGEMENT ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'show_emoji' not in st.session_state: st.session_state.show_emoji = False

# --- 6. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image(LOGO_SVG, width=120)
    if st.session_state.logged_in:
        st.success(f"Hello, {st.session_state.username}!")
        nav = st.radio("Menu", ["🎬 Live Feed", "🏆 Leaders", "🔔 Notifications", "📤 Upload Joy"])
        st.divider()
        if st.button("☕ Support Us"):
            st.info("Redirecting to support page...")
        if st.button("🚪 Logout"): 
            st.session_state.logged_in = False
            st.rerun()
    else:
        st.subheader("Join the Laughter")
        mode = st.radio("Account", ["Login", "Sign Up"])
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Go"):
            if mode == "Sign Up":
                try:
                    supabase.table("users").insert({"username": u, "password": hash_pw(p), "email": f"{u}@haha.com"}).execute()
                    st.success("Account created! Please login.")
                except: st.error("Username already exists!")
            else:
                res = supabase.table("users").select("*").eq("username", u).eq("password", hash_pw(p)).execute()
                if res.data:
                    st.session_state.logged_in, st.session_state.username = True, u
                    st.rerun()
                else: st.error("Invalid credentials!")

# --- 7. MAIN CONTENT ---
if st.session_state.logged_in:
    if st.session_state.show_emoji:
        st.markdown('<div class="floating-emoji">🤣</div>', unsafe_allow_html=True)
        st.session_state.show_emoji = False

    if nav == "🎬 Live Feed":
        st.title("🎬 Joy Feed")
        vids = supabase.table("videos").select("*").order("id", desc=True).execute().data
        if not vids:
            st.info("No videos yet. Be the first to share joy! 📤")
        for v in vids:
            with st.container():
                st.subheader(v['title'])
                st.video(v['url'])
                c1, c2 = st.columns([3, 1])
                c1.caption(f"By @{v['uploader_name']} | 🤣 {v['haha_count']} Laughs")
                if c2.button(f"🤣 Ha Ha", key=f"v_{v['id']}"):
                    st.components.v1.html("<script>window.parent.playHaha();</script>", height=0)
                    st.session_state.show_emoji = True
                    supabase.table("videos").update({"haha_count": v['haha_count'] + 1}).eq("id", v['id']).execute()
                    if v['uploader_name'] != st.session_state.username:
                        add_notif(v['uploader_name'], f"🤣 {st.session_state.username} laughed at your video!")
                    time.sleep(0.4); st.rerun()
            st.divider()

    elif nav == "📤 Upload Joy":
        st.title("📤 Share a Laugh")
        with st.form("upload"):
            t = st.text_input("Video Title")
            url = st.text_input("Direct Video Link (MP4)")
            if st.form_submit_button("Post Now 🚀"):
                if t and url:
                    supabase.table("videos").insert({"title": t, "url": url, "uploader_name": st.session_state.username}).execute()
                    st.success("Successfully posted!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Please fill all fields!")
