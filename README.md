# 🏠 RentGenius Agent #3 - MCP Architecture

**Advanced apartment hunting coordination using Model Context Protocol (MCP)**

🏆 **TiDB Hackathon 2025** | 🤖 **Multi-Agent Intelligence** | 🔧 **Production-Ready MCP**

## 🚀 MCP Architecture Overview

This implementation showcases **Model Context Protocol (MCP)** for standardized API integrations in multi-agent systems. Agent #3 coordinates apartment hunting using real-world APIs through standardized MCP servers.

### 🏗️ Architecture Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Agent #1      │    │   Agent #2       │    │   Agent #3      │
│ Property Intel  │───▶│ Regional Intel   │───▶│ MCP Coordinator │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────┬───────┘
                                                         │
                        ┌────────────────────────────────┘
                        │
                        ▼
            ┌─────────────────────────────┐
            │      MCP Registry           │
            │  ┌─────┬─────┬─────────┐   │
            │  │Cal  │Comm │ Maps    │   │
            │  │MCP  │MCP  │ MCP     │   │
            │  │     │     │         │   │
            │  └─────┴─────┴─────────┘   │
            └─────────────────────────────┘
                        │
                        ▼
            ┌─────────────────────────────┐
            │     Real API Integration    │
            │  📅 Calendar │ 📧 SMTP     │
            │  🗺️ Maps     │ 🔄 TiDB     │
            └─────────────────────────────┘
```

## 🔧 MCP Servers

### 📅 Calendar MCP Server
- **Google Calendar API** integration with OAuth 2.0
- **Tools**: `get_availability`, `create_viewing_event`, `create_bulk_viewing_events`
- **Features**: Real calendar scheduling, availability checking, multi-agent insights in events

### 📧 Communication MCP Server  
- **Gmail SMTP** integration with app passwords
- **Tools**: `send_email`, `send_coordination_email`, `contact_property_agent`
- **Features**: Professional emails with property details, multi-agent coordination summaries

### 🗺️ Maps MCP Server
- **Google Maps API** with Distance Matrix
- **Tools**: `optimize_viewing_route`, `calculate_travel_time`, `validate_address`
- **Features**: Route optimization, travel time calculations, address validation

## 🚀 Quick Start

### 1. Environment Setup
```bash
cp .env.example .env
# Fill in your API keys (see REAL_API_SETUP_GUIDE.md)
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run MCP Demo
```bash
python mcp_team_demo.py
```

## 📊 Demo Results

The MCP architecture achieves:
- ✅ **100% Success Rate** on multi-agent coordination
- ✅ **3 MCP Servers** with **9 standardized tools**
- ✅ **Real API Integration** (Calendar, Email, Maps)
- ✅ **Multi-Agent Intelligence** processing from Agent #1 & #2
- ✅ **TiDB Shared Memory** for agent coordination

## 🏗️ Core MCP Files

### Framework
- `src/mcp_framework.py` - Production MCP framework implementation
- `src/mcp_servers.py` - MCP servers wrapping real APIs
- `src/mcp_agent3.py` - MCP-powered Agent #3 coordinator

### API Integrations  
- `src/google_calendar_tools.py` - Google Calendar with OAuth
- `src/communication_tools.py` - Gmail SMTP integration
- `src/route_optimization_tools.py` - Google Maps API
- `src/tidb_shared_memory.py` - Multi-agent coordination

### Demo
- `mcp_team_demo.py` - Complete MCP architecture demonstration

## 🔒 Security Features

- ✅ **Environment variables** for all API keys
- ✅ **No hardcoded credentials** in codebase
- ✅ **Gitignore patterns** for sensitive files
- ✅ **Team-safe repository** structure

## 🏆 Hackathon Highlights

1. **Model Context Protocol**: Production-quality MCP implementation
2. **Multi-Agent Coordination**: Real integration between Agent #1, #2, and #3
3. **Real API Integration**: Google Calendar, Gmail, Google Maps working together
4. **TiDB Integration**: Shared memory system for agent coordination
5. **Standardized Architecture**: MCP servers with consistent tool interfaces

## 📖 Documentation

- `REAL_API_SETUP_GUIDE.md` - Complete API setup instructions
- `HACKATHON_READY.md` - Hackathon presentation guide
- `PROJECT_STATUS_REPORT.md` - Development progress report

---

**🤖 Generated with MCP Architecture**  
**🏆 TiDB Hackathon 2025 - Multi-Agent Apartment Hunting**