import streamlit as st
from supabase import create_client, Client
import hashlib
import time

# --- 1. الربط المباشر بقاعدة البيانات (لحل مشكلة الخطأ -2) ---
URL = "https://bjzievktdyjtnkjghjll.supabase.co"
KEY = "sb_secret_DdkncknmDlgIUvaWAGlpRA_sPXPnjMt"

@st.cache_resource
def init_db():
    return create_client(URL, KEY)

supabase = init_db()

# --- 2. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="Ha Ha only 🤣", page_icon="🤣", layout="wide")

LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiByeD0iMTAwIiBmaWxsPSIjRkZEMzAwIi8+Cjx0ZXh0IHg9IjUwJSIgeT0iNjAlIiBmb250LXNpemU9IjI4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZpbGw9ImJsYWNrIj7wn6SjPC90ZXh0Pgo8L3N2Zz4="

st.markdown(f"""
    <style>
    /* شاشة التحميل الصفراء */
    #splash-screen {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #FFD300; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 100000;
        animation: fadeOut 2.5s forwards;
    }}
    @keyframes fadeOut {{ 0% {{opacity:1}} 80% {{opacity:1}} 100% {{opacity:0; visibility:hidden}} }}
    
    /* الشريط الأصفر المتحرك */
    .marquee {{
        background-color: #FFD300; color: black; padding: 10px;
        font-weight: bold; white-space: nowrap; overflow: hidden; border-radius: 10px;
    }}
    .marquee div {{ display: inline-block; animation: scroll 15s linear infinite; padding-left: 100%; }}
    @keyframes scroll {{ 0% {{transform: translateX(0);}} 100% {{transform: translateX(-100%);}} }}

    /* الإيموجي المتطاير */
    .emoji-fly {{ position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 150px; z-index: 9999; animation: fly 0.8s ease-out forwards; }}
    @keyframes fly {{ 0% {{opacity:0; scale:0.5}} 30% {{opacity:1; scale:1.2}} 100% {{opacity:0; scale:3}} }}
    </style>
    
    <div id="splash-screen"><img src="{LOGO_SVG}" width="150"><h1>Ha Ha only</h1></div>
    
    <div class="marquee"><div>Welcome to Ha Ha only! Share your funny videos and spread the joy! 🤣 🚀 🤣</div></div>

    <audio id="haha-sound" src="https://www.soundjay.com/human/laughter-2.mp3" preload="auto"></audio>
    <script>function playHaha() {{ var s = document.getElementById("haha-sound"); s.currentTime=0; s.play(); }}</script>
    """, unsafe_allow_html=True)

# --- 3. إدارة الجلسة ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'show_emoji' not in st.session_state: st.session_state.show_emoji = False

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.image(LOGO_SVG, width=100)
    if not st.session_state.logged_in:
        st.subheader("Join the Fun")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            res = supabase.table("users").select("*").eq("username", u).execute()
            if res.data:
                st.session_state.logged_in, st.session_state.username = True, u
                st.rerun()
            else: st.error("User not found!")
    else:
        st.success(f"Hi {st.session_state.username}!")
        nav = st.radio("Go to", ["🎬 Feed", "📤 Upload"])
        st.markdown("[☕ Buy us a Coffee](https://www.buymeacoffee.com)")
        if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

# --- 5. المحتوى الرئيسي ---
if st.session_state.show_emoji:
    st.markdown('<div class="emoji-fly">🤣</div>', unsafe_allow_html=True)
    st.session_state.show_emoji = False

if st.session_state.logged_in or st.checkbox("Browse as Guest"):
    tab = "🎬 Feed" if 'nav' not in locals() else nav
    
    if tab == "🎬 Feed":
        vids = supabase.table("videos").select("*").order("id", desc=True).execute().data
        for v in vids:
            st.subheader(v['title'])
            st.video(v['url'])
            c1, c2, c3 = st.columns([2,1,1])
            if c1.button(f"🤣 Ha Ha", key=v['id']):
                st.components.v1.html("<script>window.parent.playHaha();</script>", height=0)
                st.session_state.show_emoji = True
                supabase.table("videos").update({"haha_count": v.get('haha_count', 0)+1}).eq("id", v['id']).execute()
                time.sleep(0.4); st.rerun()
            c2.markdown(f'[📥 Download]({v["url"]})')
            if c3.button("🚩 Report", key=f"r{v['id']}"): st.warning("Reported!")
            st.divider()
            
    elif tab == "📤 Upload":
        with st.form("up"):
            title = st.text_input("Title")
            url = st.text_input("Direct MP4 Link")
            if st.form_submit_button("Post Joy 🚀"):
                supabase.table("videos").insert({"title": title, "url": url, "uploader_name": st.session_state.username}).execute()
                st.success("Posted!"); time.sleep(1); st.rerun()
