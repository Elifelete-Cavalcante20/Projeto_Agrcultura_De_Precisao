import streamlit as st
import tensorflow as tf
import numpy as np
import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# =====================================================
# FUNÇÃO PARA GERAR PDF
# =====================================================
def gerar_pdf(imagem_path, classe, dica):
    pdf_path = "relatorio_planta.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Título
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 80, "Relatório de Diagnóstico de Planta")

    # Classe identificada
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 130, f"Diagnóstico: {classe}")

    # Dicas
    c.setFont("Helvetica", 12)
    text = c.beginText(50, height - 170)
    text.textLines(f"Dicas de cuidado:\n{dica}")
    c.drawText(text)

    # Imagem
    try:
        img = ImageReader(imagem_path)
        c.drawImage(img, 50, 100, width=200, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print("Erro ao carregar imagem no PDF:", e)

    c.showPage()
    c.save()
    return pdf_path

# =====================================================
# FUNÇÃO DE PREDIÇÃO
# =====================================================
def model_prediction(image_path):
    model = tf.keras.models.load_model(
        r'C:\Users\SRV\Projeto_Agrcultura_De_Precisao\Plant_Disease_Prediction\trained_plant_disease_model.keras'
    )
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.expand_dims(input_arr, axis=0)
    prediction = model.predict(input_arr)
    result_index = np.argmax(prediction)
    return result_index

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("MENU")
app_mode = st.sidebar.selectbox("Select Page", ["INICIO", "SOBRE", "RECONHECIMENTO"])

# =====================================================
# HOME PAGE
# =====================================================
if app_mode == "INICIO":
    st.header("SISTEMA DE RECONHECIMENTO DE DOENÇAS DE PLANTAS")
    image_path = r"C:\Users\SRV\Projeto_Agrcultura_De_Precisao\Plant_Disease_Prediction\home_page.jpeg"
    st.image(image_path, width="stretch")
    st.markdown("""
        Bem-vindo ao Sistema de Reconhecimento de Doenças de Plantas!

        Nossa missão é ajudar na identificação de doenças em plantas de forma eficiente.
        Envie uma imagem na aba **RECONHECIMENTO** e veja o diagnóstico!
    """)

# =====================================================
# PÁGINA SOBRE
# =====================================================
elif app_mode == "SOBRE":
    st.header("SOBRE")
    with st.expander("FUNCIONAMENTO E OBJETIVOS"):
        st.write("""
        O sistema realiza a classificação automática de imagens agrícolas por meio de modelos de visão computacional.
        """)

    with st.expander("MAIS INFORMAÇÕES"):
        st.subheader("INTEGRANTES")
        st.write("""
        - Elifelete Cavalcante  
        - Daniel Lopes  
        - Murilo Laino  
        - Gabriel Gardenal  
        - Gabriel Lopes  
        - Emanuel Moura  
        - Carlos Eduardo  
        """)

        st.subheader("SOBRE A INSTITUIÇÃO")
        st.write("""
        **DISCIPLINA:** Complexidade de Algoritmos  
        **CURSO:** Ciência da Computação  
        """)

    with st.expander("SOBRE O DATASET"):
        st.markdown("""
            Dataset original do Kaggle com cerca de 87 mil imagens divididas em 38 classes.
        """)

# =====================================================
# PÁGINA DE RECONHECIMENTO
# =====================================================
elif app_mode == "RECONHECIMENTO":
    st.header("RECONHECIMENTO")

    test_image = st.file_uploader("Escolher imagem:", type=["jpg", "jpeg", "png"])

    # Lista de classes
    class_name = [
        'Maçã - Sarna da maçã',
        'Maçã - Podridão negra da maçã',
        'Maçã - Ferrugem do cedro da maçã',
        'Maçã - Saudável',
        'Mirtilo - Saudável',
        'Cereja (incluindo azeda) ___ Oídio',
        'Cereja (incluindo azeda) ___ Saudável',
        'Milho - Mancha foliar de Cercospora (Mancha cinzenta da folha)',
        'Milho - Ferrugem comum',
        'Milho - Queima do norte da folha',
        'Milho - Saudável',
        'Uva - Podridão negra',
        'Uva - Esca (Sarampo negro)',
        'Uva - Queima da folha (Mancha foliar de Isariopsis)',
        'Uva - Saudável',
        'Laranja - Huanglongbing (Greening cítrico)',
        'Pêssego - Mancha bacteriana',
        'Pêssego - Saudável',
        'Pimentão - Mancha bacteriana',
        'Pimentão - Saudável',
        'Batata - Queima precoce',
        'Batata - Requeima tardia',
        'Batata - Saudável',
        'Framboesa - Saudável',
        'Soja - Saudável',
        'Abóbora - Oídio',
        'Morango - Escaldadura da folha',
        'Morango - Saudável',
        'Tomate - Mancha bacteriana',
        'Tomate - Queima precoce',
        'Tomate - Requeima tardia',
        'Tomate - Mofo da folha',
        'Tomate - Mancha de Septoria',
        'Tomate - Ácaros (Ácaro-rajado de duas manchas)',
        'Tomate - Mancha-alvo',
        'Tomate - Vírus do enrolamento amarelo da folha do tomateiro',
        'Tomate - Vírus do mosaico do tomateiro',
        'Tomate - Saudável'
    ]

    # =====================================================
    # Processamento após upload
    # =====================================================
    if test_image is not None:
        image_bytes = test_image.read()

        # Mostrar imagem
        if st.button("Mostrar Imagem"):
            st.image(image_bytes, width="stretch")

        # Salvar imagem temporária
        temp_path = "imagem_temp.jpg"
        with open(temp_path, "wb") as f:
            f.write(image_bytes)

        # Botão de predição
        if st.button("Prever Doença"):
            with st.spinner("Aguarde..."):
                result_index = model_prediction(temp_path)
                classe_predita = class_name[result_index]

                # Salvar no session_state
                st.session_state['classe_predita'] = classe_predita
                st.session_state['temp_path'] = temp_path

                # Carregar dicas JSON
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                json_path = os.path.join(BASE_DIR, "dicas.json")
                with open(json_path, "r", encoding="utf-8") as f:
                    dicas = json.load(f)

                dica = dicas.get(classe_predita, "Nenhuma dica cadastrada para essa doença.")
                st.session_state['dica'] = dica

                st.success(f"Possibilidade de: {classe_predita}")
                st.subheader("💡 Dicas de cuidado")
                st.write(dica)

        # Botão para gerar PDF fora do bloco de predição
        if 'classe_predita' in st.session_state:
            if st.button("Gerar PDF do relatório"):
                pdf_path = gerar_pdf(
                    st.session_state['temp_path'],
                    st.session_state['classe_predita'],
                    st.session_state['dica']
                )
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="Baixar Relatório PDF",
                        data=f,
                        file_name="relatorio_planta.pdf",
                        mime="application/pdf"
                    )
