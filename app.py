import streamlit as st
from supabase import create_client, Client
import hashlib
import time

# --- 1. CONFIG ---
st.set_page_config(page_title="Ha Ha only 🤣", page_icon="🤣", layout="wide")

# Logo
LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiByeD0iMTAwIiBmaWxsPSIjRkZEMzAwIi8+Cjx0ZXh0IHg9IjUwJSIgeT0iNjAlIiBmb250LXNpemU9IjI4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZpbGw9ImJsYWNrIj7wn6SjPC90ZXh0Pgo8L3N2Zz4="

# --- 2. CONNECTION ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error(f"Config error: {e}")
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
    .stVideo {{ border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }}
    </style>
    <div id="splash-screen"><img src="{LOGO_SVG}" width="120"><h1>Ha Ha only</h1></div>
    """, unsafe_allow_html=True)

# --- 4. AUTHENTICATION ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

with st.sidebar:
    st.image(LOGO_SVG, width=100)
    st.title("User Zone")
    if not st.session_state.logged_in:
        mode = st.radio("Action", ["Login", "Sign Up"])
        u = st.text_input("Username").strip()
        em = st.text_input("Email").strip() if mode == "Sign Up" else ""
        p = st.text_input("Password", type="password")
        if st.button("Go"):
            if mode == "Sign Up":
                try:
                    supabase.table("users").insert({"username": u, "password": hash_pw(p), "email": em}).execute()
                    st.success("Created! Now Login.")
                except Exception as e: st.error(f"Error: {e}")
            else:
                res = supabase.table("users").select("*").eq("username", u).eq("password", hash_pw(p)).execute()
                if res.data:
                    st.session_state.logged_in, st.session_state.username = True, u
                    st.session_state.email = res.data[0].get('email', 'Guest')
                    st.rerun()
                else: st.error("Wrong details.")
    else:
        st.success(f"Hi {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

# --- 5. CONTENT TABS ---
st.title("🎬 Global Joy Feed")
tab1, tab2 = st.tabs(["🔥 Watch", "📤 Upload"])

with tab1:
    try:
        vids = supabase.table("videos").select("*").order("id", desc=True).execute().data
        if not vids: st.info("Feed is empty.")
        for v in vids:
            st.subheader(v['title'])
            st.video(v['url'])
            st.caption(f"By: @{v['uploader_name']} | 🤣 {v.get('haha_count', 0)}")
            st.divider()
    except Exception as e: st.warning(f"Connection issue: {e}")

with tab2:
    if not st.session_state.logged_in: st.warning("Login to upload.")
    else:
        with st.form("upload"):
            t = st.text_input("Title")
            url = st.text_input("Video URL (.mp4)")
            if st.form_submit_button("Post"):
                supabase.table("videos").insert({"title": t, "url": url, "uploader_name": st.session_state.username}).execute()
                st.success("Shared!")
                time.sleep(1)
                st.rerun()
