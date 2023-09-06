import streamlit as st


def contacto_componente():
    st.title("Formulario de Contacto")
    st.write(
        "Si tienes alguna pregunta o comentario, por favor completa el formulario a continuación:"
    )

    # Campos del formulario
    nombre = st.text_input("Nombre")
    email = st.text_input("Email")
    mensaje = st.text_area("Mensaje", height=150)

    # Botón para enviar el formulario
    if st.button("Enviar"):
        if nombre and email and mensaje:
            st.success("¡Formulario enviado correctamente!")
            # Aquí podrías agregar lógica para enviar el mensaje por correo electrónico o guardar en una base de datos
        else:
            st.warning(
                "Por favor completa todos los campos antes de enviar el formulario."
            )
