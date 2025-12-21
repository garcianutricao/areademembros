import streamlit as st
from PIL import Image

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Sua Área de Membros",
    page_icon="▶️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CSS (O SEGREDO DO VISUAL GREENN/KIWIFY) ---
# Aqui injetamos CSS para forçar o fundo preto e botões verdes
st.markdown("""
<style>
    /* Fundo Principal */
    .stApp {
        background-color: #0E0E0E;
        color: #FFFFFF;
    }
    
    /* Sidebar (Menu Lateral) */
    [data-testid="stSidebar"] {
        background-color: #161616;
        border-right: 1px solid #2d2d2d;
    }
    
    /* Botões (Estilo Greenn - Verde Neon) */
    .stButton > button {
        background-color: #00E676;
        color: #000000;
        border: none;
        border-radius: 6px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #00C853;
        color: #FFFFFF;
    }

    /* Títulos e Textos */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-family: 'Helvetica', sans-serif;
    }
    
    /* Cards (Expansores) */
    .streamlit-expanderHeader {
        background-color: #1E1E1E;
        color: white;
        border-radius: 5px;
    }
    
    /* Barra de Progresso Customizada */
    .stProgress > div > div > div > div {
        background-color: #00E676;
    }
</style>
""", unsafe_allow_html=True)

# --- DADOS MOCKADOS (SIMULAÇÃO DO BANCO DE DADOS) ---
modulos = {
    "Comece por Aqui": ["Boas-vindas", "Visão Geral", "Suporte"],
    "Módulo 1: Mentalidade": ["O Poder do Hábito", "Disciplina x Motivação"],
    "Módulo 2: Nutrição": ["Calculando Macros", "Lista de Compras", "Receitas Práticas"],
    "Bônus": ["E-book Exclusivo", "Comunidade VIP"]
}

# --- BARRA LATERAL (NAVEGAÇÃO) ---
with st.sidebar:
    st.image("https://placehold.co/200x50/000000/00E676?text=MY+CLASS", use_container_width=True)
    st.markdown("---")
    
    st.write("### 📚 Meus Cursos")
    
    # Menu de Seleção
    menu_principal = st.radio(
        "Navegue:",
        ["🏠 Dashboard (Home)", "▶️ Assistir Aulas", "👤 Meu Perfil"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Progresso do Aluno
    st.write("Sua Evolução")
    st.progress(35)
    st.caption("35% Concluído")

# --- CONTEÚDO PRINCIPAL ---

# 1. TELA DE DASHBOARD (VISÃO GERAL)
if "Dashboard" in menu_principal:
    # Banner Principal (Hero Section)
    st.image("https://placehold.co/1200x300/111/00E676?text=BEM-VINDO+DE+VOLTA,+ALUNO!", use_container_width=True)
    
    st.title("Meus Cursos")
    st.markdown("Continue de onde parou:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://placehold.co/400x250/222/FFF?text=Mentoria+Premium", use_container_width=True)
        st.write("**Mentoria Premium**")
        st.progress(80)
        st.button("Continuar Assistindo", key="btn1")
        
    with col2:
        st.image("https://placehold.co/400x250/222/FFF?text=Nutricao+Eficiente", use_container_width=True)
        st.write("**Nutrição Eficiente**")
        st.progress(15)
        st.button("Acessar Curso", key="btn2")
        
    with col3:
        st.image("https://placehold.co/400x250/222/FFF?text=Treino+em+Casa", use_container_width=True)
        st.write("**Treino em Casa**")
        st.progress(0)
        st.button("Começar Agora", key="btn3")

# 2. TELA DE ASSISTIR AULAS (PLAYER DE VÍDEO)
elif "Assistir" in menu_principal:
    
    col_nav, col_video = st.columns([1, 3])
    
    # Navegação Específica do Curso (Esquerda ou Direita)
    with col_nav:
        st.subheader("Conteúdo")
        
        # Criação dinâmica dos módulos estilo "Accordion"
        aula_selecionada = None
        for modulo, aulas in modulos.items():
            with st.expander(modulo, expanded=False):
                opcao = st.radio(f"Aulas {modulo}", aulas, label_visibility="collapsed")
                if opcao:
                    aula_selecionada = f"{modulo} - {opcao}"

    # Área do Player (Direita)
    with col_video:
        st.markdown(f"## 🎬 {aula_selecionada if aula_selecionada else 'Selecione uma aula'}")
        
        # Simula o Player de Vídeo
        # (Substitua por st.video("link") na vida real)
        st.image("https://placehold.co/800x450/000000/333333?text=PLAYER+DE+VIDEO+HD", use_container_width=True)
        
        # Botões de Ação abaixo do vídeo
        c1, c2, c3 = st.columns([1,1,3])
        with c1:
            st.button("⬅️ Anterior")
        with c2:
            st.button("Próximo ➡️")
        with c3:
            st.button("✅ Marcar como Concluída")
            
        st.markdown("---")
        
        # Conteúdo em Texto (Aquela copy que criamos antes)
        st.markdown("""
        ### Sobre esta aula
        
        Bem-vindo a esta aula fundamental! Aqui vamos discutir os pilares da transformação.
        
        **Materiais de Apoio:**
        - 📄 [Baixar PDF da Aula](#)
        - 🎧 [Áudio MP3](#)
        
        > *"A disciplina é a ponte entre metas e realizações."*
        """)

# 3. TELA DE PERFIL
elif "Perfil" in menu_principal:
    st.title("Configurações da Conta")
    st.info("Aqui você pode alterar sua senha e dados de pagamento.")
    
    st.text_input("Nome Completo", value="Seu Nome Aqui")
    st.text_input("E-mail", value="email@exemplo.com")
    st.button("Salvar Alterações")
