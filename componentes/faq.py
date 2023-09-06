import streamlit as st


# Lista de preguntas y respuestas de ejemplo
faq_data = [
    {
        "pregunta": "¿Qué es una herencia y cómo se reparte?",
        "respuesta": "Una herencia es el conjunto de bienes, derechos y obligaciones que deja una persona tras su fallecimiento. Se reparte entre los herederos de acuerdo a la ley o el testamento.",
    },
    {
        "pregunta": "¿Cómo se puede aceptar o renunciar a una herencia?",
        "respuesta": "Se puede aceptar una herencia de manera expresa o tácita. Si se considera que la herencia puede generar deudas, es posible renunciar a ella, pero es importante hacerlo de forma formal ante notario.",
    },
    {
        "pregunta": "¿Qué es un testamento y cómo se hace?",
        "respuesta": "Un testamento es un documento legal en el que una persona expresa sus deseos sobre cómo deben repartirse sus bienes después de su fallecimiento. Se hace ante notario y puede ser abierto o cerrado.",
    },
    {
        "pregunta": "¿Qué impuestos se deben pagar en una herencia?",
        "respuesta": "En España, las herencias están sujetas al Impuesto sobre Sucesiones y Donaciones. El importe varía según la comunidad autónoma y el grado de parentesco.",
    },
    {
        "pregunta": "¿Cómo se puede planificar una herencia para minimizar impuestos?",
        "respuesta": "Se pueden utilizar estrategias legales de planificación, como donaciones en vida, seguros de vida o crear sociedades patrimoniales, para reducir la carga tributaria en una herencia.",
    },
    # Agrega más preguntas y respuestas aquí
]


def faq_componente():
    st.title("FAQs - Preguntas Frecuentes")
    st.write(
        "Bienvenido a nuestra sección de Preguntas Frecuentes. A continuación, encontrarás respuestas a algunas de las preguntas más comunes."
    )

    # Dividir en dos columnas
    col1, col2 = st.columns(2)

    for i in range(0, len(faq_data), 2):
        with col1:
            with st.expander(faq_data[i]["pregunta"]):
                st.write(faq_data[i]["respuesta"])
        with col2:
            if i + 1 < len(faq_data):
                with st.expander(faq_data[i + 1]["pregunta"]):
                    st.write(faq_data[i + 1]["respuesta"])
