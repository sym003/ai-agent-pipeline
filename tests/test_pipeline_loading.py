"""
Pipeline 配置加载测试
"""

import sys
from pathlib import Path

# 添加 src 目录到 path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core import (
    load_pipeline_from_file,
    validate_pipeline,
    PipelineStatus,
    HandlerType
)


def test_load_pipeline():
    """测试加载 Pipeline 配置"""
    print("=" * 60)
    print("测试 1: 加载 Pipeline 配置")
    print("=" * 60)

    config_path = Path(__file__).parent.parent / "configs" / "pipelines" / "rd-pipeline-v1.json"

    if not config_path.exists():
        print(f"❌ 配置文件不存在: {config_path}")
        return False

    try:
        pipeline = load_pipeline_from_file(config_path)
        print(f"✅ 加载成功!")
        print(f"   Pipeline ID: {pipeline.meta.id}")
        print(f"   Pipeline Name: {pipeline.meta.name}")
        print(f"   Version: {pipeline.meta.version}")
        print(f"   Stages: {len(pipeline.stages)}")
        print()

        for stage in pipeline.stages:
            print(f"   📌 {stage.id}")
            print(f"      Name: {stage.name}")
            print(f"      Order: {stage.order}")
            print(f"      Handler: {stage.handler.type}")
            if stage.handler.agent:
                print(f"      Agent: {stage.handler.agent}")
            if stage.handler.approver:
                print(f"      Approver: {stage.handler.approver}")
            print()

        return True

    except Exception as e:
        print(f"❌ 加载失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_validate_pipeline():
    """测试 Pipeline 验证"""
    print("=" * 60)
    print("测试 2: 验证 Pipeline 配置")
    print("=" * 60)

    config_path = Path(__file__).parent.parent / "configs" / "pipelines" / "rd-pipeline-v1.json"

    try:
        pipeline = load_pipeline_from_file(config_path)
        is_valid, errors = validate_pipeline(pipeline)

        if is_valid:
            print("✅ 验证通过!")
        else:
            print(f"❌ 验证失败:")
            for error in errors:
                print(f"   - {error}")

        return is_valid

    except Exception as e:
        print(f"❌ 验证出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_stage_ordering():
    """测试 Stage 排序"""
    print("=" * 60)
    print("测试 3: Stage 顺序验证")
    print("=" * 60)

    config_path = Path(__file__).parent.parent / "configs" / "pipelines" / "rd-pipeline-v1.json"

    try:
        pipeline = load_pipeline_from_file(config_path)

        print("Stage 执行顺序:")
        for i, stage in enumerate(pipeline.stages):
            print(f"   {i + 1}. {stage.id} ({stage.name})")
            if i > 0:
                prev_output = pipeline.stages[i - 1].output.type
                curr_input = stage.input.type
                if prev_output == curr_input:
                    print(f"      ✅ 输入输出匹配: {prev_output} -> {curr_input}")
                else:
                    print(f"      ⚠️ 输入输出不匹配: {prev_output} -> {curr_input}")

        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("\n🚀 AI Pipeline Factory - 测试套件\n")

    results = []

    results.append(("加载 Pipeline", test_load_pipeline()))
    print()

    results.append(("验证 Pipeline", test_validate_pipeline()))
    print()

    results.append(("Stage 排序", test_stage_ordering()))
    print()

    print("=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {name}: {status}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("🎉 所有测试通过!")
    else:
        print("⚠️ 部分测试失败，请检查输出")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
