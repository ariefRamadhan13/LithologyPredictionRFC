import streamlit as st
import upload_file  # Mengimpor file upload_file.py

# Menyimpan status halaman dalam session_state
if 'page' not in st.session_state:
    st.session_state.page = 1  # Halaman pertama (Intro)

# Fungsi untuk halaman pertama (Intro)
def halaman_awal():
    st.title("Prediksi Litologi dengan Data MudLog dengan RandomForestClassification")

    st.write("""
    Aplikasi ini digunakan untuk memprediksi litologi berdasarkan data mudlog menggunakan model RandomForestClassifier. 
    Silakan lanjutkan dengan mengunggah file data yang akan digunakan untuk membuat model.
    """)

    # Tombol untuk lanjut ke halaman berikutnya (upload file)
    if st.button('Next'):
        st.session_state.page = 2  # Mengubah halaman ke halaman upload file

# Fungsi untuk halaman penutup
def halaman_penutup():
    st.title("Terima Kasih telah Menggunakan Aplikasi")

    # Menampilkan gambar penutup
    # st.image("LINE_ALBUM_Arunika part 1_251117_3.jpg", caption="Terima Kasih", use_container_width =True)

    # Opsi untuk kembali ke menu awal
    if st.button('Kembali ke Menu Awal'):
        st.session_state.page = 1  # Kembali ke halaman awal

# Menampilkan halaman yang sesuai berdasarkan status 'page'
if st.session_state.page == 1:
    halaman_awal()  # Menampilkan halaman awal
elif st.session_state.page == 2:
    upload_file.halaman_upload_file()  # Memanggil halaman upload file dari file upload_file.py
elif st.session_state.page == 3:
    upload_file.tampilkan_info_kualitas_data()  # Menampilkan informasi kualitas data setelah file diunggah
elif st.session_state.page == 4:
    upload_file.clean_data()  # Memanggil fungsi untuk membersihkan data
elif st.session_state.page == 5:
    upload_file.tampilkan_heatmap()  # Menampilkan heatmap korelasi antar variabel
elif st.session_state.page == 6:
    upload_file.tampilkan_feature_importance()  # Menampilkan feature importance
elif st.session_state.page == 7:
    upload_file.tampilkan_input_parameters()  # Menampilkan input parameter (train-test split dan top features)
elif st.session_state.page == 8:
    upload_file.tampilkan_perbandingan_aktual_prediksi()  # Menampilkan perbandingan aktual vs prediksi
elif st.session_state.page == 9:
    upload_file.download_prediksi_litologi()  # Menyediakan download prediksi litologi
elif st.session_state.page == 10:
    upload_file.upload_file_baru()  # Halaman untuk upload data mudlog baru
elif st.session_state.page == 11:
    upload_file.tampilkan_perbandingan_aktual_prediksi_baru()  # Menampilkan perbandingan aktual vs prediksi pada data baru
elif st.session_state.page == 12:
    halaman_penutup()  # Halaman penutup
