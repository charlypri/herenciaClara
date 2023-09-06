import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from componentes.calculadora import herencia_component
from componentes.chatbot import chatbot_component
from componentes.summarizer_pdf import pdf_smmarizer_component
from componentes.blog import blog_componente
from componentes.faq import faq_componente
from componentes.contacto import contacto_componente
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Herencia Clara",
    page_icon=":classical_building:",
    # layout="wide",
    initial_sidebar_state="expanded",
)


# hashed_passwords = stauth.Hasher(["charlypri", "def"]).generate()
# print(hashed_passwords)
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)

name, authentication_status, username = authenticator.login("Login", "main")


if authentication_status is False:
    st.error("Usuario/contraseña incorrecta")
elif authentication_status is None:
    st.warning("Por favor introduzca su nombre y usuario")

if authentication_status:
    # Página principal: formulario de cálculo de herencia

    # Página secundaria: chatbot
    with st.sidebar:
        selected = option_menu(
            "",
            [
                "Calculadora",
                "Chatbot",
                "Pregunta al documento",
                "Blog",
                "FAQ",
                "Contacto",
            ],
            icons=["house", "robot", "file-earmark-text"],
            menu_icon="",
            default_index=0,
        )
        # Configurar la navegación entre páginas
        pages = {
            "Calculadora": herencia_component,
            "Chatbot": chatbot_component,
            "Pregunta al documento": pdf_smmarizer_component,
            "Blog": blog_componente,
            "FAQ": faq_componente,
            "Contacto": contacto_componente,
        }

        # st.sidebar.title("Navegación")
        # selection = st.sidebar.radio("Ir a:", list(pages.keys()))
    page = pages[selected]
    page()
    st.divider()
