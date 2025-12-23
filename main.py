# home.py
import streamlit as st
from PIL import Image

img = Image.open("Logo_Institut_Teknologi_Bandung (1).png")
st.image(img,width = 1500)

def main():
    # Judul aplikasi utama
    st.title("Prediksi Litologi dari MudLog Data")
    
    # Pilihan aplikasi yang ingin dijalankan
    app_choice = st.selectbox("Pilih Aplikasi", ["Prediksi Harga Minyak (ARIMA Model)", "Prediksi Harga Minyak (LSTM Model)","Prediksi Harga Minyak (RNN Model)", "Analisis Downhole P&T (RF)", "Prediksi Litologi (RF)"])
    
    if app_choice == "Prediksi Harga Minyak (ARIMA Model)":
        # Menjalankan aplikasi ARIMA dari Tes2.py
        print('Hello World')

if __name__ == "__main__":
    main()
