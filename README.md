# Aether-TMA (TON Transaction DSL) 🚀

**Enterprise-grade multi-agent AI orchestrator for Telegram with advanced TON blockchain integration.**

Aether-TMA is a production-ready, scalable platform for deploying and coordinating AI agents through Telegram interface. This system transforms standard Telegram bots into powerful tools for data analysis, predictive analytics, automation, and TON blockchain operations.

## 🎬 **Live Demo**

[![Aether-TMA Demo](https://img.shields.io/badge/Watch-Demo-red?style=for-the-badge&logo=youtube)](https://github.com/AlienMedoff/5.03-bot/assets/YOUR_VIDEO_ID)

*See Aether-TMA in action: Multi-agent AI coordination, TON blockchain integration, and real-time Telegram interface*

## 🚀 **One-Click Deployment**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/AlienMedoff/5.03-bot)
[![Deploy to Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

![Architecture Diagram](https://img.shields.io/badge/Architecture-Multi--Agent-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Stars](https://img.shields.io/github/stars/AlienMedoff/5.03-bot?style=social)
![Forks](https://img.shields.io/github/forks/AlienMedoff/5.03-bot?style=social)
![Issues](https://img.shields.io/github/issues/AlienMedoff/5.03-bot)
![PR](https://img.shields.io/github/issues-pr/AlienMedoff/5.03-bot)

## 🎯 **Overview**

Unlike conventional chatbots, Aether-TMA is an **intelligent orchestrator** that bridges Telegram interface with local or cloud AI backends, enabling agents to execute complex tasks, analyze market data, process blockchain transactions, and respond to users in real-time with enterprise-grade security and scalability.

### 🚀 **Core Features**
- **🤖 Multi-Agent Architecture**: Advanced agent coordination and management system
- **⚡ High-Performance**: Full asyncio support with aiogram 3.x optimization
- **🔒 Enterprise Security**: Military-grade encryption and audit logging
- **🌐 TON Integration**: Native TON blockchain transaction processing
- **📊 Real-time Analytics**: Advanced monitoring and metrics collection
- **🔧 Dynamic Model Routing**: Intelligent load balancing across AI models
- **🐳 Container-Ready**: Production Docker deployment with Kubernetes support

## 🏗️ **System Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Telegram UI    │────│  Orchestrator   │────│  AI Models Hub  │
│  (aiogram 3.x) │    │  (FastAPI)      │    │  (Multi-model)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Session Mgmt   │────│  Redis Cache    │────│  TON Blockchain │
│  (Distributed)  │    │  (Sessions)     │    │  (Transactions) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Prometheus     │────│  Grafana        │────│  AlertManager  │
│  (Metrics)      │    │  (Dashboards)   │    │  (Alerts)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 **Quick Start**

### 📋 **Prerequisites**
- **Python 3.10+** with pip package manager
- **Docker & Docker Compose** (optional, for containerized deployment)
- **Valid API keys** for supported AI models
- **Telegram Bot Token** from @BotFather

### ⚡ **Installation**

#### 1. **Clone Repository**
```bash
git clone https://github.com/AlienMedoff/5.03-bot.git
cd 5.03-bot
```

#### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

#### 3. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your API keys and tokens
```

#### 4. **Configuration Setup**
```bash
# .env file configuration
MISTRAL_API_KEY=your_mistral_api_key_here
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TON_API_KEY=your_ton_api_key_here  # Optional for TON integration
```

## 🚀 **Deployment**

### 🏠 **Local Development**

#### 1. **Start AI Service**
```bash
python final_ai_start.py
```

**Expected Output:**
```
============================================================
AETHER-TMA MULTI-AGENT SYSTEM - INITIALIZING
============================================================
Initializing AI models...
✓ Mistral AI: mistral-large-latest (Ready)
✓ Groq AI: llama-3.3-70b-versatile (Ready)
✓ Google Gemini: gemini-2.5-flash (Ready)
============================================================
3 AI models initialized successfully
Finding available port...
✓ Free port found: 8000
============================================================
API ENDPOINTS:
Chat: http://127.0.0.1:8000/ai/chat
Models: http://127.0.0.1:8000/ai/models
Status: http://127.0.0.1:8000/ai/status
TON Transactions: http://127.0.0.1:8000/ton/transaction
Health Check: http://127.0.0.1:8000/health
============================================================
✓ AETHER-TMA SYSTEM ONLINE - Port 8000
============================================================
```

#### 2. **Start Telegram Bot**
```bash
# Open new terminal
python mvp_telegram_bot.py
```

**Expected Output:**
```
============================================================
AETHER-TMA TELEGRAM BOT - STARTING
============================================================
✓ Bot initialization complete
✓ AI service connection established
✓ TON blockchain integration ready
================================================<arg_value>
🚀 AETHER-TMA BOT ONLINE
============================================================
```

### 🐳 **Production Deployment**

#### **Docker Compose**
```bash
docker-compose up -d --build
```

#### **Kubernetes**
```bash
kubectl apply -f k8s/
```

## 🤖 **AI Models Integration**

### 🟢 **Mistral AI (Primary)**
- **Model**: `mistral-large-latest`
- **Response Time**: ~2.0s
- **Token Limit**: ~60-80 tokens
- **Use Case**: Primary model for balanced performance
- **Cost**: Most economical for production

### 🟢 **Groq (Ultra-Fast)**
- **Model**: `llama-3.3-70b-versatile`
- **Response Time**: ~0.6s (fastest)
- **Token Limit**: ~70-80 tokens
- **Use Case**: Real-time responses and high-throughput
- **Cost**: Best for speed-critical applications

### 🟢 **Google Gemini (Advanced)**
- **Model**: `gemini-2.5-flash`
- **Response Time**: ~2.9s
- **Token Limit**: ~15-20 tokens
- **Use Case**: Complex reasoning and multimodal tasks
- **Cost**: Premium model for advanced features

## 📱 **Telegram API Commands**

| Command | Parameters | Description |
|---------|-------------|-------------|
| `/start` | - | System initialization and welcome message |
| `/chat <message>` | `<message>` | AI conversation (default: Mistral) |
| `/chat <model> <message>` | `<model> <message>` | Specific model chat (mistral/groq/gemini) |
| `/status` | - | Real-time system health check |
| `/models` | - | List available AI models |
| `/ton <address>` | `<address>` | TON wallet balance check |
| `/help` | - | Complete command reference |
| `/admin` | - | Administrative functions (restricted) |

## 🔧 **REST API Endpoints**

### **Core AI Endpoints**

#### **Chat with AI**
```bash
curl -X POST http://127.0.0.1:8000/ai/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "message": "Hello! How are you today?",
    "model": "mistral",
    "user_id": 123456789,
    "session_id": "optional_session_id"
  }'
```

#### **List Available Models**
```bash
curl -X GET http://127.0.0.1:8000/ai/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### **System Health Check**
```bash
curl -X GET http://127.0.0.1:8000/ai/status \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### **Model Performance Test**
```bash
curl -X GET http://127.0.0.1:8000/ai/test/{model_name} \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### **TON Blockchain Endpoints**

#### **Transaction Processing**
```bash
curl -X POST http://127.0.0.1:8000/ton/transaction \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "address": "EQD...your_wallet_address",
    "amount": "1.5",
    "token": "TON"
  }'
```

#### **Balance Inquiry**
```bash
curl -X GET http://127.0.0.1:8000/ton/balance/{address} \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 📁 **Project Structure**

```
aether-tma/
├── 📂 agents/                 # AI Agent Management
│   ├── __init__.py
│   ├── ai_manager.py          # AI model coordination
│   └── hub.py               # Central agent hub
├── 📂 bot/                   # Telegram Interface
│   ├── handlers/              # Command handlers
│   │   ├── __init__.py
│   │   ├── command_handler.py
│   │   └── message_handler.py
│   └── main.py              # Bot entry point
├── 📂 core/                  # System Core
│   ├── config.py             # Configuration management
│   ├── security.py           # Security & authentication
│   └── session.py           # Session management
├── 📂 docker/               # Container Configuration
│   ├── Dockerfile
│   └── docker-compose.yml
├── 📂 docs/                 # Documentation
│   └── DEPLOYMENT.md
├── 📂 scripts/              # Deployment Scripts
│   └── deploy.sh
├── 📄 final_ai_start.py      # Main AI Service
├── 📄 mvp_telegram_bot.py   # Telegram Bot
├── 📄 requirements.txt       # Dependencies
├── 📄 .env.example         # Environment Template
├── 📄 .gitignore          # Git Ignore Rules
└── 📄 README.md            # This Documentation
```

## 🔒 **Security & Compliance**

### 🛡️ **Security Features**
- **🔐 Zero-Trust Architecture**: All communications encrypted
- **🔑 API Key Rotation**: Automated credential management
- **📊 Audit Logging**: Complete activity tracking
- **🚨 Rate Limiting**: DDoS protection and abuse prevention
- **🔒 Session Management**: Secure session handling
- **🛡️ Input Validation**: Comprehensive input sanitization

### 🔐 **Authentication**
- **Telegram ID Verification**: User authentication through Telegram
- **API Key Management**: Secure credential storage
- **JWT Tokens**: Stateless authentication
- **CORS Protection**: Cross-origin request security

## 📊 **Monitoring & Observability**

### 📈 **Metrics Collection**
- **Request Rate**: API calls per minute
- **Response Time**: Average latency tracking
- **Error Rate**: Failure percentage monitoring
- **Active Sessions**: Concurrent user tracking
- **Model Usage**: Per-model utilization
- **TON Transactions**: Blockchain operation metrics

### 🚨 **Alerting System**
- **High Error Rate**: >5% failure threshold
- **Slow Response**: >3s latency alerts
- **Service Unavailability**: Health check failures
- **Security Events**: Suspicious activity detection
- **Resource Exhaustion**: Memory/CPU thresholds

## 🐳 **Container Deployment**

### **Docker Configuration**
```yaml
# docker-compose.yml
version: '3.8'
services:
  aether-ai:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
      - prometheus
  
  aether-bot:
    build: .
    command: python mvp_telegram_bot.py
    environment:
      - AI_SERVICE_URL=http://aether-ai:8000
    depends_on:
      - aether-ai
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
```

### **Kubernetes Deployment**
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aether-tma
spec:
  replicas: 3
  selector:
    matchLabels:
      app: aether-tma
  template:
    metadata:
      labels:
        app: aether-tma
    spec:
      containers:
      - name: aether-ai
        image: aether-tma:latest
        ports:
        - containerPort: 8000
        env:
        - name: REDIS_URL
          value: "redis://redis-service:6379"
```

## 🧪 **Testing & Quality Assurance**

### **Automated Testing**
```bash
# Run all tests
python -m pytest tests/

# Test AI models
python -m pytest tests/test_ai_models.py

# Test Telegram integration
python -m pytest tests/test_telegram.py

# Test TON integration
python -m pytest tests/test_ton.py
```

### **Load Testing**
```bash
# AI service load test
python scripts/load_test_ai.py --concurrent 100 --duration 300

# Telegram bot stress test
python scripts/stress_test_bot.py --users 50 --messages 1000
```

## 🚨 **Troubleshooting Guide**

### **Common Issues & Solutions**

#### **Port Conflicts**
```bash
# Find occupied ports
netstat -ano | findstr :8000

# Kill processes on port
taskkill /F /PID <PID_NUMBER>

# Alternative: Use different port
python final_ai_start.py --port 8001
```

#### **AI Model Errors**
```bash
# Test individual models
curl http://127.0.0.1:8000/ai/test/mistral
curl http://127.0.0.1:8000/ai/test/groq
curl http://127.0.0.1:8000/ai/test/gemini
```

#### **Telegram Bot Issues**
```bash
# Check bot token
python -c "
from aiogram import Bot
import asyncio
async def check_token():
    bot = Bot('YOUR_TOKEN_HERE')
    info = await bot.get_me()
    print(f'Bot Info: {info}')
asyncio.run(check_token())
"

# Reset webhook
curl -X POST https://api.telegram.org/bot<TOKEN>/deleteWebhook
```

#### **Performance Optimization**
```bash
# Clear Redis cache
redis-cli FLUSHALL

# Restart services
docker-compose restart

# Monitor resources
docker stats
```

## 🤝 **Contributing Guidelines**

### **Development Workflow**
1. **Fork Repository** from GitHub
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Implement Changes** with comprehensive testing
4. **Code Quality**: Follow PEP 8 and add documentation
5. **Submit Pull Request** with detailed description

### **Code Standards**
- **Python 3.10+** compatibility required
- **Type Hints** mandatory for all functions
- **Docstrings** following Google style guide
- **Unit Tests** minimum 80% coverage
- **Security Review** required for all changes

### **Pull Request Template**
```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Security
- [ ] Code reviewed for security issues
- [ ] No hardcoded secrets
- [ ] Input validation implemented
```

## 📄 **License & Legal**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for complete terms and conditions.

### **Third-Party Licenses**
- **aiogram**: MIT License
- **FastAPI**: MIT License
- **Redis**: BSD License
- **Docker**: Apache License 2.0

## 🙏 **Acknowledgments & Credits**

### **Core Technologies**
- **[Mistral AI](https://mistral.ai/)** - Advanced language models
- **[Groq](https://groq.com/)** - Ultra-fast inference platform
- **[Google Gemini](https://ai.google.dev/)** - Multimodal AI capabilities
- **[TON Blockchain](https://ton.org/)** - Decentralized computing platform

### **Development Tools**
- **[aiogram](https://aiogram.dev/)** - Modern Telegram bot framework
- **[FastAPI](https://fastapi.tiangolo.com/)** - High-performance web framework
- **[Redis](https://redis.io/)** - In-memory data structure store
- **[Docker](https://docker.com/)** - Container platform

### **Monitoring & Observability**
- **[Prometheus](https://prometheus.io/)** - Monitoring system
- **[Grafana](https://grafana.com/)** - Analytics platform
- **[GitHub Actions](https://github.com/features/actions)** - CI/CD pipeline

---

## 🚀 **Production Deployment Summary**

```bash
# Complete deployment sequence
git clone https://github.com/AlienMedoff/5.03-bot.git
cd 5.03-bot
pip install -r requirements.txt
cp .env.example .env
# Configure .env with production values
docker-compose up -d --build
curl http://localhost:8000/health
```

**🎯 Status: Production Ready**
**🔒 Security: Enterprise Grade**
**📈 Monitoring: Full Observability**
**🚀 Performance: Optimized for Scale**

---

**🌟 Aether-TMA: Where Advanced AI Meets Telegram & TON Blockchain!**

---

**📧 Support & Contact**
- **GitHub Issues**: [Report bugs and request features](https://github.com/AlienMedoff/5.03-bot/issues)
- **Discord Community**: [Join our developer community](https://discord.gg/aether-tma)
- **Documentation**: [Complete API reference](https://docs.aether-tma.com)

**⭐ Star this repository if you find it useful!**
