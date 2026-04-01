"""
Artifact - 流水线中传递的产出物
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field


class ArtifactStatus(str, Enum):
    """产出物状态"""
    DRAFT = "draft"           # 草稿
    PENDING = "pending"       # 待处理
    PROCESSING = "processing" # 处理中
    COMPLETED = "completed"   # 已完成
    FAILED = "failed"         # 失败
    CANCELLED = "cancelled"    # 已取消


class ArtifactRef(BaseModel):
    """产出物类型引用"""
    type: str = Field(..., description="产出物类型 ID")
    required: bool = Field(default=True, description="是否必需")


class ArtifactType(BaseModel):
    """产出物类型定义"""
    id: str = Field(..., description="产出物类型唯一标识")
    name: str = Field(..., description="产出物类型显示名称")
    description: Optional[str] = Field(None, description="产出物类型描述")
    json_schema: Optional[dict] = Field(None, alias="schema", description="JSON Schema 定义")
    stages: list[str] = Field(default_factory=list, description="可产出该类型的所有阶段")

    class Config:
        populate_by_name = True

    class Config:
        frozen = True


class Artifact(BaseModel):
    """流水线中传递的产出物实例"""
    id: str = Field(..., description="产出物唯一标识")
    type: str = Field(..., description="产出物类型 ID")

    # 内容
    title: Optional[str] = Field(None, description="标题")
    content: dict = Field(default_factory=dict, description="产出物内容")

    # 元数据
    status: ArtifactStatus = Field(default=ArtifactStatus.DRAFT, description="状态")
    created_by: str = Field(..., description="创建者")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")

    # 关联
    pipeline_id: Optional[str] = Field(None, description="所属 Pipeline ID")
    stage_id: Optional[str] = Field(None, description="所属 Stage ID")
    source_artifact_id: Optional[str] = Field(None, description="源产出物 ID")

    # 版本控制
    version: int = Field(default=1, description="版本号")
    parent_artifact_id: Optional[str] = Field(None, description="父产出物 ID（用于分支）")

    # 审批信息
    approver: Optional[str] = Field(None, description="审批人")
    approved_at: Optional[datetime] = Field(None, description="审批时间")
    approval_comment: Optional[str] = Field(None, description="审批意见")

    class Config:
        use_enum_values = True

    def mark_completed(self) -> "Artifact":
        """标记为完成，返回新实例"""
        return self.model_copy(update={
            "status": ArtifactStatus.COMPLETED,
            "updated_at": datetime.utcnow()
        })

    def mark_failed(self, error: str = None) -> "Artifact":
        """标记为失败"""
        return self.model_copy(update={
            "status": ArtifactStatus.FAILED,
            "updated_at": datetime.utcnow()
        })

    def approve(self, approver: str, comment: str = None) -> "Artifact":
        """审批通过"""
        return self.model_copy(update={
            "status": ArtifactStatus.COMPLETED,
            "approver": approver,
            "approved_at": datetime.utcnow(),
            "approval_comment": comment,
            "updated_at": datetime.utcnow()
        })

    def reject(self, approver: str, comment: str) -> "Artifact":
        """审批拒绝"""
        return self.model_copy(update={
            "approver": approver,
            "approved_at": datetime.utcnow(),
            "approval_comment": comment,
            "updated_at": datetime.utcnow()
        })

    def create_next_version(self, new_content: dict) -> "Artifact":
        """创建新版本"""
        return Artifact(
            id=f"{self.type}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            type=self.type,
            title=self.title,
            content=new_content,
            status=ArtifactStatus.DRAFT,
            created_by=self.created_by,
            pipeline_id=self.pipeline_id,
            source_artifact_id=self.source_artifact_id,
            version=self.version + 1,
            parent_artifact_id=self.id
        )
