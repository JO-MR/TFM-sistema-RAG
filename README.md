# TFM – Sistema RAG de consulta de contratos públicos (AENA/ADIF)

Repositorio con el código y el notebook del TFM.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JO-MR/TFM-sistema-RAG/blob/main/notebooks/TFM_RAG.ipynb)
[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Space-Demo-blue)](https://huggingface.co/spaces/JonasDMR/tfm-consultor-contratos-publicos)

---

## **Descargar el código**
- **ZIP directo:** https://github.com/JO-MR/TFM-sistema-RAG/archive/refs/heads/main.zip  
- **Clonar:** `git clone https://github.com/JO-MR/TFM-sistema-RAG.git`

## **Requisitos**
- Python 3.9+
- `requirements.txt`

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
# .venv\Scripts\activate
pip install -r requirements.txt
```

## **Variables de entorno (no subir claves)**
Este proyecto usa OpenAI. Crea un archivo `.env` en la raíz con:

```env
OPENAI_API_KEY=tu_clave_aqui
```

Incluimos `.env.example` como plantilla y `.gitignore` con `.env`.

**Colab (solo en la sesión actual):**
```python
import os, getpass
os.environ["OPENAI_API_KEY"] = getpass.getpass("Pega tu OpenAI API key: ")
```

**Hugging Face Space:** en *Settings → Variables and secrets* añade `OPENAI_API_KEY`.

---

## **Cómo ejecutar**
**A) Notebook (recomendado para revisión)**
```bash
jupyter notebook notebooks/TFM_RAG.ipynb
```

**B) App (Gradio)**
```bash
python app.py
```
Abre la URL que muestre Gradio en la consola.

---

## **Estructura**
```
.
├── notebooks/
│   └── TFM_RAG.ipynb
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## **Notas**
- No subas datos/datasets pesados al repo; usa enlaces externos si hace falta.
- Antes de commitear el notebook, puedes **limpiar salidas** para reducir tamaño.
- Las claves/API **nunca** deben aparecer en el código ni en el historial de git.

---

## **Licencia**
MIT

