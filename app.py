import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

st.title("Citas de Lana Del Rey")

# Carga de la nueva imagen
image = Image.open('gato_artista.jpg')  # Asegúrate de tener este archivo en la misma carpeta
st.image(image, width=350)

with st.sidebar:
    st.subheader("Escribe una cita melancólica y escúchala en voz alta.")

# Crear carpeta temporal si no existe
try:
    os.mkdir("temp")
except:
    pass

# Texto fijo en pantalla
st.subheader("Fragmento Inspirado en Lana Del Rey")
st.write('A veces me siento como si caminara por una autopista solitaria al atardecer, '
         'con la brisa del verano acariciando mi piel, y la tristeza suave de una canción vieja '
         'llenando el aire. Nací para morir, pero por un momento... viví como en un sueño.')

st.markdown("¿Quieres escuchar tu propia cita al estilo Lana? Escribe aquí abajo:")

text = st.text_area("Ingresa tu texto melancólico:")

# Idiomas disponibles
option_lang = st.selectbox(
    "Selecciona el idioma",
    ("Español", "English", "Français", "Português"))

# Diccionario de idiomas
lang_map = {
    "Español": "es",
    "English": "en",
    "Français": "fr",
    "Português": "pt"
}
lg = lang_map[option_lang]

# Conversión de texto a voz
def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

if st.button("Convertir a Audio"):
    result, output_text = text_to_speech(text, 'com', lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown("## Tu audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    with open(f"temp/{result}.mp3", "rb") as f:
        data = f.read()

    def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Descargar {file_label}</a>'
        return href

    st.markdown(get_binary_file_downloader_html(f"temp/{result}.mp3", file_label="Archivo de Audio"), unsafe_allow_html=True)

# Limpieza de archivos viejos
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Eliminado ", f)

remove_files(7)
