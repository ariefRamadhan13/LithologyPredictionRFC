import streamlit as st
import pandas as pd

# Halaman upload file
def halaman_upload_file():
    st.title("Unggah Dua File untuk Prediksi Litologi")

    # Deskripsi untuk menjelaskan pengguna
    st.write("""
    Silakan unggah dua file:
    1. **Data Log Acuan**: Data log yang sudah diketahui dan digunakan untuk referensi.
    2. **Data Log yang akan di Prediksi**: Data log yang belum diketahui dan akan diprediksi berdasarkan model.
    """)

    # Upload file 1: Data Log Acuan
    file1 = st.file_uploader("Unggah Data Log Acuan", type=["csv", "xlsx"])
    
    # Upload file 2: Data Log yang akan Prediksi
    file2 = st.file_uploader("Unggah Data Log yang akan di Prediksi", type=["csv", "xlsx"])

    # Proses jika kedua file diunggah
    if file1 is not None and file2 is not None:
        # Membaca file yang diunggah
        data1 = pd.read_csv(file1) if file1.name.endswith("csv") else pd.read_excel(file1)
        data2 = pd.read_csv(file2) if file2.name.endswith("csv") else pd.read_excel(file2)

        # Menampilkan preview data
        st.subheader("Preview Data Log Acuan")
        st.write(data1.head())  # Menampilkan 5 baris pertama data1
        
        st.subheader("Preview Data Log yang akan di Prediksi")
        st.write(data2.head())  # Menampilkan 5 baris pertama data2

        # Lakukan analisis atau prediksi di sini (misalnya, prediksi atau analisis berdasarkan data)
        st.write("Data berhasil diunggah, sekarang dapat melanjutkan ke proses analisis atau prediksi.")
