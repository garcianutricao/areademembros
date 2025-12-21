import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Portal do Aluno", page_icon="💪", layout="wide")

# --- ESTILO VISUAL (DARK MODE) ---
st.markdown("""
<style>
    .stApp { background-color: #0E0E0E; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #161616; border-right: 1px solid #2d2d2d; }
    .stButton > button { background-color: #00E676; color: #000000; border: none; font-weight: bold; }
    .stButton > button:hover { background-color: #00C853; color: #FFFFFF; }
    .stTextInput > div > div > input { color: white; background-color: #262626; border: 1px solid #333; }
    h1, h2, h3 { color: #FFFFFF !important; }
    p, label { color: #E0E0E0 !important; }
    .stAlert { background-color: #262626; color: white; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- CARREGAR DADOS ---
try:
    with open('config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("Erro: Arquivo config.yaml não encontrado.")
    st.stop()

# --- AUTENTICAÇÃO ---
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- TELA DE LOGIN (CORREÇÃO AQUI) ---
# Não usamos mais "name, status, username = ...". Apenas chamamos a função.
authenticator.login('main', fields={'Form name': 'Login'})

# --- VERIFICAÇÃO DE STATUS ---
# Agora checamos direto na memória do sistema (session_state)

if st.session_state["authentication_status"] is False:
    st.error('Usuário ou senha incorretos.')
    
elif st.session_state["authentication_status"] is None:
    st.warning('Por favor, faça login para acessar sua área.')
    
elif st.session_state["authentication_status"]:
    
    # --- ÁREA LOGADA ---
    
    # Recuperamos os dados da memória manualmente
    username = st.session_state["username"]
    name = st.session_state["name"]
    
    # Busca dados extras no YAML
    if username in config['credentials']['usernames']:
        dados_usuario = config['credentials']['usernames'][username]
    else:
        st.error("Erro ao carregar perfil.")
        st.stop()
    
    # --- MENU LATERAL ---
    with st.sidebar:
        st.title(f"Olá, {name}! 👋")
        st.caption(f"Plano: **{dados_usuario.get('plano', 'Padrão')}**")
        st.divider()
        
        menu = st.radio(
            "Navegação", 
            ["🏠 Dashboard", "▶️ Aulas", "🍎 Dieta e Treino"],
            label_visibility="collapsed"
        )
        
        st.divider()
        authenticator.logout('Sair', 'sidebar')

    # --- TELA 1: DASHBOARD ---
    if menu == "🏠 Dashboard":
        st.image("https://placehold.co/1200x300/111/00E676?text=BEM-VINDO", use_container_width=True)
        
        if 'avisos' in dados_usuario:
            st.info(f"🔔 **Aviso:** {dados_usuario['avisos']}")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Aulas", "12/40")
        with col2: st.metric("Peso", "75kg", "-2kg")
        with col3:
            prog = dados_usuario.get('progresso', 0)
            st.write(f"**Progresso: {prog}%**")
            st.progress(prog)

    # --- TELA 2: AULAS ---
    elif menu == "▶️ Aulas":
        st.title("Meus Cursos")
        col_vid, col_lst = st.columns([2, 1])
        with col_vid:
            st.video("https://www.youtube.com/watch?v=inpok4MKVLM")
            st.markdown("### Aula 01: Introdução")
        with col_lst:
            with st.expander("Módulo 1", expanded=True):
                st.markdown("✅ Aula 01")
                st.markdown("⬜ Aula 02")

    # --- TELA 3: DIETA ---
    elif menu == "🍎 Dieta e Treino":
        st.header(f"Plano: {dados_usuario.get('plano')}")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🥗 Dieta")
            if 'link_dieta' in dados_usuario:
                 st.link_button("📄 Baixar Dieta", dados_usuario['link_dieta'])
            else:
                st.warning("Sem dieta cadastrada.")
        with col2:
            st.subheader("🏋️ Treino")
            st.write("Ficha A: Superiores")
            st.write("Ficha B: Inferiores")
