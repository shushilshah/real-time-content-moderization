# 🛡️ Real-Time Content Moderation System (AI + Async Architecture)

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Redis](https://img.shields.io/badge/Redis-Queue-red)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-orange)
![ML](https://img.shields.io/badge/ML-Toxicity%20Detection-purple)
![Status](https://img.shields.io/badge/status-active-success)

A **production-style real-time content moderation system** built using **FastAPI, Redis, Streamlit, and Machine Learning inference**.

It demonstrates a full **async distributed architecture** with queue-based processing, caching, logging, metrics tracking, and live monitoring.

---

# 🚀 Features

## ⚙️ Backend (FastAPI)
- Async moderation API
- Request ID generation
- Redis queue integration (job system)
- Rate limiting per user
- Response caching

## 🤖 ML System
- Toxicity prediction model
- Hybrid rule-based + ML scoring
- Decision engine:
  - `blocked`
  - `review`
  - `allowed`

## 🧵 Worker System
- Redis queue consumer
- Background ML inference
- Database logging
- Metrics tracking (latency, throughput)

## 🖥️ Frontend (Streamlit)
- Content moderation UI
- Live result polling
- Admin dashboard (logs)
- Metrics dashboard (system monitoring)

---
