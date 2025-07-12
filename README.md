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
    or
mysql -u root -proot
```

#1 To start docker and create user:
```
docker ps

docker logs restapi-python-api-1

docker logs restapi-python-usersdb-1

docker compose down
docker compose build
docker compose up -d

curl -X POST -F "username=testuser" -F "password=testpass" http://localhost:8000/register

docker exec -it restapi-python-usersdb-1 mysql -u root -proot

USE users-db;
SELECT * FROM Users;
```
#2 To use Kubernetes(Container is already on DockerHub)
```
kubectl get pods

kubectl get services

kubectl get deployments

kubectl logs devsecops-api-[POD_NAME]

eval $(minikube docker-env)
docker build -t devsecops-api .

kubectl rollout restart deployment devsecops-api

kubectl port-forward service/devsecops-api 8000:8000 &

curl -X POST -F "username=testuser" -F "password=testpass" http://localhost:8000/register

kubectl exec -it mysql-[POD_NAME] -- mysql -u root -proot -e "USE users-db; SELECT * FROM Users;"

pkill -f "kubectl port-forward"
```

#3 Diagnostics and checks
```
docker network inspect restapi-python_default

docker exec restapi-python-api-1 python -c "import socket; print(socket.gethostbyname('usersdb'))"

kubectl exec devsecops-api-[POD_NAME] -- env | grep MYSQL

kubectl describe pod devsecops-api-[POD_NAME]
```

---

## ⚙️ Features

| Component      | Description                                         |
|----------------|-----------------------------------------------------|
| REST API       | Simple endpoints: `/health`, `/status`, `/echo`     |
| Docker         | Image built from Dockerfile                         |
| GitHub Actions | Runs tests, linter, Trivy scan, and pushes image    |
| Trivy          | Scans Docker image for known vulnerabilities (CVEs) |
| Helm           | Deploys API to local Kubernetes cluster (Minikube)  |

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
