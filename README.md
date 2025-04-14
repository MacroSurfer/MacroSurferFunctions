# 🌊 MacroSurfer Scout

***Built for traders, quants, and macro thinkers. Surf the data tide.*** 🌊

## What is MacroSurfer Scout?

**MacroSurfer Scout** is an open-source intelligence layer designed for quantitative developers, financial engineers, and traders who want to build powerful data pipelines and leverage LLMs for fast insights into financial and economic data.

Scout makes it easy to:
- 🏗️ Build your own **big data curation pipeline** to store economic, fundamental, and news data into an SQL database.
- 🤖 Query complex datasets using a **LLM-powered natural language agent**, skipping manual SQL writing.
- 🚀 Deploy a **cloud-native API** to Google Cloud in just a few clicks — ready to be connected to any UI, terminal, or automated workflow.

---

## 🧠 Why MacroSurfer Scout?

Modern quantitative investing requires a seamless flow from raw data to actionable insights. Scout is built to help you:

- **Ingest and manage** vast financial data sources at scale.
- **Ask questions like a human**, and get structured answers with SQL-driven accuracy.
- **Deploy in the cloud**, and integrate with dashboards, bots, notebooks, or mobile apps.

Whether you're building a systematic macro model, a real-time alert system, or your own Bloomberg Terminal — Scout gives you the foundation.

---

## 🚀 Features

### 📊 1. Scalable Data Curation Engine
- Ingest data from APIs (e.g., FRED, EDGAR, News APIs, Alpha Vantage, etc.).
- Normalize and store in **PostgreSQL** or any compatible SQL database.
- Modular connectors for custom data sources.
- Timestamped and structured for **quantitative analytics**.

### 🤖 2. LLM-Powered Agent
- Chat-style interface or API call to **query data in natural language**.
- Powered by OpenAI / local models (configurable).
- Handles multi-table joins, summaries, trend spotting, and anomaly detection.
- Designed for **research acceleration** and exploration.

### ☁️ 3. Cloud-Native Deployment (GCP)
- One-command deployment to **Google Cloud Run / App Engine**.
- Auto-scales and integrates with **GCP SQL**, **IAM**, and **logging**.
- Exposes REST API endpoints to hook into **Streamlit**, **React**, **CLI tools**, or **trading bots**.

---

## 📦 Getting Started

### 🔧 Prerequisites

- Python 3.13+
- PostgreSQL instance (local or cloud) we recommend Supabase to get you started free
- GCP account & project (for deployment)
- [OpenAI API key](https://platform.openai.com/) (or custom LLM)

### 🐍 Install Locally

```bash
git clone git@github.com:MacroSurfer/MacroSurferFunctions.git
cd MacroSurferFunctions
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### ⚙️ Setup Config
Create a .env file in the /functions (example in functions/env-example):
```bash
DB_USERNAME=""
DB_PASSWORD=""
DB_HOST_NAME=""
DB_PORT=""
DB_NAME=""
FINANCIAL_MODELINGPREP_API_KEY=""
OPENAI_API_KEY=""
```

### 🧪 Run the Agent Locally
```bash
python functions/test_agent.py
```

Ask questions like:
```vbnet
> What is the GDP growth trend for the past 5 years?
> Show me all companies with increasing ROE in the last 3 quarters.
> What's the inflation rate spike during oil shocks since 2000?
```

## ☁️ Deploy to Google Cloud
---
```bash
gcloud auth login
gcloud config set project your-gcp-project
gcloud builds submit --tag gcr.io/your-gcp-project/macrosurfer-scout
gcloud run deploy scout-api --image gcr.io/your-gcp-project/macrosurfer-scout --platform managed
```
Now your API endpoint is live and scalable. 🎉

## 🧩 Integrations
* 🖥️ Connect to dashboards (Streamlit, React, Grafana).

* 🔗 Use in Jupyter Notebooks or trading pipelines.

* ⚡ Webhooks or Slack bot integration ready.

## 🤝 Contributing
We welcome contributors of all experience levels! Here's how to get involved:

1. Fork the repo and clone it locally.

2. Create a new branch: git checkout -b feature-your-feature-name

3. Make your changes and commit: git commit -m "Add feature"

4. Push and submit a PR: git push origin feature-your-feature-name

Please follow the [Conventional Commits](https://www.conventionalcommits.org/) format and include test coverage where possible.

## 📄 License
```
MIT License

Copyright (c) 2025 MacroSurfer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...

```