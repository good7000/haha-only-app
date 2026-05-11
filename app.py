import streamlit as st
from supabase import create_client, Client
import hashlib
import time

# --- 1. DATABASE CONFIGURATION (Supabase) ---
# ملاحظة: تم استخدام القيم الخاصة بك لضمان الربط المباشر
SUPABASE_URL = "https://bjzievktdyjtnkjghjll.supabase.co"
SUPABASE_KEY = "sb_secret_DdkncknmDlgIUvaWAGlpRA_sPXPnjMt"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

def hash_pw(pw):
    return hashlib.sha256(str.encode(pw)).hexdigest()

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(page_title="Ha Ha only 🤣", page_icon="🤣", layout="wide")

# --- 3. UI & AESTHETICS (CSS / JS) ---
LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiByeD0iMTAwIiBmaWxsPSIjRkZEMzAwIi8+Cjx0ZXh0IHg9IjUwJSIgeT0iNjAlIiBmb250LXNpemU9IjI4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZpbGw9ImJsYWNrIj7wn6SjPC90ZXh0Pgo8L3N2Zz4="

st.markdown(f"""
    <style>
    /* Golden Support Button */
    .stButton>button {{
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: black !important; font-weight: bold !important; border-radius: 12px;
        transition: 0.3s;
    }}
    .stButton>button:hover {{ transform: scale(1.05); }}
    
    /* Splash Screen Animation */
    #splash-screen {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #FFD300; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 100000;
        animation: fadeOutSplash 2.5s forwards;
    }}
    @keyframes fadeOutSplash {{ 0% {{ opacity: 1; }} 80% {{ opacity: 1; }} 100% {{ opacity: 0; visibility: hidden; }} }}
    
    /* Floating Emoji */
    .floating-emoji {{ 
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
        font-size: 120px; z-index: 9999; animation: emojiAnim 0.8s ease-out forwards; 
        pointer-events: none; 
    }}
    @keyframes emojiAnim {{ 
        0% {{ opacity: 0; scale: 0.3; }} 
        30% {{ opacity: 1; scale: 1.2; }} 
        100% {{ opacity: 0; scale: 2.5; }} 
    }}
    
    .install-banner {{ display: flex; align-items: center; background-color: #1E1E1E; padding: 15px; border-radius: 12px; border: 2px solid #FFD300; margin-bottom: 25px; color: white; }}
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

# --- 4. SESSION MANAGEMENT ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'is_guest' not in st.session_state: st.session_state.is_guest = False
if 'show_emoji' not in st.session_state: st.session_state.show_emoji = False

# --- 5. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image(LOGO_SVG, width=120)
    st.title("Ha Ha only")
    
    if st.session_state.logged_in:
        nav = st.radio("Navigation", ["🎬 Live Feed", "🏆 Leaders", "📤 Upload Joy"])
        st.divider()
        st.write("Support the platform ⬇️ ☺️")
        if st.button("☕ Buy us a Coffee", use_container_width=True):
            st.markdown("[Click here to Support ☺️](https://www.buymeacoffee.com)")
            
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False; st.rerun()
            
    elif st.session_state.is_guest:
        nav = st.radio("Navigation", ["🎬 Live Feed", "🏆 Leaders"])
        if st.button("🔐 Login / Join"): st.session_state.is_guest = False; st.rerun()
        
    else:
        auth_mode = st.tabs(["Login", "Sign Up"])
        
        with auth_mode[0]: # Login
            u_in = st.text_input("Username", key="login_u")
            p_in = st.text_input("Password", type="password", key="login_p")
            if st.button("Login"):
                res = supabase.table("users").select("*").eq("username", u_in).eq("password", hash_pw(p_in)).execute()
                if res.data:
                    st.session_state.logged_in, st.session_state.username = True, u_in
                    st.rerun()
                else: st.error("Wrong Username or Password")
        
        with auth_mode[1]: # Sign Up
            new_u = st.text_input("Choose Username")
            new_e = st.text_input("Email Address")
            new_p = st.text_input("Choose Password", type="password")
            if st.button("Create Account"):
                if new_u and new_p and new_e:
                    try:
                        supabase.table("users").insert({
                            "username": new_u, 
                            "email": new_e, 
                            "password": hash_pw(new_p)
                        }).execute()
                        st.success("Account created! Please Login.")
                    except: st.error("Username already exists!")
                else: st.warning("Please fill all fields")
                
        if st.button("🕶️ Guest Mode"): st.session_state.is_guest = True; st.rerun()

# --- 6. MAIN CONTENT ---
if st.session_state.logged_in or st.session_state.is_guest:
    
    st.markdown("""<div class="install-banner"><span>📲</span><div><b>Elite Experience</b><br><small>Add Ha Ha only to Home Screen ⬇️ ☺️</small></div></div>""", unsafe_allow_html=True)

    if st.session_state.show_emoji:
        st.markdown('<div class="floating-emoji">🤣</div>', unsafe_allow_html=True)
        st.session_state.show_emoji = False

    if nav == "🎬 Live Feed":
        st.title("🎬 Global Smile Feed")
        try:
            vids = supabase.table("videos").select("*").order("id", desc=True).execute().data
            if not vids: st.info("No videos yet. Be the first to post!")
            for v in vids:
                with st.container():
                    st.subheader(v['title'])
                    st.video(v['url'])
                    c1, c2 = st.columns([3, 1])
                    c1.caption(f"By @{v.get('uploader_name', 'Guest')} | 🤣 {v.get('haha_count', 0)} Laughter")
                    with c2:
                        if st.session_state.logged_in:
                            if st.button(f"🤣 Ha Ha", key=f"h_{v['id']}"):
                                st.components.v1.html("<script>window.parent.playHaha();</script>", height=0)
                                st.session_state.show_emoji = True
                                new_count = v.get('haha_count', 0) + 1
                                supabase.table("videos").update({"haha_count": new_count}).eq("id", v['id']).execute()
                                time.sleep(0.4); st.rerun()
                st.divider()
        except: st.error("Connection Error! Check Supabase connectivity.")

    elif nav == "📤 Upload Joy":
        st.title("📤 Share Your Joy")
        with st.form("upload_form", clear_on_submit=True):
            v_title = st.text_input("Title of the Joy")
            v_url = st.text_input("Direct Video Link (.mp4)")
            if st.form_submit_button("Post to World 🚀"):
                if v_title and v_url:
                    supabase.table("videos").insert({
                        "title": v_title, 
                        "url": v_url, 
                        "uploader_name": st.session_state.username,
                        "haha_count": 0
                    }).execute()
                    st.success("Your joy is now live!")
                    time.sleep(1); st.rerun()
                else: st.warning("Please fill all fields")

    elif nav == "🏆 Leaders":
        st.title("🏆 Hall of Laughter")
        st.info("The top viral videos will appear here soon!")

else:
    st.info("Welcome to Ha Ha only! Please Login or Browse as a Guest. 🤣")
