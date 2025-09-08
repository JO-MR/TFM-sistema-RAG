import os
import json
import pandas as pd
import gradio as gr
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI

# =========================
# Configuración
# =========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
if not OPENAI_API_KEY:
    print(" Falta OPENAI_API_KEY en los Secrets del Space.")

client = OpenAI(api_key=OPENAI_API_KEY)

COLLECTION_NAME = "contratos_rag"
EMBEDDING_MODEL = "text-embedding-3-small"
JSON_CARGA = "datos_para_cargar.json"   # debe existir en el repo

# =========================
# Inicialización del índice (solo logs, no UI)
# =========================
def init_index():
    chroma_client = chromadb.PersistentClient(path="chroma_db")

    embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name=EMBEDDING_MODEL
    )

    existing = {c.name for c in chroma_client.list_collections()}
    if COLLECTION_NAME in existing:
        collection = chroma_client.get_collection(COLLECTION_NAME, embedding_function=embedding_fn)
    else:
        collection = chroma_client.create_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_fn
        )

    try:
        count = collection.count()
        if count == 0 and os.path.exists(JSON_CARGA):
            with open(JSON_CARGA, "r", encoding="utf-8") as f:
                datos = json.load(f)

            collection.add(
                documents=datos["documents"],
                metadatas=datos.get("metadatas") or None,
                ids=datos["ids"]
            )
            count = collection.count()

        print("Embeddings OpenAI listos.")
        print(f"Cargados {count} documentos desde {JSON_CARGA}.")
        print(f"Documentos en índice: {count}")

    except Exception as e:
        print(f"Error cargando la colección: {e}")

    return collection

collection = init_index()

# =========================
# Consulta
# =========================
def consultar(query: str, fuente: str):
    query = (query or "").strip()
    if not query:
        return "Escribe una pregunta.", "", None, "", ""

    where = None
    if fuente and fuente != "Todos":
        where = {"fuente": fuente}

    try:
        result = collection.query(
            query_texts=[query],
            n_results=5,
            where=where,
            include=["documents", "metadatas"]   # ¡no 'ids'!
        )
    except Exception as e:
        return f"Error al consultar el índice: {e}", "", None, "", ""

    if not result or not result.get("documents") or not result["documents"][0]:
        return "No encontré información relevante en los documentos.", "", None, "", ""

    docs = result["documents"][0]
    metas = result.get("metadatas", [[]])[0] or [{} for _ in docs]

    # Contexto para el modelo
    contexto = "\n\n".join(docs)
    prompt = f"""
Eres un especialista en contratación pública (AENA/ADIF).
Responde de forma clara y profesional únicamente con la información del contexto.
Si falta información, dilo explícitamente.

Contexto:
{contexto}

Pregunta: {query}
Respuesta:
"""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un experto legal en contratos públicos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        respuesta = completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generando respuesta: {e}", "", None, "", ""

    # Fragmentos formateados
    frag_txt = []
    for i, (doc, m) in enumerate(zip(docs, metas), start=1):
        etiqueta = f"{m.get('fuente','?')} · {m.get('expediente','?')}"
        frag_txt.append(f"--- Documento {i} ({etiqueta}) ---\n{doc[:800]}...")
    docs_soporte = "\n\n".join(frag_txt)

    # DataFrame para exportación
    filas = []
    for i, (doc, m) in enumerate(zip(docs, metas), start=1):
        filas.append({
            "rank": i,
            "fuente": m.get("fuente", ""),
            "expediente": m.get("expediente", ""),
            "adjudicatario": m.get("adjudicatario", ""),
            "lugar": m.get("lugar", ""),
            "fecha_acuerdo": m.get("fecha_acuerdo", ""),
            "importe_con_iva": m.get("importe_con_iva", ""),
            "texto": doc
        })
    df_res = pd.DataFrame(filas)

    return respuesta, docs_soporte, df_res, respuesta, docs_soporte

# =========================
# Exportaciones (devuelven la ruta del archivo)
# =========================
def export_csv(df: pd.DataFrame):
    if df is None or df.empty:
        raise gr.Error("No hay resultados para exportar.")
    path = "/tmp/resultados_rag.csv"
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path  # Gradio usará este path como valor del botón

def export_txt(respuesta: str, fragmentos: str):
    if not (respuesta or fragmentos):
        raise gr.Error("No hay contenido para exportar.")
    path = "/tmp/resultados_rag.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write("### Respuesta\n")
        f.write(respuesta or "")
        f.write("\n\n### Fragmentos\n")
        f.write(fragmentos or "")
    return path  # Gradio usará este path como valor del botón

# =========================
# Interfaz Gradio
# =========================
with gr.Blocks(title="Asistente de Contratación Pública (RAG)") as demo:
    gr.Markdown("## Asistente de Contratación Pública (RAG)")
    gr.Markdown("Consulta contratos de AENA y ADIF usando un sistema RAG.")

    with gr.Row():
        fuente_radio = gr.Radio(
            choices=["Todos", "AENA", "ADIF"],
            value="Todos",
            label="Fuente"
        )

    pregunta = gr.Textbox(
        label="Tu pregunta",
        placeholder="Ej.: ¿Cuál es el NIF de la empresa ELKOR ELECTRICIDAD SA?"
    )
    btn_buscar = gr.Button("Buscar", variant="primary")

    respuesta_box = gr.Textbox(label="Respuesta", lines=6)
    fragmentos_box = gr.Textbox(label="Fragmentos utilizados (contexto)", lines=14)

    # Estados ocultos para exportación
    st_df = gr.State(None)
    st_resp = gr.State("")
    st_frags = gr.State("")

    with gr.Row():
        # En Gradio 5 no se usa 'file_name' en DownloadButton
        btn_csv = gr.DownloadButton(label="Descargar CSV")
        btn_txt = gr.DownloadButton(label="Descargar TXT")

    # Acciones
    btn_buscar.click(
        consultar,
        inputs=[pregunta, fuente_radio],
        outputs=[respuesta_box, fragmentos_box, st_df, st_resp, st_frags]
    )

    # Los callbacks devuelven la ruta; Gradio la pone como valor del botón
    btn_csv.click(export_csv, inputs=st_df, outputs=btn_csv)
    btn_txt.click(export_txt, inputs=[st_resp, st_frags], outputs=btn_txt)

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", "7860")))