# AI Agent Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+--green.svg)](https://fastapi.tiangolo.com/)

> An enterprise-grade AI-powered R&D pipeline platform that automates the entire journey from creative idea to product delivery.

---

## 项目简介 / Overview

AI Agent Pipeline 是一个企业级 AI Agent 协作流水线平台，通过多个专业 AI Agent 团队实现从商机捕获到产品上线的完整研发流程自动化，与飞书（Lark）多维表格深度集成，实现研发流程的智能化升级。

AI Agent Pipeline is an enterprise-grade AI Agent collaboration platform that automates the entire R&D workflow from opportunity capture to product launch. It features deep integration with Feishu (Lark) Bitable for intelligent R&D process management.

**核心理念 / Core Philosophy**: 团队转型而非个人武装——让多个专业 Agent 各司其职、协同产出。

**Team Transformation over Individual Empowerment** — Multiple specialized Agents working together, each handling their domain with shared context and collaborative output.

---

## 核心流程 / Core Pipeline

```
📡 Intelligence → 📊 Pre-Sales → 🎯 AI Product Owner → 📝 Requirements → 🏗️ Architecture → 💻 Coding → 🧪 Testing
```

情报收集 → 售前分析 → AI产品负责人 → 需求分析 → 架构设计 → 编码 → 测试

---

## 核心特性 / Key Features

- 🤖 **Multi-Agent Collaboration / 多Agent协作** — 7个专业化AI团队各司其职
- 🔄 **State Machine Engine / 状态机引擎** — 完整的实体生命周期管理
- 📊 **Feishu Integration / 飞书集成** — 与飞书多维表格深度联动
- 📧 **Smart Notifications / 智能通知** — 邮件+飞书消息实时同步
- 🔀 **Git Automation / Git自动化** — 自动分支、PR、代码审查
- 🛡️ **Fallback Mechanism / 兜底机制** — 无专项Agent时的通用保障

---

## 技术栈 / Tech Stack

| 组件 Component | 技术 Technology |
|----------------|-----------------|
| Web框架 Web Framework | FastAPI |
| Agent编排 Agent Orchestration | CrewAI + LangGraph |
| 事件总线 Event Bus | Redis Stream |
| 任务队列 Task Queue | Celery + Redis |
| LLM后端 LLM Backend | DashScope (Qwen) |
| 敏捷管理 Agile Management | 飞书/Lark Bitable |
| 版本管理 Version Control | Git |
| 部署 Deployment | Docker + Nginx |

---

## 项目结构 / Project Structure

```
ai-agent-pipeline/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── docs/
│   ├── requirements.md              # 原始需求 / Original Requirements
│   ├── 状态机设计.md                 # 状态机设计 / State Machine Design
│   ├── 技术架构设计.md              # 技术架构 / Technical Architecture
│   ├── 产品设计文档.md              # 产品设计 / Product Design
│   └── prototypes/                 # 交互原型 / Interactive Prototypes
│       └── prototype.html          # 高保真HTML原型
├── src/                            # 源代码 / Source Code
│   ├── core/                       # 核心引擎 [规划中] / Core Engine
│   │   ├── state_machine.py
│   │   └── orchestrator.py
│   ├── teams/                      # AI团队 [规划中] / AI Teams
│   │   ├── intelligence_team.py   # 情报团队
│   │   ├── pre_sales_team.py      # 售前团队
│   │   ├── product_owner_team.py  # 产品负责人团队
│   │   ├── requirement_team.py    # 需求团队
│   │   ├── architecture_team.py   # 架构团队
│   │   ├── coding_team.py         # 编码团队
│   │   ├── testing_team.py        # 测试团队
│   │   ├── acceptance_team.py     # 验收团队
│   │   ├── quality_team.py        # 质量团队
│   │   └── fallback_agent.py      # 兜底Agent
│   └── infrastructure/             # 基础设施 [规划中] / Infrastructure
│       ├── feishu/                 # 飞书集成
│       ├── git/                    # Git自动化
│       ├── email/                  # 邮件通知
│       ├── llm/                    # LLM调用
│       ├── security/               # 安全模块
│       └── logging/                # 日志模块
├── configs/                       # 配置文件 / Configuration
├── tests/                         # 测试用例 / Tests
└── output/                        # 输出文件 / Output Files
```

---

## 快速开始 / Quick Start

```bash
# 克隆仓库 / Clone the repository
git clone https://github.com/sym003/ai-agent-pipeline.git
cd ai-agent-pipeline

# 安装依赖 / Install dependencies
pip install -r requirements.txt

# 配置环境变量 / Configure environment variables
cp configs/env.example .env
# Edit .env with your API keys

# 运行应用 / Run the application
python -m src.main
```

---

## 路线图 / Roadmap

### Phase 1: Foundation ✅
- [x] 状态机设计 / State Machine Design
- [x] 技术架构设计 / Technical Architecture
- [x] 产品设计文档 / Product Design Document
- [x] 高保真HTML原型 / High-fidelity HTML Prototype
- [x] 项目骨架搭建 / Project Skeleton Setup

### Phase 2: Core Engine 🚧
- [ ] 状态机引擎实现 / State Machine Engine
- [ ] Agent编排器 / Agent Orchestrator
- [ ] 飞书Webhook接入 / Feishu Webhook Integration
- [ ] 飞书API连通性验证 / Feishu API Connectivity

### Phase 3: AI Teams 📋
- [ ] 7个AI团队实现 / 7 AI Teams Implementation
- [ ] 兜底机制 / Fallback Mechanism

### Phase 4: Integration 🚀
- [ ] 端到端测试 / End-to-End Testing
- [ ] 云端部署 / Cloud Deployment

---

## 许可证 / License

MIT License - 详见 [LICENSE](LICENSE) 文件

MIT License - See [LICENSE](LICENSE) file for details.
