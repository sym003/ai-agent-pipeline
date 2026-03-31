"""小龙虾养殖赛马评判引擎"""

from typing import List, Dict, Optional
from datetime import datetime
from collections import defaultdict
import statistics
from .models import (
    Farmer, Pond, EnvironmentData, HarvestRecord, 
    FeedRecord, CostRecord, RaceParticipant, RaceConfig, RaceResult
)


class RaceEvaluator:
    """赛马评判引擎"""
    
    def __init__(self, config: RaceConfig):
        self.config = config
    
    def evaluate_race(self, participants: List[RaceParticipant], 
                     harvest_records: List[HarvestRecord],
                     cost_records: List[CostRecord]) -> List[RaceResult]:
        """执行比赛评估"""
        
        results = []
        
        # 按养殖户分组数据
        farmer_harvests = defaultdict(list)
        farmer_costs = defaultdict(list)
        
        for record in harvest_records:
            farmer_harvests[record.pond_id].append(record)
            
        for record in cost_records:
            farmer_costs[record.farmer_id].append(record)
        
        # 为每个参赛者计算结果
        for participant in participants:
            result = self._calculate_farmer_result(participant, farmer_harvests, farmer_costs)
            results.append(result)
        
        # 排名
        results.sort(key=lambda x: x.total_score, reverse=True)
        for i, result in enumerate(results, 1):
            result.ranking = i
            if i <= len(self.config.prize_names):
                result.prize = self.config.prize_names[i-1]
        
        return results
    
    def _calculate_farmer_result(self, participant: RaceParticipant,
                               harvest_data: Dict[str, List[HarvestRecord]],
                               cost_data: Dict[str, List[CostRecord]]) -> RaceResult:
        """计算单个养殖户的比赛结果"""
        
        # 收集该农户的所有收获数据
        farmer_harvests = []
        for pond_id in participant.pond_ids:
            farmer_harvests.extend(harvest_data.get(pond_id, []))
        
        # 收集该农户的成本数据
        farmer_costs = cost_data.get(participant.farmer_id, [])
        
        if not farmer_harvests:
            # 如果没有收获数据，返回零分结果
            return RaceResult(
                race_id=self.config.id,
                farmer_id=participant.farmer_id,
                total_yield=0,
                avg_crayfish_weight=0,
                premium_rate=0,
                survival_rate=0,
                total_cost=sum(c.total_cost for c in farmer_costs),
                total_revenue=0,
                profit=-sum(c.total_cost for c in farmer_costs),
                yield_score=0,
                quality_score=0,
                cost_score=0,
                total_score=0,
                ranking=0
            )
        
        # 计算各项指标
        total_yield = sum(h.quantity for h in farmer_harvests)
        avg_weight = statistics.mean([h.average_weight for h in farmer_harvests])
        survival_rates = [h.survival_rate for h in farmer_harvests]
        avg_survival = statistics.mean(survival_rates) if survival_rates else 0
        
        # 计算精品虾比例
        premium_count = sum(1 for h in farmer_harvests if h.crayfish_grade.value.startswith("精品"))
        premium_rate = (premium_count / len(farmer_harvests)) * 100 if farmer_harvests else 0
        
        # 计算收入和成本
        total_revenue = sum(h.total_revenue for h in farmer_harvests)
        total_cost = sum(c.total_cost for c in farmer_costs) if farmer_costs else 0
        profit = total_revenue - total_cost
        
        # 计算各项得分（标准化到0-100分）
        yield_score = self._calculate_yield_score(total_yield, participant)
        quality_score = self._calculate_quality_score(avg_weight, premium_rate, avg_survival)
        cost_score = self._calculate_cost_score(profit, total_cost, total_yield)
        
        # 加权总分
        total_score = (
            yield_score * self.config.yield_weight +
            quality_score * self.config.quality_weight +
            cost_score * self.config.cost_weight
        )
        
        return RaceResult(
            race_id=self.config.id,
            farmer_id=participant.farmer_id,
            total_yield=total_yield,
            avg_crayfish_weight=avg_weight,
            premium_rate=premium_rate,
            survival_rate=avg_survival,
            total_cost=total_cost,
            total_revenue=total_revenue,
            profit=profit,
            yield_score=yield_score,
            quality_score=quality_score,
            cost_score=cost_score,
            total_score=total_score,
            ranking=0  # 等待后续排名
        )
    
    def _calculate_yield_score(self, total_yield: float, participant: RaceParticipant) -> float:
        """计算产量得分"""
        # 基于单位面积产量计算
        total_area = len(participant.pond_ids)  # 简化处理，实际应该查询池塘面积
        yield_per_area = total_yield / max(total_area, 1)
        
        # 设定基准产量（可根据历史数据调整）
        baseline_yield = 2000  # 斤/池塘
        max_yield = 5000       # 斤/池塘
        
        if yield_per_area <= baseline_yield:
            score = 50
        elif yield_per_area >= max_yield:
            score = 100
        else:
            # 线性插值
            score = 50 + ((yield_per_area - baseline_yield) / (max_yield - baseline_yield)) * 50
            
        return min(100, max(0, score))
    
    def _calculate_quality_score(self, avg_weight: float, premium_rate: float, survival_rate: float) -> float:
        """计算品质得分"""
        # 重量得分 (6钱=30克为基准)
        weight_score = min(100, max(0, (avg_weight / 30) * 50))
        
        # 精品率得分
        premium_score = premium_rate  # 直接使用百分比
        
        # 成活率得分
        survival_score = survival_rate  # 直接使用百分比
        
        # 综合品质得分
        quality_score = (weight_score * 0.4 + premium_score * 0.4 + survival_score * 0.2)
        return min(100, max(0, quality_score))
    
    def _calculate_cost_score(self, profit: float, total_cost: float, total_yield: float) -> float:
        """计算成本控制得分"""
        if total_yield <= 0:
            return 0
            
        # 计算单位成本
        cost_per_yield = total_cost / max(total_yield, 1)
        
        # 设定合理的成本范围 (元/斤)
        optimal_cost = 8   # 最优成本
        max_cost = 20      # 最大可接受成本
        
        if cost_per_yield <= optimal_cost:
            score = 100
        elif cost_per_yield >= max_cost:
            score = 0
        else:
            # 反向线性插值（成本越低分数越高）
            score = 100 - ((cost_per_yield - optimal_cost) / (max_cost - optimal_cost)) * 100
            
        return min(100, max(0, score))


class DataImporter:
    """数据导入器"""
    
    @staticmethod
    def from_manual_input(data: dict) -> tuple[List[Farmer], List[Pond], List[HarvestRecord]]:
        """从手工输入数据创建对象"""
        # 实现手工数据导入逻辑
        pass
    
    @staticmethod  
    def from_iot_data(iot_records: List[dict]) -> List[EnvironmentData]:
        """从IoT传感器数据创建环境数据"""
        # 实现IoT数据导入逻辑
        pass
    
    @staticmethod
    def from_feishu_table(table_data: dict) -> List[RaceParticipant]:
        """从飞书表格导入参赛者信息"""
        # 实现飞书表格导入逻辑
        pass


class ReportGenerator:
    """报告生成器"""
    
    @staticmethod
    def generate_ranking_report(results: List[RaceResult], farmers: List[Farmer]) -> str:
        """生成排名报告"""
        report = f"# 小龙虾养殖赛马排名报告\n\n"
        report += f"比赛时间: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        report += "## 排名结果\n\n"
        
        for result in results:
            farmer = next((f for f in farmers if f.id == result.farmer_id), None)
            if farmer:
                report += f"**第{result.ranking}名**: {farmer.name} ({farmer.farm_name})\n"
                report += f"- 总得分: {result.total_score:.1f}分\n"
                report += f"- 产量: {result.total_yield:.1f}斤\n"
                report += f"- 净利润: {result.profit:.1f}元\n"
                if result.prize:
                    report += f"- 获得奖项: {result.prize}\n"
                report += "\n"
        
        return report