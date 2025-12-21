import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Portal do Aluno", page_icon="💪", layout="wide")

# --- ESTILO VISUAL (DARK MODE GREENN/KIWIFY) ---
st.markdown("""
<style>
    /* Fundo e Cores Principais */
    .stApp { background-color: #0E0E0E; color: #FFFFFF; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #161616; border-right: 1px solid #2d2d2d; }
    
    /* Botões Verdes Neon */
    .stButton > button { 
        background-color: #00E676; 
        color: #000000; 
        border: none; 
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton > button:hover { 
        background-color: #00C853; 
        color: #FFFFFF; 
    }
    
    /* Inputs de Texto (Login) */
    .stTextInput > div > div > input { 
        color: white; 
        background-color: #262626; 
        border: 1px solid #333;
    }
    
    /* Textos */
    h1, h2, h3 { color: #FFFFFF !important; }
    p, label { color: #E0E0E0 !important; }
    
    /* Mensagens de Erro/Sucesso */
    .stAlert { background-color: #262626; color: white; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- CARREGAR DADOS MANUALMENTE (Para acesso aos dados do usuário depois) ---
try:
    with open('config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("Erro: O arquivo config.yaml não foi encontrado.")
    st.stop()

# --- AUTENTICAÇÃO (CORRIGIDA PARA NOVA VERSÃO) ---
# Na versão nova, passamos o caminho do arquivo ou o dicionário completo
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- TELA DE LOGIN (CORRIGIDA) ---
# O erro acontecia aqui. Agora passamos 'main' como primeiro argumento.
# 'fields' define o título do formulário.
name, authentication_status, username = authenticator.login('main', fields={'Form name': 'Login'})

# --- LÓGICA DE ACESSO ---
if authentication_status is False:
    st.error('Usuário ou senha incorretos.')
    
elif authentication_status is None:
    st.warning('Por favor, faça login para acessar sua área.')
    
elif authentication_status:
    
    # --- AQUI COMEÇA A ÁREA DO ALUNO (SÓ SE ESTIVER LOGADO) ---
    
    # Busca os dados desse usuário específico no YAML
    if username in config['credentials']['usernames']:
        dados_usuario = config['credentials']['usernames'][username]
    else:
        st.error("Erro ao carregar dados do usuário.")
        st.stop()
    
    # --- BARRA LATERAL (MENU) ---
    with st.sidebar:
        st.title(f"Olá, {name}! 👋") # Usamos a variável 'name' retornada pelo login
        st.caption(f"Plano Ativo: **{dados_usuario.get('plano', 'Padrão')}**")
        
        st.divider()
        
        menu = st.radio(
            "Navegação", 
            ["🏠 Dashboard", "▶️ Aulas", "🍎 Dieta e Treino"],
            label_visibility="collapsed"
        )
        
        st.divider()
        # Botão de Sair
        authenticator.logout('Sair', 'sidebar')

    # --- TELA 1: DASHBOARD ---
    if menu == "🏠 Dashboard":
        # Banner Principal
        st.image("https://placehold.co/1200x300/111/00E676?text=BEM-VINDO+AO+SEU+PORTAL", use_container_width=True)
        
        # Área de Avisos Pessoais
        if 'avisos' in dados_usuario:
            st.info(f"🔔 **Aviso Importante:** {dados_usuario['avisos']}")
        
        st.markdown("### Sua Evolução")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Aulas Assistidas", "12/40")
        with col2:
            st.metric("Peso Atual", "75kg", "-2kg")
        with col3:
            progresso = dados_usuario.get('progresso', 0)
            st.write(f"**Progresso Geral: {progresso}%**")
            st.progress(progresso)

    # --- TELA 2: AULAS (ESTILO NETFLIX) ---
    elif menu == "▶️ Aulas":
        st.title("Meus Cursos")
        
        col_video, col_lista = st.columns([2, 1])
        
        with col_video:
            # Exemplo de vídeo do YouTube
            st.video("https://www.youtube.com/watch?v=inpok4MKVLM") 
            st.markdown("### Aula 01: Introdução ao Método")
            st.write("Nesta aula vamos alinhar as expectativas e definir suas metas.")
            
        with col_lista:
            st.markdown("#### Próximas Aulas")
            with st.expander("Módulo 1: Mentalidade", expanded=True):
                st.markdown("✅ Aula 01: Introdução")
                st.markdown("⬜ Aula 02: Disciplina")
                st.markdown("⬜ Aula 03: Rotina")
            with st.expander("Módulo 2: Nutrição"):
                st.markdown("⬜ Aula 04: Macros")
                st.markdown("⬜ Aula 05: Supermercado")

    # --- TELA 3: DIETA E TREINO ---
    elif menu == "🍎 Dieta e Treino":
        st.header(f"Seu Plano: {dados_usuario.get('plano')}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🥗 Dieta")
            st.info("Sua dieta está focada em **Definição Muscular**.")
            
            if 'link_dieta' in dados_usuario:
                 st.link_button("📄 Baixar PDF da Dieta", dados_usuario['link_dieta'])
            else:
                st.warning("Dieta ainda não disponível.")
                
        with col2:
            st.subheader("🏋️ Treino")
            st.write("Ficha A: Superiores e Cardio")
            st.write("Ficha B: Inferiores Completo")
            st.checkbox("Marcar treino de hoje como feito")
