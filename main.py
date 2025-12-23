import streamlit as st
import pandas as pd

# Fungsi untuk halaman upload file
def halaman_upload_file():
    # Judul halaman upload file
    st.title("Unggah Dua File untuk Prediksi Litologi")

    # Deskripsi singkat aplikasi
    st.write("""
    Silakan unggah dua file:
    1. **Data Log Acuan**: Data log yang sudah diketahui dan digunakan untuk referensi.
    2. **Data Log yang akan di Prediksi**: Data log yang belum diketahui dan akan diprediksi berdasarkan model.
    """)

    # Upload file 1: Data Log Acuan
    file1 = st.file_uploader("Unggah Data Log Acuan (File CSV atau Excel)", type=["csv", "xlsx"])
    
    # Upload file 2: Data Log yang akan Prediksi
    file2 = st.file_uploader("Unggah Data Log yang akan di Prediksi (File CSV atau Excel)", type=["csv", "xlsx"])

    # Proses jika kedua file diunggah
    if file1 is not None and file2 is not None:
        # Membaca file yang diunggah
        try:
            if file1.name.endswith("csv"):
                data1 = pd.read_csv(file1)
            else:
                data1 = pd.read_excel(file1)
            
            if file2.name.endswith("csv"):
                data2 = pd.read_csv(file2)
            else:
                data2 = pd.read_excel(file2)

            # Menampilkan preview data dari kedua file
            st.subheader("Preview Data Log Acuan")
            st.write(data1.head())  # Menampilkan 5 baris pertama data1
            
            st.subheader("Preview Data Log yang akan di Prediksi")
            st.write(data2.head())  # Menampilkan 5 baris pertama data2

            st.write("Data berhasil diunggah. Sekarang bisa melanjutkan ke proses analisis atau prediksi.")
        
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses file: {e}")
