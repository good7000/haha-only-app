import streamlit as st
import time

# --- 1. CONFIG & BRANDING ---
st.set_page_config(page_title="Ha Ha only 🤣", page_icon="🤣", layout="wide")

# Logo (Yellow Square with Smile)
LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiByeD0iMTAwIiBmaWxsPSIjRkZEMzAwIi8+Cjx0ZXh0IHg9IjUwJSIgeT0iNjAlIiBmb250LXNpemU9IjI4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZpbGw9ImJsYWNrIj7wn6SjPC90ZXh0Pgo8L3N2Zz4="

# --- 2. CSS, ANIMATIONS & SOUND ---
st.markdown(f"""
    <style>
    /* Splash Screen */
    #splash-screen {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #FFD300; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 100000;
        animation: fadeOut 2.5s forwards;
    }}
    @keyframes fadeOut {{ 0% {{opacity:1}} 80% {{opacity:1}} 100% {{opacity:0; visibility:hidden}} }}
    
    /* Floating Emoji Animation */
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
        <h1 style="color: black; font-family: sans-serif; margin-top: 20px;">Ha Ha only</h1>
    </div>

    <audio id="laugh-sound" src="https://www.soundjay.com/human/laughter-2.mp3" preload="auto"></audio>
    <script>
    function playLaugh() {{
        var audio = document.getElementById("laugh-sound");
        audio.currentTime = 0; audio.play();
    }}
    </script>
    """, unsafe_allow_html=True)

# --- 3. IN-MEMORY DATABASE ---
if 'joy_list' not in st.session_state:
    st.session_state.joy_list = [
        {"title": "Welcome to Ha Ha only! 🤣", "url": "https://www.w3schools.com/html/mov_bbb.mp4", "count": 12},
        {"title": "Try not to laugh challenge", "url": "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4", "count": 8}
    ]
if 'emoji_trigger' not in st.session_state: st.session_state.emoji_trigger = False

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image(LOGO_SVG, width=100)
    st.title("Ha Ha only")
    st.success("Public Mode: Everyone can watch & post!")
    st.write("---")
    st.info("Spread the laughter! No login required. 🤣")

# --- 5. MAIN CONTENT ---
if st.session_state.emoji_trigger:
    st.markdown('<div class="floating-emoji">🤣</div>', unsafe_allow_html=True)
    st.session_state.emoji_trigger = False

st.title("🎬 Global Joy Feed")
tab1, tab2 = st.tabs(["🔥 Watch & Laugh", "📤 Post Something Funny"])

with tab1:
    # Display videos from newest to oldest
    for i, v in enumerate(st.session_state.joy_list[::-1]):
        st.subheader(v['title'])
        st.video(v['url'])
        col1, col2 = st.columns([4, 1])
        col1.caption(f"🤣 {v['count']} people laughed at this")
        
        # The Laugh Button
        if col2.button(f"🤣 Ha Ha", key=f"btn_{i}"):
            # Play Sound & Show Animation
            st.components.v1.html("<script>window.parent.playLaugh();</script>", height=0)
            st.session_state.emoji_trigger = True
            v['count'] += 1
            time.sleep(0.5)
            st.rerun()
        st.divider()

with tab2:
    st.subheader("Add to the Joy! 📤")
    with st.form("public_upload", clear_on_submit=True):
        t = st.text_input("Title of the video")
        u = st.text_input("Video Link (Direct .mp4 link)")
        if st.form_submit_button("Post to Feed 🚀"):
            if t and u:
                st.session_state.joy_list.append({"title": t, "url": u, "count": 0})
                st.success("Your joy has been shared with the world!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Please enter both a title and a valid video link.")
