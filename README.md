# AI Agent Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+--green.svg)](https://fastapi.tiangolo.com/)

> An enterprise-grade AI-powered pipeline factory that automates the entire journey from creative idea to product delivery through configurable multi-agent collaboration.

---

## 项目简介 / Overview

AI Agent Pipeline 是一个**可配置的 AI 流水线工厂**，通过模块化的 Stage 和 Handler 实现从创意到交付的完整流程自动化。

- **旧定位**：AI 研发助手（固定 7 个 Agent 流水线）
- **新定位**：AI 流水线工厂（可配置 Stage，像搭乐高一样灵活）

AI Agent Pipeline is a **configurable AI pipeline factory** that automates the entire R&D workflow through modular Stages and Handlers.

**核心理念 / Core Philosophy**: 团队转型而非个人武装——让多个专业 Agent 各司其职、协同产出。

**Team Transformation over Individual Empowerment** — Multiple specialized Agents working together, each handling their domain with shared context and collaborative output.

---

## 核心概念 / Core Concepts

| 概念 | 说明 |
|------|------|
| **Pipeline** | 可配置的流水线，由一串 Stage 组成 |
| **Stage** | 装配工位，定义输入 → 处理 → 输出 |
| **Artifact** | 流水线中传递的产出物 |
| **Handler** | Stage 的执行逻辑（AI自动 / 人工 / AI+人工协作）|

### Handler 类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| **AI_AUTO** | AI 自动处理，无需人工介入 | 情报提取、格式转换、数据清洗 |
| **HUMAN_ONLY** | 纯人工处理，AI 仅做辅助 | 需求评审、架构审批、UAT 验收 |
| **AI_DRAFT_HUMAN_APPROVE** | AI 出草稿，人工确认/修改 | 意向分析、特性评审、方案选择 |

---

## 核心流程 / Core Pipeline

```
📡 情报收集(AI) → 📊 情报分析(AI) → 🎯 意向分析(AI+人工) → ✅ 意向确认(人工)
```

情报收集 → 情报分析 → 意向分析 → 意向确认

---

## 核心特性 / Key Features

- 🔧 **Configurable Pipeline / 可配置流水线** — JSON Schema 定义，可视化编辑
- 🤖 **Multi-Agent Collaboration / 多Agent协作** — 专业化 Agent 团队各司其职
- 📦 **Artifact-Driven / 产出物驱动** — 流水线中传递的是产出物而非对话消息
- 🔄 **Flexible Handlers / 灵活处理器** — AI / Human / Hybrid 三种模式
- 🛠️ **Tool Registry / 工具注册中心** — 支持内置工具和 MCP 扩展
- 📊 **Feishu Integration / 飞书集成** — 与飞书多维表格深度联动

---

## 技术栈 / Tech Stack

| 组件 Component | 技术 Technology |
:|----------------|-----------------|
| Web框架 Web Framework | FastAPI |
| 数据验证 Data Validation | Pydantic |
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
│   ├── requirements.md              # 原始需求
│   ├── 状态机设计.md                 # 状态机设计
│   ├── 技术架构设计.md              # 技术架构
│   ├── 架构升级设计.md              # v2.0 架构升级设计
│   ├── 产品设计文档.md              # 产品设计
│   └── prototypes/                 # 交互原型
│       └── prototype.html
├── src/                            # 源代码
│   └── core/                       # 核心引擎 ✅ Phase 1
│       ├── models/                 # 数据模型
│       │   ├── artifact.py         # Artifact & ArtifactType
│       │   ├── pipeline.py         # Pipeline & PipelineMeta
│       │   ├── stage.py            # Stage & RetryConfig
│       │   └── handlers.py         # Handler types
│       └── schema/                 # Schema 定义
│           ├── pipeline_schema.json # JSON Schema
│           ├── loader.py            # 配置加载器
│           └── validator.py        # 配置验证器
├── configs/
│   └── pipelines/                  # Pipeline 配置示例
│       └── rd-pipeline-v1.json     # 研发流水线配置
└── tests/                         # 测试用例
    └── test_pipeline_loading.py    # Pipeline 加载测试
```

---

## 快速开始 / Quick Start

```bash
# 克隆仓库
git clone https://github.com/sym003/ai-agent-pipeline.git
cd ai-agent-pipeline

# 安装依赖
pip install pydantic

# 运行测试
python tests/test_pipeline_loading.py

# 加载 Pipeline 配置
python -c "
from src.core import load_pipeline_from_file
pipeline = load_pipeline_from_file('configs/pipelines/rd-pipeline-v1.json')
print(f'Pipeline: {pipeline.meta.name}')
for stage in pipeline.stages:
    print(f'  - {stage.name} ({stage.handler.type})')
"
```

---

## 路线图 / Roadmap

### Phase 1: Foundation ✅
- [x] 架构升级设计（v2.0） / Architecture Upgrade Design
- [x] Pipeline Schema JSON Schema 定义 / Pipeline Schema Definition
- [x] 核心数据模型实现 / Core Data Models
- [x] Pipeline 配置加载器 / Pipeline Config Loader
- [x] Pipeline 配置验证器 / Pipeline Config Validator
- [x] 测试用例 / Tests

### Phase 2: Pipeline Executor 🚧
- [ ] PipelineExecutor 实现 / PipelineExecutor Implementation
- [ ] Stage Handler 接口实现 / Stage Handler Implementation
- [ ] ArtifactStore 持久化 / Artifact Store
- [ ] ToolRegistry 工具注册 / Tool Registry

### Phase 3: AI Teams 📋
- [ ] 情报收集 Stage 实现 / Intelligence Stage
- [ ] 意向分析 Stage 实现 / Prospect Analysis Stage
- [ ] 人工审批 Handler / Human Approval Handler

### Phase 4: Integration 🚀
- [ ] 飞书 Webhook 接入 / Feishu Webhook Integration
- [ ] 端到端测试 / End-to-End Testing
- [ ] 云端部署 / Cloud Deployment

---

## 许可证 / License

MIT License - 详见 [LICENSE](LICENSE) 文件

MIT License - See [LICENSE](LICENSE) file for details.
