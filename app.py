import streamlit as st

# Configuração da página
st.set_page_config(page_title="Área do Membro", page_icon="💪")

# Título Principal
st.title("Área do Membro - Bem-vindo à sua jornada de transformação!")

st.write("Olá! Seja muito bem-vindo(a) à sua *Área do Membro*.")
st.success("Estou muito feliz por você estar aqui e dar esse passo importante em direção a uma vida mais saudável e equilibrada.")

st.info("Esta é a sua central de recursos. Explore cada seção com calma e lembre-se: *transformação real acontece um dia de cada vez*. 💪")

st.divider()

# Seção: Comece por aqui
st.header("🚀 Comece por aqui")
st.write("Antes de tudo, assista aos vídeos abaixo:")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("> *📹 **Vídeo 1: Introdução***\n\n(Vídeo aqui)")
with col2:
    st.markdown("> *📹 **Vídeo 2: Como Funciona***\n\n(Vídeo aqui)")
with col3:
    st.markdown("> *📹 **Vídeo 3: Primeiros Passos***\n\n(Vídeo aqui)")

st.divider()

# Seção: Tutoriais
st.header("📱 Tutoriais")

with st.expander("Tutorial 1: Como usar o aplicativo de registro alimentar"):
    st.markdown("""
    - Faça o download do aplicativo recomendado
    - Configure seu perfil com seus dados e objetivos
    - Registre cada refeição com fotos
    - Acompanhe suas estatísticas diárias
    """)

with st.expander("Tutorial 2: Como acompanhar sua evolução"):
    st.markdown("""
    - Registre medidas e peso semanalmente
    - Tire fotos de progresso mensalmente
    - Celebre cada pequena vitória!
    """)

with st.expander("Tutorial 3: Planejamento de refeições"):
    st.markdown("""
    - Use a função de planejamento semanal
    - Monte sua lista de compras
    - Mantenha opções saudáveis sempre à mão
    """)

st.divider()

# Seção: Dúvidas (FAQ)
st.header("❓ Dúvidas Frequentes")

faq = {
    "Como devo registrar minhas refeições?": "Registre todas as suas refeições no aplicativo recomendado. Seja honesto nos registros.",
    "O que fazer se eu 'sair da dieta'?": "Respire fundo. *Ninguém é perfeito*. Retome seus hábitos na próxima refeição.",
    "Quanto tempo até ver resultados?": "Mudanças físicas entre 3-4 semanas. Mudanças internas acontecem mais cedo.",
    "Como entro em contato?": "Mensagem pelo WhatsApp. Respondo em até 24-48 horas úteis."
}

for pergunta, resposta in faq.items():
    st.markdown(f"**{pergunta}**")
    st.caption(resposta)
    st.write("") # Espaço

st.divider()

# Mensagem Final
st.markdown("## Mensagem Final")
st.warning("*Você tomou a melhor decisão ao investir em você mesmo(a).* Estou aqui para te apoiar.")
st.write("Vamos juntos nessa transformação! 🌱")
