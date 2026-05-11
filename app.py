import streamlit as st
import time

# --- 1. PAGE CONFIG & BRANDING ---
st.set_page_config(page_title="Ha Ha only 🤣", page_icon="🤣", layout="wide")

LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiByeD0iMTAwIiBmaWxsPSIjRkZEMzAwIi8+Cjx0ZXh0IHg9IjUwJSIgeT0iNjAlIiBmb250LXNpemU9IjI4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZpbGw9ImJsYWNrIj7wn6SjPC90ZXh0Pgo8L3N2Zz4="

# --- 2. ADVANCED UI: STYLING & ANIMATIONS ---
st.markdown(f"""
    <style>
    /* Splash Screen */
    #splash-screen {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #FFD300; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 100000;
        animation: fadeOutSplash 2.5s forwards;
    }}
    @keyframes fadeOutSplash {{ 0% {{opacity:1}} 80% {{opacity:1}} 100% {{opacity:0; visibility:hidden}} }}
    
    /* Moving Yellow Bar */
    .yellow-bar {{
        background-color: #FFD300; color: black; padding: 10px 0;
        font-weight: bold; font-size: 18px; overflow: hidden;
        white-space: nowrap; border-radius: 10px; margin-bottom: 20px;
    }}
    .marquee {{ display: inline-block; padding-left: 100%; animation: marquee 15s linear infinite; }}
    @keyframes marquee {{ 0% {{ transform: translate(0, 0); }} 100% {{ transform: translate(-100%, 0); }} }}

    /* Floating Emoji */
    .floating-emoji {{ 
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
        font-size: 180px; z-index: 9999; animation: emojiAnim 1s ease-out forwards; 
        pointer-events: none;
    }}
    @keyframes emojiAnim {{ 0% {{opacity:0; scale:0.5;}} 30% {{opacity:1; scale:1.3;}} 100% {{opacity:0; scale:4;}} }}
    
    .stVideo {{ border-radius: 25px; border: 5px solid #FFD300; }}
    
    /* Install Instruction Style */
    .install-box {{
        background: linear-gradient(135deg, #FFD300 0%, #FFA500 100%);
        padding: 15px; border-radius: 15px; color: black; font-weight: bold;
        text-align: center; margin-bottom: 20px; border: 2px solid #000;
    }}
    </style>
    
    <div id="splash-screen">
        <img src="{LOGO_SVG}" width="150" style="border-radius: 30px;">
        <h1 style="color: black; margin-top: 20px; font-family: sans-serif;">Ha Ha only</h1>
    </div>

    <div class="yellow-bar">
        <div class="marquee">Welcome to Ha Ha only! 🤣 TikTok Style Activated! 🚀 Autoplay & Loop ON! 🤣 Spread the joy! 🚀</div>
    </div>

    <audio id="haha-sound" src="https://www.soundjay.com/human/laughter-2.mp3" preload="auto"></audio>
    <script>
    function playHaha() {{
        var audio = document.getElementById("haha-sound");
        audio.currentTime = 0; audio.play();
    }}
    </script>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE & DATA ---
if 'joy_feed' not in st.session_state:
    st.session_state.joy_feed = [
        {"title": "First Smile! 🤣", "url": "https://www.w3schools.com/html/mov_bbb.mp4", "likes": 75, "comment": "Welcome to Ha Ha only!"}
    ]
if 'emoji_trigger' not in st.session_state: st.session_state.emoji_trigger = False

# --- 4. SIDEBAR: INSTALL & ADMIN & BUY COFFEE ---
with st.sidebar:
    st.image(LOGO_SVG, width=120)
    st.title("Ha Ha only")
    
    # INSTALL APP BUTTON (The "Add to Home Screen" Logic)
    st.markdown("""
    <div class="install-box">
        📲 INSTALL APP<br>
        <small>Click ⋮ then "Add to Home Screen"</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Buy Me A Coffee Official Button
    st.markdown("""
    <a href="https://www.buymeacoffee.com/yourprofile" target="_blank">
        <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 50px !important;width: 180px !important;">
    </a>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Hidden Admin Panel
    with st.expander("🔐 Admin Panel"):
        admin_pass = st.text_input("Password", type="password")
        if admin_pass == "admin123":
            v_titles = [v['title'] for v in st.session_state.joy_feed]
            to_del = st.selectbox("Select to delete", v_titles)
            if st.button("🗑️ Delete Video"):
                st.session_state.joy_feed = [v for v in st.session_state.joy_feed if v['title'] != to_del]
                st.rerun()

# --- 5. MAIN FEED ---
if st.session_state.emoji_trigger:
    st.markdown('<div class="floating-emoji">🤣</div>', unsafe_allow_html=True)
    st.session_state.emoji_trigger = False

st.title("🎬 Joy Feed")
t1, t2 = st.tabs(["🔥 Watch & Laugh", "📤 Post Joy"])

with t1:
    for i, v in enumerate(st.session_state.joy_feed[::-1]):
        st.subheader(v['title'])
        # TikTok Logic: Autoplay, Muted, Loop
        st.video(v['url'], autoplay=True, muted=True, loop=True)
        
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"💬 {v['comment']}")
            st.caption(f"🤣 {v['likes']} Laughs")
        
        with col2:
            if st.button(f"🤣 Ha Ha", key=f"btn_{i}"):
                st.components.v1.html("<script>window.parent.playHaha();</script>", height=0)
                st.session_state.emoji_trigger = True
                v['likes'] += 1
                time.sleep(0.4)
                st.rerun()
        st.divider()

with t2:
    st.subheader("Post Something Funny 📤")
    with st.form("public_post", clear_on_submit=True):
        title = st.text_input("Video Title")
        url = st.text_input("Direct Video Link (.mp4)")
        joke = st.text_area("Write a joke or comment...")
        if st.form_submit_button("Post Joy 🚀"):
            if title and url:
                st.session_state.joy_feed.append({
                    "title": title, "url": url, "likes": 0, "comment": joke
                })
                st.success("Your video is live! Go to the Watch tab.")
                time.sleep(1); st.rerun()
