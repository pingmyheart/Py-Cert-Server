# PY-CERT-SERVER

*All-in-one SSL Certificate Manager*

![Last Commit](https://img.shields.io/github/last-commit/pingmyheart/Py-Cert-Server)
![Repo Size](https://img.shields.io/github/repo-size/pingmyheart/Py-Cert-Server)
![Issues](https://img.shields.io/github/issues/pingmyheart/Py-Cert-Server)
![Pull Requests](https://img.shields.io/github/issues-pr/pingmyheart/Py-Cert-Server)
![License](https://img.shields.io/github/license/pingmyheart/Py-Cert-Server)
![Top Language](https://img.shields.io/github/languages/top/pingmyheart/Py-Cert-Server)
![Language Count](https://img.shields.io/github/languages/count/pingmyheart/Py-Cert-Server)

## 🚀 Overview

**Py-Cert-Server** is a comprehensive SSL certificate management solution that simplifies the process of obtaining,
renewing, and managing SSL certificates for your domains offering a user-friendly web interface for easy management.

## ✨ Features

- 🔐 **SSL Certificate Management:** Generate the CA and SSL certificates for your domains.
- 🌍 **Web Interface:** User-friendly web UI for managing certificates.
- 🔄 **Automatic Renewal:** Automatically renew certificates before they expire.

## 🛠️ Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

#### Native Installation

1. Clone the repository

```bash
1. git clone https://github.com/pingmyheart/Py-Cert-Server.git```
cd Py-Cert-Server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

2. Set up environment variables

```bash
MONGODB_USERNAME=root
MONGODB_PASSWORD=root
MONGODB_HOST=localhost
MONGODB_DB=py-cert-server
```

#### Docker Installation

1. Pull the docker image

```bash
docker pull ghcr.io/pingmyheart/py-cert-server:${VERSION}
```

2. Run the container

```yaml
services:
  mongodb:
    image: mongo:latest
    environment:
      - MONGO_INITDB_ROOT_USERNAME=root
      - MONGO_INITDB_ROOT_PASSWORD=root
    volumes:
      - mongodb_data:/data/db
  vulvy-ring-bot:
    image: ghcr.io/pingmyheart/py-cert-server:${VERSION}
    environment:
      - MONGODB_USERNAME=root
      - MONGODB_PASSWORD=root
      - MONGODB_HOST=mongodb
      - MONGODB_DB=py-cert-server
```

## 📚 Usage

- Access the web interface at `http://localhost:5000` or the appropriate host and port.(`http://localhost:8080` if using
  Docker)
- Follow the on-screen instructions to manage your SSL certificates.