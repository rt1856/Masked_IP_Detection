🛡️ Masked IP Detection Microservice
🎯 Overview

A real-time Machine Learning–powered microservice for detecting masked, anonymous, and suspicious IP addresses.
The system helps strengthen Web Application Firewall (WAF) security by identifying potentially malicious IP behavior such as VPNs, proxies, Tor exits, and datacenter-origin traffic.

This project is designed as a scalable, extensible backend service, suitable for academic projects, hackathons (SIH/MSME), and production-ready security systems.

🌟 Key Features

🚀 Real-time IP Analysis (<50ms per request)
🧠 ML Ensemble Model (Random Forest + XGBoost)
🔍 Masked IP Classification (ML-based detection)
⚡ FastAPI REST Microservice
🧰 Extensible Feature Engineering Pipeline
🧠 Behavior-aware Inputs (request count, user agents)
🗃️ Optional Redis Caching (auto-fallback to memory)
🖥️ Web UI Dashboard for live testing
📦 Clean, Modular Architecture
🏗️ System Architecture

Client / Web App / WAF
        │
        ▼
┌────────────────────────────┐
│ Masked IP Detection API    │
│ ─────────────────────────  │
│ FastAPI Service            │
│  ├─ IP Validation          │
│  ├─ Feature Extraction     │
│  ├─ ML Ensemble Prediction │
│  ├─ Risk Scoring           │
│  └─ Response Generation    │
│                            │
│ Cache Layer                │
│  ├─ Redis (optional)       │
│  └─ In-memory fallback     │
└────────────────────────────┘

🔍 Detection Scope
✅ Currently Implemented

IP structural feature extraction (IPv4/IPv6)
ML-based masked vs unmasked classification
Ensemble probability scoring
Risk level categorization (LOW → CRITICAL)
REST API endpoints
Web-based UI for testing IPs
Optional Redis caching

🚀 Planned Enhancements

Tor exit node live feed integration
ASN-based VPN & datacenter detection
MaxMind GeoIP & ASN enrichment
AbuseIPDB & IPQualityScore integration
Incremental / online retraining
Advanced behavioral anomaly detection

📊 Dataset Sources (For Training & Extension)

⚠️ These sources are used during model training or planned integration, not all are active in runtime yet.

Tor Exit Nodes

https://check.torproject.org/exit-addresses
https://www.dan.me.uk/torlist/

Public Proxy Lists

https://github.com/TheSpeedX/PROXY-List
https://github.com/clarketm/proxy-list
https://github.com/ShiftyTR/Proxy-List

ASN & Datacenter Mapping

RIPE, ARIN, APNIC
AWS, GCP, Azure, DigitalOcean, OVH, Vultr

Threat Intelligence (Optional)

AbuseIPDB
IPQualityScore
MaxMind GeoLite2 (City + ASN)

🚀 Getting Started

Prerequisites

Python 3.8+
Git
Redis (optional)

1️⃣ Clone Repository
git clone https://github.com/yourusername/masked-ip-detection.git
cd masked-ip-detection

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Linux/Mac

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Model Files (Required)

Model files are not included in the repository.

Place trained models here:

models/
├── random_forest_model.pkl
├── xgboost_model.pkl
└── feature_names.pkl

5️⃣ Run the Service
uvicorn src.api.main:app --reload

🌐 Access Points
Service	URL
Web UI Dashboard	http://localhost:8000/

API Docs (Swagger)	http://localhost:8000/docs

Health Check	http://localhost:8000/health

API Metadata	http://localhost:8000/api
📡 API Usage
🔹 Check Single IP
curl -X POST http://localhost:8000/api/v1/check \
-H "Content-Type: application/json" \
-d '{
  "ip_address": "8.8.8.8",
  "include_details": true
}'

🔹 Batch IP Check
curl -X POST http://localhost:8000/api/v1/batch \
-H "Content-Type: application/json" \
-d '{
  "ip_addresses": ["8.8.8.8", "1.1.1.1", "185.220.101.1"],
  "include_details": false
}'

🔹 Python Client Example
import requests

res = requests.post(
    "http://localhost:8000/api/v1/check",
    json={"ip_address": "8.8.8.8"}
)

print(res.json())

🎥 Demo Video

▶️ Masked IP Detection – Live Demo

This demo shows:

Web UI interaction

Masked vs unmasked IP testing

Risk level & confidence output

API usage via Swagger

📺 Watch Demo Video:
https://drive.google.com/file/d/1jt4LbHBgiFcyORbWaBX5pYnxlv_oeNiE/view?usp=sharing

📈 Model Performance (Offline Evaluation)
Model	        Accuracy	Precision  Recall	   F1	   ROC-AUC
Random Forest	94.2%	93.8%	  94.5%	  94.1%	    0.97
XGBoost	         95.1%	94.9%	  95.3%	  95.1%	    0.98
Ensemble	         96.3%	96.1%	  96.5%	  96.3%	    0.99

Note: Metrics are based on offline datasets and may vary in real-world traffic.

🧪 Testing
pytest tests/

🐳 Docker (Optional)
docker-compose build
docker-compose up -d

🔒 Security Considerations

Rate limiting recommended in production
API key authentication suggested
HTTPS required for deployment
Redis recommended for scale

📁 Repository Notes

models/, venv/, and .env are intentionally ignored
Add models manually before running
.gitignore is preconfigured

📝 License

MIT License

🤝 Contributing

Pull requests are welcome.
For major changes, please open an issue first.

📧 Support

GitHub Issues: https://github.com/rt1856/masked-ip-detection/issues

🙏 Acknowledgments

Tor Project
Open-source proxy list maintainers
MaxMind GeoLite2
Open-source ML ecosystem
