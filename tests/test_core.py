"""
GhostLens-Pro 核心功能单元测试

覆盖指纹采集、评分、配置生成、一致性校验和指纹对比等核心模块。
"""

import json
import os
import sys
import tempfile
import unittest

# 确保可以导入包
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ghostlens_pro.fingerprint_collector import FingerprintCollector
from ghostlens_pro.detection_scorer import DetectionScorer
from ghostlens_pro.profile_generator import ProfileGenerator
from ghostlens_pro.consistency_checker import ConsistencyChecker
from ghostlens_pro.fingerprint_comparator import FingerprintComparator
from ghostlens_pro.cli import build_parser, main


class TestFingerprintCollector(unittest.TestCase):
    """指纹采集引擎测试。"""

    def test_collector_init_default(self) -> None:
        """测试默认初始化。"""
        collector = FingerprintCollector()
        self.assertIsNotNone(collector)

    def test_collector_init_with_seed(self) -> None:
        """测试带种子的初始化。"""
        collector = FingerprintCollector(seed=42)
        self.assertIsNotNone(collector)

    def test_collect_all_windows_chrome(self) -> None:
        """测试采集 Windows Chrome 指纹。"""
        collector = FingerprintCollector(seed=42)
        result = collector.collect_all(os_type="windows", browser="chrome", device_type="desktop")
        self.assertIn("fingerprint", result)
        self.assertIn("scores", result)
        self.assertIn("metadata", result)
        self.assertGreater(len(result["fingerprint"]), 20)

    def test_collect_all_macos_safari(self) -> None:
        """测试采集 macOS Safari 指纹。"""
        collector = FingerprintCollector(seed=42)
        result = collector.collect_all(os_type="macos", browser="safari", device_type="desktop")
        self.assertIn("fingerprint", result)
        fp = result["fingerprint"]
        self.assertIn("user_agent", fp)
        self.assertIn("screen", fp)
        self.assertIn("canvas", fp)

    def test_collect_all_mobile(self) -> None:
        """测试采集移动设备指纹。"""
        collector = FingerprintCollector(seed=42)
        result = collector.collect_all(os_type="android", browser="chrome", device_type="mobile")
        fp = result["fingerprint"]
        self.assertTrue(fp["touch"]["supported"])
        self.assertGreater(fp["touch"]["max_touch_points"], 0)

    def test_dimension_count(self) -> None:
        """测试指纹维度数量。"""
        collector = FingerprintCollector(seed=42)
        collector.collect_all()
        self.assertGreaterEqual(collector.get_dimension_count(), 25)

    def test_reproducible_with_seed(self) -> None:
        """测试相同种子产生相同结果。"""
        c1 = FingerprintCollector(seed=123)
        r1 = c1.collect_all()
        c2 = FingerprintCollector(seed=123)
        r2 = c2.collect_all()
        self.assertEqual(r1["fingerprint"]["user_agent"], r2["fingerprint"]["user_agent"])
        self.assertEqual(r1["fingerprint"]["screen"], r2["fingerprint"]["screen"])

    def test_to_json(self) -> None:
        """测试 JSON 序列化。"""
        collector = FingerprintCollector(seed=42)
        collector.collect_all()
        json_str = collector.to_json()
        data = json.loads(json_str)
        self.assertIn("fingerprint", data)
        self.assertIn("scores", data)

    def test_from_json(self) -> None:
        """测试 JSON 反序列化。"""
        collector = FingerprintCollector(seed=42)
        collector.collect_all()
        json_str = collector.to_json()
        restored = FingerprintCollector.from_json(json_str)
        self.assertEqual(collector.get_fingerprint()["user_agent"],
                         restored.get_fingerprint()["user_agent"])

    def test_all_dimensions_have_scores(self) -> None:
        """测试所有维度都有风险评分。"""
        collector = FingerprintCollector(seed=42)
        result = collector.collect_all()
        fp_keys = set(result["fingerprint"].keys())
        score_keys = set(result["scores"].keys())
        self.assertTrue(fp_keys.issubset(score_keys))


class TestDetectionScorer(unittest.TestCase):
    """反检测评分引擎测试。"""

    def setUp(self) -> None:
        """测试前准备。"""
        self.collector = FingerprintCollector(seed=42)
        self.fingerprint_data = self.collector.collect_all()
        self.scorer = DetectionScorer()

    def test_score_returns_report(self) -> None:
        """测试评分返回完整报告。"""
        report = self.scorer.score(self.fingerprint_data)
        self.assertIn("overall_score", report)
        self.assertIn("grade", report)
        self.assertIn("category_scores", report)
        self.assertIn("dimension_details", report)
        self.assertIn("suggestions", report)

    def test_score_range(self) -> None:
        """测试评分在合理范围内。"""
        report = self.scorer.score(self.fingerprint_data)
        score = report["overall_score"]
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_grade_assignment(self) -> None:
        """测试评分等级分配。"""
        report = self.scorer.score(self.fingerprint_data)
        grade = report["grade"]
        self.assertIn(grade, ["A+", "A", "B", "C", "D"])

    def test_category_scores(self) -> None:
        """测试风险分类评分。"""
        report = self.scorer.score(self.fingerprint_data)
        categories = report["category_scores"]
        self.assertIn("automation_detection", categories)
        self.assertIn("fingerprint_uniqueness", categories)
        self.assertIn("behavioral_analysis", categories)
        self.assertIn("network_characteristics", categories)

    def test_to_json(self) -> None:
        """测试 JSON 导出。"""
        self.scorer.score(self.fingerprint_data)
        json_str = self.scorer.to_json()
        data = json.loads(json_str)
        self.assertIn("overall_score", data)

    def test_to_html(self) -> None:
        """测试 HTML 导出。"""
        self.scorer.score(self.fingerprint_data)
        html = self.scorer.to_html()
        self.assertIn("<html", html)
        self.assertIn("GhostLens-Pro", html)

    def test_summary_text(self) -> None:
        """测试文本摘要。"""
        self.scorer.score(self.fingerprint_data)
        summary = self.scorer.summary_text()
        self.assertIn("GhostLens-Pro", summary)
        self.assertIn("评分", summary)


class TestProfileGenerator(unittest.TestCase):
    """指纹配置生成器测试。"""

    def test_generate_default(self) -> None:
        """测试默认配置生成。"""
        gen = ProfileGenerator(seed=42)
        profile = gen.generate()
        self.assertIn("profile", profile)
        self.assertIn("fingerprint", profile)
        self.assertIn("scores", profile)

    def test_generate_with_template(self) -> None:
        """测试使用模板生成。"""
        gen = ProfileGenerator(seed=42)
        profile = gen.generate(template_name="chrome_win10")
        self.assertEqual(profile["profile"]["browser"], "chrome")
        self.assertEqual(profile["profile"]["os_type"], "windows")

    def test_generate_invalid_template(self) -> None:
        """测试无效模板名称。"""
        gen = ProfileGenerator(seed=42)
        with self.assertRaises(ValueError):
            gen.generate(template_name="nonexistent_template")

    def test_list_templates(self) -> None:
        """测试列出模板。"""
        gen = ProfileGenerator()
        templates = gen.list_templates()
        self.assertGreater(len(templates), 0)
        template_ids = [t["id"] for t in templates]
        self.assertIn("chrome_win10", template_ids)
        self.assertIn("safari_macos", template_ids)

    def test_export_import_json(self) -> None:
        """测试 JSON 导出导入。"""
        gen = ProfileGenerator(seed=42)
        profile = gen.generate(template_name="chrome_win10")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            filepath = f.name

        try:
            gen.export_json(profile, filepath)
            self.assertTrue(os.path.exists(filepath))

            imported = gen.import_json(filepath)
            self.assertEqual(profile["profile"]["browser"], imported["profile"]["browser"])
        finally:
            os.unlink(filepath)

    def test_batch_generate(self) -> None:
        """测试批量生成。"""
        gen = ProfileGenerator(seed=42)
        profiles = gen.generate_batch("chrome_win10", count=5)
        self.assertEqual(len(profiles), 5)


class TestConsistencyChecker(unittest.TestCase):
    """指纹一致性校验器测试。"""

    def setUp(self) -> None:
        """测试前准备。"""
        self.collector = FingerprintCollector(seed=42)
        self.fingerprint_data = self.collector.collect_all()
        self.checker = ConsistencyChecker()

    def test_check_returns_result(self) -> None:
        """测试校验返回结果。"""
        result = self.checker.check(self.fingerprint_data)
        self.assertIn("consistency_score", result)
        self.assertIn("grade", result)
        self.assertIn("issues", result)
        self.assertIn("checks", result)

    def test_score_range(self) -> None:
        """测试一致性评分范围。"""
        result = self.checker.check(self.fingerprint_data)
        score = result["consistency_score"]
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_check_consistent_profile(self) -> None:
        """测试一致性配置通过校验。"""
        gen = ProfileGenerator(seed=42)
        profile = gen.generate(template_name="chrome_win10")
        result = self.checker.check(profile)
        self.assertGreaterEqual(result["consistency_score"], 70)

    def test_summary_text(self) -> None:
        """测试文本摘要。"""
        self.checker.check(self.fingerprint_data)
        summary = self.checker.summary_text()
        self.assertIn("GhostLens-Pro", summary)

    def test_to_json(self) -> None:
        """测试 JSON 导出。"""
        self.checker.check(self.fingerprint_data)
        json_str = self.checker.to_json()
        data = json.loads(json_str)
        self.assertIn("consistency_score", data)


class TestFingerprintComparator(unittest.TestCase):
    """指纹对比分析器测试。"""

    def setUp(self) -> None:
        """测试前准备。"""
        self.comparator = FingerprintComparator()
        c1 = FingerprintCollector(seed=42)
        c2 = FingerprintCollector(seed=100)
        self.fp1 = c1.collect_all()
        self.fp2 = c2.collect_all()

    def test_compare_returns_result(self) -> None:
        """测试对比返回结果。"""
        result = self.comparator.compare(self.fp1, self.fp2)
        self.assertIn("overall_similarity", result)
        self.assertIn("dimension_diffs", result)
        self.assertIn("high_risk_diffs", result)

    def test_compare_similarity_range(self) -> None:
        """测试相似度范围。"""
        result = self.comparator.compare(self.fp1, self.fp2)
        similarity = result["overall_similarity"]
        self.assertGreaterEqual(similarity, 0)
        self.assertLessEqual(similarity, 100)

    def test_compare_identical(self) -> None:
        """测试相同指纹的相似度。"""
        result = self.comparator.compare(self.fp1, self.fp1)
        self.assertEqual(result["overall_similarity"], 100.0)
        self.assertEqual(result["different_count"], 0)

    def test_compare_different(self) -> None:
        """测试不同指纹的相似度。"""
        result = self.comparator.compare(self.fp1, self.fp2)
        self.assertLess(result["overall_similarity"], 100.0)
        self.assertGreater(result["different_count"], 0)

    def test_summary_text(self) -> None:
        """测试文本摘要。"""
        self.comparator.compare(self.fp1, self.fp2)
        summary = self.comparator.summary_text()
        self.assertIn("GhostLens-Pro", summary)

    def test_to_json(self) -> None:
        """测试 JSON 导出。"""
        self.comparator.compare(self.fp1, self.fp2)
        json_str = self.comparator.to_json()
        data = json.loads(json_str)
        self.assertIn("overall_similarity", data)

    def test_batch_compare(self) -> None:
        """测试批量对比。"""
        gen = ProfileGenerator(seed=42)
        profiles = gen.generate_batch("chrome_win10", count=5)
        results = self.comparator.batch_compare(profiles, base_index=0)
        self.assertEqual(len(results), 4)


class TestCLI(unittest.TestCase):
    """CLI 命令行测试。"""

    def test_parser_creation(self) -> None:
        """测试解析器创建。"""
        parser = build_parser()
        self.assertIsNotNone(parser)

    def test_version(self) -> None:
        """测试版本号。"""
        parser = build_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(["--version"])

    def test_scan_command(self) -> None:
        """测试 scan 命令。"""
        ret = main(["scan", "--quiet"])
        self.assertEqual(ret, 0)

    def test_scan_with_json(self) -> None:
        """测试 scan --json 命令。"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            filepath = f.name
        try:
            ret = main(["scan", "--json", "--output", filepath, "--quiet"])
            self.assertEqual(ret, 0)
            self.assertTrue(os.path.exists(filepath))
            with open(filepath, "r") as f:
                data = json.load(f)
            self.assertIn("fingerprint", data)
        finally:
            os.unlink(filepath)

    def test_generate_command(self) -> None:
        """测试 generate 命令。"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            filepath = f.name
        try:
            ret = main(["generate", "--template", "chrome_win10", "--output", filepath, "--quiet"])
            self.assertEqual(ret, 0)
            self.assertTrue(os.path.exists(filepath))
        finally:
            os.unlink(filepath)

    def test_list_profiles_command(self) -> None:
        """测试 list-profiles 命令。"""
        ret = main(["list-profiles", "--quiet"])
        self.assertEqual(ret, 0)

    def test_report_command(self) -> None:
        """测试 report 命令。"""
        ret = main(["report", "--quiet"])
        self.assertEqual(ret, 0)

    def test_report_html_output(self) -> None:
        """测试 report --html 命令。"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            filepath = f.name
        try:
            ret = main(["report", "--html", "--output", filepath, "--quiet"])
            self.assertEqual(ret, 0)
            self.assertTrue(os.path.exists(filepath))
            with open(filepath, "r") as f:
                content = f.read()
            self.assertIn("<html", content)
        finally:
            os.unlink(filepath)

    def test_no_command_shows_help(self) -> None:
        """测试无命令时显示帮助。"""
        ret = main([])
        self.assertEqual(ret, 0)

    def test_check_command_with_file(self) -> None:
        """测试 check 命令。"""
        # 先生成一个配置文件
        gen = ProfileGenerator(seed=42)
        profile = gen.generate(template_name="chrome_win10")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            filepath = f.name
        try:
            gen.export_json(profile, filepath)
            ret = main(["check", "--input", filepath, "--quiet"])
            self.assertEqual(ret, 0)
        finally:
            os.unlink(filepath)

    def test_compare_command(self) -> None:
        """测试 compare 命令。"""
        gen = ProfileGenerator(seed=42)
        fp1 = gen.generate(template_name="chrome_win10")
        fp2 = gen.generate(template_name="chrome_macos")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f1:
            file1 = f1.name
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f2:
            file2 = f2.name
        try:
            gen.export_json(fp1, file1)
            gen.export_json(fp2, file2)
            ret = main(["compare", "--file1", file1, "--file2", file2, "--quiet"])
            self.assertEqual(ret, 0)
        finally:
            os.unlink(file1)
            os.unlink(file2)


if __name__ == "__main__":
    unittest.main()
