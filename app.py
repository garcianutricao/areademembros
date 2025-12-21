import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

senha_que_eu_quero = "admin"
codigo_gerado = stauth.Hasher([senha_que_eu_quero]).generate()
st.error(f"COPIE ESTE CÓDIGO PARA O CONFIG.YAML: {codigo_gerado[0]}")

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Portal da Mentoria", page_icon="🔐", layout="wide")

# --- ESTILO VISUAL (DARK MODE) ---
st.markdown("""
<style>
    .stApp { background-color: #0E0E0E; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #161616; border-right: 1px solid #2d2d2d; }
    .stButton > button { background-color: #00E676; color: #000; border: none; font-weight: bold; }
    .stButton > button:hover { background-color: #00C853; color: #FFF; }
    .stTextInput > div > div > input { color: white; background-color: #262626; border: 1px solid #333; }
    h1, h2, h3 { color: #FFFFFF !important; }
    .stSelectbox > div > div { background-color: #262626; color: white; }
</style>
""", unsafe_allow_html=True)

# --- CARREGAR DADOS ---
try:
    with open('config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("Erro: config.yaml não encontrado.")
    st.stop()

# --- AUTENTICAÇÃO ---
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Tela de Login
authenticator.login('main', fields={'Form name': 'Login'})

# --- LÓGICA DE ACESSO ---
if st.session_state["authentication_status"] is False:
    st.error('Usuário ou senha incorretos.')
    
elif st.session_state["authentication_status"] is None:
    st.warning('Por favor, faça login.')
    
elif st.session_state["authentication_status"]:
    
    # Pegar dados da sessão
    username = st.session_state["username"]
    name = st.session_state["name"]
    
    # Verifica se é ADMIN ou ALUNO
    role = config['credentials']['usernames'][username].get('role', 'user')

    # =========================================================
    # ÁREA DO ADMINISTRADOR
    # =========================================================
    if username == 'admin':
        with st.sidebar:
            st.title("Painel Admin ⚙️")
            st.write(f"Logado como: **{name}**")
            admin_menu = st.radio("Gerenciar:", ["➕ Adicionar Aluno", "📋 Lista de Alunos", "💾 Salvar Alterações"])
            st.divider()
            authenticator.logout('Sair', 'sidebar')

        if admin_menu == "➕ Adicionar Aluno":
            st.title("Cadastrar Novo Paciente")
            
            with st.form("novo_aluno"):
                col1, col2 = st.columns(2)
                with col1:
                    new_user = st.text_input("Usuário (Login)").lower().strip()
                    new_name = st.text_input("Nome Completo")
                    new_email = st.text_input("E-mail")
                with col2:
                    new_pass = st.text_input("Senha Inicial", type="password")
                    new_plano = st.selectbox("Plano", ["Emagrecimento", "Hipertrofia", "Performance"])
                    new_progresso = st.slider("Progresso Inicial %", 0, 100, 0)
                
                # Links personalizados
                new_dieta = st.text_input("Link do PDF da Dieta (Google Drive/Canva)")
                new_aviso = st.text_area("Mensagem de boas-vindas")
                
                submitted = st.form_submit_button("Criar Aluno")
                
                if submitted:
                    if new_user and new_pass:
                        # 1. Gerar Hash da Senha
                        hashed_pass = stauth.Hasher([new_pass]).generate()[0]
                        
                        # 2. Criar estrutura do usuário
                        novo_dado = {
                            'name': new_name,
                            'email': new_email,
                            'password': hashed_pass,
                            'plano': new_plano,
                            'progresso': new_progresso,
                            'link_dieta': new_dieta,
                            'avisos': new_aviso,
                            'role': 'user'
                        }
                        
                        # 3. Adicionar ao dicionário na memória
                        config['credentials']['usernames'][new_user] = novo_dado
                        
                        # 4. Salvar no arquivo local (temporário na nuvem)
                        with open('config.yaml', 'w', encoding='utf-8') as f:
                            yaml.dump(config, f, default_flow_style=False)
                            
                        st.success(f"Aluno {new_name} criado com sucesso!")
                        st.info("⚠️ Importante: Vá na aba 'Salvar Alterações' para garantir que não perderá os dados.")
                    else:
                        st.error("Preencha usuário e senha.")

        elif admin_menu == "📋 Lista de Alunos":
            st.title("Alunos Ativos")
            
            # Converter dicionário em tabela para visualizar
            usuarios = config['credentials']['usernames']
            for user, data in usuarios.items():
                if user != 'admin': # Não mostrar o admin
                    with st.expander(f"👤 {data['name']} ({user})"):
                        st.write(f"**Email:** {data['email']}")
                        st.write(f"**Plano:** {data.get('plano')}")
                        st.write(f"**Progresso:** {data.get('progresso')}%")
                        st.write(f"**Link Dieta:** {data.get('link_dieta')}")
                        # Aqui poderia ter botão de excluir futuramente

        elif admin_menu == "💾 Salvar Alterações":
            st.header("Backup de Segurança")
            st.warning("""
            **ATENÇÃO:** Como o Streamlit Cloud reinicia, os usuários criados aqui podem sumir se o site cair.
            Para salvar de verdade, copie o código abaixo e cole no seu arquivo 'config.yaml' no GitHub.
            """)
            
            # Gera o YAML atualizado para copiar
            yaml_texto = yaml.dump(config, default_flow_style=False, allow_unicode=True)
            st.code(yaml_texto, language='yaml')

    # =========================================================
    # ÁREA DO PACIENTE (Código Original)
    # =========================================================
    else: 
        dados_usuario = config['credentials']['usernames'][username]
        
        with st.sidebar:
            st.title(f"Olá, {name}! 👋")
            st.caption(f"Plano: **{dados_usuario.get('plano', 'Padrão')}**")
            st.divider()
            menu = st.radio("Navegação", ["🏠 Dashboard", "▶️ Aulas", "🍎 Dieta e Treino"], label_visibility="collapsed")
            st.divider()
            authenticator.logout('Sair', 'sidebar')

        if menu == "🏠 Dashboard":
            st.image("https://placehold.co/1200x300/111/00E676?text=BEM-VINDO", use_container_width=True)
            if 'avisos' in dados_usuario:
                st.info(f"🔔 {dados_usuario['avisos']}")
            col1, col2 = st.columns(2)
            with col1: st.metric("Progresso", f"{dados_usuario.get('progresso',0)}%")
            with col2: st.progress(dados_usuario.get('progresso',0))

        elif menu == "▶️ Aulas":
            st.title("Conteúdo Exclusivo")
            st.video("https://www.youtube.com/watch?v=inpok4MKVLM")

        elif menu == "🍎 Dieta e Treino":
            st.header(f"Plano: {dados_usuario.get('plano')}")
            if 'link_dieta' in dados_usuario and dados_usuario['link_dieta']:
                 st.link_button("📄 Baixar Dieta PDF", dados_usuario['link_dieta'])
            else:
                st.warning("Dieta sendo preparada.")

