from pathlib import Path
import streamlit as st
from datetime import datetime

texto = "valor dinamico"
html = f"""
<html>
  <body>
    <p>{texto}</p>
  </body>
</html>
"""

st.download_button("Baixar HTML", html, file_name="relatorio.html", mime="text/html")
