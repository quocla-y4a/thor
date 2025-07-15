import streamlit as st
from bot_config.ask_bot import ask
from streamlit_chat import message
from datetime import datetime
import time

st.set_page_config(
    page_title="Puppy - Professional Assistant for FBA Team",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon="🐶"
)

# --- Custom CSS ---
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f7f9fc;
        color: #333;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
        max-width: 800px;
        margin: auto;
    }

    .main-title {
        font-size: 2.5em;
        text-align: center;
        font-weight: bold;
        color: #1e3d59;
        margin-bottom: 0.5em;
        padding-top: 1em; 
    }

    .puppy-icon {
        font-size: 0.9em;
        vertical-align: middle;
    }

    .app-subtitle, .app-credit {
        text-align: center;
        font-size: 1em;
        color: #666;
        margin-bottom: 0.5em;
    }
            
    .chat-container {
        width: 100%;
        max-width: 800px;
        margin: auto;
        padding: 1rem;
        padding-bottom: 80px;
        overflow-y: auto;
    }
            
    .message-row {
        display: flex;
        margin-bottom: 15px;
    }

    .align-right {
        justify-content: flex-end;
    }

    .align-left {
        justify-content: flex-start;
    }

    .chat-bubble {
        border-radius: 18px;
        padding: 14px 20px;
        font-size: 16px;
        max-width: 85%;
        line-height: 1.6;
        word-wrap: break-word;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        position: relative;
        padding-bottom: 30px;
    }

    .user-bubble {
        background: linear-gradient(to right, #9be15d, #00e3ae);
        color: #000;
        text-align: right;
    }

    .puppy-bubble {
        background: linear-gradient(to right, #a1c4fd, #c2e9fb);
        color: #000;
        text-align: left;
    }
            
    .timestamp-inside {
        position: absolute;
        bottom: 8px; /* Khoảng cách từ đáy bubble */
        font-size: 0.75em; /* Kích thước nhỏ hơn */
        color: rgba(0,0,0,0.6); /* Màu xám hơi mờ cho dễ đọc */
        width: calc(100% - 20px); /* Đảm bảo nằm trong padding của bubble */
    }

    .user-bubble .timestamp-inside {
        right: 10px; /* Căn phải bên trong bubble user */
        text-align: right;
    }

    .puppy-bubble .timestamp-inside {
        left: 10px; /* Căn trái bên trong bubble puppy */
        text-align: left;
    }

    /* Thanh nhập liệu chat cố định ở dưới */
    .stChatInputContainer {
        padding: 15px 10px; /* Thêm padding xung quanh input */
        background-color: #f7f9fc; /* Nền trùng với body để liền mạch */
        border-top: 1px solid #e0e0e0; /* Đường viền nhẹ phía trên */
        position: fixed; /* Cố định vị trí */
        bottom: 0; /* Đặt ở dưới cùng */
        left: 0; /* Kéo dài từ trái */
        right: 0; /* Đến phải */
        z-index: 1000; /* Đảm bảo nằm trên các nội dung khác */
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05); /* Đổ bóng nhẹ lên trên */
        display: flex; /* Dùng flexbox để căn chỉnh input */
        justify-content: center; /* Căn giữa input */
    }

    .stChatInputContainer > div {
        max-width: 800px; /* Giới hạn chiều rộng của input bên trong */
        width: 100%;
    }

    /* Điều chỉnh input text của Streamlit */
    .stTextInput > div > div > input {
        border-radius: 25px; /* Bo tròn input */
        padding: 12px 20px; /* Tăng padding */
        border: 1px solid #ddd; /* Viền nhẹ */
        box-shadow: none; /* Bỏ đổ bóng mặc định */
    }

    .stTextInput > label {
        display: none; /* Ẩn label "What would you like to ask Puppy?" vì đã có placeholder */
    }

    /* Spinner loading */
    .stSpinner > div {
        color: #1e3d59; /* Màu sắc cho spinner */
    }
    .stSpinner > div > span {
        font-size: 0.9em; /* Kích thước chữ cho "Puppy is thinking..." */
        color: #666;
    }
            
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<h1 class="main-title">Puppy - Your Assistant <span class="puppy-icon">🐶</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Trained with data. Driven by curiosity. Here to help your FBA journey.</p>', unsafe_allow_html=True)
st.markdown('<p class="app-credit">Made by QuocLA from BI team.</p>', unsafe_allow_html=True)

# --- State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Chat Display ---
# Vùng chứa chat sẽ được giữ chỗ để cập nhật liên tục
chat_display_placeholder = st.empty()

def display_messages():
    with chat_display_placeholder.container(): # Sử dụng container để gói gọn các tin nhắn
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            role = msg["role"]
            content = msg["content"]
            time_sent = msg["time"]
            
            # Xác định class căn chỉnh và class bubble
            align_class = "align-right" if role == "user" else "align-left"
            bubble_class = "user-bubble" if role == "user" else "puppy-bubble"
            avatar = "👤" if role == "user" else "🐶"

            st.markdown(f"""
                <div class="message-row {align_class}">
                    <div class="chat-bubble {bubble_class}">
                        {content}
                        <div class="timestamp-inside">{avatar} {time_sent}</div> 
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Hiển thị tin nhắn ban đầu
display_messages()

# --- Chat Input ---
user_input = st.chat_input("What would you like to ask Puppy?")
if user_input:
    now = datetime.now().strftime("%H:%M")

    # Thêm tin nhắn người dùng vào state
    st.session_state.messages.append({
        "role": "user", "content": user_input, "time": now
    })
    
    # Hiển thị lại tất cả tin nhắn bao gồm cả tin nhắn mới của người dùng
    display_messages()

    # Bot đang "nghĩ"
    with st.spinner("🐶 Puppy is thinking..."):
        full_reply = ask(user_input) # Gọi hàm ask từ bot_config
        reply_time = datetime.now().strftime("%H:%M")

        # Tạo một placeholder mới cho hiệu ứng typing của bot
        typing_placeholder = st.empty()
        simulated_text = ""
        for char in full_reply:
            simulated_text += char
            with typing_placeholder.container():
                # Dùng markdown để tạo hiệu ứng typing
                st.markdown(f"""
                    <div class="message-row align-left">
                        <div class="chat-bubble puppy-bubble">
                            {simulated_text}▌ 
                            <div class="timestamp-inside">🐶 {reply_time}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            time.sleep(0.01) # Điều chỉnh tốc độ typing ở đây

        # Sau khi typing xong, hiển thị toàn bộ tin nhắn cuối cùng (bỏ con trỏ nhấp nháy)
        with typing_placeholder.container():
             st.markdown(f"""
                <div class="message-row align-left">
                    <div class="chat-bubble puppy-bubble">
                        {full_reply}
                        <div class="timestamp-inside">🐶 {reply_time}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)


    # Thêm tin nhắn của bot vào state sau khi hoàn thành typing
    st.session_state.messages.append({
        "role": "assistant", "content": full_reply, "time": reply_time
    })
    
    st.experimental_rerun()