import streamlit as st
import tensorflow as tf
import numpy as np

#Tensorflow Model Prediction
def model_prediction(test_image):
    model  = tf.keras.models.load_model(r'C:\Users\SRV\Projeto_Agrcultura_De_Precisao\Plant_Disease_Prediction\trained_plant_disease_model.keras')
    image = tf.keras.preprocessing.image.load_img(test_image,target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr]) #Convert single image to a batch
    prediction = model.predict(input_arr)
    result_index = np.argmax(prediction)
    return result_index

#Sidebar
st.sidebar.title("MENU")
app_mode = st.sidebar.selectbox("Select Page",["INICIO","SOBRE","RECONHECIMENTO"])

#Home Page
if(app_mode=="INICIO"):
    st.header("SISTEMA DE RECONHECIMENTO DE DOENÇAS DE PLANTAS")
    image_path = r"C:\Users\SRV\Projeto_Agrcultura_De_Precisao\Plant_Disease_Prediction\home_page.jpeg"
    st.image(image_path, use_container_width=True)
    st.markdown("""
    Bem-vindo ao Sistema de Reconhecimento de Doenças de Plantas! 🌿🔍

Nossa missão é ajudar na identificação de doenças em plantas de forma eficiente. Faça upload de uma imagem de uma planta e nosso sistema irá analisá-la para detectar sinais de doenças. Juntos, vamos proteger nossas plantações e garantir uma colheita mais saudável!

### Como Funciona
1. **Enviar Imagem:** Vá para a página **Reconhecimento de Doenças** e envie uma imagem de uma planta com suspeita de doença.
2. **Análise:** Nosso sistema processará a imagem usando algoritmos avançados para identificar possíveis doenças.
3. **Resultados:** Veja os resultados e recomendações para ações futuras.

### Por que Escolher Nós?
- **Precisão:** Nosso sistema utiliza técnicas avançadas de aprendizado de máquina para detecção precisa de doenças.
- **Fácil de Usar:** Interface simples e intuitiva para uma experiência do usuário tranquila.
- **Rápido e Eficiente:** Receba resultados em segundos, permitindo uma tomada de decisão rápida.

### Comece Agora
Clique na página **Reconhecimento de Doenças** na barra lateral para enviar uma imagem e experimentar o poder do nosso Sistema de Reconhecimento de Doenças em Plantas!

### Sobre Nós
Saiba mais sobre o projeto, nossa equipe e nossos objetivos na página **Sobre**.
""")

#About Page
elif(app_mode=="SOBRE"):
    st.header("SOBRE")
    st.markdown("""
    #### About Dataset
    This dataset is recreated using offline augmentation from the original dataset. The original dataset can be found on this github repo. This dataset consists of about 87K rgb images of healthy and diseased crop leaves which is categorized into 38 different classes. The total dataset is divided into 80/20 ratio of training and validation set preserving the directory structure. A new directory containing 33 test images is created later for prediction purpose.
    #### Content
    1. Train (70295 images)
    2. Valid (17572 image)
    3. Test (33 images)
""")
    
#Prediction Page
elif(app_mode=="RECONHECIMENTO"):
    st.header("RECONHECIMENTO")
    test_image = st.file_uploader("Choose an Image:")
    if(st.button("Show Image")):
        st.image(test_image,use_column_width=True)
    #Predict Button
    if(st.button("Predict")):
        with st.spinner("Please Wait.."):
            st.write("Our Prediction")
            result_index = model_prediction(test_image)
            #Define Class
            class_name = ['Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy']
        st.success("Model is Predicting it's a {}".format(class_name[result_index]))
