import streamlit as st


def expander_comp():
    st.sidebar.markdown(
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
        unsafe_allow_html=True,
    )
    disclaimer_expander = st.expander("Descargo de Responsabilidad 😀")
    with disclaimer_expander:
        st.markdown(
            """ 
        <div class="alert alert-info" role="alert" style="background-color: #e6f7ff; padding: 15px; border-radius: 10px;">
            La información proporcionada aquí tiene la intención de ofrecer estimaciones e ideas generales. Para estudios legales precisos y asesoramiento, te recomendamos contactar a nuestro equipo legal experto.
            <hr>
            <p class="mb-0">Este mensaje es proporcionado solo con fines informativos y no debe considerarse asesoramiento legal oficial.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
