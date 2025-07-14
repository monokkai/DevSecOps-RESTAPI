terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0.2"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.1.0"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}


resource "helm_release" "devsecops_api" {
  name      = "devsecops-api"
  chart     = "${path.module}/../helm/devsecops"
  namespace = "default"
  values = [
    file("${path.module}/values.yaml")
  ]
}