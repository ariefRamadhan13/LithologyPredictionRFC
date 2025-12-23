import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# File Upload
st.title("Data Analysis with File Uploads")
file1 = st.file_uploader("Upload First File", type=['csv', 'xlsx'])
file2 = st.file_uploader("Upload Second File", type=['csv', 'xlsx'])

# Check if files are uploaded
if file1 is not None and file2 is not None:
    # Load the files into pandas dataframes
    data1 = pd.read_csv(file1) if file1.name.endswith('csv') else pd.read_excel(file1)
    data2 = pd.read_csv(file2) if file2.name.endswith('csv') else pd.read_excel(file2)

    # Display first rows of the data
    st.subheader("Data Preview")
    st.write("First File Data", data1.head())
    st.write("Second File Data", data2.head())

    # Example analysis: Correlation heatmap for the first file
    st.subheader("Correlation Heatmap")
    correlation_matrix = data1.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    st.pyplot()

    # Example: Save processed data to CSV
    processed_file1 = "processed_file1.csv"
    processed_file2 = "processed_file2.csv"
    
    # Assuming some processing logic is done here
    data1.to_csv(processed_file1, index=False)
    data2.to_csv(processed_file2, index=False)
    
    # Provide download links
    st.subheader("Download Processed Files")
    st.download_button(label="Download Processed File 1", data=open(processed_file1, 'rb').read(), file_name=processed_file1)
    st.download_button(label="Download Processed File 2", data=open(processed_file2, 'rb').read(), file_name=processed_file2)
