# Snitchboard Log Generator
Distributed Logging and Monitoring System - using all Open source tools

This is a simple Python application that generates log messages and writes them to a local file (`snitchboard-app.log`). The app simulates real-world log generation and is used to demonstrate production-grade logging using Kubernetes and Grafana Loki.

---

## 📦 Features

- Continuously writes log entries to `snitchboard-app.log`
- Packaged as a Docker container
- Deployed to a Kubernetes cluster
- Vector sidecar collects logs and ships them to Grafana Loki
- Logs are visualized via Grafana

---

## 🛠️ How It Works

1. The Python app logs simulated messages to `/logs/snitchboard-app.log`
2. A Vector sidecar container in the same pod tails this log file
3. Vector pushes log data to **Grafana Loki**
4. Logs are explored and visualized in **Grafana**

---

## 🚀 Deployment Steps

### 1. Build and Push Docker Image

```bash
docker buildx build --platform linux/amd64 \
  -t us-west1-docker.pkg.dev/robertb724-personal/apps/images/snitchboard:8.0 \
  . \
  --push

Next Run kubectl apply -f deploy/


##Setup
Create a virtual env using command "python -m venv .venv"

