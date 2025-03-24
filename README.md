# Introduction
This is a project for a course it's aim is creating a mini jenkins-shop with CI/CD flow of a simple messaging queue application

# Prerequisite
1. A k3s installation with
  1. Ingress as kong
  1. Builtin monitoring stack enabled

# Architecture

```mermaid
graph
  direction BT
  Jenk --> JenkCI
  Jenk --> JenkCD
  consume <--> rabbit
  producer  <--> rabbit
  Prometheus --> consume
  World --> kongdep

  kongdep --> Grafana
  kongdep --> Jenk 
  kongdep --> rancherDep 
  Grafana --> Prometheus
  AlertManager --> Prometheus 

  

  subgraph git[git Repository]
    JenkCI[Jenkinsfile CI]
    JenkCD[Jenkinsfile CD]
  end

  subgraph Kubernetes
  
  subgraph kong
  kongdep["Kong(Ingress)"]
  end
  
  
  
  subgraph Ranchercont[Rancher]
  direction BT

  subgraph rancher
    rancherDep[Rancher]
  end
 
  subgraph rancher-monitoring
    direction LR
    Prometheus
    Grafana
    AlertManager

  end

  
  end

  subgraph Infrastructure
  Jenk[Jenkins]
  rabbit[Rabbitmq]
  end

  subgraph Application
  subgraph project-cloud
    consume[Consumer]
    producer[Producer]
  end
  end
  end
```
