import streamlit as st

# Page Config for Mobile
st.set_page_config(page_title="Girl Math VIP", page_icon="💖", layout="centered")

# Custom CSS to make it look like Alexandra's drawing
st.markdown("""
    <style>
    .main { background-color: #fff5f7; }
    h1 { color: #ff85a2; font-family: 'Comic Sans MS', cursive; text-align: center; font-size: 3rem !important; }
    .stButton>button { 
        background-color: #ff85a2; color: white; border-radius: 20px; 
        width: 100%; font-weight: bold; border: none; padding: 15px;
    }
    .vip-card {
        background: white; border: 3px solid #ffb3c1; padding: 20px;
        border-radius: 25px; text-align: center; margin-bottom: 20px;
        box-shadow: 5px 5px 15px rgba(255, 133, 162, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("# 💖 VIP PASS 💖")
st.markdown("<p style='text-align: center; color: #ffb3c1; font-weight: bold;'>AT: GIRL MATH HAIR SALON</p>", unsafe_allow_html=True)

# VIP Status
if 'is_vip' not in st.session_state:
    st.session_state.is_vip = False

with st.container():
    st.markdown('<div class="vip-card">', unsafe_allow_html=True)
    st.subheader("How to get VIP?")
    st.write("*(A worker will tell you how to get V.I.P. Just ask! 😊)*")
    
    if st.button("ASK FOR VIP STATUS" if not st.session_state.is_vip else "✨ YOU ARE NOW VIP ✨"):
        st.session_state.is_vip = True
        st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

# Snack Bar & Spa (Tabs for Mobile Navigation)
tab1, tab2, tab3 = st.tabs(["🥤 Snack Bar", "💅 Spa/Comics", "🏷️ Name Tag"])

with tab1:
    st.markdown("### 🍿 Access To:")
    st.checkbox("Healthy Pack")
    st.checkbox("Sweat Tooth")
    st.checkbox("Lemonade (Refresher)")
    st.checkbox("Milkshakes")

with tab2:
    st.markdown("### 🎨 Spa Treatments")
    st.info("Check back daily for new Comics!")
    st.image("https://via.placeholder.com/400x200.png?text=Comic+Scene+Loading...", caption="1 Second Later...")

with tab3:
    st.markdown("### 📛 Custom Name Tag")
    name = st.text_input("Enter your name:")
    color = st.color_picker("Pick your tag color:", "#ff85a2")
    if name:
        st.markdown(f"""
            <div style="background:{color}; padding:20px; border-radius:15px; text-align:center; color:white;">
                <h2 style="margin:0;">{name}</h2>
                <p style="margin:0;">VIP MEMBER + GEMS</p>
            </div>
        """, unsafe_allow_html=True)

# Early Gift
st.write("---")
st.markdown("<p style='text-align: center;'>🎁 <b>EARLY GIFT:</b> STICKER</p>", unsafe_allow_html=True)
