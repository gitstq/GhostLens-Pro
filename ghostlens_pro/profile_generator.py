"""
GhostLens-Pro 指纹配置生成器

生成逼真的浏览器指纹配置文件，支持多种浏览器和操作系统模板。
支持自定义配置、随机化和配置文件导入/导出。
"""

import json
import os
import random
import time
from typing import Any, Dict, List, Optional, Tuple

from .fingerprint_collector import FingerprintCollector


class ProfileGenerator:
    """指纹配置生成器，负责生成和管理浏览器指纹配置文件。"""

    # 内置配置模板
    BUILTIN_TEMPLATES: Dict[str, Dict[str, Any]] = {
        "chrome_win10": {
            "name": "Chrome on Windows 10",
            "description": "标准 Chrome 浏览器在 Windows 10 上的指纹配置",
            "browser": "chrome",
            "os_type": "windows",
            "device_type": "desktop",
            "overrides": {
                "platform": {"value": "Win32"},
                "screen": {"width": 1920, "height": 1080, "color_depth": 24, "pixel_ratio": 1.0},
            },
        },
        "chrome_win11": {
            "name": "Chrome on Windows 11",
            "description": "标准 Chrome 浏览器在 Windows 11 上的指纹配置",
            "browser": "chrome",
            "os_type": "windows",
            "device_type": "desktop",
            "overrides": {
                "platform": {"value": "Win32"},
                "screen": {"width": 2560, "height": 1440, "color_depth": 32, "pixel_ratio": 1.25},
            },
        },
        "chrome_macos": {
            "name": "Chrome on macOS",
            "description": "标准 Chrome 浏览器在 macOS 上的指纹配置",
            "browser": "chrome",
            "os_type": "macos",
            "device_type": "desktop",
            "overrides": {
                "platform": {"value": "MacIntel"},
                "screen": {"width": 2560, "height": 1440, "color_depth": 30, "pixel_ratio": 2.0},
            },
        },
        "chrome_linux": {
            "name": "Chrome on Linux",
            "description": "标准 Chrome 浏览器在 Linux 上的指纹配置",
            "browser": "chrome",
            "os_type": "linux",
            "device_type": "desktop",
            "overrides": {
                "platform": {"value": "Linux x86_64"},
                "screen": {"width": 1920, "height": 1080, "color_depth": 24, "pixel_ratio": 1.0},
            },
        },
        "firefox_win10": {
            "name": "Firefox on Windows 10",
            "description": "标准 Firefox 浏览器在 Windows 10 上的指纹配置",
            "browser": "firefox",
            "os_type": "windows",
            "device_type": "desktop",
            "overrides": {
                "platform": {"value": "Win32"},
                "screen": {"width": 1920, "height": 1080, "color_depth": 24, "pixel_ratio": 1.0},
            },
        },
        "firefox_macos": {
            "name": "Firefox on macOS",
            "description": "标准 Firefox 浏览器在 macOS 上的指纹配置",
            "browser": "firefox",
            "os_type": "macos",
            "device_type": "desktop",
            "overrides": {
                "platform": {"value": "MacIntel"},
                "screen": {"width": 2880, "height": 1800, "color_depth": 30, "pixel_ratio": 2.0},
            },
        },
        "safari_macos": {
            "name": "Safari on macOS",
            "description": "标准 Safari 浏览器在 macOS 上的指纹配置",
            "browser": "safari",
            "os_type": "macos",
            "device_type": "desktop",
            "overrides": {
                "platform": {"value": "MacIntel"},
                "screen": {"width": 3024, "height": 1964, "color_depth": 30, "pixel_ratio": 2.0},
            },
        },
        "edge_win10": {
            "name": "Edge on Windows 10",
            "description": "标准 Edge 浏览器在 Windows 10 上的指纹配置",
            "browser": "edge",
            "os_type": "windows",
            "device_type": "desktop",
            "overrides": {
                "platform": {"value": "Win32"},
                "screen": {"width": 1920, "height": 1080, "color_depth": 24, "pixel_ratio": 1.0},
            },
        },
        "chrome_ios": {
            "name": "Chrome on iOS",
            "description": "Chrome 浏览器在 iOS 设备上的指纹配置",
            "browser": "chrome",
            "os_type": "ios",
            "device_type": "mobile",
            "overrides": {
                "platform": {"value": "iPhone"},
                "screen": {"width": 390, "height": 844, "color_depth": 32, "pixel_ratio": 3.0},
            },
        },
        "chrome_android": {
            "name": "Chrome on Android",
            "description": "Chrome 浏览器在 Android 设备上的指纹配置",
            "browser": "chrome",
            "os_type": "android",
            "device_type": "mobile",
            "overrides": {
                "platform": {"value": "Linux armv8l"},
                "screen": {"width": 412, "height": 915, "color_depth": 24, "pixel_ratio": 2.625},
            },
        },
        "safari_ios": {
            "name": "Safari on iOS",
            "description": "Safari 浏览器在 iOS 设备上的指纹配置",
            "browser": "safari",
            "os_type": "ios",
            "device_type": "mobile",
            "overrides": {
                "platform": {"value": "iPhone"},
                "screen": {"width": 414, "height": 896, "color_depth": 32, "pixel_ratio": 3.0},
            },
        },
        "chrome_android_pixel": {
            "name": "Chrome on Pixel 5",
            "description": "Chrome 浏览器在 Google Pixel 5 上的指纹配置",
            "browser": "chrome",
            "os_type": "android",
            "device_type": "mobile",
            "overrides": {
                "platform": {"value": "Linux armv8l"},
                "screen": {"width": 393, "height": 851, "color_depth": 24, "pixel_ratio": 2.75},
            },
        },
    }

    def __init__(self, seed: Optional[int] = None) -> None:
        """初始化指纹配置生成器。

        Args:
            seed: 随机种子，用于可重复的配置生成。默认为None（随机）。
        """
        self._seed = seed
        self._rng = random.Random(seed)

    def generate(self, template_name: Optional[str] = None,
                 browser: Optional[str] = None,
                 os_type: Optional[str] = None,
                 device_type: Optional[str] = None,
                 randomize: bool = True,
                 overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """生成指纹配置文件。

        Args:
            template_name: 内置模板名称。如果指定，将使用模板的默认值。
            browser: 浏览器类型 (chrome, firefox, safari, edge)。
            os_type: 操作系统类型 (windows, macos, linux, ios, android)。
            device_type: 设备类型 (desktop, mobile)。
            randomize: 是否随机化非关键参数。
            overrides: 自定义覆盖配置。
            seed: 随机种子。

        Returns:
            完整的指纹配置字典。
        """
        # 确定参数
        if template_name and template_name in self.BUILTIN_TEMPLATES:
            template = self.BUILTIN_TEMPLATES[template_name]
            browser = browser or template["browser"]
            os_type = os_type or template["os_type"]
            device_type = device_type or template["device_type"]
            template_overrides = template.get("overrides", {})
        else:
            template_overrides = {}
            if template_name and template_name not in self.BUILTIN_TEMPLATES:
                raise ValueError(f"Unknown template: {template_name}. Available: {list(self.BUILTIN_TEMPLATES.keys())}")

        # 设置默认值
        browser = browser or "chrome"
        os_type = os_type or "windows"
        device_type = device_type or "desktop"

        # 使用 FingerprintCollector 生成基础指纹
        collector_seed = self._seed if self._seed is not None else self._rng.randint(1, 999999)
        collector = FingerprintCollector(seed=collector_seed)
        fingerprint_data = collector.collect_all(os_type=os_type, browser=browser, device_type=device_type)
        fingerprint = fingerprint_data["fingerprint"]
        scores = fingerprint_data["scores"]

        # 应用模板覆盖
        for key, value in template_overrides.items():
            if key in fingerprint:
                if isinstance(value, dict) and isinstance(fingerprint[key], dict):
                    fingerprint[key].update(value)
                else:
                    fingerprint[key] = value

        # 应用自定义覆盖
        if overrides:
            for key, value in overrides.items():
                if key in fingerprint:
                    if isinstance(value, dict) and isinstance(fingerprint[key], dict):
                        fingerprint[key].update(value)
                    else:
                        fingerprint[key] = value

        # 随机化非关键参数
        if randomize:
            fingerprint = self._randomize_non_critical(fingerprint)

        return {
            "profile": {
                "name": template_name or f"custom_{browser}_{os_type}",
                "browser": browser,
                "os_type": os_type,
                "device_type": device_type,
                "template": template_name,
                "created_at": time.time(),
                "version": "1.0.0",
            },
            "fingerprint": fingerprint,
            "scores": scores,
        }

    def _randomize_non_critical(self, fingerprint: Dict[str, Any]) -> Dict[str, Any]:
        """对非关键参数进行随机化。

        Args:
            fingerprint: 指纹数据字典。

        Returns:
            随机化后的指纹数据。
        """
        # 随机化 Canvas 哈希（添加噪声）
        if "canvas" in fingerprint:
            canvas = dict(fingerprint["canvas"])
            noise = self._rng.randint(0, 1000)
            canvas["hash"] = canvas["hash"][:60] + f"{noise:040d}"[:64 - 60] if len(canvas["hash"]) >= 60 else canvas["hash"]
            fingerprint["canvas"] = canvas

        # 随机化存储使用量
        if "storage" in fingerprint:
            storage = dict(fingerprint["storage"])
            quota = storage.get("quota", 100000)
            storage["usage"] = self._rng.randint(int(quota * 0.01), int(quota * 0.3))
            fingerprint["storage"] = storage

        # 随机化连接信息
        if "connection" in fingerprint:
            conn = dict(fingerprint["connection"])
            conn["downlink"] = round(self._rng.uniform(1.0, 100.0), 2)
            conn["rtt"] = self._rng.randint(10, 300)
            fingerprint["connection"] = conn

        # 随机化 Performance API 精度
        if "performance" in fingerprint:
            perf = dict(fingerprint["performance"])
            perf["resource_count"] = self._rng.randint(5, 30)
            fingerprint["performance"] = perf

        return fingerprint

    def list_templates(self) -> List[Dict[str, str]]:
        """列出所有内置配置模板。

        Returns:
            模板信息列表。
        """
        templates = []
        for key, tmpl in self.BUILTIN_TEMPLATES.items():
            templates.append({
                "id": key,
                "name": tmpl["name"],
                "description": tmpl["description"],
                "browser": tmpl["browser"],
                "os_type": tmpl["os_type"],
                "device_type": tmpl["device_type"],
            })
        return templates

    def get_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """获取指定模板的详细信息。

        Args:
            template_name: 模板名称。

        Returns:
            模板配置字典，如果不存在则返回None。
        """
        return self.BUILTIN_TEMPLATES.get(template_name)

    def export_json(self, profile: Dict[str, Any], filepath: str) -> None:
        """将配置文件导出为 JSON 文件。

        Args:
            profile: 配置文件字典。
            filepath: 输出文件路径。
        """
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)

    def import_json(self, filepath: str) -> Dict[str, Any]:
        """从 JSON 文件导入配置文件。

        Args:
            filepath: 输入文件路径。

        Returns:
            配置文件字典。

        Raises:
            FileNotFoundError: 文件不存在。
            json.JSONDecodeError: JSON 格式错误。
        """
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_batch(self, template_name: str, count: int = 10) -> List[Dict[str, Any]]:
        """批量生成指纹配置。

        Args:
            template_name: 模板名称。
            count: 生成数量。

        Returns:
            配置文件列表。
        """
        profiles = []
        for i in range(count):
            seed = (self._seed or 0) + i if self._seed is not None else self._rng.randint(1, 999999)
            gen = ProfileGenerator(seed=seed)
            profile = gen.generate(template_name=template_name, randomize=True)
            profiles.append(profile)
        return profiles
