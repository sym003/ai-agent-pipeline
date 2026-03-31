"""小龙虾养殖赛马主模块"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from .models import *
from .agents import CrayfishRacingTeam
from .evaluator import RaceEvaluator

router = APIRouter(prefix="/crayfish-racing", tags=["小龙虾赛马"])

# 全局赛马团队实例
racing_team = CrayfishRacingTeam()


class RaceRequest(BaseModel):
    """赛马请求"""
    name: str
    start_date: datetime
    end_date: datetime
    evaluation_period: int = 30
    yield_weight: float = 0.4
    quality_weight: float = 0.3
    cost_weight: float = 0.3
    prize_count: int = 3


class RaceResponse(BaseModel):
    """赛马响应"""
    race_id: str
    status: str
    message: str


@router.post("/start-race", response_model=RaceResponse)
async def start_crayfish_race(request: RaceRequest, background_tasks: BackgroundTasks):
    """启动小龙虾赛马"""
    try:
        # 创建比赛配置
        config = RaceConfig(
            id=f"race_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            name=request.name,
            start_date=request.start_date,
            end_date=request.end_date,
            evaluation_period=request.evaluation_period,
            yield_weight=request.yield_weight,
            quality_weight=request.quality_weight,
            cost_weight=request.cost_weight,
            prize_count=request.prize_count
        )
        
        # 在后台执行赛马
        background_tasks.add_task(execute_race_async, config)
        
        return RaceResponse(
            race_id=config.id,
            status="started",
            message=f"赛马 '{request.name}' 已启动，正在后台执行..."
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动赛马失败: {str(e)}")


@router.get("/races/{race_id}")
async def get_race_status(race_id: str):
    """获取赛马状态"""
    # 这里应该查询数据库获取比赛状态
    # 暂时返回模拟数据
    return {
        "race_id": race_id,
        "status": "completed",
        "progress": 100,
        "results_available": True
    }


@router.get("/races/{race_id}/results")
async def get_race_results(race_id: str):
    """获取赛马结果"""
    # 这里应该从数据库查询实际结果
    # 暂时返回示例数据
    sample_results = [
        {
            "ranking": 1,
            "farmer_name": "张三",
            "farm_name": "清水小龙虾养殖场",
            "total_score": 92.5,
            "total_yield": 2500,
            "profit": 15000,
            "prize": "冠军"
        },
        {
            "ranking": 2,
            "farmer_name": "李四",
            "farm_name": "绿源生态农场",
            "total_score": 88.3,
            "total_yield": 2300,
            "profit": 13500,
            "prize": "亚军"
        }
    ]
    
    return {
        "race_id": race_id,
        "results": sample_results
    }


@router.get("/leaderboard/{race_id}")
async def get_leaderboard(race_id: str):
    """获取排行榜HTML"""
    # 返回排行榜网页
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>小龙虾养殖赛马排行榜 - {race_id}</title>
        <meta charset="utf-8">
        <style>
            body {{ 
                font-family: 'Microsoft YaHei', Arial, sans-serif; 
                margin: 0; 
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(45deg, #2c5aa0, #3a7bd5);
                color: white;
                text-align: center;
                padding: 30px 20px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 2.5em;
            }}
            .header p {{
                margin: 10px 0 0 0;
                opacity: 0.9;
            }}
            .content {{
                padding: 30px;
            }}
            .rank-item {{
                display: flex;
                align-items: center;
                padding: 20px;
                margin: 15px 0;
                border-radius: 10px;
                background: #f8f9fa;
                transition: transform 0.2s;
            }}
            .rank-item:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }}
            .rank-number {{
                font-size: 2em;
                font-weight: bold;
                width: 60px;
                text-align: center;
            }}
            .rank-1 .rank-number {{ color: #FFD700; }}
            .rank-2 .rank-number {{ color: #C0C0C0; }}
            .rank-3 .rank-number {{ color: #CD7F32; }}
            .farmer-info {{
                flex: 1;
            }}
            .farmer-name {{
                font-size: 1.3em;
                font-weight: bold;
                color: #333;
            }}
            .farm-name {{
                color: #666;
                margin-top: 5px;
            }}
            .score {{
                font-size: 1.8em;
                font-weight: bold;
                color: #2c5aa0;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                color: #666;
                border-top: 1px solid #eee;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🦐 小龙虾养殖赛马</h1>
                <p>排行榜 - {race_id}</p>
            </div>
            <div class="content">
                <div class="rank-item rank-1">
                    <div class="rank-number">🥇1</div>
                    <div class="farmer-info">
                        <div class="farmer-name">张三</div>
                        <div class="farm-name">清水小龙虾养殖场</div>
                    </div>
                    <div class="score">92.5分</div>
                </div>
                <div class="rank-item rank-2">
                    <div class="rank-number">🥈2</div>
                    <div class="farmer-info">
                        <div class="farmer-name">李四</div>
                        <div class="farm-name">绿源生态农场</div>
                    </div>
                    <div class="score">88.3分</div>
                </div>
                <div class="rank-item rank-3">
                    <div class="rank-number">🥉3</div>
                    <div class="farmer-info">
                        <div class="farmer-name">王五</div>
                        <div class="farm-name">富农水产基地</div>
                    </div>
                    <div class="score">85.7分</div>
                </div>
            </div>
            <div class="footer">
                <p>比赛时间: {datetime.now().strftime('%Y年%m月%d日')}</p>
                <p>由 Agent Teams Harness 驱动</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content


async def execute_race_async(config: RaceConfig):
    """异步执行赛马"""
    try:
        # 这里应该调用实际的赛马执行逻辑
        print(f"开始执行赛马: {config.name}")
        # await racing_team.execute_race(config, data_sources)
        print(f"赛马执行完成: {config.name}")
    except Exception as e:
        print(f"赛马执行失败: {e}")


# 导出路由器
__all__ = ["router"]