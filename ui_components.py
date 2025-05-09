import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from io import BytesIO
from utils import format_tanggal_indonesia, generate_pdf_from_html

def display_filters(df):
    st.subheader("🎛️ Filter Data")
    kategori_opsi = ["Semua"] + sorted(df["Kategori"].dropna().unique().tolist())
    instansi_opsi = ["Semua"] + sorted(df["Instansi"].dropna().unique().tolist())

    selected_kategori = st.selectbox("Jenis Pengadaan", kategori_opsi)
    selected_instansi = st.selectbox("Nama K/L/PD/Instansi Lainnya", instansi_opsi)

    if selected_kategori != "Semua":
        df = df[df["Kategori"] == selected_kategori]
    if selected_instansi != "Semua":
        df = df[df["Instansi"] == selected_instansi]

    search_query = st.text_input("🔍 Cari Nama Paket")
    if search_query:
        df = df[df["Nama Paket"].str.contains(search_query, case=False, na=False)]

    return df

def display_table(df_display):
    st.subheader("📄 Daftar Tender")
    gb = GridOptionsBuilder.from_dataframe(df_display)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
    gb.configure_default_column(resizable=True, sortable=True, filter=True)
    grid_options = gb.build()

    AgGrid(
        df_display,
        gridOptions=grid_options,
        enable_enterprise_modules=False,
        fit_columns_on_grid_load=True,
        height=500
    )

def display_download_buttons(df_display, tahun):
    st.subheader("⬇️ Unduh Data")

    col1, col2, col3 = st.columns(3)
    with col1:
        csv = df_display.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Unduh CSV", csv, file_name="tender_lpse.csv", mime="text/csv")
    with col2:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_display.to_excel(writer, index=False, sheet_name='Tender')
        st.download_button("📥 Unduh Excel", output.getvalue(), file_name="tender_lpse.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    with col3:
        pdf = generate_pdf_from_html(df_display, tahun)
        st.download_button("📥 Unduh PDF", pdf, file_name="tender_lpse.pdf", mime="application/pdf")
