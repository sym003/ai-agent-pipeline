"""
Stage - 流水线中的工位
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

from .artifact import ArtifactRef, ArtifactType, ArtifactStatus
from .handlers import HandlerType, HandlerConfig


class StageStatus(str, Enum):
    """阶段状态"""
    PENDING = "pending"       # 等待执行
    RUNNING = "running"      # 执行中
    WAITING_APPROVAL = "waiting_approval"  # 等待审批
    APPROVED = "approved"    # 已审批
    REJECTED = "rejected"     # 已拒绝
    COMPLETED = "completed"   # 已完成
    FAILED = "failed"         # 失败
    SKIPPED = "skipped"       # 跳过


class StageExecution(BaseModel):
    """阶段执行记录"""
    id: str = Field(..., description="执行记录 ID")
    stage_id: str = Field(..., description="阶段 ID")
    pipeline_execution_id: str = Field(..., description="流水线执行 ID")

    # 输入输出
    input_artifact_id: Optional[str] = Field(None, description="输入产出物 ID")
    output_artifact_id: Optional[str] = Field(None, description="输出产出物 ID")

    # 执行状态
    status: StageStatus = Field(default=StageStatus.PENDING)
    started_at: Optional[datetime] = Field(None, description="开始时间")
    completed_at: Optional[datetime] = Field(None, description="完成时间")
    error: Optional[str] = Field(None, description="错误信息")

    # AI 执行详情
    llm_calls: int = Field(default=0, description="LLM 调用次数")
    tool_calls: int = Field(default=0, description="工具调用次数")
    retry_count: int = Field(default=0, description="重试次数")

    class Config:
        use_enum_values = True


class Stage(BaseModel):
    """流水线中的工位"""
    id: str = Field(..., description="阶段唯一标识符")
    name: str = Field(..., description="阶段显示名称")
    description: Optional[str] = Field(None, description="阶段详细描述")
    order: int = Field(..., ge=1, description="执行顺序")

    # 输入输出定义
    input: ArtifactRef = Field(..., description="输入产出物类型")
    output: ArtifactRef = Field(..., description="输出产出物类型")

    # 处理器配置
    handler: HandlerConfig = Field(..., description="处理器配置")

    # 执行配置
    retry: Optional["RetryConfig"] = Field(None, description="重试配置")
    timeout: int = Field(default=3600, ge=1, description="超时时间（秒）")
    on_error: str = Field(default="fail", description="出错时的行为")

    class Config:
        frozen = True

    def validate_handler(self) -> list[str]:
        """验证 handler 配置的合法性"""
        errors = []
        handler_type = self.handler.type

        if handler_type == HandlerType.AI_AUTO:
            if not self.handler.agent:
                errors.append("AI_AUTO handler must have an agent")
            if not self.handler.tools:
                errors.append("AI_AUTO handler must have tools")

        elif handler_type == HandlerType.AI_DRAFT_HUMAN_APPROVE:
            if not self.handler.agent:
                errors.append("AI_DRAFT_HUMAN_APPROVE handler must have an agent")
            if not self.handler.approver:
                errors.append("AI_DRAFT_HUMAN_APPROVE handler must have an approver")

        elif handler_type == HandlerType.HUMAN_ONLY:
            if not self.handler.approver:
                errors.append("HUMAN_ONLY handler must have an approver")

        return errors


class RetryConfig(BaseModel):
    """重试配置"""
    max_attempts: int = Field(default=3, ge=1, description="最大重试次数")
    backoff_multiplier: float = Field(default=2.0, ge=1, description="退避倍数")
    initial_delay: int = Field(default=1, ge=1, description="初始延迟（秒）")


# 前向引用解析
Stage.model_rebuild()
