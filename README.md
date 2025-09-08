# TFM – Sistema RAG de consulta de contratos públicos (AENA/ADIF)

Repositorio con el código y el notebook del TFM.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JO-MR/TFM-sistema-RAG/blob/main/notebooks/TFM_RAG.ipynb)
[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Space-Demo-blue)](https://huggingface.co/spaces/JonasDMR/tfm-consultor-contratos-publicos)

---

## Descargar el código
- **ZIP directo:** https://github.com/JO-MR/TFM-sistema-RAG/archive/refs/heads/main.zip  
- **Clonar:** `git clone https://github.com/JO-MR/TFM-sistema-RAG.git`

## Requisitos
- Python 3.9+
- `requirements.txt`

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
# .venv\Scripts\activate
pip install -r requirements.txt

## **Variables de entorno (no subir claves)**

Este proyecto usa OpenAI. Crea un archivo `.env` en la raíz con:
```env
OPENAI_API_KEY=tu_clave_aqui
