import streamlit as st
import plotly.express as px
from componentes.expander import expander_comp


# Función para calcular el porcentaje de herencia
def calcular_herencia(porcentajes, personas, testamento, parentesco):
    # Lógica para calcular el porcentaje de herencia
    # Utiliza los parámetros proporcionados
    # Retorna el porcentaje de herencia calculado
    # Calcular los porcentajes para todas las personas
    porcentajes = [porcentajes] * personas

    # Crear nombres de personas de forma numérica
    nombres = [f"{parentesco} {i}" for i in range(1, personas + 1)]

    if testamento:
        partes = [
            "Tercio de Mejora",
            "Tercio de Libre Disposición",
            "Tercio de Libre Disposición",
        ]
        st.markdown("## Reparto por tercios")
        col1, col2, col3 = st.columns(3)
        with col1:
            fig1 = px.pie(values=porcentajes, names=nombres, title="Tercio Estricta")
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = px.pie(
                values=porcentajes,
                names=nombres,
                title="Tercio de mejora",
                color_discrete_sequence=["#FF5733", "#E84545", "#D32F2F", "#C62828"],
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col3:
            fig3 = px.pie(
                values=porcentajes,
                names=nombres,
                title="Tercio de Libre Disposición",
                color_discrete_sequence=["#2ECC71", "#27AE60", "#1E8449", "#196F3D"],
            )
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("## Reparto total de la herencia")
        partes = []
        porcentajes = []
        for persona in range(personas):
            partes.append(f"Tercio de mejora del {parentesco} {persona}")
            porcentajes.append(30 / personas)
        for persona in range(personas):
            partes.append(f"Tercio Estricta del {parentesco} {persona}")
            porcentajes.append(30 / personas)
        for persona in range(personas):
            partes.append(f"Tercio de Libre Disposición del {parentesco} {persona}")
            porcentajes.append(30 / personas)

        fig1 = px.pie(
            values=porcentajes,
            names=partes,
            title="Reparto de Herencia",
        )
        st.plotly_chart(fig1, use_container_width=True)

    else:
        fig = px.pie(
            values=porcentajes, names=nombres, title="Reparto de Herencia"
        )
        st.plotly_chart(fig)


def herencia_component():
    st.title("Bienvenido a HerenciaClara :classical_building: :scroll:")
    st.divider()
    st.markdown(" ## Formulario de Consulta de Herencia")
    st.write("Por favor, responde algunas preguntas para que podamos estimar tu caso:")

    col1, col2 = st.columns(2)

    with col1:
        # Pregunta 1
        hay_testamento = st.radio("Pregunta 1: ¿Hay un testamento?", ("Sí", "No"))

    with col2:
        # Pregunta 2 (Independientemente de si hay un testamento o no)
        parentesco = st.selectbox(
            "Pregunta 2: ¿Cuál es el parentesco con el difunto?",
            (
                "",
                "Hijo/Hija",
                "Nieto/Nieta",
                "Padre/Madre",
                "Abuelo/Abuela",
                "Hermano/Hermana",
                "Cónyuge no separado legalmente",
                "Sobrino/Sobrina",
                "Colaterales hasta 4º: Primos hermanos",
                "Otros",
            ),
        )

    # Mostrar preguntas adicionales basadas en la respuesta de parentesco
    if parentesco == "Hijo/Hija":
        pregunta_hijos(hay_testamento)
    elif parentesco == "Nieto/Nieta":
        pregunta_nietos(hay_testamento)
    elif parentesco == "Padre/Madre":
        pregunta_padres(hay_testamento)
    elif parentesco == "Abuelo/Abuela":
        pregunta_abuelos(hay_testamento)
    elif parentesco == "Cónyuge no separado legalmente":
        pregunta_conyuge(hay_testamento)
    elif parentesco == "Hermano/Hermana":
        pregunta_hermanos(hay_testamento)
    elif parentesco == "Sobrino/Sobrina":
        pregunta_sobrino(hay_testamento)
    elif parentesco == "Colaterales hasta 4º: Primos hermanos":
        pregunta_colaterales(hay_testamento)
    elif parentesco == "Otros":
        pregunta_otros(hay_testamento)
    expander_comp()


def pregunta_hijos(hay_testamento):
    cantidad_hijos = st.number_input(
        "Pregunta adicional: ¿Cuántos hijos tiene en total el difunto?",
        min_value=0,
        max_value=100,
        value=0,
        step=1,
    )
    if hay_testamento == "No":
        if cantidad_hijos >= 1:
            porcentaje = 1 / cantidad_hijos
            calcular_herencia(porcentaje, cantidad_hijos, testamento=False, parentesco="Hijo")
        else:
            st.write("Introduce un numero válido de hijos")
    else:
        if cantidad_hijos == 1:
            porcentaje = 1 / cantidad_hijos
            calcular_herencia(porcentaje, cantidad_hijos, testamento=True, parentesco="Hijo")
            st.write(
                """
                    Mínimo tendrás derecho a un tercio de la herencia.
                    
                    Si no hay ninguna disposición en el testamento respecto al tercio de mejora, tu derecho se incrementaría a dos terceras parte de la herencia.
                    
                    Si tampoco hay ninguna disposición respecto al terccio de libre disposición, tendrías derecho a 100%.
                    
                    Hay que valorar cualquier otra disposición especial como usufructo a favor del cónyuge o cualquier otra disposición especial.
                    
                    *Si desea un asesoramiento más especializado puede ponerse en contacto con nuestros asesores legales para que estudien su caso en concreto y puedan ayudarle en lo que necesite.
                """
            )
        elif cantidad_hijos > 1:
            st.write(
                """
                    *LEGÍTIMA ESTRICTA*: Mínimo tendrás derecho a LEGÍTIMA de la herencia.

                    *TERCIO DE MEJORA*: Si no hay ninguna disposición en el testamento respecto al tercio de mejora, tu derecho en el tercio de mejora sería de un TERCIO MEJORA de la herencia.
                    
                    *TERCIO DE LIBRE DISPOSICIÓN*: Si tampoco hay ninguna disposición respecto al tercio de libre disposición, tendrías derecho a TERCIOLIBRE DISPOSICIÓN de la herencia. 
                    
                    Hay que valorar cualquier otra disposición especial como usufructo a favor del cónyuge, legado o cualquier otra disposición especial.
                    
                    *Si desea un asesoramiento más especializado puede ponerse en contacto con nuestros asesores legales para que estudien su caso en concreto y puedan ayudarle en lo que necesite.
                """
            )
            porcentaje = 1 / cantidad_hijos
            calcular_herencia(porcentaje, cantidad_hijos, testamento=True, parentesco="Hijo")


def pregunta_nietos(hay_testamento):
    progenitor_vivo = st.radio(
        "Pregunta adicional: ¿Tu progenitor hijo/a de tu abuelo/a vive?",
        ("Sí", "No"),
    )
    if progenitor_vivo == "Sí":
        if hay_testamento == "No":
            st.write(
                "No tienes derecho, ya que en principio le correspondería a tu progenitor salvo algunos supuestos muy específicos.de la herencia."
            )
        else:
            st.write(
                """
                    LEGÍTIMA: No tienes derecho, ya que en principio le correspondería a tu progenitor salvo algunos supuestos muy específicos.de la herencia.

                    MEJORA: Salvo disposición expresa en el testamento en favor de usted, tampoco tendría derecho.

                    TERCIO DE LIBRE DISPOSICIÓN: Habría que analizar el testamento para ver si su abuelo/a le ha nombrado heredero.

                    Hay que valorar cualquier otra disposición especial como usufructo a favor del cónyuge o cualquier otra disposición especial.

                    *Si desea un asesoramiento más especializado puede ponerse en contacto con nuestros asesores legales para que estudien su caso en concreto y puedan ayudarle en lo que necesite.
                """
            )
    else:
        mas_hermanos = st.radio(
            "Pregunta adicional: ¿Tienes más hermanos?", ("Sí", "No")
        )
        if mas_hermanos == "Sí":
            cantidad_hermanos = st.number_input(
                "¿Cuántos hermanos tienes?",
                min_value=0,
                max_value=100,
                value=0,
                step=1,
            )
        else:
            cantidad_hermanos = 0

        tios_vivos = st.radio(
            "Pregunta adicional: ¿Tienes tíos vivos o que hayan fallecido?",
            ("Sí", "No"),
        )
        if tios_vivos == "Sí":
            cantidad_tios = st.number_input(
                "¿Cuántos tíos tienes?", min_value=0, max_value=100, value=0, step=1
            )
        else:
            cantidad_tios = 0

        porcentaje = 100 / (cantidad_tios + cantidad_hermanos + 1)
        personas = cantidad_tios + cantidad_hermanos + 1
        if hay_testamento == "No":
            calcular_herencia(porcentaje, personas, testamento=False, parentesco="Nieto")
        else:
            calcular_herencia(porcentaje, personas, testamento=True, parentesco="Nieto")
        


def pregunta_padres(hay_testamento):
    if hay_testamento == "No":
        hijos_o_nietos = st.radio(
            "Pregunta adicional: ¿El difunto tiene hijos o nietos?", ("Sí", "No")
        )
        if hijos_o_nietos == "No":
            vive_otro_progenitor = st.radio(
                "Pregunta adicional: ¿Vive el otro progenitor?", ("Sí", "No")
            )
            if vive_otro_progenitor == "Sí":
                porcentaje = 100 / 2
                personas = 2

            else:
                porcentaje = 100
                personas = 1
            calcular_herencia(porcentaje, personas, testamento=False, parentesco="Progenitor")
        else:
            st.markdown(" ### La herencia le corresponde a sus hijos / nietos")

    else:
        hijos_o_nietos = st.radio(
            "Pregunta adicional: ¿El difunto tiene hijos o nietos?", ("Sí", "No")
        )
        if hijos_o_nietos == "No":
            estaba_casado = st.radio(
                "Pregunta adicional: ¿Estaba casado?", ("Sí", "No")
            )
            vive_otro_progenitor = st.radio(
                "Pregunta adicional: ¿Vive el otro progenitor?", ("Sí", "No")
            )
            if estaba_casado == "Sí" and vive_otro_progenitor == "Sí":
                porcentaje = 100 / 2
                personas = 2
                calcular_herencia(porcentaje, personas, testamento=True, parentesco="Progenitor")

            elif estaba_casado == "Sí" and vive_otro_progenitor == "No":
                porcentaje = 100
                personas = 1
                calcular_herencia(porcentaje, personas, testamento=True, parentesco="Progenitor")

            if estaba_casado == "No" and vive_otro_progenitor == "Sí":
                st.markdown(
                    """
                    LEGÍTIMA ESTRICTA: Tiene derecho a la mitad de la herencia, la otra mitad será de libre disposición, que habrá que ver si en el testamento dispuso de ella o no. En el caso de que no hubiese dispuesto de ella, tendría derecho al 100%.

                    Hay que valorar cualquier otra disposición especial como usufructo a favor del cónyuge o cualquier otra disposición especial.

                    *Si desea un asesoramiento más especializado puede ponerse en contacto con nuestros asesores legales para que estudien su caso en concreto y puedan ayudarle en lo que necesite.

                """
                )

            elif estaba_casado == "No" and vive_otro_progenitor == "No":
                st.markdown(
                    """
                    LEGÍTIMA ESTRICTA: Tiene derecho a un 25% de la herencia.

                    MITAD DE LIBRE DISPOSICIÓN: habrá que ver si en el testamento dispuso de ella o no. En el caso de que no hubiese dispuesto de ella, tendría derecho al 25%.

                    Hay que valorar cualquier otra disposición especial como usufructo a favor del cónyuge o cualquier otra disposición especial.

                    *Si desea un asesoramiento más especializado puede ponerse en contacto con nuestros asesores legales para que estudien su caso en concreto y puedan ayudarle en lo que necesite.
                """
                )

        else:
            st.markdown(
                """
                    LEGÍTIMA ESTRICTA: No tiene derecho a la legítima.

                    TERCIO DE MEJORA: No tiene derecho.

                    TERCIO DE LIBRE DISPOSICIÓN: habrá que valorar el testamento y ver si su hijo/a dispuso del tercio de libre disposición en su favor.

                    Hay que valorar cualquier otra disposición especial como usufructo a favor del cónyuge o cualquier otra disposición especial.

                    *Si desea un asesoramiento más especializado puede ponerse en contacto con nuestros asesores legales para que estudien su caso en concreto y puedan ayudarle en lo que necesite.
                """
            )


def pregunta_abuelos(hay_testamento):
    if hay_testamento == "No":
        viven_hijos_nietos_padres = st.radio(
            "Pregunta adicional: ¿Viven los hijos, nietos o padres del difunto?",
            ("Sí", "No"),
        )

        vive_otro_abuelo_misma_linea = st.radio(
            "¿Vive el otro abuelo de su misma línea?", ("Sí", "No")
        )
        if vive_otro_abuelo_misma_linea == "Sí":
            cantidad_abuelos_otra_linea = st.number_input(
                "¿Cuántos abuelos viven de la otra línea?",
                min_value=0,
                max_value=2,
                value=0,
                step=1,
            )

        porcentaje = 100
        personas = 2
        calcular_herencia(porcentaje, personas, testamento=False, parentesco="Abuelo")

    else:
        viven_hijos_nietos = st.radio(
            "Pregunta adicional: ¿Su nieto fallecido ha tenido hijos o nietos?",
            ("Sí", "No"),
        )

        if viven_hijos_nietos == "Sí":
            st.markdown("""
                LEGÍTIMA ESTRICTA: No tiene derecho a la legítima.

                TERCIO DE MEJORA: No tiene derecho.

                TERCIO DE LIBRE DISPOSICIÓN: habrá que valorar el testamento y ver si su hijo/a dispuso del tercio de libre disposición en su favor.

                Hay que valorar cualquier otra disposición especial como usufructo a favor del cónyuge o cualquier otra disposición especial.

                *Si desea un asesoramiento más especializado puede ponerse en contacto con nuestros asesores legales para que estudien su caso en concreto y puedan ayudarle en lo que necesite.
            """)
        else:
            estaba_casado = st.radio(
                "¿Estaba casado?", ("Sí", "No")
            )
            progenitores_vivos = st.radio(
                "¿Viven algún progenitor de su nieto?", ("Sí", "No")
            )
            if progenitores_vivos == "Sí":
                st.markdown("""
                    LEGÍTIMA ESTRICTA: No tiene derecho a la legítima.

                    TERCIO DE MEJORA: No tiene derecho.

                    TERCIO DE LIBRE DISPOSICIÓN: habrá que valorar el testamento y ver si su hijo/a dispuso del tercio de libre disposición en su favor.

                    Hay que valorar cualquier otra disposición especial como usufructo a favor del cónyuge o cualquier otra disposición especial.

                    *Si desea un asesoramiento más especializado puede ponerse en contacto con nuestros asesores legales para que estudien su caso en concreto y puedan ayudarle en lo que necesite.
                """)
            else:
                abuelos_vivos = st.radio(
                    "¿Tiene más abuelos vivos?", ("Sí", "No")
                )
                if abuelos_vivos == "Sí":
                    misma_linea = st.radio(
                        "¿De la misma línea paterna o materna que usted? ¿O de ambas? (A parte de usted).",
                        ("Misma línea", "Ambas")
                    )
                    if misma_linea == "Misma línea":
                        if estaba_casado == "Sí":
                            porcentaje = "25%"
                            personas = 2
                            st.markdown("## Te toca un 1/6")
                            # calcular_herencia(porcentaje, personas, testamento=True, parentesco="Abuelo")
                        else:
                            porcentaje = "25%"
                            personas = 2
                            st.markdown("## Te toca un 25%")
                            # calcular_herencia(porcentaje, personas, testamento=True, parentesco="Abuelo")
                    else:
                        if estaba_casado == "Sí":
                            porcentaje = 1/6
                            personas = 2
                            st.markdown("## Te toca un 1/12")
                            # calcular_herencia(porcentaje, personas, testamento=True, parentesco="Abuelo")
                        else:
                            porcentaje = "25%"
                            personas = 2
                            st.markdown("## Te toca un 1/8")
                            # calcular_herencia(porcentaje, personas, testamento=True, parentesco="Abuelo")
                
                else:
                    st.markdown("""
                        LEGÍTIMA ESTRICTA: Tiene derecho a un tercio de la herencia, la otra mitad será de libre disposición, que habrá que ver si en el testamento dispuso de ella o no. En el caso de que no hubiese dispuesto de ella, tendría derecho al 100%.

                        Hay que valorar cualquier otra disposición especial como usufructo a favor del cónyuge o cualquier otra disposición especial.

                        *Si desea un asesoramiento más especializado puede ponerse en contacto con nuestros asesores legales para que estudien su caso en concreto y puedan ayudarle en lo que necesite.
                    """)


def pregunta_conyuge(hay_testamento):
    if hay_testamento == "No":
        descendiente_ascendiente_vivo = st.radio(
            "Pregunta adicional: ¿Tiene el difunto algún descendiente o ascendiente vivo?",
            ("Sí", "No"),
        )
        if descendiente_ascendiente_vivo == "No":
            porcentaje = 100 / 1
            personas = 1
            calcular_herencia(porcentaje, personas, testamento=False, parentesco="Conyuge")
        else:
            st.markdown(" ### La herencia le corresponde a su descendiente/ascendiente")

    else:
        tiene_hijos_vivos = st.radio(
            "Pregunta adicional: ¿Tiene el difunto algún descendiente vivo?",
            ("Sí", "No"),
        )
        if tiene_hijos_vivos == "No":
            tiene_ascendientes_vivos = st.radio(
                "Pregunta adicional: ¿Tiene progenitores vivos u otros ascendientes?",
                ("Sí", "No"),
            )
            if tiene_ascendientes_vivos == "No":
                st.markdown(""" 
                    Legítima estricta: tiene derecho al usufructo de la mitad de la herencia.

                    Tercio de libre disposición: habrá que ver si en el testamento dispuso de ella o no. En el caso de que no hubiese dispuesto de ella.

                    Hay que valorar cualquier otra disposición especial como usufructo a favor del cónyuge o cualquier otra disposición especial.

                    *Si desea un asesoramiento más especializado puede ponerse en contacto con nuestros asesores legales para que estudien su caso en concreto y puedan ayudarle en lo que necesite.
                """)

                porcentaje = 100 / 1
                personas = 1
                calcular_herencia(porcentaje, personas, testamento=False, parentesco="Conyuge")
            else:
                st.markdown(""" 
                    Legítima estricta: tiene derecho al usufructo de dos tercios de la herencia.

                    Tercio de libre disposición: habrá que ver si en el testamento dispuso de ella o no. En el caso de que no hubiese dispuesto de ella.

                    Hay que valorar cualquier otra disposición especial como usufructo a favor del cónyuge o cualquier otra disposición especial.

                    *Si desea un asesoramiento más especializado puede ponerse en contacto con nuestros asesores legales para que estudien su caso en concreto y puedan ayudarle en lo que necesite.
                """)

                porcentaje = 100 / 1
                personas = 1
                calcular_herencia(porcentaje, personas, testamento=False, parentesco="Conyuge")
        else:
            st.markdown(""" Legítima estricta: tiene derecho al usufructo del tercio destinado a la mejora.
                Tercio de libre disposición: habrá que ver si en el testamento dispuso de ella o no. En el caso de que no hubiese dispuesto de ella.

                Hay que valorar cualquier otra disposición especial como usufructo a favor del cónyuge o cualquier otra disposición especial.

                *Si desea un asesoramiento más especializado puede ponerse en contacto con nuestros asesores legales para que estudien su caso en concreto y puedan ayudarle en lo que necesite.
            """)



def pregunta_hermanos(hay_testamento):
    if hay_testamento == "No":
        descendiente_ascendiente_conyuge_vivo = st.radio(
            "Pregunta adicional: ¿Tiene el difunto algún descendiente, ascendiente o cónyuge no separado legalmente o de hecho vivo?",
            ("Sí", "No"),
        )
        if descendiente_ascendiente_conyuge_vivo == "No":
            hermanos_vivos = st.radio(
                "Pregunta adicional: ¿Tienes hermanos vivos o fallecidos?", ("Sí", "No")
            )
            if hermanos_vivos == "Sí":
                cantidad_hermanos = st.number_input(
                    "¿Cuántos hermanos tienes?",
                    min_value=0,
                    max_value=100,
                    value=0,
                    step=1,
                )
            else:
                cantidad_hermanos = 0

            porcentaje = 100 / (cantidad_hermanos + 1)
            personas = cantidad_hermanos + 1
            calcular_herencia(porcentaje, personas, testamento=False, parentesco="Hermanos")
        else:
            st.markdown(
                " ### La herencia le corresponde a su descendiente, ascendiente o cónyuge no separado legalmente o de hecho"
            )
    else:
        pass


def pregunta_sobrino(hay_testamento):
    if hay_testamento == "No":
        progenitor_hermano_vivo = st.radio(
            "Pregunta adicional: ¿Tu progenitor hermano de tu tío ha fallecido?",
            ("Sí", "No"),
        )
        if progenitor_hermano_vivo == "Si":
            descendiente_ascendiente_conyuge_vivos = st.radio(
                "¿Tiene el difunto algún descendiente, ascendiente o cónyuge no separado legalmente o de hecho vivo?",
                ("Sí", "No"),
            )
            if descendiente_ascendiente_conyuge_vivos == "No":
                hermanos_tio = st.number_input(
                    "¿Cuántos hermanos tenía tu tío a parte de tu progenitor?",
                    min_value=0,
                    max_value=10,
                    value=0,
                    step=1,
                )
                hermanos = st.number_input(
                    "¿Cuántos hermanos tienes",
                    min_value=0,
                    max_value=10,
                    value=0,
                    step=1,
                )
                porcentaje = 100 / ((100 / hermanos_tio) / hermanos + 1)
                personas = hermanos_tio + hermanos
                calcular_herencia(porcentaje, personas, testamento=False, parentesco="Sobrino")
            else:
                st.markdown(" ### No te corresponde ninguna herencia")
        else:
            st.markdown(" ### No te corresponde ninguna herencia")

    else:
        pass


def pregunta_colaterales(hay_testamento):
    if hay_testamento == "No":
        parentesco_colaterales = st.radio(
            "Pregunta adicional: ¿Tiene el difunto algún descendiente, ascendiente, cónyuge no separado legalmente o de hecho vivo, hermano o sobrino?",
            ("Sí", "No"),
        )
        if parentesco_colaterales == "No":
            descendiente_ascendiente_conyuge_hermano_sobrino = st.radio(
                "Pregunta adicional: ¿Hay más primos vivos del difunto?",
                ("Sí", "No"),
            )
            if descendiente_ascendiente_conyuge_hermano_sobrino == "No":
                porcentaje = 100 / 1
                personas = 1
                calcular_herencia(porcentaje, personas, testamento=False, parentesco="Colateral")
            else:
                primos_parte_materna = st.number_input(
                    "Si eres primo por parte materna, ¿cuántos primos maternos vivos tienes? Si eres primo por parte paterna, ¿cuántos primos paternos vivos? Inclúyete a ti",
                    min_value=0,
                    max_value=10,
                    value=0,
                    step=1,
                )

                porcentaje = 50 / (primos_parte_materna + 1)
                personas = primos_parte_materna + 1
                calcular_herencia(porcentaje, personas, testamento=False, parentesco="Colateral")
        else:
            st.markdown(" ### No te corresponde ninguna herencia")

    else:
        pass


def pregunta_otros(hay_testamento):
    if hay_testamento == "No":
        st.markdown(
            " ### No te corresponde ninguna herencia, hereda el Estado en este caso"
        )

    else:
        pass
