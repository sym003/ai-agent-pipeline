#!/usr/bin/env python3
"""
小龙虾养殖赛马示例脚本
演示如何使用赛马模块进行养殖效果评比
"""

import sys
import os
import asyncio
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.crayfish_racing.models import *
from src.crayfish_racing.evaluator import RaceEvaluator
from src.crayfish_racing.agents import CrayfishRacingTeam


async def create_sample_data():
    """创建示例数据"""
    
    # 创建养殖户
    farmers = [
        Farmer(
            id="farmer_001",
            name="张三",
            farm_name="清水小龙虾养殖场",
            farm_type=FarmType.INDIVIDUAL,
            location="江苏省盱眙县",
            contact="zhangsan@email.com"
        ),
        Farmer(
            id="farmer_002", 
            name="李四",
            farm_name="绿源生态农场",
            farm_type=FarmType.COOPERATIVE,
            location="湖北省潜江市",
            contact="lisi@email.com"
        ),
        Farmer(
            id="farmer_003",
            name="王五",
            farm_name="富农水产基地",
            farm_type=FarmType.COMPANY,
            location="湖南省岳阳市",
            contact="wangwu@email.com"
        )
    ]
    
    # 创建池塘
    ponds = [
        Pond(id="pond_001", farmer_id="farmer_001", pond_name="一号池", area=10.0, water_depth=1.5, stocking_density=8000),
        Pond(id="pond_002", farmer_id="farmer_001", pond_name="二号池", area=8.0, water_depth=1.3, stocking_density=7500),
        Pond(id="pond_003", farmer_id="farmer_002", pond_name="A区池", area=15.0, water_depth=1.6, stocking_density=8500),
        Pond(id="pond_004", farmer_id="farmer_002", pond_name="B区池", area=12.0, water_depth=1.4, stocking_density=8200),
        Pond(id="pond_005", farmer_id="farmer_003", pond_name="主养池", area=20.0, water_depth=1.8, stocking_density=9000),
        Pond(id="pond_006", farmer_id="farmer_003", pond_name="辅养池", area=10.0, water_depth=1.5, stocking_density=7800)
    ]
    
    # 创建收获记录
    harvest_records = [
        # 张三的收获记录
        HarvestRecord(
            id="harvest_001",
            pond_id="pond_001",
            harvest_date=datetime.now() - timedelta(days=10),
            crayfish_grade=CrayfishGrade.PREMIUM,
            quantity=1200,
            average_weight=35,
            survival_rate=85,
            selling_price=28,
            total_revenue=33600
        ),
        HarvestRecord(
            id="harvest_002",
            pond_id="pond_002",
            harvest_date=datetime.now() - timedelta(days=8),
            crayfish_grade=CrayfishGrade.FIRST,
            quantity=800,
            average_weight=28,
            survival_rate=82,
            selling_price=25,
            total_revenue=20000
        ),
        # 李四的收获记录
        HarvestRecord(
            id="harvest_003",
            pond_id="pond_003",
            harvest_date=datetime.now() - timedelta(days=12),
            crayfish_grade=CrayfishGrade.PREMIUM,
            quantity=1800,
            average_weight=32,
            survival_rate=88,
            selling_price=27,
            total_revenue=48600
        ),
        HarvestRecord(
            id="harvest_004",
            pond_id="pond_004",
            harvest_date=datetime.now() - timedelta(days=9),
            crayfish_grade=CrayfishGrade.FIRST,
            quantity=1200,
            average_weight=26,
            survival_rate=84,
            selling_price=24,
            total_revenue=28800
        ),
        # 王五的收获记录
        HarvestRecord(
            id="harvest_005",
            pond_id="pond_005",
            harvest_date=datetime.now() - timedelta(days=15),
            crayfish_grade=CrayfishGrade.PREMIUM,
            quantity=2200,
            average_weight=38,
            survival_rate=90,
            selling_price=30,
            total_revenue=66000
        ),
        HarvestRecord(
            id="harvest_006",
            pond_id="pond_006",
            harvest_date=datetime.now() - timedelta(days=11),
            crayfish_grade=CrayfishGrade.SECOND,
            quantity=900,
            average_weight=22,
            survival_rate=78,
            selling_price=20,
            total_revenue=18000
        )
    ]
    
    # 创建成本记录
    cost_records = [
        CostRecord(
            id="cost_001",
            farmer_id="farmer_001",
            record_date=datetime.now() - timedelta(days=30),
            seed_cost=8000,
            feed_cost=12000,
            medicine_cost=2000,
            labor_cost=5000,
            total_cost=27000
        ),
        CostRecord(
            id="cost_002",
            farmer_id="farmer_002",
            record_date=datetime.now() - timedelta(days=30),
            seed_cost=12000,
            feed_cost=18000,
            medicine_cost=3000,
            equipment_cost=5000,
            labor_cost=8000,
            total_cost=46000
        ),
        CostRecord(
            id="cost_003",
            farmer_id="farmer_003",
            record_date=datetime.now() - timedelta(days=30),
            seed_cost=15000,
            feed_cost=25000,
            medicine_cost=4000,
            equipment_cost=10000,
            labor_cost=12000,
            total_cost=66000
        )
    ]
    
    # 创建参赛者
    participants = [
        RaceParticipant(farmer_id="farmer_001", pond_ids=["pond_001", "pond_002"]),
        RaceParticipant(farmer_id="farmer_002", pond_ids=["pond_003", "pond_004"]),
        RaceParticipant(farmer_id="farmer_003", pond_ids=["pond_005", "pond_006"])
    ]
    
    return farmers, ponds, harvest_records, cost_records, participants


async def run_sample_race():
    """运行示例赛马"""
    
    print("🦐 开始小龙虾养殖赛马演示...")
    print("=" * 50)
    
    # 创建示例数据
    farmers, ponds, harvest_records, cost_records, participants = await create_sample_data()
    
    # 创建比赛配置
    config = RaceConfig(
        id="demo_race_2024",
        name="2024年第一季度小龙虾养殖赛马",
        start_date=datetime.now() - timedelta(days=90),
        end_date=datetime.now(),
        evaluation_period=90,
        yield_weight=0.4,
        quality_weight=0.3,
        cost_weight=0.3,
        prize_count=3,
        prize_names=["🏆 冠军", "🥈 亚军", "🥉 季军"]
    )
    
    print(f"比赛名称: {config.name}")
    print(f"参赛人数: {len(participants)} 人")
    print(f"评判权重: 产量{config.yield_weight*100}% + 品质{config.quality_weight*100}% + 成本{config.cost_weight*100}%")
    print()
    
    # 执行评估
    evaluator = RaceEvaluator(config)
    results = evaluator.evaluate_race(participants, harvest_records, cost_records)
    
    # 显示结果
    print("🏁 比赛结果:")
    print("-" * 50)
    
    for result in results:
        farmer = next((f for f in farmers if f.id == result.farmer_id), None)
        if farmer:
            print(f"第{result.ranking}名: {farmer.name} ({farmer.farm_name})")
            print(f"  总得分: {result.total_score:.1f}分")
            print(f"  产量得分: {result.yield_score:.1f}分 (总产量: {result.total_yield:.0f}斤)")
            print(f"  品质得分: {result.quality_score:.1f}分 (精品率: {result.premium_rate:.1f}%)")
            print(f"  成本得分: {result.cost_score:.1f}分 (净利润: {result.profit:.0f}元)")
            if result.prize:
                print(f"  🎉 获得奖项: {result.prize}")
            print()
    
    # 生成报告
    print("📄 生成比赛报告...")
    from src.crayfish_racing.evaluator import ReportGenerator
    report = ReportGenerator.generate_ranking_report(results, farmers)
    print(report)
    
    return results


async def main():
    """主函数"""
    try:
        results = await run_sample_race()
        print("✅ 赛马演示完成!")
        
        # 可以在这里添加更多演示功能
        # 比如保存结果到文件、生成图表等
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())