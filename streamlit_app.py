import streamlit as st
import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
from dateutil import parser

def extract_table_from_pdf(file, password=None):
    try:
        with pdfplumber.open(file, password=password) as pdf:
            all_tables = []
            headers = ["Date", "Transaction Details", "Type", "Amount"]

            for page in pdf.pages:
                raw_text = page.extract_text()
                if not raw_text:
                    continue

                table_settings = {
                    "vertical_strategy": "text",
                    "horizontal_strategy": "lines",
                    "snap_tolerance": 3,
                    "snap_x_tolerance": 3,
                    "snap_y_tolerance": 3,
                    "text_keep_blank_chars": True
                }

                tables = page.extract_tables(table_settings)
                if not tables:
                    continue

                for table_data in tables:
                    if not table_data or len(table_data) < 2:
                        continue

                    if len(table_data[0]) == len(headers):
                        all_tables.extend(table_data)
                    else:
                        adjusted_table = [row[:len(headers)] for row in table_data]
                        all_tables.extend(adjusted_table)

            if not all_tables:
                return None, "No tables detected in the PDF."

            df = pd.DataFrame(all_tables, columns=headers)
            return df, None

    except Exception as e:
        return None, str(e)

def main():
    st.title("PhonePe Transaction Insights")
    st.markdown("This tool extracts data from your PhonePe_Transaction_Statement, provides transactional insights and visualizes the data.")

    uploaded_file = st.file_uploader("Please upload your PhonePe_Transaction_Statement PDF file", type="pdf")
    password = st.text_input("Enter password if the PDF is encrypted (leave blank if not)", type="password")

    if uploaded_file:
        with st.spinner("Processing the PDF..."):
            table_data, error = extract_table_from_pdf(uploaded_file, password=password or None)

        if error:
            st.error(f"Error: {error}")
        elif table_data is not None:
            st.success("Table extracted successfully!")
            st.write("### Extracted Table Data")
            st.dataframe(table_data)
        else:
            st.warning("Please enter your password to extract the table data.")

if __name__ == "__main__":
    main()
