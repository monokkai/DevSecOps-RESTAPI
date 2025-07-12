# 🔐 Junior DevSecOps Demo Project

## 📦 Description

This is a demo project to practice core DevSecOps skills.  
It includes:
- REST API (written in Go or Python FastAPI)
- Docker containerization
- CI/CD pipeline with GitHub Actions
- Vulnerability scanning with Trivy
- Helm chart for Kubernetes deployment (Minikube)

---

## 📁 Project Structure

```
├── api/ 
├── Dockerfile 
├── .github/workflows/ 
├── helm/ 
└── README.md 
```

```
docker exec -it restapi-python-usersdb-1 mysql -u root -proot
```

---

## ⚙️ Features

| Component         | Description                                           |
|-------------------|-------------------------------------------------------|
| REST API          | Simple endpoints: `/health`, `/status`, `/echo`      |
| Docker            | Image built from Dockerfile                          |
| GitHub Actions    | Runs tests, linter, Trivy scan, and pushes image     |
| Trivy             | Scans Docker image for known vulnerabilities (CVEs)  |
| Helm              | Deploys API to local Kubernetes cluster (Minikube)   |

---

## 🚀 Getting Started

1. **Run manually (Docker):**

```bash
docker build -t devsecops-demo .
docker run -p 8080:8080 devsecops-demo

    Deploy with Helm (Minikube):

minikube start
helm install demo-api ./helm

    CI/CD:

    Pushing to GitHub triggers:

        ✅ Unit tests

        🧼 Linting

        🔍 Trivy image scan

        🐳 Docker build + push

        (optional: auto-deploy)

🛡️ Skills Practiced

    🐧 Linux & Docker basics

    ⚙️ CI/CD automation

    🧪 Testing & linting

    🔍 Security scanning

    🚀 Kubernetes + Helm deployment

✅ Next Steps

After completing this project, you can:

    Add authentication (e.g., JWT)

    Integrate logging/monitoring (Prometheus + Grafana)

    Connect to a real DB (PostgreSQL, MongoDB)

    Deploy to cloud (e.g., Fly.io, GCP, or Render)