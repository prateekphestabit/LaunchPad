"""
Multi-RAG System — Streamlit Interface
Integrates Day2 (Text RAG), Day3 (Image RAG), Day4 (SQL RAG)

Flow
────
  /ask       → Day2  hybrid_retriever (via rag_api)   → LLM answer   → UI
  /askImage  → Day3  text_to_image   (via image_api)  → images       → UI
  /askSql    → Day4  main.py         (via sql_api)    → LLM answer   → UI
"""

import streamlit as st
import sys
import os
import traceback
from pathlib import Path
from PIL import Image

# ──────────────────────────────────────────────────────────────────────────
# 1.  RESOLVE PROJECT PATHS
# ──────────────────────────────────────────────────────────────────────────
CURR_FILE = Path(__file__).resolve()        # .../week7/Day5/deployment/app.py
WEEK7_DIR = CURR_FILE.parents[2]            # .../week7
DAY2_DIR  = WEEK7_DIR / "Day2"
DAY3_DIR  = WEEK7_DIR / "Day3"
DAY4_DIR  = WEEK7_DIR / "Day4"

# ──────────────────────────────────────────────────────────────────────────
# 2.  LOAD .env FILES *BEFORE* ANY PROJECT IMPORTS
#     Day2/.env  →  GROQ_API_KEY, GROQ_MODEL
#     Day4/.env  →  PG_DATABASE, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT
# ──────────────────────────────────────────────────────────────────────────
from dotenv import load_dotenv

load_dotenv(DAY2_DIR / ".env")                  # GROQ creds
load_dotenv(DAY4_DIR / ".env", override=False)  # PG + GROQ (won't overwrite)

# ──────────────────────────────────────────────────────────────────────────
# 3.  IMPORT EACH BACKEND WITH ISOLATED sys.path
#
#     Day2 and Day4 both have a top-level `generator/` package.
#     If both directories sit on sys.path at the same time, Day4's
#     generator/ (which has __init__.py) shadows Day2's, breaking
#     `from generator.generator import generate_answer`.
#
#     Strategy: import Day2 first, then flush the cached `generator`
#     module, then import Day4.
# ──────────────────────────────────────────────────────────────────────────
_ask_rag   = None
_ask_image = None
_ask_sql   = None
_import_errors: dict = {}

# ── Day2  (Text RAG) — import BEFORE Day4 touches sys.path ──────────────
for _p in [str(DAY2_DIR), str(DAY2_DIR / "retriever")]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from rag_api import ask_rag
    _ask_rag = ask_rag
except Exception:
    _import_errors["ask"] = traceback.format_exc()

# ── Day3  (Image RAG) — no namespace conflicts ─────────────────────────
for _p in [str(DAY3_DIR / "retriever")]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from image_api import ask_image
    _ask_image = ask_image
except Exception:
    _import_errors["askImage"] = traceback.format_exc()

# ── Flush Day2's `generator` so Day4 can load its own ──────────────────
for _mod in [k for k in sys.modules if k == "generator" or k.startswith("generator.")]:
    del sys.modules[_mod]

# ── Day4  (SQL RAG) — now safe to add its path ─────────────────────────
for _p in [str(DAY4_DIR)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from sql_api import ask_sql
    _ask_sql = ask_sql
except Exception:
    _import_errors["askSql"] = traceback.format_exc()


# ══════════════════════════════════════════════════════════════════════════
#  STREAMLIT  UI
# ══════════════════════════════════════════════════════════════════════════

st.set_page_config(page_title="Multi-RAG System", page_icon="🧠", layout="wide")

st.title("🧠 Multi-RAG System")
st.caption("Unified interface — Text RAG · Image Search · SQL Q&A")

# ── Sidebar ──────────────────────────────────────────────────────────────
mode = st.sidebar.radio(
    "Choose mode",
    ["📄 Ask", "🖼️ Ask Image", "🗄️ Ask SQL"],
    captions=[
        "Hybrid retrieval + LLM  (Day 2)",
        "CLIP text → image search  (Day 3)",
        "Natural-language → SQL  (Day 4)",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Services required**\n\n"
    "- Qdrant  (`:6333`) — Ask & Ask Image\n"
    "- PostgreSQL (`:5432`) — Ask SQL\n"
)


# ── /ask  ────────────────────────────────────────────────────────────────
if mode == "📄 Ask":
    st.header("📄 Ask — Text Document RAG")
    st.markdown(
        "Hybrid retrieval (**dense + BM25 → RRF fusion**) over your "
        "ingested documents, answered by **Groq LLM**."
    )

    if "ask" in _import_errors:
        st.error("⚠️  Text RAG backend failed to load.")
        with st.expander("Show traceback"):
            st.code(_import_errors["ask"])
        st.stop()

    question = st.text_input(
        "Your question",
        placeholder="e.g. What is machine learning?",
        key="ask_q",
    )

    if st.button("Get Answer", type="primary", key="ask_btn"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Retrieving documents & generating answer …"):
                try:
                    answer = _ask_rag(question)
                    st.markdown("### 💬 Answer")
                    st.markdown(answer)
                except Exception as exc:
                    st.error(f"Error: {exc}")
                    with st.expander("Traceback"):
                        st.code(traceback.format_exc())


# ── /askImage  ───────────────────────────────────────────────────────────
elif mode == "🖼️ Ask Image":
    st.header("🖼️ Ask Image — Text-to-Image Search")
    st.markdown(
        "Uses **CLIP** embeddings to find the most relevant images "
        "extracted from your ingested PDFs."
    )

    if "askImage" in _import_errors:
        st.error("⚠️  Image RAG backend failed to load.")
        with st.expander("Show traceback"):
            st.code(_import_errors["askImage"])
        st.stop()

    question = st.text_input(
        "Describe the image you're looking for",
        placeholder="e.g. bispecific mutated",
        key="img_q",
    )
    top_k = st.slider("Results to return", 1, 10, 5, key="img_k")

    if st.button("Search Images", type="primary", key="img_btn"):
        if not question.strip():
            st.warning("Please enter a search query.")
        else:
            with st.spinner("Searching images …"):
                try:
                    results = _ask_image(question, top_k)

                    if not results:
                        st.info("No images matched your query.")
                    else:
                        st.success(f"Found **{len(results)}** image(s)")

                        for idx, r in enumerate(results, 1):
                            with st.container():
                                st.markdown(
                                    f"#### Result {idx}  —  score `{r['score']:.4f}`"
                                )
                                col_img, col_meta = st.columns([1, 1])

                                img_path = r["image_path"]
                                # resolve relative paths against Day3
                                if not os.path.isabs(img_path):
                                    img_path = str(DAY3_DIR / img_path)

                                with col_img:
                                    if os.path.isfile(img_path):
                                        st.image(
                                            Image.open(img_path),
                                            use_container_width=True,
                                        )
                                    else:
                                        st.warning(f"File not found:\n`{img_path}`")

                                with col_meta:
                                    st.markdown(f"**Source PDF:** `{r['source_pdf']}`")
                                    st.markdown(f"**Page:** {r['page_number']}")
                                    st.markdown(f"**Type:** {r['content_type']}")
                                    st.markdown(f"**Path:** `{img_path}`")

                            st.divider()

                except Exception as exc:
                    st.error(f"Error: {exc}")
                    with st.expander("Traceback"):
                        st.code(traceback.format_exc())


# ── /askSql  ─────────────────────────────────────────────────────────────
elif mode == "🗄️ Ask SQL":
    st.header("🗄️ Ask SQL — Natural-Language Database Q&A")
    st.markdown(
        "Translates your question into **SQL**, validates & executes it "
        "against PostgreSQL, then summarises the results with an LLM."
    )

    if "askSql" in _import_errors:
        st.error("⚠️  SQL RAG backend failed to load.")
        with st.expander("Show traceback"):
            st.code(_import_errors["askSql"])
        st.stop()

    question = st.text_input(
        "Your question",
        placeholder="e.g. Show all customers from New York",
        key="sql_q",
    )

    if st.button("Run Query", type="primary", key="sql_btn"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Generating SQL & executing …"):
                try:
                    result = _ask_sql(question)

                    st.markdown(f"**Question:** {result['question']}")

                    # ── Generated SQL ──
                    st.markdown("### 🛠️ Generated SQL")
                    st.code(result.get("sql", "—"), language="sql")

                    if result.get("error"):
                        st.error(f"❌ {result['error']}")
                    else:
                        st.success("✅ Query executed successfully")

                        # ── Results table ──
                        if result.get("result_table"):
                            st.markdown("### 📊 Query Results")
                            st.code(result["result_table"], language="text")

                            if result.get("result"):
                                rows  = result["result"].get("row_count", 0)
                                trunc = result["result"].get("truncated", False)
                                badge = " *(truncated)*" if trunc else ""
                                st.caption(f"{rows} row(s) returned{badge}")

                        # ── LLM Summary ──
                        if result.get("summary"):
                            st.markdown("### 💬 AI Summary")
                            st.markdown(result["summary"])

                except Exception as exc:
                    st.error(f"Error: {exc}")
                    with st.expander("Traceback"):
                        st.code(traceback.format_exc())


# ── Footer ───────────────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.caption("Week 7 · Multi-RAG System")
