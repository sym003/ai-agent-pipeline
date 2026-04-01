"""
AI Pipeline Factory - 核心引擎

核心模块:
- models: 数据模型（Pipeline, Stage, Artifact, Handler）
- schema: 配置加载和验证
"""

from .models import (
    Pipeline,
    PipelineStatus,
    Stage,
    StageStatus,
    Artifact,
    ArtifactType,
    ArtifactStatus,
    ArtifactRef,
    HandlerType,
    HandlerConfig,
    LLMConfig,
    AIHandler,
    HumanHandler,
    HybridHandler,
)

from .schema import (
    PipelineLoader,
    load_pipeline_from_file,
    load_pipeline_from_dict,
    PipelineValidator,
    validate_pipeline,
)

__version__ = "2.0.0-alpha.1"

__all__ = [
    # 版本
    "__version__",
    # 模型
    "Pipeline",
    "PipelineStatus",
    "Stage",
    "StageStatus",
    "Artifact",
    "ArtifactType",
    "ArtifactStatus",
    "ArtifactRef",
    "HandlerType",
    "HandlerConfig",
    "LLMConfig",
    "AIHandler",
    "HumanHandler",
    "HybridHandler",
    # Schema
    "PipelineLoader",
    "load_pipeline_from_file",
    "load_pipeline_from_dict",
    "PipelineValidator",
    "validate_pipeline",
]
