import pandas as pd
from datetime import datetime

def format_tanggal_indonesia(dt):
    bulan_id = [
        "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    if pd.isnull(dt):
        return ""
    dt = pd.to_datetime(dt, errors="coerce")
    if pd.isnull(dt):
        return ""
    return f"{dt.day} {bulan_id[dt.month]} {dt.year}"

def generate_pdf_from_html(dataframe, year):
    import pdfkit

    html = dataframe.to_html(index=False, border=0)
    html_content = f"""
    <html>
    <head>
        <meta charset=\"UTF-8\">
        <style>
            body {{ font-family: Arial; font-size: 12px; margin: 20px; }}
            h2 {{ text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ccc; padding: 6px; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h2>Data Tender LPSE - {year}</h2>
        {html}
    </body>
    </html>
    """

    options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
        'margin-top': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'margin-right': '10mm',
    }
    pdf = pdfkit.from_string(html_content, False, options=options)
    return pdf