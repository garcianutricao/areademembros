import streamlit as st

# Configuração da Página
st.set_page_config(page_title="Consultoria Nutri", page_icon="🌿", layout="wide")

# Barra Lateral (Menu de Navegação)
st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Ir para:",
    ["🏠 Início", "📹 Vídeos Explicativos", "❓ Dúvidas Frequentes", "🧮 Calculadora de IMC"]
)

# --- PÁGINA INICIAL ---
if pagina == "🏠 Início":
    st.title("🌿 Bem-vindo à sua Área do Paciente")
    st.markdown("""
    Olá! Fico muito feliz em ter você aqui.
    
    Esta plataforma foi criada para centralizar todo o nosso processo.
    Aqui você vai encontrar:
    * Tutoriais de como seguir a dieta.
    * Explicações sobre suplementação.
    * Ferramentas para acompanhar seu progresso.
    
    **Selecione uma opção no menu ao lado para começar.**
    """)
    
    # Exemplo de aviso importante
    st.info("🔔 Aviso: O seu plano alimentar será enviado pelo WhatsApp em até 24h após a anamnese.")

# --- PÁGINA DE VÍDEOS ---
elif pagina == "📹 Vídeos Explicativos":
    st.title("Biblioteca de Conteúdo")
    
    st.subheader("1. Como funciona a consultoria")
    # Substitua pelo link do seu vídeo não listado
    st.video("https://www.youtube.com/watch?v=SEU_LINK_AQUI")
    
    st.divider()
    
    st.subheader("2. Como usar o aplicativo de dieta")
    st.video("https://www.youtube.com/watch?v=SEU_OUTRO_LINK")

# --- PÁGINA DE DÚVIDAS (FAQ) ---
elif pagina == "❓ Dúvidas Frequentes":
    st.title("Perguntas Comuns")
    
    # O st.expander cria aquele efeito de "sanfona" igual ao Notion
    with st.expander("🍷 Posso beber álcool na dieta?"):
        st.write("""
        O álcool inibe a oxidação de gordura. Se você tiver um evento, 
        prefira destilados com tônica zero ou vinho seco, e intercale com água.
        """)

    with st.expander("💊 Preciso tomar Whey Protein?"):
        st.write("""
        Não é obrigatório, mas ajuda muito na praticidade para bater a meta de proteínas.
        Se você consegue comer carnes/ovos o suficiente, não precisa.
        """)