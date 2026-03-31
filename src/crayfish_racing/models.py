"""小龙虾养殖赛马数据模型"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class FarmType(str, Enum):
    """养殖场类型"""
    INDIVIDUAL = "个体养殖户"
    COOPERATIVE = "合作社"
    COMPANY = "公司化养殖"


class WaterQualityGrade(str, Enum):
    """水质等级"""
    EXCELLENT = "优"
    GOOD = "良"
    FAIR = "一般"
    POOR = "差"


class CrayfishGrade(str, Enum):
    """小龙虾规格等级"""
    PREMIUM = "精品虾(≥8钱)"
    FIRST = "一级虾(6-8钱)"
    SECOND = "二级虾(4-6钱)"
    THIRD = "三级虾(≤4钱)"


class Farmer(BaseModel):
    """养殖户信息"""
    id: str = Field(..., description="养殖户ID")
    name: str = Field(..., description="养殖户姓名")
    farm_name: str = Field(..., description="养殖场名称")
    farm_type: FarmType = Field(..., description="养殖场类型")
    location: str = Field(..., description="养殖地点")
    contact: str = Field(..., description="联系方式")
    registered_at: datetime = Field(default_factory=datetime.now, description="注册时间")
    status: str = Field(default="active", description="状态")


class Pond(BaseModel):
    """养殖池信息"""
    id: str = Field(..., description="池塘ID")
    farmer_id: str = Field(..., description="所属养殖户ID")
    pond_name: str = Field(..., description="池塘名称")
    area: float = Field(..., description="面积(亩)")
    water_depth: float = Field(..., description="水深(米)")
    stocking_density: int = Field(..., description="放养密度(尾/亩)")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")


class EnvironmentData(BaseModel):
    """环境监测数据"""
    id: str = Field(..., description="数据ID")
    pond_id: str = Field(..., description="池塘ID")
    recorded_at: datetime = Field(..., description="记录时间")
    
    # 水质参数
    water_temperature: float = Field(..., description="水温(℃)", ge=0, le=40)
    dissolved_oxygen: float = Field(..., description="溶解氧(mg/L)", ge=0)
    pH: float = Field(..., description="pH值", ge=0, le=14)
    ammonia_nitrogen: float = Field(..., description="氨氮(mg/L)", ge=0)
    nitrite: float = Field(..., description="亚硝酸盐(mg/L)", ge=0)
    transparency: float = Field(..., description="透明度(cm)", ge=0)
    
    # 气象参数
    air_temperature: Optional[float] = Field(None, description="气温(℃)")
    humidity: Optional[float] = Field(None, description="湿度(%)")
    rainfall: Optional[float] = Field(None, description="降雨量(mm)")


class HarvestRecord(BaseModel):
    """收获记录"""
    id: str = Field(..., description="记录ID")
    pond_id: str = Field(..., description="池塘ID")
    harvest_date: datetime = Field(..., description="收获日期")
    crayfish_grade: CrayfishGrade = Field(..., description="小龙虾规格")
    quantity: float = Field(..., description="产量(斤)")
    average_weight: float = Field(..., description="平均重量(克)")
    survival_rate: float = Field(..., description="成活率(%)", ge=0, le=100)
    selling_price: float = Field(..., description="销售单价(元/斤)")
    total_revenue: float = Field(..., description="总收入(元)")


class FeedRecord(BaseModel):
    """饲料投喂记录"""
    id: str = Field(..., description="记录ID")
    pond_id: str = Field(..., description="池塘ID")
    feed_date: datetime = Field(..., description="投喂日期")
    feed_type: str = Field(..., description="饲料类型")
    feed_amount: float = Field(..., description="投喂量(斤)")
    feed_cost: float = Field(..., description="饲料费用(元)")


class CostRecord(BaseModel):
    """成本记录"""
    id: str = Field(..., description="记录ID")
    farmer_id: str = Field(..., description="养殖户ID")
    record_date: datetime = Field(..., description="记录日期")
    seed_cost: float = Field(default=0, description="苗种费用(元)")
    feed_cost: float = Field(default=0, description="饲料费用(元)")
    medicine_cost: float = Field(default=0, description="药品费用(元)")
    equipment_cost: float = Field(default=0, description="设备费用(元)")
    labor_cost: float = Field(default=0, description="人工费用(元)")
    other_cost: float = Field(default=0, description="其他费用(元)")
    total_cost: float = Field(default=0, description="总成本(元)")


class RaceParticipant(BaseModel):
    """赛马参赛者"""
    farmer_id: str = Field(..., description="养殖户ID")
    pond_ids: List[str] = Field(..., description="参与比赛的池塘IDs")
    registration_date: datetime = Field(default_factory=datetime.now, description="报名时间")
    status: str = Field(default="registered", description="参赛状态")


class RaceConfig(BaseModel):
    """赛马配置"""
    id: str = Field(..., description="比赛ID")
    name: str = Field(..., description="比赛名称")
    start_date: datetime = Field(..., description="开始日期")
    end_date: datetime = Field(..., description="结束日期")
    evaluation_period: int = Field(..., description="评估周期(天)")
    
    # 评判权重
    yield_weight: float = Field(default=0.4, description="产量权重", ge=0, le=1)
    quality_weight: float = Field(default=0.3, description="品质权重", ge=0, le=1)
    cost_weight: float = Field(default=0.3, description="成本权重", ge=0, le=1)
    
    # 奖项设置
    prize_count: int = Field(default=3, description="奖项数量")
    prize_names: List[str] = Field(default=["冠军", "亚军", "季军"], description="奖项名称")


class RaceResult(BaseModel):
    """比赛结果"""
    race_id: str = Field(..., description="比赛ID")
    farmer_id: str = Field(..., description="养殖户ID")
    
    # 评估指标
    total_yield: float = Field(..., description="总产量(斤)")
    avg_crayfish_weight: float = Field(..., description="平均虾重(克)")
    premium_rate: float = Field(..., description="精品虾比例(%)")
    survival_rate: float = Field(..., description="平均成活率(%)")
    total_cost: float = Field(..., description="总成本(元)")
    total_revenue: float = Field(..., description="总收入(元)")
    profit: float = Field(..., description="净利润(元)")
    
    # 评分
    yield_score: float = Field(..., description="产量得分")
    quality_score: float = Field(..., description="品质得分")
    cost_score: float = Field(..., description="成本控制得分")
    total_score: float = Field(..., description="总得分")
    
    ranking: int = Field(..., description="排名")
    prize: Optional[str] = Field(None, description="获得奖项")
    evaluated_at: datetime = Field(default_factory=datetime.now, description="评估时间")