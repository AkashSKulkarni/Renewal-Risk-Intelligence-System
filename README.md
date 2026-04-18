# 📊 Renewal Risk Intelligence System (LLM + Rule-Based Hybrid)

## 📌 Overview

This project is a **Renewal Risk Intelligence System** that identifies enterprise accounts at risk of churn or non-renewal.

It combines:
- 📊 Structured customer data (usage, tickets, NPS)
- 🤖 LLM-based insights (CSM notes + product changelog)
- 📉 Rule-based risk scoring engine
- 🌐 Flask REST API for serving predictions

The system outputs:
- Risk Score (0 to 1)
- Risk Tier (LOW / MEDIUM / HIGH)
- Key contributing factors
- Human-readable LLM explanation

---

# 🧠 Problem Statement

Enterprise SaaS companies often struggle to identify customers who are likely to churn before renewal.

This system solves that by combining:
- Behavioral signals (usage, support tickets)
- Customer sentiment (NPS)
- AI-generated insights (CSM notes, changelog)

to proactively predict renewal risk.

---

# ⚙️ Tech Stack

- Python 🐍
- Flask 🌐
- Pandas 📊
- PyTorch 🔥
- HuggingFace Transformers 🤖
- Qwen2.5-3B Instruct LLM 🧠

---

# 🏗️ System Architecture

```text
Data Sources
   ↓
Ingestion Layer (CSV + Text Files)
   ↓
Feature Engineering Layer
   ↓
LLM Signal Extraction Layer
   ↓
Risk Scoring Engine
   ↓
Flask API Layer
   ↓
JSON Response
