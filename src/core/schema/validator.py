"""
Pipeline 配置验证器

验证 Pipeline 配置是否符合 Schema 定义
"""

import json
from typing import Tuple, List, Optional
from pathlib import Path

try:
    from jsonschema import Draft7Validator, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

from ..models import Pipeline


class PipelineValidationError(Exception):
    """Pipeline 验证错误"""
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__(f"Pipeline validation failed: {', '.join(errors)}")


class PipelineValidator:
    """Pipeline 配置验证器"""

    def __init__(self, schema_path: Optional[str] = None):
        """
        初始化验证器

        Args:
            schema_path: JSON Schema 文件路径，默认使用内置 Schema
        """
        self.schema = self._load_schema(schema_path)

    def _load_schema(self, schema_path: Optional[str] = None) -> dict:
        """加载 JSON Schema"""
        if schema_path and Path(schema_path).exists():
            with open(schema_path, "r", encoding="utf-8") as f:
                return json.load(f)

        # 使用内置 Schema
        schema_file = Path(__file__).parent / "pipeline_schema.json"
        if schema_file.exists():
            with open(schema_file, "r", encoding="utf-8") as f:
                return json.load(f)

        return {}

    def validate(self, pipeline: Pipeline) -> Tuple[bool, List[str]]:
        """
        验证 Pipeline 配置

        Args:
            pipeline: Pipeline 对象

        Returns:
            (是否通过, 错误列表)
        """
        errors = []

        # 1. JSON Schema 验证（如果可用）
        if HAS_JSONSCHEMA and self.schema:
            try:
                pipeline_dict = self._pipeline_to_dict(pipeline)
                Draft7Validator(self.schema).validate(pipeline_dict)
            except ValidationError as e:
                errors.append(f"Schema validation error: {e.message}")
            except Exception as e:
                errors.append(f"Schema validation error: {str(e)}")

        # 2. 业务逻辑验证
        business_errors = pipeline.validate()
        errors.extend(business_errors)

        # 3. 检查 Artifact 类型引用
        artifact_type_ids = set()
        for stage in pipeline.stages:
            artifact_type_ids.add(stage.input.type)
            artifact_type_ids.add(stage.output.type)

        # 如果配置了 artifact_types，检查是否所有引用都有定义
        # （这里简化处理，实际可以从配置中读取 artifact_types）

        return (len(errors) == 0, errors)

    def _pipeline_to_dict(self, pipeline: Pipeline) -> dict:
        """将 Pipeline 对象转换为字典"""
        return {
            "pipeline": {
                "id": pipeline.meta.id,
                "name": pipeline.meta.name,
                "description": pipeline.meta.description,
                "version": pipeline.meta.version,
                "enabled": pipeline.meta.enabled
            },
            "stages": [
                {
                    "id": s.id,
                    "name": s.name,
                    "description": s.description,
                    "order": s.order,
                    "input": {
                        "type": s.input.type,
                        "required": s.input.required
                    },
                    "output": {
                        "type": s.output.type,
                        "required": s.output.required
                    },
                    "handler": {
                        "type": s.handler.type.value if hasattr(s.handler.type, 'value') else s.handler.type,
                        "agent": s.handler.agent,
                        "approver": s.handler.approver,
                        "tools": s.handler.tools,
                        "prompt_template": s.handler.prompt_template,
                        "llm_config": s.handler.llm_config.model_dump() if s.handler.llm_config else None
                    },
                    "retry": s.retry.model_dump() if s.retry else None,
                    "timeout": s.timeout,
                    "on_error": s.on_error
                }
                for s in pipeline.stages
            ]
        }


def validate_pipeline(pipeline: Pipeline, schema_path: Optional[str] = None) -> Tuple[bool, List[str]]:
    """
    验证 Pipeline 配置

    Args:
        pipeline: Pipeline 对象
        schema_path: 可选的 JSON Schema 路径

    Returns:
        (是否通过, 错误列表)
    """
    validator = PipelineValidator(schema_path)
    return validator.validate(pipeline)
