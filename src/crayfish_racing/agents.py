"""小龙虾养殖赛马 Agent 团队"""

from typing import List, Dict, Any
from datetime import datetime
import json
from ..core.orchestrator import BaseAgentTeam
from ..infrastructure.feishu.client import FeishuClient
from ..infrastructure.email.sender import EmailSender
from .models import *
from .evaluator import RaceEvaluator, DataImporter, ReportGenerator


class DataCollectionAgent:
    """数据收集 Agent - 负责收集各种养殖数据"""
    
    def __init__(self):
        self.feishu_client = FeishuClient()
    
    async def collect_manual_data(self, farmer_info: dict) -> Dict[str, Any]:
        """收集手工录入的养殖数据"""
        # 解析农户基本信息
        farmer = Farmer(**farmer_info)
        
        # 这里可以添加更多数据收集逻辑
        return {
            "farmer": farmer,
            "status": "collected",
            "collected_at": datetime.now()
        }
    
    async def collect_iot_data(self, device_ids: List[str]) -> List[EnvironmentData]:
        """收集IoT传感器数据"""
        # 模拟IoT数据收集
        environment_data = []
        # 实际实现会调用IoT平台API
        return environment_data
    
    async def sync_feishu_participants(self, table_id: str) -> List[RaceParticipant]:
        """从飞书表格同步参赛者信息"""
        records = await self.feishu_client.get_bitable_records(table_id)
        participants = []
        
        for record in records:
            participant = RaceParticipant(
                farmer_id=record["fields"].get("farmer_id"),
                pond_ids=record["fields"].get("pond_ids", []),
                registration_date=datetime.fromisoformat(record["created_at"])
            )
            participants.append(participant)
            
        return participants


class AnalysisAgent:
    """数据分析 Agent - 负责分析养殖数据并生成洞察"""
    
    def __init__(self):
        pass
    
    async def analyze_farming_performance(self, harvest_records: List[HarvestRecord], 
                                        environment_data: List[EnvironmentData]) -> Dict[str, Any]:
        """分析养殖绩效"""
        analysis = {
            "total_yield": sum(r.quantity for r in harvest_records),
            "avg_survival_rate": sum(r.survival_rate for r in harvest_records) / len(harvest_records) if harvest_records else 0,
            "best_performing_farms": [],
            "environment_correlations": {},
            "recommendations": []
        }
        
        # 找出表现最好的农场
        if harvest_records:
            best_records = sorted(harvest_records, key=lambda x: x.quantity * x.selling_price, reverse=True)[:5]
            analysis["best_performing_farms"] = [
                {
                    "farm_id": rec.pond_id,
                    "revenue": rec.quantity * rec.selling_price,
                    "yield": rec.quantity
                } for rec in best_records
            ]
        
        return analysis


class EvaluationAgent:
    """评估 Agent - 负责执行赛马评估"""
    
    def __init__(self):
        pass
    
    async def run_race_evaluation(self, config: RaceConfig, 
                                participants: List[RaceParticipant],
                                harvest_records: List[HarvestRecord],
                                cost_records: List[CostRecord]) -> List[RaceResult]:
        """运行赛马评估"""
        evaluator = RaceEvaluator(config)
        results = evaluator.evaluate_race(participants, harvest_records, cost_records)
        return results


class ReportingAgent:
    """报告生成 Agent - 负责生成各种报告和可视化"""
    
    def __init__(self):
        self.feishu_client = FeishuClient()
        self.email_sender = EmailSender()
    
    async def generate_leaderboard(self, results: List[RaceResult], 
                                 farmers: List[Farmer]) -> str:
        """生成排行榜网页"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>小龙虾养殖赛马排行榜</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { text-align: center; color: #2c5aa0; }
                .rank-card { 
                    border: 1px solid #ddd; 
                    border-radius: 8px; 
                    padding: 15px; 
                    margin: 10px 0;
                    background: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .rank-1 { border-left: 5px solid gold; }
                .rank-2 { border-left: 5px solid silver; }
                .rank-3 { border-left: 5px solid #cd7f32; }
                .metrics { display: flex; justify-content: space-around; margin-top: 10px; }
                .metric { text-align: center; }
                .metric-value { font-size: 24px; font-weight: bold; color: #2c5aa0; }
                .metric-label { font-size: 12px; color: #666; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🦐 小龙虾养殖赛马排行榜</h1>
                <p>""" + datetime.now().strftime("%Y年%m月%d日") + """</p>
            </div>
        """
        
        for result in results:
            farmer = next((f for f in farmers if f.id == result.farmer_id), None)
            if not farmer:
                continue
                
            rank_class = f"rank-{result.ranking}" if result.ranking <= 3 else ""
            medal = "🥇" if result.ranking == 1 else "🥈" if result.ranking == 2 else "🥉" if result.ranking == 3 else f"#{result.ranking}"
            
            html_content += f"""
            <div class="rank-card {rank_class}">
                <h2>{medal} {farmer.name} - {farmer.farm_name}</h2>
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value">{result.total_score:.1f}</div>
                        <div class="metric-label">总得分</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{result.total_yield:.0f}斤</div>
                        <div class="metric-label">总产量</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{result.profit:.0f}元</div>
                        <div class="metric-label">净利润</div>
                    </div>
                </div>
                """ + (f"<p><strong>🏆 获得奖项:</strong> {result.prize}</p>" if result.prize else "") + """
            </div>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        return html_content
    
    async def send_results_notification(self, results: List[RaceResult], 
                                      farmers: List[Farmer]):
        """发送比赛结果通知"""
        winners = [r for r in results if r.prize]
        
        for result in winners:
            farmer = next((f for f in farmers if f.id == result.farmer_id), None)
            if farmer and farmer.contact:
                subject = f"🎉 恭喜您在小龙虾养殖赛马中获得{result.prize}!"
                body = f"""
                尊敬的{farmer.name}：
                
                恭喜您在本次小龙虾养殖赛马比赛中荣获{result.prize}！
                
                比赛成绩：
                • 总得分：{result.total_score:.1f}分
                • 总产量：{result.total_yield:.1f}斤
                • 净利润：{result.profit:.1f}元
                • 最终排名：第{result.ranking}名
                
                感谢您的参与！
                
                小龙虾养殖赛马组委会
                {datetime.now().strftime("%Y-%m-%d")}
                """
                
                await self.email_sender.send_email(farmer.contact, subject, body)


class CrayfishRacingTeam(BaseAgentTeam):
    """小龙虾养殖赛马主团队"""
    
    def __init__(self):
        super().__init__("crayfish_racing")
        self.data_agent = DataCollectionAgent()
        self.analysis_agent = AnalysisAgent()
        self.evaluation_agent = EvaluationAgent()
        self.reporting_agent = ReportingAgent()
    
    async def execute_race(self, race_config: RaceConfig, 
                          data_sources: Dict[str, Any]) -> Dict[str, Any]:
        """执行完整的赛马流程"""
        
        # 1. 数据收集
        participants = await self.data_agent.sync_feishu_participants(
            data_sources.get("feishu_table_id", "")
        )
        
        # 2. 数据分析
        analysis = await self.analysis_agent.analyze_farming_performance(
            data_sources.get("harvest_records", []),
            data_sources.get("environment_data", [])
        )
        
        # 3. 比赛评估
        results = await self.evaluation_agent.run_race_evaluation(
            race_config,
            participants,
            data_sources.get("harvest_records", []),
            data_sources.get("cost_records", [])
        )
        
        # 4. 生成报告
        leaderboard_html = await self.reporting_agent.generate_leaderboard(
            results, data_sources.get("farmers", [])
        )
        
        # 5. 发送通知
        await self.reporting_agent.send_results_notification(
            results, data_sources.get("farmers", [])
        )
        
        return {
            "race_id": race_config.id,
            "results": results,
            "analysis": analysis,
            "leaderboard_html": leaderboard_html,
            "completed_at": datetime.now()
        }