from pdf_page_number_adder import (
    add_page_numbers
)

import streamlit as st
import base64
import os

def convert_position_name(ja_name):
    en_name = ""
    if ja_name == "右下":
        en_name = "br"
    elif ja_name == "右上":
        en_name = "tr"
    elif ja_name == "左下":
        en_name = "bl"
    elif ja_name == "左上":
        en_name = "tl"
    return en_name

# UI
st.title("PDF Page Number Adder")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    position = st.selectbox("Select position for page number:", ['右上', '右下', '左上', '左下'])
    offset = st.number_input("Enter page number offset:", min_value=0, value=0)

    # ページ番号を追加
    if st.button("Add Page Numbers"):
        position = convert_position_name(position)
        edited_pdf = add_page_numbers(uploaded_file, position, offset)

        # 編集後のPDFプレビュー
        st.subheader("Preview:")
        st_pdf_edited = st.empty()
        pdf_b64_edited = base64.b64encode(edited_pdf.getvalue()).decode('utf-8')
        pdf_edited_display = f'<iframe src="data:application/pdf;base64,{pdf_b64_edited}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_edited_display, unsafe_allow_html=True)

        # ダウンロードリンク
        base_name, _ = os.path.splitext(uploaded_file.name)
        edited_pdf_name = f"{base_name}_edited.pdf"
        href = f'<a href="data:application/pdf;base64,{pdf_b64_edited}" download="{edited_pdf_name}">Download Edited PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
