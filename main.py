import streamlit as st

# Judul aplikasi
st.title("Prediksi Litologi dari Data Mudlog")

# Deskripsi singkat aplikasi
st.write("""
Aplikasi ini digunakan untuk memprediksi litologi berdasarkan data mudlog. 
Silakan lanjutkan dengan mengunggah dua file untuk analisis.
""")

# Tombol untuk lanjut ke halaman berikutnya
if st.button('Next'):
    st.write("Tombol Next ditekan! Lanjutkan ke halaman upload file.")  # Bisa diganti dengan kode untuk halaman berikutnya
