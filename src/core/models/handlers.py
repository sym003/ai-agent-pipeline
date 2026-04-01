"""
Handler - Stage 的执行逻辑
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class HandlerType(str, Enum):
    """处理器类型"""
    AI_AUTO = "AI_AUTO"               # AI 自动处理
    HUMAN_ONLY = "HUMAN_ONLY"         # 纯人工处理
    AI_DRAFT_HUMAN_APPROVE = "AI_DRAFT_HUMAN_APPROVE"  # AI 出草稿，人工确认


class LLMConfig(BaseModel):
    """LLM 配置"""
    provider: str = Field(default="dashscope", description="LLM 提供商")
    model: str = Field(default="qwen-turbo", description="模型名称")
    temperature: float = Field(default=0.7, ge=0, le=2, description="温度参数")
    max_tokens: int = Field(default=2000, ge=1, description="最大 token 数")


class HandlerConfig(BaseModel):
    """处理器配置"""
    type: HandlerType = Field(..., description="处理器类型")
    agent: Optional[str] = Field(None, description="Agent ID（用于 AI_AUTO 和 AI_DRAFT_HUMAN_APPROVE）")
    approver: Optional[str] = Field(None, description="审批人 ID（用于 HUMAN_ONLY 和 AI_DRAFT_HUMAN_APPROVE）")
    tools: list[str] = Field(default_factory=list, description="使用的工具列表")
    prompt_template: Optional[str] = Field(None, description="LLM Prompt 模板")
    llm_config: Optional[LLMConfig] = Field(None, description="LLM 配置")

    class Config:
        use_enum_values = True


class AIHandler:
    """
    AI 自动处理器

    适用于：情报提取、格式转换、数据清洗等纯 AI 处理场景
    """

    def __init__(
        self,
        agent_id: str,
        tools: list[str],
        llm_config: LLMConfig = None,
        prompt_template: str = None
    ):
        self.agent_id = agent_id
        self.tools = tools
        self.llm_config = llm_config or LLMConfig()
        self.prompt_template = prompt_template

    async def execute(self, input_artifact: "Artifact", context: dict = None) -> "Artifact":
        """
        执行 AI 自动处理

        Args:
            input_artifact: 输入产出物
            context: 额外上下文

        Returns:
            输出的产出物
        """
        # TODO: 实现 Agent Loop
        raise NotImplementedError("AI Handler execution not implemented yet")


class HumanHandler:
    """
    纯人工处理器

    适用于：需求评审、架构审批、UAT 验收等必须人工处理场景
    """

    def __init__(self, approver_id: str):
        self.approver_id = approver_id

    async def create_task(self, input_artifact: "Artifact", notification: dict = None) -> dict:
        """
        创建人工任务并通知审批人

        Args:
            input_artifact: 输入产出物
            notification: 通知配置

        Returns:
            任务信息
        """
        # TODO: 实现人工任务创建和通知
        raise NotImplementedError("Human Handler task creation not implemented yet")

    async def get_result(self, task_id: str) -> "Artifact":
        """
        获取人工处理结果

        Args:
            task_id: 任务 ID

        Returns:
            审批后的产出物
        """
        # TODO: 实现结果获取
        raise NotImplementedError("Human Handler result retrieval not implemented yet")


class HybridHandler:
    """
    AI+人工协作处理器

    适用于：AI 出草稿，人工确认/修改的场景

    流程:
    1. AI 根据输入生成草稿
    2. 通知人工审批
    3. 人工确认/修改后完成
    """

    def __init__(
        self,
        agent_id: str,
        approver_id: str,
        tools: list[str] = None,
        llm_config: LLMConfig = None,
        prompt_template: str = None
    ):
        self.agent_id = agent_id
        self.approver_id = approver_id
        self.tools = tools or []
        self.llm_config = llm_config or LLMConfig()
        self.prompt_template = prompt_template

    async def create_draft(self, input_artifact: "Artifact") -> "Artifact":
        """
        AI 生成草稿

        Args:
            input_artifact: 输入产出物

        Returns:
            AI 生成的草稿产出物
        """
        # TODO: 实现 AI 草稿生成
        raise NotImplementedError("Hybrid Handler draft creation not implemented yet")

    async def create_approval_task(self, draft_artifact: "Artifact", notification: dict = None) -> dict:
        """
        创建人工审批任务

        Args:
            draft_artifact: AI 生成的草稿
            notification: 通知配置

        Returns:
            审批任务信息
        """
        # TODO: 实现人工审批任务创建
        raise NotImplementedError("Hybrid Handler approval task not implemented yet")

    async def finalize(self, task_id: str, approved_artifact: "Artifact") -> "Artifact":
        """
        完成处理（人工审批通过后）

        Args:
            task_id: 审批任务 ID
            approved_artifact: 审批后的产出物

        Returns:
            最终产出物
        """
        # TODO: 实现最终产出物生成
        raise NotImplementedError("Hybrid Handler finalization not implemented yet")
