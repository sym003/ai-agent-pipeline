# 小龙虾养殖赛马模块

这是一个基于 Agent Teams Harness 框架的小龙虾养殖赛马功能模块，用于对养殖户的养殖效果进行评比和排名。

## 功能特点

- 🦐 **多维度评估**: 产量、品质、成本控制综合评分
- 🤖 **智能Agent驱动**: 自动数据收集、分析、评估、报告生成
- 📊 **可视化展示**: 生成美观的排行榜网页
- 📧 **自动通知**: 通过邮件通知获奖者
- 🔗 **飞书集成**: 支持从飞书表格导入参赛者信息

## 核心组件

### 数据模型 (models.py)
- `Farmer`: 养殖户信息
- `Pond`: 养殖池信息  
- `HarvestRecord`: 收获记录
- `EnvironmentData`: 环境监测数据
- `RaceConfig`: 赛马配置
- `RaceResult`: 比赛结果

### 评估引擎 (evaluator.py)
- `RaceEvaluator`: 核心评判算法
- `DataImporter`: 数据导入工具
- `ReportGenerator`: 报告生成器

### Agent团队 (agents.py)
- `DataCollectionAgent`: 数据收集Agent
- `AnalysisAgent`: 数据分析Agent
- `EvaluationAgent`: 评估Agent
- `ReportingAgent`: 报告生成Agent
- `CrayfishRacingTeam`: 主协调团队

### API接口 (api.py)
- 赛马启动接口
- 结果查询接口
- 排行榜展示接口

## 使用示例

```python
from src.crayfish_racing import CrayfishRacingTeam, RaceConfig
from datetime import datetime

# 创建赛马配置
config = RaceConfig(
    id="race_20240101",
    name="第一季度小龙虾养殖赛马",
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 3, 31),
    evaluation_period=90
)

# 创建赛马团队
team = CrayfishRacingTeam()

# 执行赛马
results = await team.execute_race(config, data_sources)
```

## API端点

- `POST /crayfish-racing/start-race` - 启动赛马
- `GET /crayfish-racing/races/{race_id}` - 获取赛马状态
- `GET /crayfish-racing/races/{race_id}/results` - 获取赛马结果
- `GET /crayfish-racing/leaderboard/{race_id}` - 查看排行榜

## 评判标准

### 产量得分 (40%权重)
- 基于单位面积产量计算
- 基准产量：2000斤/池塘
- 最优产量：5000斤/池塘

### 品质得分 (30%权重)
- 平均虾重（40%）
- 精品虾比例（40%）
- 成活率（20%）

### 成本控制得分 (30%权重)
- 基于单位产量成本计算
- 最优成本：8元/斤
- 最大成本：20元/斤

## 部署说明

该模块可以直接集成到现有的 Agent Teams Harness 项目中，需要：

1. 在主应用中注册API路由器
2. 配置数据库连接
3. 设置邮件服务器参数
4. 配置飞书API密钥

## 注意事项

- 需要确保基础的基础设施模块（feishu、email等）已正确实现
- 实际部署时需要替换示例数据为真实数据源
- 建议定期备份比赛数据