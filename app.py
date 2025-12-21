import streamlit as st
import streamlit_authenticator as stauth

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Painel Admin", page_icon="🔐", layout="wide")

# --- CSS VISUAL ---
st.markdown("""
<style>
    .stApp { background-color: #0E0E0E; color: white; }
    [data-testid="stSidebar"] { background-color: #161616; border-right: 1px solid #333; }
    .stButton>button { background-color: #00E676; color: black; border: none; font-weight: bold; }
    .stTextInput>div>div>input { color: white; background-color: #262626; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- GERAÇÃO AUTOMÁTICA DA SENHA (PARA NÃO DAR ERRO) ---
# Isso garante que a senha "admin" sempre funcione, independente da versão
senha_admin_plana = "admin"
try:
    # Tenta gerar hash da maneira nova
    hashed_pass = stauth.Hasher([senha_admin_plana]).generate()[0]
except:
    # Fallback (caso a biblioteca mude de novo)
    import bcrypt
    hashed_pass = bcrypt.hashpw(senha_admin_plana.encode(), bcrypt.gensalt()).decode()

# --- DADOS DOS USUÁRIOS (FIXOS NO CÓDIGO) ---
# Eliminamos a leitura do YAML para evitar erros de arquivo
config_users = {
    'admin': {
        'name': 'Administrador Supremo',
        'email': 'admin@gmail.com',
        'password': hashed_pass, # Hash gerado ali em cima automaticamente
        'role': 'admin'
    },
    'joao': {
        'name': 'João Silva',
        'email': 'joao@gmail.com',
        'password': hashed_pass, # Senha também será "admin" para teste
        'role': 'user',
        'plano': 'Hipertrofia',
        'progresso': 50
    }
}

# --- CONFIGURAÇÃO DO AUTENTICADOR ---
authenticator = stauth.Authenticate(
    {'usernames': config_users},
    'cookie_novo_v5', # Mudei o nome para limpar o cache do seu navegador
    'chave_secreta_aleatoria',
    0
)

# --- TELA DE LOGIN ---
# Tenta o login usando a sintaxe da versão mais nova (que apareceu no seu erro)
try:
    authenticator.login('main', fields={'Form name': 'Acesso Restrito'})
except Exception as e:
    st.error(f"Erro interno no componente de login: {e}")

# --- LÓGICA DE ACESSO ---
if st.session_state["authentication_status"] is False:
    st.error(f'Senha incorreta! A senha correta é: {senha_admin_plana}')
    
elif st.session_state["authentication_status"] is None:
    st.info('Por favor, faça login.')
    
elif st.session_state["authentication_status"]:
    
    # --- USUÁRIO LOGADO ---
    username = st.session_state["username"]
    user_data = config_users[username]
    role = user_data.get('role', 'user')

    # --- MENU LATERAL ---
    with st.sidebar:
        st.title(f"Olá, {user_data['name']}")
        authenticator.logout('Sair', 'sidebar')
        st.divider()
        
        if role == 'admin':
            menu = st.radio("Menu Admin", ["Dashboard", "Cadastrar Alunos"])
        else:
            menu = st.radio("Menu Aluno", ["Meus Cursos", "Minha Dieta"])

    # --- CONTEÚDO ---
    if role == 'admin':
        if menu == "Dashboard":
            st.title("Painel Administrativo ⚙️")
            st.success("Você está logado como ADMIN!")
            st.write("Aqui você terá controle total do sistema.")
            
        elif menu == "Cadastrar Alunos":
            st.title("Cadastro de Novos Pacientes")
            with st.form("add_user"):
                st.text_input("Nome")
                st.text_input("Email")
                st.form_submit_button("Salvar")

    else: # Aluno
        st.title("Área do Aluno 🎓")
        st.write(f"Bem-vindo ao plano **{user_data.get('plano')}**!")
        st.progress(user_data.get('progresso', 0))
