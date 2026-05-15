"""
GhostLens-Pro 指纹一致性校验器

检查指纹配置的内部一致性，验证各维度之间的匹配关系，
检测矛盾配置并给出修复建议。
"""

import json
import time
from typing import Any, Dict, List, Optional, Tuple


class ConsistencyChecker:
    """指纹一致性校验器，检查指纹配置的内部一致性。"""

    # UA 与平台的匹配规则
    UA_PLATFORM_PATTERNS: Dict[str, List[str]] = {
        "Win32": ["Windows", "Win64", "Win32"],
        "MacIntel": ["Macintosh", "Mac OS X"],
        "Linux x86_64": ["X11", "Linux"],
        "iPhone": ["iPhone", "CPU iPhone OS"],
        "Linux armv8l": ["Linux", "Android"],
    }

    # 操作系统与字体的匹配规则
    OS_FONT_INDICATORS: Dict[str, List[str]] = {
        "windows": ["Segoe UI", "Microsoft YaHei", "Consolas", "Malgun Gothic", "MS Gothic"],
        "macos": ["PingFang SC", "Hiragino Sans", "SF Pro", "Apple Color Emoji", "Helvetica Neue"],
        "linux": ["Ubuntu", "DejaVu Sans", "Liberation", "Noto Sans", "WenQuanYi"],
        "ios": ["PingFang SC", "Hiragino Sans", "SF Pro"],
        "android": ["Roboto", "Noto Sans", "Droid Sans"],
    }

    # 操作系统与 WebGL 渲染器的匹配规则
    OS_WEBGL_INDICATORS: Dict[str, List[str]] = {
        "windows": ["ANGLE", "Direct3D", "D3D11"],
        "macos": ["Apple", "Metal"],
        "linux": ["Mesa", "X.Org", "NVIDIA Corporation"],
    }

    # 设备类型与屏幕分辨率的合理范围
    DEVICE_SCREEN_RANGES: Dict[str, Dict[str, Tuple[int, int]]] = {
        "desktop": {
            "width": (1024, 7680),
            "height": (768, 4320),
        },
        "mobile": {
            "width": (320, 768),
            "height": (480, 2048),
        },
    }

    # 设备类型与触摸支持的匹配
    DEVICE_TOUCH_EXPECTATIONS: Dict[str, bool] = {
        "desktop": False,
        "mobile": True,
    }

    # 设备类型与硬件的合理范围
    DEVICE_HARDWARE_RANGES: Dict[str, Dict[str, Tuple[int, int]]] = {
        "desktop": {
            "concurrency": (2, 64),
            "device_memory": (2, 128),
        },
        "mobile": {
            "concurrency": (2, 12),
            "device_memory": (1, 16),
        },
    }

    # 浏览器与插件的匹配规则
    BROWSER_PLUGIN_EXPECTATIONS: Dict[str, Dict[str, Any]] = {
        "chrome": {"max_count": 5, "must_contain": ["PDF Viewer"]},
        "firefox": {"max_count": 10, "must_contain": ["PDF Viewer"]},
        "safari": {"max_count": 0, "must_contain": []},
        "edge": {"max_count": 5, "must_contain": ["PDF Viewer"]},
    }

    def __init__(self) -> None:
        """初始化一致性校验器。"""
        self._issues: List[Dict[str, Any]] = []
        self._score: int = 100
        self._checks: Dict[str, Dict[str, Any]] = {}

    def check(self, fingerprint_data: Dict[str, Any]) -> Dict[str, Any]:
        """对指纹数据进行一致性校验。

        Args:
            fingerprint_data: 包含 fingerprint 的字典。

        Returns:
            包含一致性评分、问题列表和检查结果的字典。
        """
        self._issues = []
        self._checks = {}
        self._score = 100

        fingerprint = fingerprint_data.get("fingerprint", {})
        profile = fingerprint_data.get("profile", {})
        metadata = fingerprint_data.get("metadata", {})

        os_type = profile.get("os_type") or metadata.get("os_type", "windows")
        browser = profile.get("browser") or metadata.get("browser", "chrome")
        device_type = profile.get("device_type") or metadata.get("device_type", "desktop")

        # 执行各项一致性检查
        self._check_ua_platform(fingerprint, os_type)
        self._check_screen_device(fingerprint, device_type, os_type)
        self._check_fonts_os(fingerprint, os_type)
        self._check_webgl_hardware(fingerprint, os_type)
        self._check_touch_device(fingerprint, device_type)
        self._check_hardware_device(fingerprint, device_type)
        self._check_plugins_browser(fingerprint, browser)
        self._check_storage_device(fingerprint, device_type)
        self._check_color_depth(fingerprint)
        self._check_pixel_ratio(fingerprint, os_type)
        self._check_webdriver(fingerprint)
        self._check_cookies(fingerprint)
        self._check_pdf_viewer(fingerprint, browser)
        self._check_language_consistency(fingerprint, os_type)

        # 计算一致性评分
        self._calculate_score()

        return {
            "consistency_score": self._score,
            "grade": self._get_grade(self._score),
            "issues": self._issues,
            "checks": self._checks,
            "timestamp": time.time(),
            "version": "1.0.0",
        }

    def _add_issue(self, category: str, severity: str, description: str,
                   suggestion: str, dimension: str = "") -> None:
        """添加一个一致性问题。

        Args:
            category: 问题分类。
            severity: 严重程度 (critical, warning, info)。
            description: 问题描述。
            suggestion: 修复建议。
            dimension: 相关维度。
        """
        self._issues.append({
            "category": category,
            "severity": severity,
            "description": description,
            "suggestion": suggestion,
            "dimension": dimension,
        })

    def _check_ua_platform(self, fingerprint: Dict[str, Any], os_type: str) -> None:
        """检查 User-Agent 与平台信息的匹配。

        Args:
            fingerprint: 指纹数据。
            os_type: 操作系统类型。
        """
        ua_info = fingerprint.get("user_agent", {})
        platform_info = fingerprint.get("platform", {})
        ua_value = ua_info.get("value", "")
        platform_value = platform_info.get("value", "")

        # 检查 UA 是否包含与平台匹配的关键字
        expected_patterns = self.UA_PLATFORM_PATTERNS.get(platform_value, [])
        matched = any(p in ua_value for p in expected_patterns) if expected_patterns else True

        # 检查 UA 中的操作系统是否与声称的 OS 类型匹配
        os_keywords = {
            "windows": "Windows",
            "macos": "Macintosh",
            "linux": "X11",
            "ios": "iPhone",
            "android": "Android",
        }
        expected_keyword = os_keywords.get(os_type, "")
        os_matched = expected_keyword in ua_value if expected_keyword else True

        if not matched:
            self._add_issue(
                "ua_platform", "critical",
                f"User-Agent 与平台信息不匹配: platform='{platform_value}', ua='{ua_value[:50]}...'",
                f"确保 User-Agent 中包含与平台 '{platform_value}' 匹配的关键字。",
                "user_agent",
            )
            self._score -= 15

        if not os_matched:
            self._add_issue(
                "ua_platform", "critical",
                f"User-Agent 中的操作系统与声称的 OS 类型不匹配: 期望包含 '{expected_keyword}'",
                f"更新 User-Agent 或 OS 类型使其一致。",
                "user_agent",
            )
            self._score -= 15

        self._checks["ua_platform"] = {
            "passed": matched and os_matched,
            "platform": platform_value,
            "ua_contains_os": os_matched,
        }

    def _check_screen_device(self, fingerprint: Dict[str, Any], device_type: str,
                              os_type: str) -> None:
        """检查屏幕分辨率与设备类型的匹配。

        Args:
            fingerprint: 指纹数据。
            device_type: 设备类型。
            os_type: 操作系统类型。
        """
        screen = fingerprint.get("screen", {})
        width = screen.get("width", 0)
        height = screen.get("height", 0)

        ranges = self.DEVICE_SCREEN_RANGES.get(device_type, self.DEVICE_SCREEN_RANGES["desktop"])
        width_ok = ranges["width"][0] <= width <= ranges["width"][1]
        height_ok = ranges["height"][0] <= height <= ranges["height"][1]

        if not width_ok or not height_ok:
            self._add_issue(
                "screen_device", "critical",
                f"屏幕分辨率 {width}x{height} 与设备类型 '{device_type}' 不匹配",
                f"对于 {device_type} 设备，推荐分辨率范围: {ranges['width'][0]}-{ranges['width'][1]} x {ranges['height'][0]}-{ranges['height'][1]}",
                "screen",
            )
            self._score -= 10

        # 检查 available_height 不超过 height
        avail_height = screen.get("available_height", height)
        if avail_height > height:
            self._add_issue(
                "screen_device", "warning",
                f"available_height ({avail_height}) 超过了 screen height ({height})",
                "确保 available_height 不超过 screen height。",
                "screen",
            )
            self._score -= 5

        self._checks["screen_device"] = {
            "passed": width_ok and height_ok and avail_height <= height,
            "width": width,
            "height": height,
            "device_type": device_type,
        }

    def _check_fonts_os(self, fingerprint: Dict[str, Any], os_type: str) -> None:
        """检查字体列表与操作系统的匹配。

        Args:
            fingerprint: 指纹数据。
            os_type: 操作系统类型。
        """
        fonts_info = fingerprint.get("fonts", {})
        font_list = fonts_info.get("list", [])

        if not font_list:
            self._checks["fonts_os"] = {"passed": False, "reason": "empty_font_list"}
            return

        indicators = self.OS_FONT_INDICATORS.get(os_type, [])
        if not indicators:
            self._checks["fonts_os"] = {"passed": True, "reason": "no_indicators_defined"}
            return

        # 检查是否包含该操作系统的特征字体
        has_indicator = any(ind in font_list for ind in indicators)

        # 检查是否包含其他操作系统的特征字体（矛盾检测）
        other_os_fonts = []
        for other_os, other_indicators in self.OS_FONT_INDICATORS.items():
            if other_os != os_type:
                for ind in other_indicators:
                    if ind in font_list:
                        other_os_fonts.append((other_os, ind))

        if not has_indicator:
            self._add_issue(
                "fonts_os", "warning",
                f"字体列表中未找到 {os_type} 的特征字体",
                f"建议添加以下字体之一: {', '.join(indicators[:3])}",
                "fonts",
            )
            self._score -= 8

        if other_os_fonts:
            other_os_names = set(f[0] for f in other_os_fonts)
            self._add_issue(
                "fonts_os", "warning",
                f"字体列表中包含其他操作系统的特征字体: {', '.join(other_os_names)}",
                f"移除不属于 {os_type} 的特征字体。",
                "fonts",
            )
            self._score -= 5

        self._checks["fonts_os"] = {
            "passed": has_indicator and not other_os_fonts,
            "has_os_fonts": has_indicator,
            "conflicting_fonts": other_os_fonts,
        }

    def _check_webgl_hardware(self, fingerprint: Dict[str, Any], os_type: str) -> None:
        """检查 WebGL 渲染器与操作系统的匹配。

        Args:
            fingerprint: 指纹数据。
            os_type: 操作系统类型。
        """
        webgl = fingerprint.get("webgl", {})
        renderer = webgl.get("renderer", "")

        indicators = self.OS_WEBGL_INDICATORS.get(os_type, [])
        if not indicators or not renderer:
            self._checks["webgl_hardware"] = {"passed": True, "reason": "no_check_needed"}
            return

        has_indicator = any(ind in renderer for ind in indicators)

        if not has_indicator:
            self._add_issue(
                "webgl_hardware", "warning",
                f"WebGL 渲染器 '{renderer[:50]}...' 与操作系统 '{os_type}' 不匹配",
                f"对于 {os_type}，渲染器应包含以下关键字之一: {', '.join(indicators)}",
                "webgl",
            )
            self._score -= 8

        self._checks["webgl_hardware"] = {
            "passed": has_indicator,
            "renderer": renderer,
            "os_type": os_type,
        }

    def _check_touch_device(self, fingerprint: Dict[str, Any], device_type: str) -> None:
        """检查触摸支持与设备类型的匹配。

        Args:
            fingerprint: 指纹数据。
            device_type: 设备类型。
        """
        touch = fingerprint.get("touch", {})
        supported = touch.get("supported", False)
        max_points = touch.get("max_touch_points", 0)

        expected = self.DEVICE_TOUCH_EXPECTATIONS.get(device_type, False)

        if supported != expected:
            severity = "critical" if not expected and supported else "warning"
            self._add_issue(
                "touch_device", severity,
                f"触摸支持 ({supported}) 与设备类型 '{device_type}' 不匹配",
                f"{device_type} 设备的触摸支持应为 {expected}。",
                "touch",
            )
            self._score -= 10 if severity == "critical" else 5

        # 桌面设备不应有触摸点
        if device_type == "desktop" and max_points > 0:
            self._add_issue(
                "touch_device", "warning",
                f"桌面设备报告了 {max_points} 个触摸点",
                "桌面设备通常 max_touch_points 为 0。",
                "touch",
            )
            self._score -= 3

        self._checks["touch_device"] = {
            "passed": supported == expected,
            "supported": supported,
            "expected": expected,
            "max_touch_points": max_points,
        }

    def _check_hardware_device(self, fingerprint: Dict[str, Any], device_type: str) -> None:
        """检查硬件信息与设备类型的匹配。

        Args:
            fingerprint: 指纹数据。
            device_type: 设备类型。
        """
        hardware = fingerprint.get("hardware", {})
        concurrency = hardware.get("concurrency", 0)
        device_memory = hardware.get("device_memory", 0)

        ranges = self.DEVICE_HARDWARE_RANGES.get(device_type, self.DEVICE_HARDWARE_RANGES["desktop"])

        concurrency_ok = ranges["concurrency"][0] <= concurrency <= ranges["concurrency"][1]
        memory_ok = ranges["device_memory"][0] <= device_memory <= ranges["device_memory"][1]

        if not concurrency_ok:
            self._add_issue(
                "hardware_device", "warning",
                f"硬件并发数 {concurrency} 超出 {device_type} 设备的合理范围",
                f"对于 {device_type} 设备，推荐范围: {ranges['concurrency'][0]}-{ranges['concurrency'][1]}",
                "hardware",
            )
            self._score -= 5

        if not memory_ok:
            self._add_issue(
                "hardware_device", "warning",
                f"设备内存 {device_memory}GB 超出 {device_type} 设备的合理范围",
                f"对于 {device_type} 设备，推荐范围: {ranges['device_memory'][0]}-{ranges['device_memory'][1]}GB",
                "hardware",
            )
            self._score -= 5

        self._checks["hardware_device"] = {
            "passed": concurrency_ok and memory_ok,
            "concurrency": concurrency,
            "device_memory": device_memory,
            "device_type": device_type,
        }

    def _check_plugins_browser(self, fingerprint: Dict[str, Any], browser: str) -> None:
        """检查插件列表与浏览器类型的匹配。

        Args:
            fingerprint: 指纹数据。
            browser: 浏览器类型。
        """
        plugins_info = fingerprint.get("plugins", {})
        plugin_list = plugins_info.get("list", [])
        plugin_count = plugins_info.get("count", len(plugin_list))

        expectations = self.BROWSER_PLUGIN_EXPECTATIONS.get(browser, {})
        max_count = expectations.get("max_count", 10)
        must_contain = expectations.get("must_contain", [])

        count_ok = plugin_count <= max_count
        has_required = all(p in plugin_list for p in must_contain)

        if not count_ok:
            self._add_issue(
                "plugins_browser", "warning",
                f"插件数量 {plugin_count} 超出 {browser} 的合理范围 (最大 {max_count})",
                f"对于 {browser}，插件数量不应超过 {max_count}。",
                "plugins",
            )
            self._score -= 5

        if not has_required and must_contain:
            missing = [p for p in must_contain if p not in plugin_list]
            self._add_issue(
                "plugins_browser", "warning",
                f"{browser} 缺少必要插件: {', '.join(missing)}",
                f"确保包含以下插件: {', '.join(must_contain)}",
                "plugins",
            )
            self._score -= 5

        self._checks["plugins_browser"] = {
            "passed": count_ok and has_required,
            "count": plugin_count,
            "max_expected": max_count,
            "has_required": has_required,
        }

    def _check_storage_device(self, fingerprint: Dict[str, Any], device_type: str) -> None:
        """检查存储配额与设备类型的匹配。

        Args:
            fingerprint: 指纹数据。
            device_type: 设备类型。
        """
        storage = fingerprint.get("storage", {})
        quota = storage.get("quota", 0)

        if device_type == "mobile" and quota > 100000:
            self._add_issue(
                "storage_device", "warning",
                f"移动设备存储配额 {quota}MB 过大",
                "移动设备存储配额通常不超过 50000MB。",
                "storage",
            )
            self._score -= 3

        usage = storage.get("usage", 0)
        if usage > quota:
            self._add_issue(
                "storage_device", "critical",
                f"存储使用量 {usage}MB 超过配额 {quota}MB",
                "确保存储使用量不超过配额。",
                "storage",
            )
            self._score -= 10

        self._checks["storage_device"] = {
            "passed": usage <= quota,
            "quota": quota,
            "usage": usage,
        }

    def _check_color_depth(self, fingerprint: Dict[str, Any]) -> None:
        """检查颜色深度的合理性。

        Args:
            fingerprint: 指纹数据。
        """
        screen = fingerprint.get("screen", {})
        color_depth = screen.get("color_depth", 0)

        valid_depths = [24, 30, 32]
        if color_depth not in valid_depths:
            self._add_issue(
                "color_depth", "warning",
                f"颜色深度 {color_depth} 不是常见值",
                f"常见颜色深度: {', '.join(str(d) for d in valid_depths)}",
                "screen",
            )
            self._score -= 3

        self._checks["color_depth"] = {
            "passed": color_depth in valid_depths,
            "color_depth": color_depth,
        }

    def _check_pixel_ratio(self, fingerprint: Dict[str, Any], os_type: str) -> None:
        """检查像素比的合理性。

        Args:
            fingerprint: 指纹数据。
            os_type: 操作系统类型。
        """
        screen = fingerprint.get("screen", {})
        pixel_ratio = screen.get("pixel_ratio", 1.0)

        valid_ratios = {
            "windows": [1.0, 1.25, 1.5, 1.75, 2.0],
            "macos": [1.0, 2.0],
            "linux": [1.0, 1.25, 1.5, 2.0],
            "ios": [2.0, 3.0],
            "android": [1.5, 2.0, 2.625, 3.0, 3.5],
        }

        expected = valid_ratios.get(os_type, [1.0])
        if pixel_ratio not in expected:
            self._add_issue(
                "pixel_ratio", "warning",
                f"像素比 {pixel_ratio} 不是 {os_type} 的常见值",
                f"{os_type} 的常见像素比: {', '.join(str(r) for r in expected)}",
                "screen",
            )
            self._score -= 3

        self._checks["pixel_ratio"] = {
            "passed": pixel_ratio in expected,
            "pixel_ratio": pixel_ratio,
            "os_type": os_type,
        }

    def _check_webdriver(self, fingerprint: Dict[str, Any]) -> None:
        """检查 WebDriver 检测状态。

        Args:
            fingerprint: 指纹数据。
        """
        webdriver = fingerprint.get("webdriver", {})
        is_webdriver = webdriver.get("is_webdriver", False)
        nav_webdriver = webdriver.get("navigator_webdriver", False)
        cdc_detected = webdriver.get("cdc_detected", False)

        issues_found = []
        if is_webdriver:
            issues_found.append("navigator.webdriver 为 true")
        if nav_webdriver:
            issues_found.append("WebDriver 属性被检测到")
        if cdc_detected:
            issues_found.append("ChromeDriver (CDC) 被检测到")

        if issues_found:
            self._add_issue(
                "webdriver", "critical",
                f"WebDriver 检测到异常: {'; '.join(issues_found)}",
                "确保所有 WebDriver 相关属性为 false/undefined。",
                "webdriver",
            )
            self._score -= 20

        self._checks["webdriver"] = {
            "passed": not any(issues_found),
            "is_webdriver": is_webdriver,
            "cdc_detected": cdc_detected,
        }

    def _check_cookies(self, fingerprint: Dict[str, Any]) -> None:
        """检查 Cookie 启用状态。

        Args:
            fingerprint: 指纹数据。
        """
        cookies = fingerprint.get("cookies", {})
        enabled = cookies.get("enabled", True)

        if not enabled:
            self._add_issue(
                "cookies", "warning",
                "Cookie 被禁用",
                "大多数正常浏览器都启用 Cookie，禁用会增加指纹唯一性。",
                "cookies",
            )
            self._score -= 5

        self._checks["cookies"] = {
            "passed": enabled,
            "enabled": enabled,
        }

    def _check_pdf_viewer(self, fingerprint: Dict[str, Any], browser: str) -> None:
        """检查 PDF 查看器与浏览器的匹配。

        Args:
            fingerprint: 指纹数据。
            browser: 浏览器类型。
        """
        pdf = fingerprint.get("pdf_viewer", {})
        enabled = pdf.get("enabled", False)

        # 所有主流浏览器都应支持 PDF
        if not enabled:
            self._add_issue(
                "pdf_viewer", "info",
                f"{browser} 未启用 PDF 查看器",
                f"建议为 {browser} 启用 PDF 查看器。",
                "pdf_viewer",
            )
            self._score -= 2

        self._checks["pdf_viewer"] = {
            "passed": enabled,
            "enabled": enabled,
        }

    def _check_language_consistency(self, fingerprint: Dict[str, Any], os_type: str) -> None:
        """检查语言设置的一致性。

        Args:
            fingerprint: 指纹数据。
            os_type: 操作系统类型。
        """
        lang_info = fingerprint.get("language", {})
        primary_lang = lang_info.get("primary", "")
        languages = lang_info.get("languages", [])

        if not primary_lang:
            self._checks["language"] = {"passed": False, "reason": "no_language_set"}
            return

        # 检查语言列表是否包含主语言
        if languages and primary_lang not in languages:
            self._add_issue(
                "language", "info",
                f"主语言 '{primary_lang}' 不在语言列表中",
                "确保主语言包含在 languages 列表中。",
                "language",
            )
            self._score -= 2

        self._checks["language"] = {
            "passed": not languages or primary_lang in languages,
            "primary": primary_lang,
            "languages": languages,
        }

    def _calculate_score(self) -> None:
        """计算最终一致性评分。"""
        self._score = max(0, min(100, self._score))

    def _get_grade(self, score: int) -> str:
        """根据分数确定一致性等级。

        Args:
            score: 一致性评分（0-100）。

        Returns:
            一致性等级字符串。
        """
        if score >= 95:
            return "excellent"
        elif score >= 85:
            return "good"
        elif score >= 70:
            return "fair"
        elif score >= 50:
            return "poor"
        else:
            return "critical"

    def get_issues(self) -> List[Dict[str, Any]]:
        """获取所有一致性问题。

        Returns:
            问题列表。
        """
        return self._issues

    def get_score(self) -> int:
        """获取一致性评分。

        Returns:
            一致性评分（0-100）。
        """
        return self._score

    def summary_text(self) -> str:
        """生成文本格式的一致性校验摘要。

        Returns:
            文本格式的校验摘要。
        """
        grade_map = {
            "excellent": "优秀",
            "good": "良好",
            "fair": "一般",
            "poor": "较差",
            "critical": "严重",
        }

        lines = [
            "=" * 60,
            "  GhostLens-Pro 指纹一致性校验报告",
            "=" * 60,
            f"",
            f"  一致性评分: {self._score}/100",
            f"  一致性等级: {grade_map.get(self._get_grade(self._score), '未知')}",
            f"",
        ]

        # 检查结果摘要
        passed = sum(1 for c in self._checks.values() if c.get("passed", False))
        total = len(self._checks)
        lines.append(f"  检查项: {passed}/{total} 通过")
        lines.append("")

        # 问题列表
        if self._issues:
            lines.append("-" * 60)
            lines.append("  发现的问题:")
            for i, issue in enumerate(self._issues, 1):
                severity_map = {"critical": "严重", "warning": "警告", "info": "提示"}
                severity = severity_map.get(issue["severity"], issue["severity"])
                lines.append(f"    {i}. [{severity}] {issue['description']}")
                lines.append(f"       建议: {issue['suggestion']}")
        else:
            lines.append("  未发现一致性问题。")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)

    def to_json(self) -> str:
        """将校验结果导出为 JSON 字符串。

        Returns:
            JSON 格式的校验结果。
        """
        return json.dumps({
            "consistency_score": self._score,
            "grade": self._get_grade(self._score),
            "issues": self._issues,
            "checks": self._checks,
        }, indent=2, ensure_ascii=False)
