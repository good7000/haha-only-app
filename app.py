import streamlit as st
from supabase import create_client, Client
import hashlib
import time

# --- 1. PAGE CONFIG & BRANDING ---
st.set_page_config(page_title="Ha Ha only 🤣", page_icon="🤣", layout="wide")

# Logo (Yellow Square with Smile)
LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiByeD0iMTAwIiBmaWxsPSIjRkZEMzAwIi8+Cjx0ZXh0IHg9IjUwJSIgeT0iNjAlIiBmb250LXNpemU9IjI4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZpbGw9ImJsYWNrIj7wn6SjPC90ZXh0Pgo8L3N2Zz4="

# --- 2. SECURE CONNECTION ---
@st.cache_resource
def get_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except:
        return None

supabase = get_supabase()

def hash_pw(pw): return hashlib.sha256(str.encode(pw)).hexdigest()

# --- 3. UI STYLE, ANIMATIONS & SOUND ---
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
    .floating-emoji {{ 
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
        font-size: 150px; z-index: 9999; animation: emojiAnim 1s ease-out forwards; 
        pointer-events: none; 
    }}
    @keyframes emojiAnim {{ 0% {{ opacity: 0; scale: 0.5; }} 30% {{ opacity: 1; scale: 1.2; }} 100% {{ opacity: 0; scale: 3; }} }}

    /* Video Styling */
    .stVideo {{ border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
    </style>
    
    <div id="splash-screen">
        <img src="{LOGO_SVG}" width="150" style="border-radius: 30px;">
        <h1 style="color: black; font-family: sans-serif; margin-top: 20px;">Ha Ha only</h1>
    </div>

    <audio id="haha-audio" src="https://www.soundjay.com/human/laughter-2.mp3" preload="auto"></audio>
    <script>
    function playLaugh() {{
        var audio = document.getElementById("haha-audio");
        audio.currentTime = 0;
        audio.play();
    }}
    </script>
    """, unsafe_allow_html=True)

# --- 4. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'emoji_trigger' not in st.session_state: st.session_state.emoji_trigger = False

# --- 5. SIDEBAR (User Zone with Email) ---
with st.sidebar:
    st.image(LOGO_SVG, width=100)
    st.title("User Zone 👤")
    
    if not st.session_state.logged_in:
        mode = st.radio("Action", ["Login", "Sign Up"])
        u = st.text_input("Username").strip()
        
        email_val = ""
        if mode == "Sign Up":
            email_val = st.text_input("Email Address").strip()
            
        p = st.text_input("Password", type="password")
        
        if st.button("Submit"):
            if not supabase:
                st.error("Connection issue. Please fix your Secrets!")
            elif mode == "Sign Up":
                if u and p and email_val:
                    try:
                        supabase.table("users").insert({"username": u, "password": hash_pw(p), "email": email_val}).execute()
                        st.success("Account created! Now please Login.")
                    except Exception as e: st.error(f"Error: {e}")
                else: st.warning("Please fill all fields (Username, Email, Password).")
            else:
                res = supabase.table("users").select("*").eq("username", u).eq("password", hash_pw(p)).execute()
                if res.data:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.session_state.email = res.data[0].get('email', 'Member')
                    st.rerun()
                else: st.error("Wrong Username or Password.")
    else:
        st.success(f"Hello, {st.session_state.username}!")
        st.caption(f"📧 {st.session_state.email}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

# --- 6. MAIN FEED ---
if st.session_state.emoji_trigger:
    st.markdown('<div class="floating-emoji">🤣</div>', unsafe_allow_html=True)
    st.session_state.emoji_trigger = False

st.title("🎬 Ha Ha only Feed")
tab1, tab2 = st.tabs(["🔥 Watch & Laugh", "📤 Share Joy"])

with tab1:
    if not supabase:
        st.error("⚠️ Database not reachable. Ensure SUPABASE_URL in Secrets is correct.")
    else:
        try:
            vids = supabase.table("videos").select("*").order("id", desc=True).execute().data
            if not vids:
                st.info("No videos shared yet. Be the first!")
            for v in vids:
                st.subheader(v.get('title', 'Untitled Joy'))
                st.video(v['url'])
                col1, col2 = st.columns([4, 1])
                col1.caption(f"By: @{v.get('uploader_name', 'Guest')} | 🤣 {v.get('haha_count', 0)} laughs")
                
                if col2.button(f"🤣 Ha Ha", key=f"btn_{v['id']}"):
                    # Trigger Sound & Visual Animation
                    st.components.v1.html("<script>window.parent.playLaugh();</script>", height=0)
                    st.session_state.emoji_trigger = True
                    
                    # Update Haha counter
                    new_count = v.get('haha_count', 0) + 1
                    try:
                        supabase.table("videos").update({"haha_count": new_count}).eq("id", v['id']).execute()
                    except: pass
                    
                    time.sleep(0.5)
                    st.rerun()
                st.divider()
        except Exception as e:
            st.warning(f"🔄 Reconnecting to Ha Ha server... (Error: {e})")

with tab2:
    if not st.session_state.logged_in:
        st.warning("⚠️ Please Login from the sidebar to upload videos.")
    else:
        st.subheader("Upload Your Joy 📤")
        with st.form("upload_form", clear_on_submit=True):
            t = st.text_input("Video Title")
            url = st.text_input("Direct .mp4 Video Link")
            if st.form_submit_button("Post Joy 🚀"):
                if t and url:
                    try:
                        supabase.table("videos").insert({
                            "title": t, "url": url, 
                            "uploader_name": st.session_state.username,
                            "haha_count": 0
                        }).execute()
                        st.success("Successfully posted!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to post: {e}")
                else:
                    st.error("Title and URL are required!")
