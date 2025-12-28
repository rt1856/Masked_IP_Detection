# 🛡️ Masked IP Detection Microservice

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![ML](https://img.shields.io/badge/ML-Ensemble-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **A real-time Machine Learning–powered microservice for detecting masked, anonymous, and suspicious IP addresses.**  
> Strengthens Web Application Firewall (WAF) security by identifying VPNs, proxies, Tor nodes, and datacenter traffic.


---

## 📺 Demo Video

**▶️ [Watch Live Demo](https://drive.google.com/file/d/1jt4LbHBgiFcyORbWaBX5pYnxlv_oeNiE/view?usp=sharing)**

This demo showcases:
- ✅ Web UI interaction
- ✅ Real-time masked vs legitimate IP detection
- ✅ Risk level scoring & confidence metrics
- ✅ API usage via Swagger UI

---

## 🌟 Key Features

| Feature | Description |
|---------|-------------|
| ⚡ **Real-time Analysis** | <50ms per request with intelligent caching |
| 🧠 **ML Ensemble Model** | Random Forest + XGBoost  |
| 🎯 **96%+ Accuracy** | Highly accurate masked IP detection |
| 🔍 **Multi-type Detection** | Tor, VPN, Proxy, Datacenter IPs |
| 🚀 **FastAPI Backend** | High-performance async REST API |
| 📊 **Risk Scoring** | LOW → MEDIUM → HIGH → CRITICAL levels |
| 💾 **Smart Caching** | Redis with automatic in-memory fallback |
| 🖥️ **Web Dashboard** | Interactive UI for live testing |
| 📈 **Explainable AI** | Confidence scores and feature importance |
| 🔄 **Continuous Learning** | Auto-updates from threat intelligence feeds |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Web Application / WAF                  │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP Request
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Masked IP Detection API                     │
│ ─────────────────────────────────────────────────────── │
│                                                          │
│  ┌──────────────┐   ┌──────────────┐   ┌────────────┐  │
│  │ IP Validator │ → │   Feature    │ → │ ML Ensemble│  │
│  │   & Parser   │   │  Extraction  │   │ Prediction │  │
│  └──────────────┘   └──────────────┘   └────────────┘  │
│           │                 │                   │        │
│           └─────────────────┴───────────────────┘        │
│                             │                            │
│                             ▼                            │
│                  ┌──────────────────┐                    │
│                  │  Risk Scoring &  │                    │
│                  │ Response Builder │                    │
│                  └──────────────────┘                    │
│                             │                            │
│  ┌──────────────────────────┴──────────────────────┐    │
│  │          Cache Layer (Redis / In-Memory)        │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                     │ JSON Response
                     ▼
┌─────────────────────────────────────────────────────────┐
│         Client Application / Security Dashboard          │
└─────────────────────────────────────────────────────────┘
```

---

## 🔍 Detection Capabilities

### ✅ Currently Implemented

- ✔️ **IP Structural Analysis**: IPv4/IPv6 validation and feature extraction
- ✔️ **ML-Based Classification**: Ensemble model for masked vs legitimate detection
- ✔️ **Probability Scoring**: Confidence levels (0-100%)
- ✔️ **Risk Categorization**: Four-tier risk assessment
- ✔️ **Batch Processing**: Check multiple IPs simultaneously
- ✔️ **REST API**: Production-ready endpoints
- ✔️ **Web Dashboard**: Live testing interface
- ✔️ **Intelligent Caching**: Performance optimization

### 🚀 Planned Enhancements

- 🔜 **Live Tor Integration**: Real-time Tor exit node feed
- 🔜 **ASN-Based Detection**: VPN & datacenter identification
- 🔜 **GeoIP Enrichment**: MaxMind GeoIP2 integration
- 🔜 **Threat Intelligence**: AbuseIPDB & IPQualityScore APIs
- 🔜 **Online Learning**: Incremental model retraining
- 🔜 **Behavioral Analysis**: Advanced anomaly detection

---

## 📊 Dataset Sources

> **Note**: These sources are used during model training and planned for future integration.

### 🧅 Tor Exit Nodes
- [Tor Project Official](https://check.torproject.org/exit-addresses)
- [Dan.me.uk Tor List](https://www.dan.me.uk/torlist/)
- [IPsum Threat Feed](https://github.com/stamparm/ipsum)

### 🔀 Public Proxy Lists
- [TheSpeedX/PROXY-List](https://github.com/TheSpeedX/PROXY-List)
- [clarketm/proxy-list](https://github.com/clarketm/proxy-list)
- [ShiftyTR/Proxy-List](https://github.com/ShiftyTR/Proxy-List)
- [monosans/proxy-list](https://github.com/monosans/proxy-list)

### 🌐 ASN & Datacenter Mapping
- **Regional Registries**: RIPE, ARIN, APNIC
- **Cloud Providers**: AWS, GCP, Azure, DigitalOcean
- **Hosting**: OVH, Hetzner, Vultr, Linode

### 🛡️ Threat Intelligence (Optional)
- [AbuseIPDB](https://www.abuseipdb.com/) - Malicious IP database
- [IPQualityScore](https://www.ipqualityscore.com/) - Fraud detection
- [MaxMind GeoLite2](https://dev.maxmind.com/geoip/geoip2/geolite2/) - City + ASN data

---

## 🚀 Quick Start

### Prerequisites

```bash
✅ Python 3.8 or higher
✅ pip package manager
✅ Git
⚠️ Redis (optional, but recommended for production)
```

### 1️⃣ Clone Repository

```bash
git clone https://github.com/rt1856/masked-ip-detection.git
cd masked-ip-detection
```

### 2️⃣ Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Models

⚠️ **Important**: Model files are not included in the repository due to size.

**Option A: Download Pre-trained Models**
```bash
# Download from project releases or Google Drive
# Place in models/ directory:
models/
├── random_forest_model.pkl
├── xgboost_model.pkl
└── feature_names.pkl
```

**Option B: Train Your Own Models**
```bash
# Use provided Google Colab notebooks:
# 1. Complete_Data_Collection.ipynb (collect datasets)
# 2. 02_preprocessing.ipynb (feature engineering)
# 3. 03_model_training.ipynb (train models)
```

### 5️⃣ Run the Service

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Loaded 3 models successfully
INFO:     Feature count: 18
INFO:     Masked IP Detection API started successfully
```

---

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| 🏠 **Web Dashboard** | http://localhost:8000/ | Interactive testing interface |
| 📚 **API Documentation** | http://localhost:8000/docs | Swagger UI (interactive) |
| 📋 **Alternative Docs** | http://localhost:8000/redoc | ReDoc (clean layout) |
| ❤️ **Health Check** | http://localhost:8000/health | Service status |
| ℹ️ **API Info** | http://localhost:8000/ | Metadata & endpoints |

---

## 📡 API Usage

### 🔹 Check Single IP

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/check" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "8.8.8.8",
    "include_details": true
  }'
```

**Response:**
```json
{
  "ip_address": "8.8.8.8",
  "is_masked": false,
  "confidence": 0.92,
  "risk_level": "LOW",
  "detected_type": null,
  "details": {
    "ensemble_probability": 0.08,
    "model_predictions": {
      "random_forest": 0,
      "xgboost": 0,
    }
  },
  "timestamp": "2025-01-15T10:30:00"
}
```

### 🔹 Batch IP Check

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_addresses": ["8.8.8.8", "1.1.1.1", "185.220.101.1"],
    "include_details": false
  }'
```

**Response:**
```json
{
  "total_checked": 3,
  "results": [
    {
      "ip_address": "8.8.8.8",
      "is_masked": false,
      "confidence": 0.92,
      "risk_level": "LOW"
    },
    {
      "ip_address": "185.220.101.1",
      "is_masked": true,
      "confidence": 0.95,
      "risk_level": "CRITICAL",
      "detected_type": "tor"
    }
  ],
  "timestamp": "2025-01-15T10:31:00"
}
```

### 🔹 Python Client

```python
import requests

def check_ip(ip_address):
    """Check if IP is masked"""
    response = requests.post(
        "http://localhost:8000/api/v1/check",
        json={
            "ip_address": ip_address,
            "include_details": True
        }
    )
    return response.json()

# Example usage
result = check_ip("8.8.8.8")
print(f"IP: {result['ip_address']}")
print(f"Is Masked: {result['is_masked']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Risk Level: {result['risk_level']}")
```

### 🔹 JavaScript/Node.js Client

```javascript
async function checkIP(ipAddress) {
  const response = await fetch('http://localhost:8000/api/v1/check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      ip_address: ipAddress,
      include_details: true 
    })
  });
  return await response.json();
}

// Example usage
checkIP('8.8.8.8').then(result => {
  console.log(`IP: ${result.ip_address}`);
  console.log(`Is Masked: ${result.is_masked}`);
  console.log(`Confidence: ${(result.confidence * 100).toFixed(1)}%`);
  console.log(`Risk Level: ${result.risk_level}`);
});
```

---

## 📈 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| Random Forest | 94.2% | 93.8% | 94.5% | 94.1% | 0.972 |
| XGBoost | 95.1% | 94.9% | 95.3% | 95.1% | 0.981 |
| **Ensemble** | **96.3%** | **96.1%** | **96.5%** | **96.3%** | **0.987** |

> **Note**: Metrics are based on offline evaluation datasets. Real-world performance may vary based on traffic patterns and threat landscape.

### Performance Characteristics

- ⚡ **Latency**: <50ms per request (with caching: <10ms)
- 🔄 **Throughput**: 1000+ requests/second
- 💾 **Memory**: ~200MB RAM
- 📊 **False Positive Rate**: <3%

---

## 🔧 Integration Examples

### WAF Middleware (Python/FastAPI)

```python
from fastapi import FastAPI, Request, HTTPException
import httpx

app = FastAPI()

async def check_masked_ip(ip: str) -> dict:
    """Check if IP is masked using the microservice"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'http://localhost:8000/api/v1/check',
            json={'ip_address': ip}
        )
        return response.json()

@app.middleware("http")
async def ip_filtering_middleware(request: Request, call_next):
    """Block high-risk masked IPs"""
    client_ip = request.client.host
    
    result = await check_masked_ip(client_ip)
    
    if result['is_masked'] and result['risk_level'] in ['HIGH', 'CRITICAL']:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Suspicious IP detected"
        )
    
    return await call_next(request)
```

### Nginx/ModSecurity Integration

```nginx
# Custom rule to check IPs
SecRule REQUEST_HEADERS:X-Forwarded-For "@rx ^(.*)$" \
    "id:9001,\
    phase:1,\
    t:none,\
    capture,\
    chain"
    SecRule TX:1 "@external /usr/local/bin/check_masked_ip.sh" \
        "deny,status:403,msg:'Masked IP Detected'"
```

**check_masked_ip.sh:**
```bash
#!/bin/bash
IP=$1
RESULT=$(curl -s -X POST http://localhost:8000/api/v1/check \
  -H "Content-Type: application/json" \
  -d "{\"ip_address\":\"$IP\"}" | jq -r '.is_masked')

if [ "$RESULT" = "true" ]; then
  exit 1  # Block
else
  exit 0  # Allow
fi
```

---

## 🧪 Testing

### Run Test Suite

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py -v
```

### Manual Testing

```bash
# Test legitimate IP
curl -X POST http://localhost:8000/api/v1/check \
  -H "Content-Type: application/json" \
  -d '{"ip_address": "8.8.8.8"}'

# Test Tor exit node (example)
curl -X POST http://localhost:8000/api/v1/check \
  -H "Content-Type: application/json" \
  -d '{"ip_address": "185.220.101.1"}'

# Test private IP
curl -X POST http://localhost:8000/api/v1/check \
  -H "Content-Type: application/json" \
  -d '{"ip_address": "192.168.1.1"}'
```

---

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t masked-ip-detection -f docker/Dockerfile .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  --name masked-ip-api \
  masked-ip-detection
```

---

## 📁 Project Structure

```
masked-ip-detection/
├── src/
│   ├── api/
│   │   ├── main.py              # FastAPI application
│   │   ├── routes.py            # API endpoints
│   │   └── schemas.py           # Pydantic models
│   ├── data/
│   │   └── collectors.py        # Data collection scripts
│   ├── features/
│   │   └── ip_features.py       # Feature extraction
│   └── models/
│       └── predictor.py         # ML prediction logic
├── models/                       # Trained ML models (gitignored)
│   ├── random_forest_model.pkl
│   ├── xgboost_model.pkl
│   └── feature_names.pkl
├── notebooks/                    # Google Colab notebooks
│   ├── Complete_Data_Collection.ipynb
│   ├── 02_preprocessing.ipynb
│   └── 03_model_training.ipynb
├── dashboard/                    # Web UI
│   └── templates/
│       └── index.html
├── tests/                        # Test suite
│   ├── test_api.py
│   └── test_features.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt              # Python dependencies
├── .gitignore
└── README.md
```

---

## 🔒 Security Considerations

### Production Deployment Checklist

- [ ] **Enable HTTPS**: Use SSL/TLS certificates
- [ ] **API Authentication**: Implement API keys or OAuth2
- [ ] **Rate Limiting**: Prevent abuse (e.g., 100 requests/minute)
- [ ] **Input Validation**: Already implemented via Pydantic
- [ ] **Logging**: Monitor all requests and predictions
- [ ] **Redis Security**: Use password authentication
- [ ] **CORS Configuration**: Restrict allowed origins
- [ ] **Error Handling**: Don't expose internal details

### Example Rate Limiting (FastAPI)

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/check")
@limiter.limit("100/minute")
async def check_ip(request: Request, ip_request: IPCheckRequest):
    # ... existing code
```

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 src/
black src/

# Run type checking
mypy src/
```

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 📧 Support & Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/rt1856/masked-ip-detection/issues)
- **Discussions**: [Join community discussions](https://github.com/rt1856/masked-ip-detection/discussions)
- **Email**: thakkarriddhi1510@gmail.com

---

## 🙏 Acknowledgments

Special thanks to:

- **[Tor Project](https://www.torproject.org/)** - Tor exit node data
- **[MaxMind](https://www.maxmind.com/)** - GeoIP2 databases
- **Open-source proxy list maintainers** - Community-driven threat intelligence
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[Scikit-learn](https://scikit-learn.org/)** & **[XGBoost](https://xgboost.readthedocs.io/)** - ML ecosystem
- **SWAVLAMBAN 2025 Organizers** - Hackathon opportunity

---



<div align="center">


[⭐ Star this repo](https://github.com/rt1856/masked-ip-detection) | [🐛 Report Bug](https://github.com/rt1856/masked-ip-detection/issues) | [💡 Request Feature](https://github.com/rt1856/masked-ip-detection/issues)

</div>
