import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from io import BytesIO

# Fungsi untuk halaman upload file
def halaman_upload_file():
    # Judul halaman upload file
    st.title("Unggah Data untuk Membuat Model")

    # Deskripsi singkat aplikasi
    st.write("""
    Silakan unggah file **Excel (xlsx)** yang akan digunakan untuk membuat model RandomForestClassifier.
    """)

    # Upload file Excel (xlsx)
    file = st.file_uploader("Unggah Data (File Excel)", type=["xlsx"])

    # Proses jika file diunggah
    if file is not None:
        try:
            # Membaca file Excel yang diunggah
            data = pd.read_excel(file)

            # Menampilkan preview data dari file
            st.subheader("Preview Data yang Diupload")
            st.write(data.head())  # Menampilkan 5 baris pertama data

            # Menyimpan data untuk digunakan di halaman perbandingan kolom dan kualitas data
            st.session_state.data = data

            # Menyediakan tombol untuk melanjutkan
            if st.button('Next'):
                st.session_state.page = 3  # Pindah ke halaman kualitas data

        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses file: {e}")

# Fungsi untuk menampilkan informasi kualitas data
def tampilkan_info_kualitas_data():
    if 'data' in st.session_state:
        data = st.session_state.data

        # Menampilkan info kualitas data asli
        data_info = pd.DataFrame({
            'Jumlah Data': data.count(),
            'Jumlah N/A': data.isna().sum(),
            'Jumlah NaN': data.isnull().sum(),
            'Jumlah -999.25': (data == -999.25).sum()
        })

        # Menampilkan informasi kualitas data
        st.subheader("Informasi Kualitas Data Asli")
        st.write(data_info)

        # Menyediakan tombol untuk melanjutkan ke tahap berikutnya
        if st.button('Next'):
            st.session_state.page = 4  # Pindah ke halaman pembersihan data

# Fungsi untuk membersihkan data (mengganti -999.25 dengan NaN dan menghapus NaN)
def clean_data():
    if 'data' in st.session_state:
        data = st.session_state.data

        # Menyimpan jumlah data sebelum pembersihan
        data_before_cleaning = data.shape[0]  # Jumlah baris sebelum pembersihan

        # Membersihkan data: Mengganti -999.25 dengan NaN dan menghapus baris dengan NaN
        data_cleaned = data.replace(-999.25, pd.NA).dropna()

        # Menyimpan jumlah data setelah pembersihan
        data_after_cleaning = data_cleaned.shape[0]  # Jumlah baris setelah pembersihan

        # Menghitung jumlah data yang dibersihkan (yang terhapus)
        cleaned_rows = data_before_cleaning - data_after_cleaning

        # Menampilkan data setelah pembersihan
        st.subheader("Informasi Kualitas Data Setelah Pembersihan")

        # Menampilkan jumlah data yang dibersihkan
        st.write(f"Jumlah data sebelum pembersihan: {data_before_cleaning}")
        st.write(f"Jumlah data setelah pembersihan: {data_after_cleaning}")
        st.write(f"Jumlah data yang dibersihkan: {cleaned_rows}")

        # Menyimpan data yang sudah dibersihkan
        st.session_state.data_cleaned = data_cleaned

        # Menyediakan tombol untuk melanjutkan ke tahap berikutnya
        if st.button('Next'):
            st.session_state.page = 5  # Pindah ke halaman heatmap korelasi

# Fungsi untuk menampilkan heatmap korelasi antar variabel
def tampilkan_heatmap():
    if 'data_cleaned' in st.session_state:
        data_cleaned = st.session_state.data_cleaned

        # Menghitung korelasi antar variabel
        correlation_matrix = data_cleaned.corr()

        # Membuat heatmap korelasi tanpa angka
        plt.figure(figsize=(12, 8))
        sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title('Heatmap Korelasi Antar Variabel')
        
        # Menampilkan plot heatmap
        st.pyplot(plt)  # Menggunakan st.pyplot() untuk menampilkan plot di Streamlit

        # Menyediakan tombol untuk melanjutkan ke tahap berikutnya
        if st.button('Next'):
            st.session_state.page = 6  # Pindah ke halaman Feature Importance

# Fungsi untuk menampilkan Feature Importance menggunakan RandomForestClassifier
def tampilkan_feature_importance():
    if 'data_cleaned' in st.session_state:
        data_cleaned = st.session_state.data_cleaned

        # Memisahkan fitur dan target
        X = data_cleaned.drop(columns=['LITH'])  # Fitur (semua kolom selain 'LITH')
        y = data_cleaned['LITH']  # Target variabel (Litologi)

        # Melatih model RandomForest untuk menghitung feature importance
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)

        # Mendapatkan feature importance dan mengurutkannya
        feature_importance = model.feature_importances_
        sorted_idx = feature_importance.argsort()

        # Membuat bar plot untuk feature importance
        plt.figure(figsize=(12, 8))
        plt.barh(X.columns[sorted_idx], feature_importance[sorted_idx], color='skyblue')
        plt.title('Feature Importance untuk Memprediksi Litologi (LITH)')
        plt.xlabel('Importance')
        plt.ylabel('Fitur')
        plt.gca().invert_yaxis()  # Membalik urutan fitur dari yang terpenting ke yang kurang penting
        st.pyplot(plt)  # Menampilkan plot heatmap

        # Menyediakan tombol untuk melanjutkan ke tahap berikutnya
        if st.button('Next'):
            st.session_state.page = 7  # Pindah ke halaman analisis atau prediksi

# Fungsi untuk menampilkan input parameter train-test split dan top importance features
def tampilkan_input_parameters():
    if 'data_cleaned' in st.session_state:
        data_cleaned = st.session_state.data_cleaned

        # Memisahkan fitur dan target
        X = data_cleaned.drop(columns=['LITH'])  # Fitur (semua kolom selain 'LITH')
        y = data_cleaned['LITH']  # Target variabel (Litologi)

        # Slider untuk memilih perbandingan train dan test data
        test_size = st.slider('Pilih proporsi data uji (Test Data)', 0.1, 0.9, 0.3, 0.05)

        # Input untuk jumlah fitur teratas berdasarkan importance
        num_top_features = st.number_input('Jumlah Fitur Teratas Berdasarkan Importance', min_value=1, max_value=X.shape[1], value=10)
        print('Klik Proses Kembali')
        if st.button('Proses'):
            # Menghitung feature importance dengan RandomForest
            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            # Mendapatkan feature importance dan mengurutkannya
            feature_importance = model.feature_importances_
            sorted_idx = feature_importance.argsort()

            # Memilih top features berdasarkan input user
            top_features = X.columns[sorted_idx][-(num_top_features):]  # Mengambil fitur teratas
            X_selected = X[top_features]
            st.session_state.top_features = top_features

            # Membagi data menjadi data latih dan data uji
            X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=test_size, random_state=42)

            # Melatih model RandomForest
            model.fit(X_train, y_train)

            # Prediksi pada data uji
            y_pred = model.predict(X_test)

            # Menyimpan data yang dipilih untuk analisis lebih lanjut
            st.session_state.X_train = X_train
            st.session_state.X_test = X_test
            st.session_state.y_train = y_train
            st.session_state.y_test = y_test
            st.session_state.model = model
            st.session_state.y_pred = y_pred  # Menyimpan prediksi pada y_pred

            # Menampilkan informasi model
            st.subheader('Model Random Forest Telah Dilatih')
            st.write(f"Model Random Forest telah dilatih dengan {num_top_features} fitur teratas dan perbandingan {test_size*100}% data uji.")
            st.write(f"Prediksi pertama pada data uji: {y_pred[:5]}")

            # Evaluasi Model
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred, output_dict=True)

            # Menampilkan hasil evaluasi dalam bentuk tabel
            st.subheader("Evaluasi Model Random Forest")

            # Menampilkan akurasi
            st.write(f"Akurasi: {accuracy:.2f}")

            # Menampilkan laporan klasifikasi dalam bentuk tabel
            report_df = pd.DataFrame(report).transpose()
            st.table(report_df)  # Menampilkan tabel evaluasi

            # Menyediakan tombol untuk melanjutkan ke tahap berikutnya
            st.session_state.page = 8  # Pindah ke halaman perbandingan aktual vs prediksi

# Fungsi untuk menampilkan grafik perbandingan aktual dan prediksi
def tampilkan_perbandingan_aktual_prediksi():
    if 'data_cleaned' in st.session_state and 'y_test' in st.session_state and 'y_pred' in st.session_state:
        data_cleaned = st.session_state.data_cleaned
        X_test = st.session_state.X_test
        y_pred = st.session_state.y_pred

        # Menambahkan kolom DEPT dan LITH pada data train dan test untuk plotting
        X_test['DEPT'] = data_cleaned.loc[X_test.index, 'DEPT']  # Menambahkan kolom DEPT ke X_test berdasarkan index
        X_test['LITH'] = data_cleaned.loc[X_test.index, 'LITH']  # Menambahkan kolom LITH ke X_test

        X_test['Predicted_LITH'] = y_pred  # Menambahkan kolom prediksi litologi ke X_test

        litology_mapping = {
            1: 'CLAY, SHALE',
            2: 'SANDSTONE',
            3: 'LIMESTONE',
            4: 'SHALE',
            5: 'COAL'
        }

        # Mengganti kode litologi dengan nama litologi
        X_test['LITH'] = X_test['LITH'].map(litology_mapping)
        X_test['Predicted_LITH'] = X_test['Predicted_LITH'].map(litology_mapping)

        # Menentukan warna berdasarkan litologi
        litology_colors = {'CLAY, SHALE': 'blue', 'SANDSTONE': 'yellow', 'LIMESTONE': 'orange', 'SHALE': 'red', 'COAL': 'purple'}

        # Membuat grafik dengan Depth di sumbu Y dan Litologi di sumbu X
        plt.figure(figsize=(12, 30))

        # Menambahkan offset untuk memisahkan aktual dan prediksi
        actual_offset = 0  # Rentang sumbu X untuk data aktual
        predicted_offset = 2  # Rentang sumbu X untuk data prediksi (terpisah dengan jarak yang jelas)

        # Plot untuk Litologi Aktual (Data Test)
        for i, (lith_name, color) in enumerate(litology_colors.items()):
            actual_depth = X_test[X_test['LITH'] == lith_name]
            plt.barh(actual_depth['DEPT'] + (i * 0.2), [1] * len(actual_depth), color=color, label=f'Actual - {lith_name}', alpha=0.6, left=actual_offset)

        # Plot untuk Litologi Prediksi (Data Test)
        for i, (lith_name, color) in enumerate(litology_colors.items()):
            predicted_depth = X_test[X_test['Predicted_LITH'] == lith_name]
            plt.barh(predicted_depth['DEPT'] + (i * 0.2), [1] * len(predicted_depth), color=color, label=f'Predicted - {lith_name}', alpha=0.6, left=predicted_offset)

        # Mengubah sumbu X menjadi label "Actual" dan "Predicted"
        plt.xlim(-1, 4)  # Menetapkan batas X agar ada ruang untuk "Actual" dan "Predicted"
        plt.xticks([0.5, 2.5], ['Actual', 'Predicted'])  # Menetapkan label X sebagai "Actual" dan "Predicted"

        # Menambahkan slider untuk zoom pada sumbu Y (Depth)
        min_depth = int(X_test['DEPT'].min())
        max_depth = int(X_test['DEPT'].max())
        depth_slider = st.slider('Pilih rentang Depth', min_depth, max_depth, (min_depth, max_depth))

        # Set batas sumbu Y sesuai dengan rentang yang dipilih di slider
        plt.ylim(depth_slider)

        # Menyusun plot agar lebih rapi
        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)  # Menyesuaikan ruang untuk label agar lebih terpusat

        plt.title('Actual vs Predicted Lithology vs Depth')
        plt.xlabel('Litology (Actual and Predicted)')
        plt.ylabel('Depth (FT)')
        plt.legend(title="Litology Names", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.gca().invert_yaxis()  # Membalikkan sumbu Y agar Depth yang lebih kecil muncul di atas
        st.pyplot(plt)  # Menampilkan plot bar

        # Menyediakan tombol untuk melanjutkan ke tahap berikutnya
        if st.button('Next'):
            st.session_state.page = 9  # Pindah ke halaman analisis atau prediksi

def download_prediksi_litologi():
    if 'X_test' in st.session_state and 'y_pred' in st.session_state:
        X_test = st.session_state.X_test
        y_pred = st.session_state.y_pred

        # Mapping litologi
        lithology_map = {
            1: 'CLAY, SHALE',
            2: 'SANDSTONE',
            3: 'LIMESTONE',
            4: 'SHALE',
            5: 'COAL'
        }


        # Menyiapkan DataFrame untuk menyimpan hasil prediksi Depth dan LITH
        predicted_data = pd.DataFrame({
            'DEPT': X_test['DEPT'],
            'Predicted_LITH': y_pred
        })

        # Menambahkan nama litologi berdasarkan prediksi
        predicted_data['Predicted_LITH_Name'] = predicted_data['Predicted_LITH'].map(lithology_map)

        # Simpan DataFrame ke dalam buffer memori
        buffer = BytesIO()
        predicted_data.to_excel(buffer, index=False)
        buffer.seek(0)  # Kembali ke awal buffer setelah penulisan

        # Menyediakan tombol untuk mendownload file
        st.subheader("Download Prediksi Litologi")
        st.write("Klik tombol di bawah untuk mengunduh file prediksi litologi dalam format Excel:")

        st.download_button(
            label="Download Prediksi Litologi",
            data=buffer,
            file_name="predicted_lithology.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Menyediakan tombol Next setelah download
        st.subheader("Apakah Anda ingin menggunakan model yang sama untuk prediksi data lain?")
        
        if st.button('Next'):
            st.session_state.page = 10

def upload_file_baru():
    st.title("Upload Data Mudlog untuk Prediksi Litologi")

    # Deskripsi halaman
    st.write("""
    Halaman ini untuk upload file data mudlog yang belum terdapat data litologi dengan menggunakan model yang sama pada file pertama.
    Silakan unggah file Excel (xlsx) yang berisi data mudlog tanpa litologi.
    """)

    # Upload file Excel (xlsx) untuk data baru
    file_baru = st.file_uploader("Unggah Data Mudlog Baru (File Excel)", type=["xlsx"])

    if file_baru is not None:
        try:
            # Membaca file Excel yang diunggah
            data_baru = pd.read_excel(file_baru)

            # Menampilkan preview data yang diunggah
            st.subheader("Preview Data yang Diupload")
            st.write(data_baru.head())  # Menampilkan 5 baris pertama data

            # Menyimpan data untuk diproses lebih lanjut
            st.session_state.data_baru = data_baru

            # Menyediakan tombol untuk melanjutkan proses
            if st.button('Proses Prediksi Litologi'):
                # Pastikan model yang sudah dilatih ada di session state
                if 'model' in st.session_state:
                    model = st.session_state.model
                    top_features = st.session_state.top_features  # Mengambil fitur teratas yang disimpan sebelumnya
                    # Menggunakan model yang telah dilatih untuk memprediksi litologi pada data baru
                    X_baru = data_baru[top_features]  # Menggunakan hanya fitur teratas
                    st.session_state.X_baru = X_baru
                    y_pred_baru = model.predict(X_baru)
                    st.session_state.y_pred_baru = y_pred_baru

                    lithology_map = {
                        1: 'CLAY, SHALE',
                        2: 'SANDSTONE',
                        3: 'LIMESTONE',
                        4: 'SHALE',
                        5: 'COAL'
                    }

                    # Menambahkan kolom 'Predicted_LITH' ke data baru
                    data_baru['Predicted_LITH'] = y_pred_baru
                    data_baru['Predicted_LITH_NAME'] = data_baru['Predicted_LITH'].map(lithology_map)

                    # Menyimpan data prediksi ke dalam file Excel di memori (menggunakan BytesIO)
                    buffer = BytesIO()
                    data_baru.to_excel(buffer, index=False)
                    buffer.seek(0)  # Kembali ke awal buffer setelah penulisan

                    # Menampilkan hasil prediksi
                    st.subheader("Hasil Prediksi Litologi")
                    st.write(data_baru[['DEPT', 'Predicted_LITH_NAME']])

                    # Menyediakan tombol untuk mendownload file prediksi
                    st.write("Klik tombol di bawah untuk mengunduh file prediksi litologi dalam format Excel:")

                    # Membuat tombol download menggunakan buffer
                    st.download_button(
                        label="Download Prediksi Litologi",
                        data=buffer,
                        file_name="predicted_lithology_baru.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                    # Menyediakan tombol Next setelah download
                    st.session_state.page = 11  # Pindah ke halaman analisis atau prediksi lainnya
                # Memaksa Streamlit merender ulang dan memuat halaman baru

                else:
                    st.error("Model belum tersedia. Pastikan Anda sudah melatih model terlebih dahulu.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses file: {e}")

def tampilkan_perbandingan_aktual_prediksi_baru():
    if 'data_baru' in st.session_state and 'y_pred_baru' in st.session_state:
        data_baru = st.session_state.data_baru
        y_pred_baru = st.session_state.y_pred_baru

        # Menambahkan kolom DEPT dan LITH pada data baru untuk plotting
        data_baru['Predicted_LITH'] = y_pred_baru  # Menambahkan kolom prediksi litologi ke data baru

        # Mapping litologi
        lithology_map = {
            1: 'CLAY, SHALE',
            2: 'SANDSTONE',
            3: 'LIMESTONE',
            4: 'SHALE',
            5: 'COAL'
        }

        data_baru['Predicted_LITH_Name'] = data_baru['Predicted_LITH'].map(lithology_map)

        # Menentukan warna berdasarkan litologi
        litology_colors = {'CLAY, SHALE': 'blue', 'SANDSTONE': 'yellow', 'LIMESTONE': 'orange', 'SHALE': 'red', 'COAL': 'purple'}

        # Membuat grafik dengan Depth di sumbu Y dan Litologi di sumbu X
        plt.figure(figsize=(12, 30))

        # Menentukan offset untuk memisahkan aktual dan prediksi
        actual_offset = 0  # Rentang sumbu X untuk data aktual
        predicted_offset = 1  # Rentang sumbu X untuk data prediksi (terpisah dengan jarak yang jelas)

        # Plot untuk Litologi Prediksi (Data Baru)
        for i, (lith_name, color) in enumerate(litology_colors.items()):
            predicted_depth = data_baru[data_baru['Predicted_LITH_Name'] == lith_name]
            plt.barh(predicted_depth['DEPT'] + (i * 0.2), [1] * len(predicted_depth), color=color, label=f'Predicted - {lith_name}', alpha=0.6, left=predicted_offset)

        # Mengubah sumbu X menjadi label "Predicted"
        plt.xlim(-1, 4)  # Menetapkan batas X agar ada ruang untuk "Predicted"
        plt.xticks([0, 1.5], ['','Predicted'])  # Menetapkan label X sebagai "Actual" dan "Predicted"

        # Menambahkan slider untuk zoom pada sumbu Y (Depth)
        min_depth = int(data_baru['DEPT'].min())
        max_depth = int(data_baru['DEPT'].max())
        depth_slider = st.slider('Pilih rentang Depth', min_depth, max_depth, (min_depth, max_depth))

        # Set batas sumbu Y sesuai dengan rentang yang dipilih di slider
        plt.ylim(depth_slider)

        # Menyusun plot agar lebih rapi
        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)  # Menyesuaikan ruang untuk label agar lebih terpusat

        plt.title('Prediksi Litologi vs Depth')
        plt.xlabel('Prediksi Litologi')
        plt.ylabel('Depth (FT)')
        plt.legend(title="Litology Names", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.gca().invert_yaxis()  # Membalikkan sumbu Y agar Depth yang lebih kecil muncul di atas
        st.pyplot(plt)  # Menampilkan plot bar

        # Menyediakan tombol untuk melanjutkan ke tahap berikutnya
        if st.button('Next'):
            st.session_state.page = 12
