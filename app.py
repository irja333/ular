import streamlit as st
import time
import random

# Konfigurasi Halaman
st.set_page_config(page_title="Streamlit Snake Game", page_icon="🐍")

def init_game():
    st.session_state.snake = [[10, 10], [10, 11], [10, 12]]
    st.session_state.food = [random.randint(0, 19), random.randint(0, 19)]
    st.session_state.direction = "UP"
    st.session_state.score = 0
    st.session_state.game_over = False

# Inisialisasi State
if 'snake' not in st.session_state:
    init_game()

# Layout Dashboard
st.title("🐍 Klasik Snake di Streamlit")
score_place = st.sidebar.empty()
status_place = st.sidebar.empty()

# Kontrol Kecepatan
speed = st.sidebar.slider("Kecepatan Game", 0.05, 0.5, 0.2)

# Input Kontrol (Menggunakan tombol untuk mengubah arah)
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("🔼"): st.session_state.direction = "UP"
with col1:
    if st.button("◀️"): st.session_state.direction = "LEFT"
with col3:
    if st.button("▶️"): st.session_state.direction = "RIGHT"
with col2:
    if st.button("🔽"): st.session_state.direction = "DOWN"

# Logika Pergerakan
def move_snake():
    head = st.session_state.snake[0].copy()
    
    if st.session_state.direction == "UP": head[0] -= 1
    elif st.session_state.direction == "DOWN": head[0] += 1
    elif st.session_state.direction == "LEFT": head[1] -= 1
    elif st.session_state.direction == "RIGHT": head[1] += 1
    
    # Cek Tabrakan Dinding/Tubuh
    if (head[0] < 0 or head[0] >= 20 or head[1] < 0 or head[1] >= 20 
        or head in st.session_state.snake):
        st.session_state.game_over = True
        return

    st.session_state.snake.insert(0, head)
    
    # Cek Makan
    if head == st.session_state.food:
        st.session_state.score += 1
        st.session_state.food = [random.randint(0, 19), random.randint(0, 19)]
    else:
        st.session_state.snake.pop()

# Render Papan Permainan
board_placeholder = st.empty()

if not st.session_state.game_over:
    move_snake()
    
    # Membuat visualisasi grid
    grid = [["⬜" for _ in range(20)] for _ in range(20)]
    
    # Gambar Makanan
    f_r, f_c = st.session_state.food
    grid[f_r][f_c] = "🍎"
    
    # Gambar Ular
    for i, (r, c) in enumerate(st.session_state.snake):
        grid[r][c] = "🟩" if i > 0 else "🐲"
        
    board_str = "\n".join(["".join(row) for row in grid])
    board_placeholder.code(board_str)
    
    score_place.metric("Skor", st.session_state.score)
    
    # Loop Otomatis
    time.sleep(speed)
    st.rerun()
else:
    board_placeholder.error(f"GAME OVER! Skor Akhir: {st.session_state.score}")
    if st.button("Main Lagi"):
        init_game()
        st.rerun()
