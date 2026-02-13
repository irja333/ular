import streamlit as st
import time
import random
from st_keyup import st_keyup

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Snake Pro Streamlit", page_icon="🐍", layout="centered")

# --- CSS CUSTOM UNTUK TAMPILAN KEREN ---
st.markdown("""
    <style>
    .game-board {
        font-family: 'Courier New', Courier, monospace;
        line-height: 1.1;
        letter-spacing: 2px;
        text-align: center;
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 15px;
        border: 3px solid #333;
        box-shadow: 0 0 20px rgba(0,255,0,0.1);
    }
    .score-box {
        font-size: 24px;
        font-weight: bold;
        color: #00FF00;
        text-align: center;
        margin-bottom: 10px;
    }
    .stApp { background-color: #0e1117; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
if 'snake' not in st.session_state:
    st.session_state.snake = [[10, 10], [10, 11], [10, 12]]
    st.session_state.food = [random.randint(0, 19), random.randint(0, 19)]
    st.session_state.direction = "w"
    st.session_state.score = 0
    st.session_state.game_over = False

def reset_game():
    st.session_state.snake = [[10, 10], [10, 11], [10, 12]]
    st.session_state.food = [random.randint(0, 19), random.randint(0, 19)]
    st.session_state.direction = "w"
    st.session_state.score = 0
    st.session_state.game_over = False

# --- LOGIKA GAME ---
def move_snake():
    head = st.session_state.snake[0].copy()
    direc = st.session_state.direction

    if direc == "w": head[0] -= 1
    elif direc == "s": head[0] += 1
    elif direc == "a": head[1] -= 1
    elif direc == "d": head[1] += 1
    
    # Cek Tabrakan
    if (head[0] < 0 or head[0] >= 20 or head[1] < 0 or head[1] >= 20 
        or head in st.session_state.snake):
        st.session_state.game_over = True
        return

    st.session_state.snake.insert(0, head)
    
    # Makan Apel
    if head == st.session_state.food:
        st.session_state.score += 10
        st.session_state.food = [random.randint(0, 19), random.randint(0, 19)]
    else:
        st.session_state.snake.pop()

# --- INTERFACE ---
st.title("🐍 Streamlit Snake Pro")
st.markdown(f"<div class='score-box'>SCORE: {st.session_state.score}</div>", unsafe_allow_html=True)

# Input Keyboard (W, A, S, D)
key = st_keyup("Kontrol: W (Atas), A (Kiri), S (Bawah), D (Kanan)", key="input_key")
if key and key.lower() in ['w', 'a', 's', 'd']:
    # Mencegah ular putar balik 180 derajat langsung
    forbidden = {'w': 's', 's': 'w', 'a': 'd', 'd': 'a'}
    if key.lower() != forbidden.get(st.session_state.direction):
        st.session_state.direction = key.lower()

board_placeholder = st.empty()

if not st.session_state.game_over:
    move_snake()
    
    # Render Grid
    grid = [[" " for _ in range(20)] for _ in range(20)]
    f_r, f_c = st.session_state.food
    grid[f_r][f_c] = "🍎"
    
    for i, (r, c) in enumerate(st.session_state.snake):
        grid[r][c] = "🟢" if i > 0 else "🐲"
        
    board_str = "\n".join(["".join(row) for row in grid])
    board_placeholder.markdown(f"<div class='game-board'><pre>{board_str}</pre></div>", unsafe_allow_html=True)
    
    time.sleep(0.1) # Kecepatan game
    st.rerun()
else:
    st.error(f"💥 GAME OVER! Skor Anda: {st.session_state.score}")
    if st.button("Main Lagi"):
        reset_game()
        st.rerun()

st.sidebar.info("Gunakan tombol **W, A, S, D** pada keyboard untuk bergerak. Pastikan kursor aktif di kotak input atas.")
