"""
Pipeline 配置加载器

从 JSON 文件或字典加载 Pipeline 配置
"""

import json
from pathlib import Path
from typing import Union

from ..models import (
    Pipeline,
    PipelineMeta,
    Stage,
    ArtifactRef,
    HandlerConfig,
    LLMConfig,
    RetryConfig,
)


class PipelineLoader:
    """Pipeline 配置加载器"""

    @classmethod
    def load(cls, data: Union[dict, str, Path]) -> Pipeline:
        """
        加载 Pipeline 配置

        Args:
            data: JSON 字典、JSON 字符串或文件路径

        Returns:
            Pipeline 对象

        Raises:
            ValueError: 配置格式错误
        """
        if isinstance(data, (str, Path)):
            if Path(data).exists():
                with open(data, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                # 尝试作为 JSON 字符串解析
                data = json.loads(data)

        if not isinstance(data, dict):
            raise ValueError("Pipeline data must be a dict")

        # 解析 meta
        meta_data = data.get("pipeline", {})
        meta = PipelineMeta(
            id=meta_data["id"],
            name=meta_data["name"],
            description=meta_data.get("description"),
            version=meta_data["version"],
            enabled=meta_data.get("enabled", True)
        )

        # 解析 stages
        stages = []
        for stage_data in data.get("stages", []):
            stage = cls._parse_stage(stage_data)
            stages.append(stage)

        # 按 order 排序
        stages.sort(key=lambda s: s.order)

        return Pipeline(meta=meta, stages=stages)

    @classmethod
    def _parse_stage(cls, data: dict) -> Stage:
        """解析 Stage 配置"""
        # 解析 input/output
        input_artifact = ArtifactRef(
            type=data["input"]["type"],
            required=data["input"].get("required", True)
        )
        output_artifact = ArtifactRef(
            type=data["output"]["type"],
            required=data["output"].get("required", True)
        )

        # 解析 handler
        handler_data = data.get("handler", {})
        handler = cls._parse_handler(handler_data)

        # 解析 retry
        retry = None
        if "retry" in data:
            retry = RetryConfig(
                max_attempts=data["retry"].get("max_attempts", 3),
                backoff_multiplier=data["retry"].get("backoff_multiplier", 2),
                initial_delay=data["retry"].get("initial_delay", 1)
            )

        return Stage(
            id=data["id"],
            name=data["name"],
            description=data.get("description"),
            order=data["order"],
            input=input_artifact,
            output=output_artifact,
            handler=handler,
            retry=retry,
            timeout=data.get("timeout", 3600),
            on_error=data.get("on_error", "fail")
        )

    @classmethod
    def _parse_handler(cls, data: dict) -> HandlerConfig:
        """解析 Handler 配置"""
        # 解析 LLM config
        llm_config = None
        if "llm_config" in data:
            llm_data = data["llm_config"]
            llm_config = LLMConfig(
                provider=llm_data.get("provider", "dashscope"),
                model=llm_data.get("model", "qwen-turbo"),
                temperature=llm_data.get("temperature", 0.7),
                max_tokens=llm_data.get("max_tokens", 2000)
            )

        return HandlerConfig(
            type=data["type"],
            agent=data.get("agent"),
            approver=data.get("approver"),
            tools=data.get("tools", []),
            prompt_template=data.get("prompt_template"),
            llm_config=llm_config
        )


def load_pipeline_from_file(file_path: Union[str, Path]) -> Pipeline:
    """从文件加载 Pipeline 配置"""
    return PipelineLoader.load(file_path)


def load_pipeline_from_dict(data: dict) -> Pipeline:
    """从字典加载 Pipeline 配置"""
    return PipelineLoader.load(data)
