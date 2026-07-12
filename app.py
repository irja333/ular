"""
🐍 Game Ular - Streamlit Edition (Improved)
Kontrol ular menggunakan tombol atau keyboard untuk makan makanan
dan hindari dinding serta obstacle.
"""

import streamlit as st
import time
from game import SnakeGame
from config import GAME_CONFIG

# ====== KONFIGURASI HALAMAN ======
st.set_page_config(
    page_title="🐍 Game Ular - Streamlit",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #2ecc71;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .stats-box {
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .game-over-box {
        background-color: #e74c3c;
        color: white;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        font-size: 20px;
    }
    .success-box {
        background-color: #27ae60;
        color: white;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    .control-section {
        background-color: #ecf0f1;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ====== INISIALISASI SESSION STATE ======
if 'game' not in st.session_state:
    st.session_state.game = SnakeGame("MEDIUM")
    st.session_state.show_menu = True
    st.session_state.high_scores = []

# ====== FUNGSI UTAMA ======
def init_new_game(difficulty):
    """Inisialisasi game baru dengan kesulitan tertentu"""
    st.session_state.game = SnakeGame(difficulty)
    st.session_state.show_menu = False

def toggle_pause():
    """Toggle pause game"""
    st.session_state.game.game_paused = not st.session_state.game.game_paused

def back_to_menu():
    """Kembali ke menu utama"""
    st.session_state.show_menu = True

# ====== RENDER UI ======
st.markdown("<h1 class='main-title'>🐍 GAME ULAR - STREAMLIT</h1>", unsafe_allow_html=True)

# ====== MENU UTAMA ======
if st.session_state.show_menu or st.session_state.game.game_over:
    st.markdown("---")
    
    if st.session_state.game.game_over:
        # Game Over Screen
        stats = st.session_state.game.get_stats()
        st.markdown(f"""
        <div class='game-over-box'>
            <h1>🎮 GAME OVER!</h1>
            <h2>Skor Akhir: {stats['skor']} 🎯</h2>
            <p>Panjang Ular: {stats['panjang_ular']} | Langkah: {stats['langkah']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Statistik Terakhir")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Skor", stats['skor'])
        with col2:
            st.metric("Panjang Ular", stats['panjang_ular'])
        with col3:
            st.metric("Total Langkah", stats['langkah'])
        
        st.markdown("---")
    
    if st.session_state.show_menu or st.session_state.game.game_over:
        st.markdown("### 🎯 Pilih Tingkat Kesulitan")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🟢 MUDAH (Lambat)", key="easy", use_container_width=True):
                init_new_game("EASY")
                st.rerun()
        
        with col2:
            if st.button("🟡 SEDANG (Normal)", key="medium", use_container_width=True):
                init_new_game("MEDIUM")
                st.rerun()
        
        with col3:
            if st.button("🔴 SULIT (Cepat)", key="hard", use_container_width=True):
                init_new_game("HARD")
                st.rerun()
        
        # Instruksi
        st.markdown("""
        #### 📖 Cara Bermain:
        1. **Arahkan Ular**: Gunakan tombol panah atau keyboard (↑↓←→)
        2. **Makan Makanan**: 🍎 = +10 poin
        3. **Hindari**: Dinding 🔴 obstacle dan tubuh sendiri
        4. **Tujuan**: Dapatkan skor setinggi mungkin!
        
        #### 💡 Tips:
        - Mulai dari kesulitan mudah jika baru pertama kali
        - Atur kecepatan sesuai kemampuan
        - Pantau posisi kepala ular
        """)

# ====== LAYAR GAME ======
else:
    game = st.session_state.game
    
    # Sidebar dengan kontrol dan info
    with st.sidebar:
        st.markdown("### 📊 STATISTIK GAME")
        stats = game.get_stats()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Skor", stats['skor'])
            st.metric("Panjang", stats['panjang_ular'])
        with col2:
            st.metric("Langkah", stats['langkah'])
            st.metric("Kesulitan", stats['kesulitan'])
        
        st.markdown("---")
        st.markdown("### ⚙️ KONTROL GAME")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏸️ Pause" if not game.game_paused else "▶️ Resume", 
                        use_container_width=True):
                toggle_pause()
                st.rerun()
        with col2:
            if st.button("🏠 Menu", use_container_width=True):
                back_to_menu()
                st.rerun()
        
        # Info kecepatan
        st.markdown(f"**Kecepatan:** {game.speed}s per langkah")
        
        st.markdown("---")
        st.markdown("### 🎮 KONTROL GERAKAN")
        st.write("Gunakan tombol atau tekan:")
        st.write("**↑** Atas | **↓** Bawah | **←** Kiri | **→** Kanan")
    
    # Main game area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Tombol kontrol gerakan
        st.markdown("<div class='control-section'>", unsafe_allow_html=True)
        st.markdown("#### 🎮 Arahkan Ular")
        
        # Row 1 - Tombol Atas
        button_col1, button_col2, button_col3, button_col4, button_col5 = st.columns([1, 1, 1, 1, 1])
        with button_col3:
            if st.button("🔼", key="up"):
                game.set_direction("UP")
        
        # Row 2 - Tombol Kiri, Bawah, Kanan
        button_col1, button_col2, button_col3, button_col4, button_col5 = st.columns([1, 1, 1, 1, 1])
        with button_col2:
            if st.button("◀️", key="left"):
                game.set_direction("LEFT")
        with button_col3:
            if st.button("🔽", key="down"):
                game.set_direction("DOWN")
        with button_col4:
            if st.button("▶️", key="right"):
                game.set_direction("RIGHT")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Game board
        st.markdown("#### 🎮 Papan Permainan")
        board_placeholder = st.empty()
        
        # Update game state
        if not game.game_over:
            game.spawn_powerup()
            game.move()
            
            # Render board
            board_str = game.get_board_string()
            board_placeholder.code(board_str, language=None)
            
            # Auto refresh
            time.sleep(game.speed)
            st.rerun()
        else:
            board_placeholder.code(game.get_board_string(), language=None)
    
    with col2:
        st.markdown("### 📋 Legenda")
        st.markdown("""
        🐲 = Kepala Ular  
        🟩 = Tubuh Ular  
        🍎 = Makanan (+10)  
        🔴 = Obstacle  
        ⭐ = Power-up  
        ⬜ = Kosong  
        """)
        
        st.markdown("---")
        st.markdown("### 📈 Info Board")
        st.info(f"📏 Ukuran: {game.board_size}x{game.board_size}")
        
        if game.powerup_active:
            st.success(f"⭐ Power-up Aktif: {game.powerup_type}")
        
        if game.game_paused:
            st.warning("⏸️ GAME PAUSE")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; font-size: 12px;'>
    Made with ❤️ using Streamlit | v2.0
</div>
""", unsafe_allow_html=True)
