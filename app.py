import streamlit as st
import time

# --- 1. إعدادات الصفحة والهوية ---
st.set_page_config(page_title="Ha Ha only 🤣", page_icon="🤣", layout="wide")

LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiByeD0iMTAwIiBmaWxsPSIjRkZEMzAwIi8+Cjx0ZXh0IHg9IjUwJSIgeT0iNjAlIiBmb250LXNpemU9IjI4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZpbGw9ImJsYWNrIj7wn6SjPC90ZXh0Pgo8L3N2Zz4="

# --- 2. التصميم، الشريط الأصفر، وتأثير تيك توك ---
st.markdown(f"""
    <style>
    /* شاشة التحميل */
    #splash-screen {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #FFD300; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 100000;
        animation: fadeOutSplash 2.5s forwards;
    }}
    @keyframes fadeOutSplash {{ 0% {{opacity:1}} 80% {{opacity:1}} 100% {{opacity:0; visibility:hidden}} }}
    
    /* شريط تحميل التطبيق */
    .app-download-banner {{
        background: #1E1E1E; color: #FFD300; padding: 10px;
        text-align: center; font-weight: bold; border-radius: 10px;
        border: 2px solid #FFD300; margin-bottom: 10px;
    }}

    /* الشريط الأصفر المتحرك */
    .yellow-bar {{
        background-color: #FFD300; color: black; padding: 10px 0;
        font-weight: bold; font-size: 18px; overflow: hidden;
        white-space: nowrap; border-radius: 10px; margin-bottom: 20px;
    }}
    .marquee {{ display: inline-block; padding-left: 100%; animation: marquee 15s linear infinite; }}
    @keyframes marquee {{ 0% {{ transform: translate(0, 0); }} 100% {{ transform: translate(-100%, 0); }} }}

    /* الإيموجي المتطاير */
    .floating-emoji {{ 
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
        font-size: 180px; z-index: 9999; animation: emojiAnim 1s ease-out forwards; 
        pointer-events: none;
    }}
    @keyframes emojiAnim {{ 0% {{opacity:0; scale:0.5;}} 30% {{opacity:1; scale:1.3;}} 100% {{opacity:0; scale:4;}} }}
    
    .stVideo {{ border-radius: 25px; border: 5px solid #FFD300; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
    </style>
    
    <div id="splash-screen">
        <img src="{LOGO_SVG}" width="150" style="border-radius: 30px;">
        <h1 style="color: black; margin-top: 20px;">Ha Ha only</h1>
    </div>

    <div class="app-download-banner">
        📲 Want the full experience? Click ⋮ -> "Add to Home Screen" to install Ha Ha only!
    </div>

    <div class="yellow-bar">
        <div class="marquee">Welcome to Ha Ha only! 🤣 The TikTok of Joy! 🤣 Autoplay is ON! 🚀 Upload and laugh! 🤣</div>
    </div>

    <audio id="haha-sound" src="https://www.soundjay.com/human/laughter-2.mp3" preload="auto"></audio>
    <script>
    function playHaha() {{
        var audio = document.getElementById("haha-sound");
        audio.currentTime = 0; audio.play();
    }}
    </script>
    """, unsafe_allow_html=True)

# --- 3. إدارة البيانات المؤقتة ---
if 'joy_feed' not in st.session_state:
    st.session_state.joy_feed = [
        {"title": "Welcome Joy! 🤣", "url": "https://www.w3schools.com/html/mov_bbb.mp4", "likes": 50, "comment": "TikTok style activated!"}
    ]
if 'emoji_trigger' not in st.session_state: st.session_state.emoji_trigger = False

# --- 4. القائمة الجانبية (الأدمن والدعم) ---
with st.sidebar:
    st.image(LOGO_SVG, width=120)
    st.title("Ha Ha only")
    
    # زر الدعم
    st.markdown("""
    <a href="https://www.buymeacoffee.com" target="_blank">
        <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 50px; width: 180px;">
    </a>
    """, unsafe_allow_html=True)
    
    st.divider()
    with st.expander("🔐 Admin Controls"):
        admin_pw = st.text_input("Password", type="password")
        if admin_pw == "admin123":
            video_list = [v['title'] for v in st.session_state.joy_feed]
            to_delete = st.selectbox("Select Video to Remove", video_list)
            if st.button("🗑️ Delete Selected"):
                st.session_state.joy_feed = [v for v in st.session_state.joy_feed if v['title'] != to_delete]
                st.rerun()

# --- 5. العرض الرئيسي (تفاعل تيك توك) ---
if st.session_state.emoji_trigger:
    st.markdown('<div class="floating-emoji">🤣</div>', unsafe_allow_html=True)
    st.session_state.emoji_trigger = False

st.title("🎬 Global Smile Feed")
t1, t2 = st.tabs(["🔥 Watch", "📤 Post Joy"])

with t1:
    for i, v in enumerate(st.session_state.joy_feed[::-1]):
        st.subheader(v['title'])
        # تفعيل Autoplay, Muted, Loop لمحاكاة تيك توك
        st.video(v['url'], format="video/mp4", start_time=0, autoplay=True, muted=True, loop=True)
        
        c1, c2, c3 = st.columns([3, 1, 1])
        c1.write(f"💬 {v['comment']}")
        c1.caption(f"🤣 {v['likes']} Laughs")
        
        with c2:
            # زر هاها مع الصوت
            if st.button(f"🤣 Ha Ha", key=f"l_{i}"):
                st.components.v1.html("<script>window.parent.playHaha();</script>", height=0)
                st.session_state.emoji_trigger = True
                v['likes'] += 1
                time.sleep(0.4); st.rerun()
        
        with c3:
            if st.button(f"🚩 Report", key=f"r_{i}"):
                st.warning("Reported!")
        st.divider()

with t2:
    st.subheader("Share Joy with the World! 📤")
    with st.form("public_post", clear_on_submit=True):
        t = st.text_input("Video Title")
        u = st.text_input("Video Link (.mp4 only)")
        c = st.text_area("Say something funny...")
        if st.form_submit_button("Post 🚀"):
            if t and u:
                st.session_state.joy_feed.append({"title": t, "url": u, "likes": 0, "comment": c})
                st.success("Live now!")
                time.sleep(1); st.rerun()
