import pandas as pd
import pdfkit

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
    html = dataframe.to_html(index=False, border=0)
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                font-size: 12px;
            }}
            h2 {{
                text-align: center;
                margin-bottom: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
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
