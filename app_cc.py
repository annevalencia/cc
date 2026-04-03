# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 08:23:46 2026

@author: ane.valencia
"""

import os
import pandas as pd
import time
from datetime import datetime
import random
import pytz

import streamlit as st



# Configuración de los saludos por franjas
timezone = pytz.timezone('Europe/Madrid')
hora_actual = datetime.now(timezone).hour

saludos_franjas = {
    "mañana": [
        "¿Ya estás angustiada de par de mañana o esperamos al segundo Colacao? Relaxxxx☕️",
        "¡Venga! A la piscina, que las jubiladas no se vigilan solas. 🏊‍♀️ No les dejes ahogarse porfi :)",
        'Egun on! ¿Cómo te has levantado hoy? ¿Rollo telenovela? Creo que son cosas que nunca voy a entender... porque marica se nace'  
    ],
    "tarde": [
        "¿Qué tal van las clases? Digo además de cotorrear con las alumnas, que eso ya sé que bien...",
        "No sé a qué hora estás leyendo esto, pero si has empezado ya con las cañas, seguro que te quedan numerosas visitas al baño... ¡ánimo!",
        "¿Hoy toca drama nuevo o reciclamos uno? El que sea pero siempre consuelo mutuo, aquí me tienes ;)"
    ],
    "noche": [
        "¡Tira a dormir! Que entre tus angustias y el colesterol lo mejor que puedes hacer es meterte a la cama 💤",
        "¡Hora de dormir la mona! Un día más haciéndole reir (y de oro) a tu psicóloga 🤪",
        "¿La vejiga bien? Tira a mear ahora, no sea que te levantes a las 3 de la madrugada... 🚽"
    ],
    "madrugada": [
        "¿Pero qué haces despierta a estas horas? 🦉 ¡A dormir!",
        "Cris... son horas de estar durmiendo, no con las pantallitas... 😴",
        "Iscariot!!! A estas horas Jesucristo ya estaba más que traicionado, ¡tira a dormir pero ya!"
    ]
}

# Lógica de selección de franja
if 'saludo_fijo' not in st.session_state:
    if 6 <= hora_actual < 13:
        franja = "mañana"
    elif 13 <= hora_actual < 21:
        franja = "tarde"
    elif (21 <= hora_actual <= 23) or (0 <= hora_actual < 1):
        franja = "noche"
    else:
        franja = "madrugada"
    
    # Guardamos un saludo aleatorio en la "memoria" de la app
    st.session_state.saludo_fijo = random.choice(saludos_franjas[franja])



# Configuración de la página
st.set_page_config(page_title="Felicidades Cris!", page_icon="🎁")

# --- ESTILO PERSONALIZADO (Rose Gold & Modern) ---
st.markdown("""
    <style>
    /* Fondo rosa muy, muy sutil (casi blanco) */
    .stApp {
        background-color: #FFF9FA;
    }
    
    /* Botones con estilo "Pill" (pastilla) modernos */
    .stButton>button {
        border-radius: 25px;
        border: 1px solid #F4C2C2;
        background-color: white;
        color: #D47D7D;
        font-weight: 500;
        padding: 10px 20px;
        transition: all 0.3s ease;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.02);
    }
    
    .stButton>button:hover {
        background-color: #F4C2C2;
        color: white;
        border: 1px solid #F4C2C2;
        transform: translateY(-2px);
        box-shadow: 4px 4px 10px rgba(0,0,0,0.05);
    }
    
    .stCaption {
        color: #7D5D5D !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        margin-bottom: 10px !important;
    }
    
    /* Títulos en rosa viejo */
    h1, h2, h3 {
        color: #B57171 !important;
        font-family: 'Segoe UI', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


## --- FUNCIONES ---

# PAra el ordenador
# def devolver_elemento_excel(elem):
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     ruta_excel = os.path.join(base_dir, 'frases_app_cc.xlsx')
    
#     try:
#         df = pd.read_excel(ruta_excel, sheet_name=elem)
#         fila = df.sample().iloc[0]
        
#         # Esta parte limpia los nombres de archivo que vienen del Excel
#         columnas_multimedia = ['Imagen', 'Respuestas imagen', 'Respuestas audio', 'Audio1', 'Audio2']
#         for col in columnas_multimedia:
#             if col in fila and pd.notna(fila[col]):
#                 # Cogemos solo el nombre del archivo, por si se te ha olvidado 
#                 # alguna ruta de Windows en el Excel, esto intenta limpiar:
#                 nombre_limpio = str(fila[col]).split('\\')[-1].split('/')[-1].strip()
                
#                 # Ahora le decimos a Streamlit que el archivo está en la misma carpeta que el código
#                 fila[col] = os.path.join(base_dir, nombre_limpio)
                
#         return fila
#     except Exception as e:
#         st.error(f"Error al leer la hoja {elem}: {e}")
#         return None

# PAra GitHub
def devolver_elemento_excel(elem):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_excel = os.path.join(base_dir, 'frases_app_cc.xlsx')
    
    try:
        df = pd.read_excel(ruta_excel, sheet_name=elem)
        fila = df.sample().iloc[0]
        
        columnas_multimedia = ['Imagen', 'Respuestas imagen', 'Respuestas audio', 'Audio1', 'Audio2']
        for col in columnas_multimedia:
            if col in fila and pd.notna(fila[col]):
                # 1. Convertimos a string y quitamos espacios
                ruta_sucia = str(fila[col]).strip()
                # 2. TRUCO: Cambiamos las barras \ de Windows por / de Linux
                ruta_linux = ruta_sucia.replace('\\', '/')
                # 3. Creamos la ruta completa
                fila[col] = os.path.join(base_dir, ruta_linux)
                
        return fila
    except Exception as e:
        st.error(f"Error al leer la hoja {elem}: {e}")
        return None
    

## --- INTERFAZ ---

# st.title("🌈 El rincón de Cris")
# st.subheader("¿De qué estamos hoy?")
st.markdown(f"""
    <div style="text-align: center; padding: 10px 0px 30px 0px;">
        <h1 style="font-family: 'Trebuchet MS', sans-serif; font-size: 2.2rem; margin-bottom: 5px;">
            🌈 El txokito de Cris
        </h1>
        <p style="color: #D47D7D; font-size: 1.1rem; opacity: 0.8;">
            {st.session_state.saludo_fijo}
        </p>
    </div>
    """, unsafe_allow_html=True)

# Un separador con estrellas pequeño y discreto
st.markdown("<div style='text-align: center; color: #F4C2C2; margin-bottom: 20px;'>✦ ✦ ✦</div>", unsafe_allow_html=True)

st.write("#### ¿De qué tenemos ganas hoy?")



# Creamos 4 columnas para los botones
col1, col2, col3, col4 = st.columns(4)

opcion = None
with col1:
    if st.button("😜 Chiiiiiste"):
        opcion = 'Chistes'

with col2:
    if st.button("💡 Funfact!!"):
        opcion = 'Funfacts'
    
with col3:
    if st.button("🤔 Reflexión"):
        opcion = 'Reflexiones'
        
with col4:
    if st.button("✨ Highlights"):
        opcion = 'Highlights'
        





# --- VISUALIZACIÓN  ---

# Contenedor vacío que ocupará todo el espacio de abajo
placeholder = st.empty()

if opcion:
    # Al entrar vaciar el contenedor para dejar limpio lo que hubiera de la opción anterior 
    placeholder.empty()
    
    resultado = devolver_elemento_excel(opcion)
    
    if resultado is not None:
        # Metemos todo el contenido dentro del contenedor 'with placeholder.container():'
        with placeholder.container():
            
            ## REFLEXIONES
            if opcion in ['Reflexiones', 'Frases']:
                
                st.caption('De vez en cuando, también una se puede poner un poco sentimental...')
                
                texto = resultado[opcion]
                # Paleta Zen-Elegante (Integrada con el Rose Gold)
                color_tarjeta = "#FFFFFF" 
                color_detalle = "#8DA399"  # El verde salvia que te gustaba
                color_texto = "#5D5D5D"    # Gris suave para lectura
                
                # Construimos el HTML limpio
                html_reflexion = f"""
                <div style="background-color:{color_tarjeta};padding:50px 30px;border-radius:20px;border:1px solid #F0F4F2;text-align:center;margin:20px 0px;box-shadow:0px 8px 25px rgba(141,163,153,0.12);position:relative;">
                    <div style="background-color:white;width:55px;height:55px;line-height:55px;border-radius:50%;margin:-75px auto 20px auto;font-size:1.6rem;box-shadow:0px 5px 15px rgba(141,163,153,0.1);border:1px solid #F0F4F2;">🌿</div>
                    <h4 style="color:{color_detalle};font-family:'Trebuchet MS',sans-serif;font-size:0.8rem;letter-spacing:3px;text-transform:uppercase;margin-bottom:20px;font-weight:bold;opacity:0.8;">Bienvenida al rincón de pensar</h4>
                    <p style="font-family:'Segoe UI',sans-serif;font-size:1.3rem;color:{color_texto};line-height:1.8;margin-bottom:0;font-weight:300;font-style:italic;">
                        "{texto}"
                    </p>
                    <div style="width:30px;height:2px;background-color:{color_detalle};margin:25px auto 0 auto;border-radius:2px;opacity:0.3;"></div>
                </div>
                """
                
                st.markdown(html_reflexion, unsafe_allow_html=True)
                
                
            ## CHISTES    
            elif opcion == 'Chistes':
                st.caption('Creo que ya te puedes imaginar el nivel de esta sección... por eso no me preocupo 😜')
                
                # Parte 1: Pregunta
                st.markdown(f"### {resultado['Chistes']}")
                
                # Espera 2 segundos con un spinner visual
                with st.spinner('Tranquiiiila, ahora te lo digo ;)'):
                    time.sleep(1.5)
                st.balloons() # ¡Fiesta de globos al dar la respuesta!
                st.toast("BA DUM TSSSS! 🥁") 
                
                # Parte 2: Respuesta (SOLO si no es nan / vacío)
                if pd.notna(resultado.get('Respuestas txt')):
                    st.markdown(f" #### **{resultado['Respuestas txt']}**")
                
                # Parte 3: Audio (si existe y no es NaN)
                if pd.notna(resultado.get('Respuestas audio')):
                    st.audio(resultado['Respuestas audio'])
                
                # Parte 4: Imagen (si existe y no es NaN)
                if pd.notna(resultado.get('Respuestas imagen')):
                    st.image(resultado['Respuestas imagen'], use_container_width=True)
    
    
            ## FUNFACTS
            elif opcion == 'Funfacts':
                st.caption('¡Nunca a la cama te irás sin saber una cosa más! De nada💋')
                # st.info(resultado['Funfacts'])
                # if pd.notna(resultado.get('Imagen')):
                #     st.image(resultado['Imagen'], use_container_width=True)
                texto = str(resultado['Funfacts']).strip()
                # Paleta coherente con el diseño principal (Rose Gold)
                color_tarjeta = "#FFFFFF"  # Blanco puro para que resalte
                color_borde = "#f6a0a0"    # El rosa de tus botones
                color_titulo = "#D47D7D"   # Un rosa más oscuro para el texto
                color_texto = "#5D5D5D"    # Gris suave para que no sea agresivo
    
                # Construimos el HTML en una sola cadena limpia
                html_funfact = f"""
                <div style="background-color:{color_tarjeta};padding:40px 30px;border-radius:20px;border:1px solid #FFF0F0;text-align:center;margin:20px 0px;box-shadow:0px 8px 20px rgba(244,194,194,0.15);position:relative;">
                    <div style="background-color:white;width:55px;height:55px;line-height:55px;border-radius:50%;margin:-70px auto 20px auto;font-size:1.6rem;box-shadow:0px 5px 15px rgba(212,125,125,0.1);border:1px solid #FFF0F0;">💡</div>
                    <h4 style="color:{color_titulo};font-family:'Trebuchet MS',sans-serif;font-size:1.15rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:15px;font-weight:bold;">¿Sabías que...?</h4>
                    <p style="font-family:'Segoe UI',sans-serif;font-size:1rem;color:{color_texto};line-height:1.7;margin-bottom:0;font-weight:350;">
                        {texto}
                    </p>
                    <div style="width:40px;height:2px;background-color:{color_borde};margin:20px auto 0 auto;border-radius:2px;opacity:0.5;"></div>
                </div>
                """
                
                # Renderizamos usando markdown con unsafe_allow_html
                st.markdown(html_funfact, unsafe_allow_html=True)
                                
                # Imagen (si existe) fuera del recuadro
                if pd.notna(resultado.get('Imagen')):
                    st.image(resultado['Imagen'], use_container_width=True, caption="Miraaaa, es verdad :)")
                    
                    
            ## HIGHLITHS
            elif opcion == 'Highlights':
                st.caption('Un repasito a cosicas que hemos compartido ;)')
                st.markdown(f"#### {resultado['Titulo']}")
                st.write(f"{resultado['Descripcion']}")
                st.divider() 
                
                # Imagen (si existe)
                if pd.notna(resultado.get('Imagen')):
                    st.image(resultado['Imagen'], use_container_width=True)
                    
                # Audio 1 (si existe)
                if pd.notna(resultado.get('Audio1')):
                    st.write("🎵 Puedes refrescar los oídos:")
                    st.audio(resultado['Audio1'])
                    
                # Audio 2 (si existe, debajo del primero)
                if pd.notna(resultado.get('Audio2')):
                    if pd.isna(resultado.get('Audio1')): # Por si solo hay audio 2
                         st.write("🎵 Y otro más:")
                    st.audio(resultado['Audio2'])
                    


# Un pie de página pequeñito y cariñoso
st.markdown("---")
st.caption("Hecho con ❤️ , de Anne para Cris :)")