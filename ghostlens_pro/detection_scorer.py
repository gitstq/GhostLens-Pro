"""
GhostLens-Pro 反检测评分引擎

综合评分算法，基于所有指纹维度计算总体反检测评分。
支持评分等级划分、风险分类、详细报告生成和 JSON/HTML 报告导出。
"""

import json
import time
from typing import Any, Dict, List, Optional, Tuple


class DetectionScorer:
    """反检测评分引擎，基于指纹数据计算综合反检测评分。"""

    # 评分等级定义
    GRADE_THRESHOLDS: List[Tuple[str, str, int]] = [
        ("A+", "优秀", 95),
        ("A", "良好", 85),
        ("B", "中等", 70),
        ("C", "较差", 50),
        ("D", "危险", 0),
    ]

    # 风险分类及其关联的指纹维度
    RISK_CATEGORIES: Dict[str, List[str]] = {
        "automation_detection": [
            "webdriver", "debugger", "console", "performance",
            "client_rects", "iframe",
        ],
        "fingerprint_uniqueness": [
            "canvas", "webgl", "audio", "fonts", "math_constants",
            "error_messages", "css_features",
        ],
        "behavioral_analysis": [
            "touch", "battery", "connection", "storage",
            "media_devices", "speech", "permissions",
        ],
        "network_characteristics": [
            "webrtc", "cookies", "dnt", "features",
        ],
    }

    # 各风险分类的权重
    CATEGORY_WEIGHTS: Dict[str, float] = {
        "automation_detection": 0.35,
        "fingerprint_uniqueness": 0.25,
        "behavioral_analysis": 0.20,
        "network_characteristics": 0.20,
    }

    # 改进建议模板
    IMPROVEMENT_SUGGESTIONS: Dict[str, str] = {
        "user_agent": "使用真实且常见的 User-Agent 字符串，避免使用默认或过时的 UA。",
        "screen": "使用常见的屏幕分辨率，确保与设备类型匹配。",
        "timezone": "确保时区与 IP 地址地理位置一致。",
        "language": "确保语言设置与 User-Agent 中的区域信息匹配。",
        "platform": "确保平台信息与 User-Agent 中的操作系统信息一致。",
        "canvas": "添加轻微噪声到 Canvas 渲染结果，避免指纹唯一性过高。",
        "webgl": "使用常见 GPU 的渲染器信息，避免暴露真实硬件。",
        "fonts": "确保字体列表与声称的操作系统匹配。",
        "audio": "添加音频处理噪声以降低音频指纹唯一性。",
        "hardware": "确保硬件并发数和设备内存与声称的设备匹配。",
        "touch": "桌面设备不应报告触摸支持，移动设备应报告合理的触摸点数。",
        "battery": "确保电池状态合理，桌面设备通常不暴露电池 API。",
        "connection": "使用常见的网络连接类型，确保与设备类型匹配。",
        "cookies": "确保 Cookie 已启用，禁用 Cookie 会增加指纹唯一性。",
        "dnt": "使用常见的 DNT 设置，避免使用异常值。",
        "pdf_viewer": "确保 PDF 查看器与浏览器类型匹配。",
        "plugins": "确保插件列表与浏览器类型匹配，现代浏览器通常只有内置插件。",
        "storage": "确保存储配额与设备类型匹配。",
        "media_devices": "确保媒体设备列表合理，避免暴露过多设备信息。",
        "speech": "确保语音合成声音列表与操作系统匹配。",
        "client_rects": "确保 ClientRects 精度与浏览器类型匹配。",
        "iframe": "确保 iframe 行为与正常浏览器一致。",
        "performance": "确保 Performance API 精度与浏览器类型匹配。",
        "console": "确保 Console API 行为与正常浏览器一致。",
        "debugger": "确保没有活动的调试器检测。",
        "webdriver": "确保没有 WebDriver 相关属性被检测到。",
        "webrtc": "禁用 WebRTC 或确保不泄露本地 IP 地址。",
        "permissions": "确保权限状态合理，与用户行为一致。",
        "css_features": "确保 CSS 特性支持与浏览器版本匹配。",
        "math_constants": "确保 Math 常量精度与浏览器引擎一致。",
        "error_messages": "确保错误消息格式与浏览器引擎一致。",
        "features": "确保特性检测与浏览器类型和版本匹配。",
    }

    def __init__(self) -> None:
        """初始化反检测评分引擎。"""
        self._scores: Dict[str, int] = {}
        self._fingerprint: Dict[str, Any] = {}
        self._report: Dict[str, Any] = {}

    def score(self, fingerprint_data: Dict[str, Any]) -> Dict[str, Any]:
        """对指纹数据进行综合评分。

        Args:
            fingerprint_data: 包含 fingerprint 和 scores 的字典，
                              来自 FingerprintCollector.collect_all()。

        Returns:
            包含综合评分、等级、风险分类和详细报告的字典。
        """
        self._fingerprint = fingerprint_data.get("fingerprint", {})
        self._scores = fingerprint_data.get("scores", {})

        # 计算各风险分类得分
        category_scores = self._calculate_category_scores()

        # 计算加权总分
        overall_score = self._calculate_overall_score(category_scores)

        # 确定评分等级
        grade, grade_desc = self._get_grade(overall_score)

        # 生成维度详情
        dimension_details = self._generate_dimension_details()

        # 生成改进建议
        suggestions = self._generate_suggestions()

        self._report = {
            "overall_score": overall_score,
            "grade": grade,
            "grade_description": grade_desc,
            "category_scores": category_scores,
            "dimension_scores": dict(self._scores),
            "dimension_details": dimension_details,
            "suggestions": suggestions,
            "timestamp": time.time(),
            "version": "1.0.0",
        }

        return self._report

    def _calculate_category_scores(self) -> Dict[str, Dict[str, Any]]:
        """计算各风险分类的得分。

        Returns:
            各风险分类的得分字典。
        """
        category_scores: Dict[str, Dict[str, Any]] = {}

        for category, dimensions in self.RISK_CATEGORIES.items():
            cat_scores = []
            for dim in dimensions:
                if dim in self._scores:
                    cat_scores.append(self._scores[dim])

            if cat_scores:
                avg_score = sum(cat_scores) / len(cat_scores)
                max_score = max(cat_scores)
                min_score = min(cat_scores)
            else:
                avg_score = 0
                max_score = 0
                min_score = 0

            # 反检测分数 = 100 - 风险分数
            anti_detect_score = round(100 - avg_score, 1)

            category_scores[category] = {
                "risk_score": round(avg_score, 1),
                "anti_detection_score": anti_detect_score,
                "max_risk": max_score,
                "min_risk": min_score,
                "dimensions_count": len(cat_scores),
                "weight": self.CATEGORY_WEIGHTS.get(category, 0.25),
            }

        return category_scores

    def _calculate_overall_score(self, category_scores: Dict[str, Dict[str, Any]]) -> int:
        """计算加权总分。

        Args:
            category_scores: 各风险分类的得分。

        Returns:
            综合反检测评分（0-100）。
        """
        total_weight = 0
        weighted_score = 0

        for category, data in category_scores.items():
            weight = data.get("weight", 0.25)
            anti_score = data.get("anti_detection_score", 0)
            weighted_score += anti_score * weight
            total_weight += weight

        if total_weight > 0:
            overall = round(weighted_score / total_weight)
        else:
            overall = 0

        return max(0, min(100, overall))

    def _get_grade(self, score: int) -> Tuple[str, str]:
        """根据分数确定评分等级。

        Args:
            score: 综合评分（0-100）。

        Returns:
            (等级, 描述) 元组。
        """
        for grade, desc, threshold in self.GRADE_THRESHOLDS:
            if score >= threshold:
                return grade, desc
        return "D", "危险"

    def _generate_dimension_details(self) -> List[Dict[str, Any]]:
        """生成各维度的详细评分信息。

        Returns:
            各维度详情列表。
        """
        details = []
        for dim, score in self._scores.items():
            risk_level = self._get_risk_level(score)
            details.append({
                "dimension": dim,
                "risk_score": score,
                "anti_detection_score": 100 - score,
                "risk_level": risk_level,
                "has_suggestion": dim in self.IMPROVEMENT_SUGGESTIONS,
            })
        return sorted(details, key=lambda x: x["risk_score"], reverse=True)

    def _get_risk_level(self, score: int) -> str:
        """根据风险分数确定风险等级。

        Args:
            score: 风险分数（0-100）。

        Returns:
            风险等级字符串。
        """
        if score <= 10:
            return "low"
        elif score <= 30:
            return "medium"
        elif score <= 60:
            return "high"
        else:
            return "critical"

    def _generate_suggestions(self) -> List[Dict[str, Any]]:
        """生成改进建议。

        Returns:
            改进建议列表，按风险分数降序排列。
        """
        suggestions = []
        for dim, score in sorted(self._scores.items(), key=lambda x: x[1], reverse=True):
            if score > 20 and dim in self.IMPROVEMENT_SUGGESTIONS:
                suggestions.append({
                    "dimension": dim,
                    "risk_score": score,
                    "suggestion": self.IMPROVEMENT_SUGGESTIONS[dim],
                    "priority": "high" if score > 50 else "medium" if score > 30 else "low",
                })
        return suggestions

    def get_report(self) -> Dict[str, Any]:
        """获取评分报告。

        Returns:
            完整的评分报告字典。
        """
        return self._report

    def to_json(self) -> str:
        """将评分报告导出为 JSON 字符串。

        Returns:
            JSON 格式的评分报告。
        """
        return json.dumps(self._report, indent=2, ensure_ascii=False)

    def to_html(self) -> str:
        """将评分报告导出为 HTML 字符串。

        Returns:
            HTML 格式的评分报告。
        """
        if not self._report:
            return "<html><body><p>No report data available.</p></body></html>"

        score = self._report.get("overall_score", 0)
        grade = self._report.get("grade", "N/A")
        grade_desc = self._report.get("grade_description", "N/A")

        # 确定颜色
        if score >= 95:
            color = "#28a745"
        elif score >= 85:
            color = "#5cb85c"
        elif score >= 70:
            color = "#f0ad4e"
        elif score >= 50:
            color = "#fd7e14"
        else:
            color = "#dc3545"

        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='zh-CN'>",
            "<head>",
            "<meta charset='UTF-8'>",
            "<title>GhostLens-Pro 反检测评分报告</title>",
            "<style>",
            "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 20px; background: #f5f5f5; }",
            ".container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }",
            "h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }",
            ".score-circle { width: 150px; height: 150px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: bold; color: white; margin: 20px auto; }",
            ".grade { text-align: center; font-size: 24px; margin: 10px 0; }",
            ".category { margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #007bff; }",
            ".category h3 { margin-top: 0; }",
            ".dimension { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; }",
            ".risk-low { color: #28a745; }",
            ".risk-medium { color: #f0ad4e; }",
            ".risk-high { color: #fd7e14; }",
            ".risk-critical { color: #dc3545; }",
            ".suggestion { background: #fff3cd; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 3px solid #ffc107; }",
            ".priority-high { font-weight: bold; color: #dc3545; }",
            ".priority-medium { color: #fd7e14; }",
            ".priority-low { color: #28a745; }",
            ".bar { height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; }",
            ".bar-fill { height: 100%; border-radius: 10px; transition: width 0.3s; }",
            ".timestamp { color: #6c757d; font-size: 12px; text-align: center; margin-top: 20px; }",
            "</style>",
            "</head>",
            "<body>",
            "<div class='container'>",
            "<h1>GhostLens-Pro 反检测评分报告</h1>",
            f"<div class='score-circle' style='background: {color};'>{score}</div>",
            f"<div class='grade'>等级: {grade} ({grade_desc})</div>",
        ]

        # 风险分类部分
        html_parts.append("<h2>风险分类分析</h2>")
        category_names = {
            "automation_detection": "自动化检测风险",
            "fingerprint_uniqueness": "指纹唯一性风险",
            "behavioral_analysis": "行为分析风险",
            "network_characteristics": "网络特征风险",
        }
        for cat_key, cat_data in self._report.get("category_scores", {}).items():
            cat_name = category_names.get(cat_key, cat_key)
            anti_score = cat_data.get("anti_detection_score", 0)
            bar_color = color if anti_score == score else "#6c757d"
            html_parts.append(
                f"<div class='category'>"
                f"<h3>{cat_name}</h3>"
                f"<p>反检测评分: {anti_score}/100 (权重: {cat_data.get('weight', 0) * 100:.0f}%)</p>"
                f"<div class='bar'><div class='bar-fill' style='width: {anti_score}%; background: {bar_color};'></div></div>"
                f"</div>"
            )

        # 维度详情
        html_parts.append("<h2>各维度评分详情</h2>")
        for dim in self._report.get("dimension_details", []):
            risk_class = f"risk-{dim['risk_level']}"
            html_parts.append(
                f"<div class='dimension'>"
                f"<span>{dim['dimension']}</span>"
                f"<span class='{risk_class}'>风险: {dim['risk_score']} | 反检测: {dim['anti_detection_score']}</span>"
                f"</div>"
            )

        # 改进建议
        suggestions = self._report.get("suggestions", [])
        if suggestions:
            html_parts.append("<h2>改进建议</h2>")
            for sug in suggestions:
                priority_class = f"priority-{sug['priority']}"
                html_parts.append(
                    f"<div class='suggestion'>"
                    f"<span class='{priority_class}'>[{sug['priority'].upper()}] {sug['dimension']}</span>"
                    f"<p>{sug['suggestion']}</p>"
                    f"</div>"
                )

        # 时间戳
        ts = self._report.get("timestamp", 0)
        html_parts.append(f"<div class='timestamp'>报告生成时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))}</div>")
        html_parts.append("</div></body></html>")

        return "\n".join(html_parts)

    def summary_text(self) -> str:
        """生成文本格式的评分摘要。

        Returns:
            文本格式的评分摘要。
        """
        if not self._report:
            return "No report data available."

        score = self._report.get("overall_score", 0)
        grade = self._report.get("grade", "N/A")
        grade_desc = self._report.get("grade_description", "N/A")

        lines = [
            "=" * 60,
            "  GhostLens-Pro 反检测评分报告",
            "=" * 60,
            f"",
            f"  综合评分: {score}/100",
            f"  评分等级: {grade} ({grade_desc})",
            f"",
            "-" * 60,
            "  风险分类:",
        ]

        category_names = {
            "automation_detection": "自动化检测风险",
            "fingerprint_uniqueness": "指纹唯一性风险",
            "behavioral_analysis": "行为分析风险",
            "network_characteristics": "网络特征风险",
        }
        for cat_key, cat_data in self._report.get("category_scores", {}).items():
            cat_name = category_names.get(cat_key, cat_key)
            anti_score = cat_data.get("anti_detection_score", 0)
            lines.append(f"    {cat_name}: {anti_score}/100")

        lines.append("")
        lines.append("-" * 60)
        lines.append("  高风险维度 (风险分数 > 30):")
        high_risk = [d for d in self._report.get("dimension_details", []) if d["risk_score"] > 30]
        if high_risk:
            for dim in high_risk:
                lines.append(f"    - {dim['dimension']}: 风险 {dim['risk_score']}, 反检测 {dim['anti_detection_score']}")
        else:
            lines.append("    无高风险维度")

        suggestions = self._report.get("suggestions", [])
        if suggestions:
            lines.append("")
            lines.append("-" * 60)
            lines.append("  改进建议:")
            for sug in suggestions[:5]:
                lines.append(f"    [{sug['priority'].upper()}] {sug['dimension']}: {sug['suggestion']}")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)
