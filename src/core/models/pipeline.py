"""
Pipeline - 可配置流水线
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

from .stage import Stage


class PipelineStatus(str, Enum):
    """流水线状态"""
    DRAFT = "draft"           # 草稿
    ACTIVE = "active"        # 运行中
    PAUSED = "paused"        # 暂停
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"         # 失败
    CANCELLED = "cancelled"  # 已取消


class PipelineMeta(BaseModel):
    """流水线元信息"""
    id: str = Field(..., description="流水线唯一标识符")
    name: str = Field(..., description="流水线显示名称")
    description: Optional[str] = Field(None, description="流水线描述")
    version: str = Field(..., description="语义化版本号")
    enabled: bool = Field(default=True, description="是否启用")

    class Config:
        frozen = True


class PipelineExecution(BaseModel):
    """流水线执行记录"""
    id: str = Field(..., description="执行记录 ID")
    pipeline_id: str = Field(..., description="流水线 ID")
    pipeline_version: str = Field(..., description="流水线版本")

    # 执行状态
    status: PipelineStatus = Field(default=PipelineStatus.DRAFT)
    started_at: Optional[datetime] = Field(None, description="开始时间")
    completed_at: Optional[datetime] = Field(None, description="完成时间")
    error: Optional[str] = Field(None, description="错误信息")

    # 当前阶段
    current_stage_id: Optional[str] = Field(None, description="当前执行阶段 ID")

    # 统计
    total_stages: int = Field(0, description="总阶段数")
    completed_stages: int = Field(0, description="已完成阶段数")

    class Config:
        use_enum_values = True


class Pipeline(BaseModel):
    """流水线定义"""
    meta: PipelineMeta = Field(..., description="流水线元信息")
    stages: list[Stage] = Field(default_factory=list, description="阶段列表")

    # 元数据
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # 执行记录（运行时）
    current_execution: Optional[PipelineExecution] = Field(None, exclude=True)

    class Config:
        frozen = True

    def get_stage(self, stage_id: str) -> Optional[Stage]:
        """根据 ID 获取阶段"""
        for stage in self.stages:
            if stage.id == stage_id:
                return stage
        return None

    def get_next_stage(self, current_stage_id: str) -> Optional[Stage]:
        """获取下一个阶段"""
        for i, stage in enumerate(self.stages):
            if stage.id == current_stage_id:
                if i + 1 < len(self.stages):
                    return self.stages[i + 1]
                return None
        return None

    def validate(self) -> list[str]:
        """验证流水线配置的合法性，返回错误列表"""
        errors = []

        # 检查 stages 是否为空
        if not self.stages:
            errors.append("Pipeline must have at least one stage")
            return errors

        # 检查 stage order 是否连续
        orders = [s.order for s in self.stages]
        if sorted(orders) != list(range(1, len(orders) + 1)):
            errors.append("Stage orders must be consecutive starting from 1")

        # 检查 stage IDs 是否唯一
        stage_ids = [s.id for s in self.stages]
        if len(stage_ids) != len(set(stage_ids)):
            errors.append("Stage IDs must be unique")

        # 检查第一个 stage 的 input 是否 required=False
        if self.stages and self.stages[0].input.required:
            errors.append("First stage's input should not be required (or provide initial input)")

        # 检查每个 stage 的 handler 配置
        for stage in self.stages:
            handler_errors = stage.validate_handler()
            errors.extend([f"Stage {stage.id}: {e}" for e in handler_errors])

        # 检查相邻 stage 的输入输出是否匹配
        for i in range(len(self.stages) - 1):
            current_output = self.stages[i].output.type
            next_input = self.stages[i + 1].input.type
            if current_output != next_input:
                errors.append(
                    f"Stage {self.stages[i].id} output type '{current_output}' "
                    f"does not match Stage {self.stages[i+1].id} input type '{next_input}'"
                )

        return errors
