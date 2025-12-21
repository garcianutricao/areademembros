import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Portal do Aluno", page_icon="💪", layout="wide")

# Estilo Visual (Dark Mode Green)
st.markdown("""
<style>
    .stApp { background-color: #0E0E0E; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #161616; border-right: 1px solid #2d2d2d; }
    .stButton > button { background-color: #00E676; color: #000; border: none; font-weight: bold; }
    .stButton > button:hover { background-color: #00C853; color: #FFF; }
    /* Ajuste para mensagens de erro/sucesso do login */
    .stAlert { background-color: #262626; color: white; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- CARREGAR DADOS DO ARQUIVO YAML ---
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# --- AUTENTICAÇÃO ---
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Cria a tela de login
name, authentication_status, username = authenticator.login('main')

# --- LÓGICA DE ACESSO ---

if authentication_status is False:
    st.error('Usuário ou senha incorretos.')
    
elif authentication_status is None:
    st.info('Por favor, faça login para acessar sua área.')
    
elif authentication_status:
    # --- ÁREA LOGADA (PACIENTE IDENTIFICADO) ---
    
    # Pega os dados EXCLUSIVOS do usuário logado direto do arquivo
    dados_usuario = config['credentials']['usernames'][username]
    
    # Sidebar Personalizada
    with st.sidebar:
        st.write(f"## Olá, {dados_usuario['name']}! 👋")
        st.caption(f"Plano Ativo: **{dados_usuario.get('plano', 'Padrão')}**")
        
        # Botão de Sair
        authenticator.logout('Sair', 'sidebar')
        
        st.divider()
        menu = st.radio("Navegação", ["🏠 Início", "🍎 Minha Dieta", "🏋️ Meus Treinos"])

    # Tela 1: Início
    if menu == "🏠 Início":
        st.title(f"Painel de Evolução")
        
        # Área de Avisos Personalizados
        if 'avisos' in dados_usuario:
            st.warning(f"🔔 **Mensagem do Nutri:** {dados_usuario['avisos']}")
        
        col1, col2 = st.columns(2)
        with col1:
            progresso = dados_usuario.get('progresso', 0)
            st.write(f"**Progresso da Mentoria:** {progresso}%")
            st.progress(progresso)
        
        with col2:
            st.info("Próxima consulta: **15/10 às 10h**")

    # Tela 2: Dieta
    elif menu == "🍎 Minha Dieta":
        st.header(f"Protocolo: {dados_usuario.get('plano')}")
        st.write("Aqui está o seu planejamento alimentar atualizado.")
        
        # Botão para baixar dieta (Link vindo do YAML)
        link = dados_usuario.get('link_dieta', '#')
        st.link_button("📄 Baixar Dieta em PDF", link)
        
        st.markdown("""
        > *Lembre-se: O melhor plano é aquele que você consegue seguir.*
        """)

    # Tela 3: Treinos (Exemplo genérico ou personalizado)
    elif menu == "🏋️ Meus Treinos":
        st.header("Sua rotina de exercícios")
        st.video("https://www.youtube.com/watch?v=inpok4MKVLM") # Exemplo de vídeo
        st.write("Registre seu treino de hoje no app parceiro.")
