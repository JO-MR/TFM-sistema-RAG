# TFM – Sistema RAG de consulta de contratos públicos (AENA/ADIF)

Repositorio con el código y el notebook del TFM.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JO-MR/TFM-sistema-RAG/blob/main/notebooks/TFM_RAG.ipynb)
[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Space-Demo-blue)](https://huggingface.co/spaces/JonasDMR/tfm-consultor-contratos-publicos)

---

## **Descargar el código**
- **ZIP directo:** https://github.com/JO-MR/TFM-sistema-RAG/archive/refs/heads/main.zip  
- **Clonar:** `git clone https://github.com/JO-MR/TFM-sistema-RAG.git`

---

## **Datos (contratos en PDF) – subida manual**
El notebook **no descarga automáticamente** los PDFs.  
Debes **subir manualmente** el archivo `contratos.zip` (contiene 109 PDFs de AENA y ADIF) cuando el notebook lo solicite.

- **Descarga del ZIP (para subirlo luego en el notebook):**  
  https://github.com/JO-MR/TFM-sistema-RAG/raw/main/data/contratos.zip

**Cómo hacerlo en Colab**
1. Abre el notebook con el botón **Open in Colab**.  
2. Ejecuta la celda **“SUBIR ZIP DE CONTRATOS”**: se abrirá el diálogo de subida.  
3. Selecciona el archivo `contratos.zip` y espera a que termine la carga.  
4. El notebook descomprime el ZIP y continúa con el flujo.

> La celda usa `files.upload()` de Colab. Ejemplo:
> ```python
> from google.colab import files
> print("Sube el archivo contratos.zip con los 109 PDFs (AENA y ADIF)...")
> up = files.upload()             # selecciona 'contratos.zip'
> zip_path = next(iter(up))       # nombre del archivo subido
> # ... (descompresión)
> ```

**Ejecución local (Jupyter)**
- Coloca `contratos.zip` en `data/contratos.zip` y adapta la ruta en la celda de descompresión si fuese necesario.

---

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
├── data/
│   └── contratos.zip            # Se sube manualmente al notebook (no auto-descarga)
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
- Evita subir datos/datasets muy pesados a Git. En este repo se facilita `data/contratos.zip` para ejecutarlo fácilmente.
- Antes de commitear el notebook, puedes **limpiar salidas** para reducir tamaño.
- Las claves/API **nunca** deben aparecer en el código ni en el historial de git.

---

## **Licencia**
MIT
