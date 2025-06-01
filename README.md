# Cheese Agent: RAG-Based LLM on a Cheese Dataset

> **Data Source:**  
> TidyTuesday Cheese (June 4 2024)  
> https://github.com/rfordatascience/tidytuesday/tree/main/data/2024/2024-06-04

---

## Overview

**Cheese Agent** is a Retrieval-Augmented Generation (RAG) app that:

1. Splits cheese records (flavor, origin, aging) into chunks and embeds them.
2. Stores embeddings in Astra DB.
3. At query time, embeds the user’s question, retrieves top-k cheese chunks, and sends them plus the question to GPT-4o-Mini.
4. Returns a factual, grounded answer.

---

## How It Works


1. User opens `https://cheese-agent.onrender.com`.
2. Express (on Render) serves `index.html`, CSS, and JS.
3. `<langflow-chat>` sends `POST /api/v1/run/<flow_id>` back to Express.
4. Express proxies to Langflow, which retrieves cheese data and calls GPT-4o-Mini.
5. The generated answer returns through Express to `<langflow-chat>` and displays in the chat.

## Deployment

- **Frontend (GitHub Pages)**
    - Hosts `docs/index.html`, `docs/css/`, `docs/js/`.
    - `<langflow-chat host_url>` points to the Render URL (e.g., `https://cheese-agent.onrender.com`).

- **Combined Proxy + Langflow (Render.com)**
    - **Root Directory:** `docs/`
    - **Build Command:** `npm install`
    - **Start Command:** `npm start`
        - Installs dependencies.
        - `npm start` launches both Langflow and Express in one container.

---

## Future Ideas

- Periodically ping Langflow to avoid cold-start delays.
- Expand the cheese dataset (nutritional info, images).
- Add UI polish: “typing…” indicators, show source passages.
- Enable user accounts to save favorite cheese queries.
- Collect analytics: most-asked cheeses, response times.

---

**Cheese Agent** is a concise end-to-end RAG demo: from a small cheese dataset, through vector retrieval, to GPT-4o-Mini–powered chat. Enjoy exploring cheese knowledge!  


