import streamlit as st
import pandas as pd
from io import BytesIO

st.title("File Converter and Cleaner")
st.write("Upload CSV or Excel files and clean them")

files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        if ext == "csv":
            df = pd.read_csv(file)
            st.subheader(f" {file.name} - preview")
            st.dataframe(df)

            if st.checkbox(f"Fill Missing Values - {file.name}"):
                df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
                st.success("Missing values filled")
                st.dataframe(df)
        
            selected_columns = st.multiselect(f"Select columns - {file.name}", df.columns, default=df.columns)
            df = df[selected_columns]
            st.dataframe(df)
        
        elif ext == "xlsx":
            all_sheets = pd.read_excel(file, sheet_name=None)

            for sheet_name, df in all_sheets.items():
                st.subheader(f"{file.name} - {sheet_name} preview")
                st.dataframe(df)

                if st.checkbox(f"Fill Missing Values - {file.name} / {sheet_name}"):
                    df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
                    st.success("Missing values filled")
                    st.dataframe(df)

                selected_columns = st.multiselect(f"Select columns - {file.name} / {sheet_name}", df.columns, default=df.columns)
                df = df[selected_columns]
                st.dataframe(df)

        else:
            st.error("Unsupported file type")

