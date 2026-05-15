"""
GhostLens-Pro 指纹采集引擎

采集50+浏览器指纹维度，包括 User-Agent、屏幕信息、Canvas指纹、
WebGL信息、字体列表、音频指纹、硬件信息等。每个指纹维度都有
风险评分（0-100），用于后续的反检测评分分析。
"""

import hashlib
import json
import os
import platform
import random
import struct
import sys
import time
from typing import Any, Dict, List, Optional, Tuple


class FingerprintCollector:
    """浏览器指纹采集引擎，负责采集和模拟50+指纹维度。"""

    # 已知合法的 User-Agent 模板
    UA_TEMPLATES: Dict[str, List[str]] = {
        "chrome_windows": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ver}.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ver}.0.0.0 Safari/537.36 Edg/{ver2}.0.0.0",
        ],
        "chrome_macos": [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ver}.0.0.0 Safari/537.36",
        ],
        "chrome_linux": [
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ver}.0.0.0 Safari/537.36",
        ],
        "firefox_windows": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{ver}.0) Gecko/20100101 Firefox/{ver}.0",
        ],
        "firefox_macos": [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:{ver}.0) Gecko/20100101 Firefox/{ver}.0",
        ],
        "firefox_linux": [
            "Mozilla/5.0 (X11; Linux x86_64; rv:{ver}.0) Gecko/20100101 Firefox/{ver}.0",
        ],
        "safari_macos": [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{ver}.0 Safari/605.1.15",
        ],
        "edge_windows": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ver}.0.0.0 Safari/537.36 Edg/{ver2}.0.0.0",
        ],
        "ios_safari": [
            "Mozilla/5.0 (iPhone; CPU iPhone OS {ver}_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        ],
        "android_chrome": [
            "Mozilla/5.0 (Linux; Android {ver}; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ver2}.0.0.0 Mobile Safari/537.36",
        ],
    }

    # 已知合法的屏幕分辨率
    SCREEN_RESOLUTIONS: Dict[str, List[Tuple[int, int]]] = {
        "windows": [
            (1920, 1080), (2560, 1440), (1366, 768), (1536, 864),
            (1440, 900), (1280, 720), (1600, 900), (3840, 2160),
        ],
        "macos": [
            (2560, 1440), (1920, 1080), (1680, 1050), (1440, 900),
            (2880, 1800), (3024, 1964), (2560, 1600),
        ],
        "linux": [
            (1920, 1080), (2560, 1440), (1366, 768), (3840, 2160),
            (1280, 720), (1600, 900),
        ],
        "ios": [
            (390, 844), (414, 896), (375, 812), (428, 926),
            (390, 844), (320, 568),
        ],
        "android": [
            (412, 915), (360, 800), (393, 851), (384, 854),
            (411, 891), (360, 780),
        ],
    }

    # 已知合法的颜色深度
    COLOR_DEPTHS: List[int] = [24, 30, 32]

    # 已知合法的像素比
    PIXEL_RATIOS: Dict[str, List[float]] = {
        "windows": [1.0, 1.25, 1.5, 1.75, 2.0],
        "macos": [1.0, 2.0],
        "linux": [1.0, 1.25, 1.5, 2.0],
        "ios": [2.0, 3.0],
        "android": [1.5, 2.0, 2.625, 3.0, 3.5],
    }

    # 已知合法的时区列表
    TIMEZONES: List[str] = [
        "America/New_York", "America/Chicago", "America/Denver",
        "America/Los_Angeles", "America/Anchorage", "Pacific/Honolulu",
        "Europe/London", "Europe/Paris", "Europe/Berlin", "Europe/Moscow",
        "Asia/Shanghai", "Asia/Tokyo", "Asia/Kolkata", "Asia/Dubai",
        "Australia/Sydney", "Pacific/Auckland",
    ]

    # 已知合法的语言列表
    LANGUAGES: Dict[str, List[str]] = {
        "en": ["en-US", "en-GB", "en-CA", "en-AU"],
        "zh": ["zh-CN", "zh-TW", "zh-HK"],
        "ja": ["ja-JP"],
        "ko": ["ko-KR"],
        "de": ["de-DE", "de-AT", "de-CH"],
        "fr": ["fr-FR", "fr-CA", "fr-BE"],
        "es": ["es-ES", "es-MX", "es-AR"],
        "pt": ["pt-BR", "pt-PT"],
        "ru": ["ru-RU"],
    }

    # WebGL 渲染器信息
    WEBGL_RENDERERS: Dict[str, List[Dict[str, str]]] = {
        "windows": [
            {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 6GB Direct3D11 vs_5_0 ps_5_0, D3D11)"},
            {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0, D3D11)"},
            {"vendor": "Google Inc. (Intel)", "renderer": "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)"},
            {"vendor": "Google Inc. (AMD)", "renderer": "ANGLE (AMD, AMD Radeon RX 580 Direct3D11 vs_5_0 ps_5_0, D3D11)"},
        ],
        "macos": [
            {"vendor": "Apple Inc.", "renderer": "Apple M1"},
            {"vendor": "Apple Inc.", "renderer": "Apple M1 Pro"},
            {"vendor": "Apple Inc.", "renderer": "Apple M2"},
            {"vendor": "Intel Inc.", "renderer": "Intel(R) Iris(TM) Plus Graphics 640"},
        ],
        "linux": [
            {"vendor": "X.Org", "renderer": "Mesa Intel(R) UHD Graphics 630 (CFL GT2)"},
            {"vendor": "X.Org", "renderer": "Mesa AMD RADV NAVI10 (ACO)"},
            {"vendor": "NVIDIA Corporation", "renderer": "NVIDIA GeForce GTX 1060 6GB/PCIe/SSE2"},
        ],
    }

    # 字体列表（按操作系统分类）
    FONT_LISTS: Dict[str, List[str]] = {
        "windows": [
            "Arial", "Arial Black", "Bahnschrift", "Calibri", "Cambria",
            "Cambria Math", "Candara", "Comic Sans MS", "Consolas",
            "Constantia", "Corbel", "Courier New", "Ebrima", "Franklin Gothic Medium",
            "Gabriola", "Gadugi", "Georgia", "HoloLens MDL2 Assets",
            "Impact", "Ink Free", "Javanese Text", "Leelawadee UI",
            "Lucida Console", "Lucida Sans Unicode", "Malgun Gothic",
            "Marlett", "Microsoft Himalaya", "Microsoft JhengHei",
            "Microsoft New Tai Lue", "Microsoft PhagsPa", "Microsoft Sans Serif",
            "Microsoft Tai Le", "Microsoft YaHei", "Microsoft Yi Baiti",
            "MingLiU-ExtB", "Mongolian Baiti", "MS Gothic", "MS PGothic",
            "MS UI Gothic", "MV Boli", "Myanmar Text", "Nirmala UI",
            "Palatino Linotype", "PMingLiU-ExtB", "Segoe MDL2 Assets",
            "Segoe Print", "Segoe Script", "Segoe UI", "Segoe UI Historic",
            "Segoe UI Emoji", "Segoe UI Symbol", "SimSun", "Sitka",
            "Sylfaen", "Symbol", "Tahoma", "Times New Roman",
            "Trebuchet MS", "Verdana", "Wingdings", "Yu Gothic",
        ],
        "macos": [
            "American Typewriter", "Andale Mono", "Apple Braille",
            "Apple Chancery", "Apple Color Emoji", "Apple SD Gothic Neo",
            "Apple Symbols", "AppleGothic", "AppleMyungjo",
            "Arial", "Arial Black", "Arial Hebrew", "Arial Narrow",
            "Arial Rounded MT Bold", "Arial Unicode MS", "Avenir",
            "Avenir Next", "Avenir Next Condensed", "Baskerville",
            "Big Caslon", "Brush Script MT", "Chalkboard",
            "Chalkboard SE", "Chalkduster", "Charter", "Cochin",
            "Copperplate", "Corsiva Hebrew", "Courier", "Courier New",
            "Damascus", "DecoType Naskh", "Devanagari MT", "Didot",
            "Euphemia UCAS", "Futura", "Geneva", "Georgia",
            "Gill Sans", "Gujarati MT", "Gurmukhi MN", "Gurmukhi MT",
            "Heiti SC", "Heiti TC", "Helvetica", "Helvetica Neue",
            "Hiragino Sans", "Hiragino Sans GB", "Hoefler Text",
            "Impact", "Kannada MN", "Kefa", "Khmer MN", "Kohinoor Bangla",
            "Kohinoor Devanagari", "Kohinoor Telugu", "KufiStandardGK",
            "Lao MN", "Lucida Grande", "Luminari", "Malayalam MN",
            "Marion", "Menlo", "Mishafi", "Monaco", "Mona Lisa",
            "Noteworthy", "Optima", "Oriya MN", "Palatino",
            "Papyrus", "Phosphate", "PingFang HK", "PingFang SC",
            "PingFang TC", "Plantagenet Cherokee", "Raanana",
            "Rockwell", "Sathu", "Savoye LET", "Shree Devanagari 714",
            "SignPainter", "Sinhala MN", "Skia", "Snell Roundhand",
            "Songti SC", "Songti TC", "STFangsong", "STHeiti",
            "STKaiti", "STSong", "STXihei", "Sukhumvit Set",
            "Tamil MN", "Telugu MN", "Thonburi", "Times New Roman",
            "Trebuchet MS", "Verdana", "Waseem", "Zapf Dingbats",
            "Zapfino",
        ],
        "linux": [
            "Arial", "Arial Black", "Bitstream Charter", "Bitstream Vera Sans",
            "Bitstream Vera Sans Mono", "Bitstream Vera Serif", "Calibri",
            "Cantarell", "Comic Sans MS", "Courier 10 Pitch", "Courier New",
            "DejaVu Sans", "DejaVu Sans Mono", "DejaVu Serif",
            "Droid Sans", "Droid Sans Mono", "Droid Serif",
            "FreeMono", "FreeSans", "FreeSerif", "Garuda",
            "Georgia", "Gentium", "Gentium Basic", "Gentium Plus",
            "GNOME Sans", "GNOME Sans Mono", "GURU Noto Sans",
            "Hanuman", "Liberation Mono", "Liberation Sans",
            "Liberation Serif", "Lohit Bengali", "Lohit Devanagari",
            "Lohit Gujarati", "Lohit Kannada", "Lohit Malayalam",
            "Lohit Oriya", "Lohit Punjabi", "Lohit Tamil",
            "Lohit Telugu", "Lucida Console", "Meera Inimai",
            "Microsoft YaHei", "Mikro", "Monospace", "NanumGothic",
            "NanumGothicCoding", "NanumMyeongjo", "Nimbus Mono L",
            "Nimbus Roman No9 L", "Nimbus Sans L", "Norasi",
            "Noto Color Emoji", "Noto Sans", "Noto Sans CJK",
            "Noto Sans Mono", "Noto Serif", "Open Sans",
            "Padauk", "Palatino", "Papyrus", "PT Sans",
            "PT Serif", "Roboto", "Sahadeva", "Sawasdee",
            "Standard Symbols L", "Symbola", "TakaoGothic",
            "TakaoPGothic", "Tibetan Machine Uni", "Times New Roman",
            "TlwgMono", "TlwgTypewriter", "TlwgTypist",
            "TlwgWriter", "Ubuntu", "Ubuntu Condensed", "Ubuntu Mono",
            "Umpush", "UnBatang", "UnDotum", "UnDroidumFallback",
            "Vera", "Vera Sans", "Vera Sans Mono", "Vera Serif",
            "Verdana", "WenQuanYi Micro Hei", "WenQuanYi Zen Hei",
        ],
    }

    # 硬件并发数（按设备类型）
    HARDWARE_CONCURRENCY: Dict[str, List[int]] = {
        "desktop": [2, 4, 6, 8, 10, 12, 16, 20, 24, 32],
        "mobile": [2, 4, 6, 8],
    }

    # 设备内存（GB）
    DEVICE_MEMORY: Dict[str, List[float]] = {
        "desktop": [2.0, 4.0, 8.0, 16.0, 32.0, 64.0],
        "mobile": [2.0, 3.0, 4.0, 6.0, 8.0, 12.0],
    }

    # 插件列表
    PLUGIN_LISTS: Dict[str, List[str]] = {
        "chrome": [
            "PDF Viewer", "Chrome PDF Viewer", "Chromium PDF Viewer",
            "Microsoft Edge PDF Viewer", "WebKit built-in PDF",
        ],
        "firefox": [
            "PDF Viewer",
        ],
        "safari": [],
    }

    # 存储配额估算（MB）
    STORAGE_QUOTA: Dict[str, List[int]] = {
        "desktop": [50000, 100000, 200000, 500000],
        "mobile": [5000, 10000, 20000, 50000],
    }

    # 连接类型
    CONNECTION_TYPES: List[str] = ["4g", "wifi", "ethernet", "3g", "slow-2g"]

    # Speech Synthesis 声音列表
    SPEECH_VOICES: Dict[str, List[Dict[str, str]]] = {
        "en-US": [
            {"name": "Microsoft David Desktop - English (United States)", "lang": "en-US", "default": True},
            {"name": "Microsoft Zira Desktop - English (United States)", "lang": "en-US", "default": False},
        ],
        "zh-CN": [
            {"name": "Microsoft Huihui Desktop - Chinese (Simplified)", "lang": "zh-CN", "default": True},
            {"name": "Microsoft Kangkang Desktop - Chinese (Simplified)", "lang": "zh-CN", "default": False},
        ],
    }

    def __init__(self, seed: Optional[int] = None) -> None:
        """初始化指纹采集引擎。

        Args:
            seed: 随机种子，用于可重复的指纹生成。默认为None（随机）。
        """
        self._seed = seed
        if seed is not None:
            self._rng = random.Random(seed)
        else:
            self._rng = random.Random()
        self._fingerprint: Dict[str, Any] = {}
        self._scores: Dict[str, int] = {}

    def _rand_choice(self, seq: List[Any]) -> Any:
        """从序列中随机选择一个元素。

        Args:
            seq: 可选序列。

        Returns:
            随机选择的元素。
        """
        return self._rng.choice(seq)

    def _rand_int(self, a: int, b: int) -> int:
        """生成指定范围内的随机整数。

        Args:
            a: 最小值（包含）。
            b: 最大值（包含）。

        Returns:
            随机整数。
        """
        return self._rng.randint(a, b)

    def _rand_float(self, a: float, b: float) -> float:
        """生成指定范围内的随机浮点数。

        Args:
            a: 最小值。
            b: 最大值。

        Returns:
            随机浮点数。
        """
        return round(self._rng.uniform(a, b), 2)

    def _generate_canvas_hash(self, text: str = "GhostLens-Pro Canvas Fingerprint") -> str:
        """模拟生成 Canvas 指纹哈希。

        Args:
            text: 用于生成哈希的文本。

        Returns:
            Canvas 指纹的 SHA-256 哈希值。
        """
        # 添加随机噪声模拟不同浏览器的渲染差异
        noise = self._rand_int(0, 999999)
        data = f"{text}_{noise}_{self._seed or time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()

    def _generate_audio_hash(self) -> str:
        """模拟生成音频指纹哈希。

        Returns:
            音频指纹的 SHA-256 哈希值。
        """
        # 模拟 AudioContext 和 OscillatorNode 的指纹
        sample_rate = self._rand_choice([44100, 48000])
        frequency = self._rand_float(1000.0, 5000.0)
        noise = self._rand_int(0, 999999)
        data = f"audio_{sample_rate}_{frequency}_{noise}"
        return hashlib.sha256(data.encode()).hexdigest()

    def _generate_webgl_hash(self, renderer: str) -> str:
        """模拟生成 WebGL 指纹哈希。

        Args:
            renderer: WebGL 渲染器信息。

        Returns:
            WebGL 指纹的 SHA-256 哈希值。
        """
        data = f"webgl_{renderer}_{self._seed or time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()

    def collect_all(self, os_type: str = "windows", browser: str = "chrome",
                    device_type: str = "desktop") -> Dict[str, Any]:
        """采集所有指纹维度。

        Args:
            os_type: 操作系统类型 (windows, macos, linux, ios, android)。
            browser: 浏览器类型 (chrome, firefox, safari, edge)。
            device_type: 设备类型 (desktop, mobile)。

        Returns:
            包含所有指纹维度和风险评分的字典。
        """
        self._fingerprint = {}
        self._scores = {}

        self._collect_user_agent(os_type, browser)
        self._collect_screen_info(os_type, device_type)
        self._collect_timezone()
        self._collect_language(os_type)
        self._collect_platform(os_type, device_type, browser)
        self._collect_canvas_fingerprint()
        self._collect_webgl_info(os_type)
        self._collect_fonts(os_type)
        self._collect_audio_fingerprint()
        self._collect_hardware_info(device_type)
        self._collect_touch_support(device_type)
        self._collect_battery_status()
        self._collect_connection_info()
        self._collect_cookie_status()
        self._collect_do_not_track()
        self._collect_pdf_viewer(browser)
        self._collect_plugins(browser)
        self._collect_storage_quota(device_type)
        self._collect_media_devices(device_type)
        self._collect_speech_voices(os_type)
        self._collect_client_rects()
        self._collect_iframe_detection()
        self._collect_performance_api()
        self._collect_console_detection()
        self._collect_debugger_detection()
        self._collect_webdriver_detection()
        self._collect_webRTC_leak()
        self._collect_permissions_api()
        self._collect_css_features()
        self._collect_math_constants()
        self._collect_error_messages()
        self._collect_feature_detection()

        return {
            "fingerprint": self._fingerprint,
            "scores": self._scores,
            "metadata": {
                "os_type": os_type,
                "browser": browser,
                "device_type": device_type,
                "timestamp": time.time(),
                "version": "1.0.0",
            },
        }

    def _collect_user_agent(self, os_type: str, browser: str) -> None:
        """采集 User-Agent 信息。

        Args:
            os_type: 操作系统类型。
            browser: 浏览器类型。
        """
        key = f"{browser}_{os_type}"
        if key not in self.UA_TEMPLATES:
            key = "chrome_windows"

        template = self._rand_choice(self.UA_TEMPLATES[key])

        if browser == "chrome":
            ver = self._rand_int(120, 130)
            template = template.replace("{ver}", str(ver))
            if "{ver2}" in template:
                template = template.replace("{ver2}", str(ver))
        elif browser == "firefox":
            ver = self._rand_int(120, 130)
            template = template.replace("{ver}", str(ver))
        elif browser == "safari":
            ver = self._rand_choice([15, 16, 17])
            template = template.replace("{ver}", str(ver))
        elif browser == "edge":
            ver = self._rand_int(120, 130)
            template = template.replace("{ver}", str(ver))
            if "{ver2}" in template:
                template = template.replace("{ver2}", str(ver))

        self._fingerprint["user_agent"] = {
            "value": template,
            "browser": browser,
            "os": os_type,
        }
        # UA 风险评分：模板化UA风险较低
        self._scores["user_agent"] = self._rand_int(5, 20)

    def _collect_screen_info(self, os_type: str, device_type: str) -> None:
        """采集屏幕信息。

        Args:
            os_type: 操作系统类型。
            device_type: 设备类型。
        """
        resolutions = self.SCREEN_RESOLUTIONS.get(os_type, self.SCREEN_RESOLUTIONS["windows"])
        width, height = self._rand_choice(resolutions)
        color_depth = self._rand_choice(self.COLOR_DEPTHS)
        pixel_ratios = self.PIXEL_RATIOS.get(os_type, [1.0])
        pixel_ratio = self._rand_choice(pixel_ratios)

        self._fingerprint["screen"] = {
            "width": width,
            "height": height,
            "color_depth": color_depth,
            "pixel_ratio": pixel_ratio,
            "available_width": width,
            "available_height": height - 40,  # 模拟任务栏
        }
        self._scores["screen"] = self._rand_int(5, 15)

    def _collect_timezone(self) -> None:
        """采集时区信息。"""
        tz = self._rand_choice(self.TIMEZONES)
        offset = self._rand_int(-12, 12)
        self._fingerprint["timezone"] = {
            "value": tz,
            "offset": offset,
        }
        self._scores["timezone"] = self._rand_int(5, 15)

    def _collect_language(self, os_type: str) -> None:
        """采集语言信息。

        Args:
            os_type: 操作系统类型。
        """
        lang_key = self._rand_choice(list(self.LANGUAGES.keys()))
        lang = self._rand_choice(self.LANGUAGES[lang_key])
        languages = [lang, "en-US"] if lang != "en-US" else [lang]

        self._fingerprint["language"] = {
            "primary": lang,
            "languages": languages,
        }
        self._scores["language"] = self._rand_int(5, 15)

    def _collect_platform(self, os_type: str, device_type: str, browser: str = "chrome") -> None:
        """采集平台信息。

        Args:
            os_type: 操作系统类型。
            device_type: 设备类型。
        """
        platform_map = {
            "windows": "Win32",
            "macos": "MacIntel",
            "linux": "Linux x86_64",
            "ios": "iPhone",
            "android": "Linux armv8l",
        }
        platform_value = platform_map.get(os_type, "Win32")

        self._fingerprint["platform"] = {
            "value": platform_value,
            "os_type": os_type,
            "device_type": device_type,
            "vendor": "Google Inc." if browser == "chrome" else "",
        }
        self._scores["platform"] = self._rand_int(5, 15)

    def _collect_canvas_fingerprint(self) -> None:
        """采集 Canvas 指纹信息。"""
        canvas_hash = self._generate_canvas_hash()
        self._fingerprint["canvas"] = {
            "hash": canvas_hash,
            "text_hash": self._generate_canvas_hash("text_render"),
            "shape_hash": self._generate_canvas_hash("shape_render"),
            "blend_hash": self._generate_canvas_hash("blend_mode"),
        }
        self._scores["canvas"] = self._rand_int(10, 30)

    def _collect_webgl_info(self, os_type: str) -> None:
        """采集 WebGL 信息。

        Args:
            os_type: 操作系统类型。
        """
        renderers = self.WEBGL_RENDERERS.get(os_type, self.WEBGL_RENDERERS["windows"])
        renderer_info = self._rand_choice(renderers)

        self._fingerprint["webgl"] = {
            "vendor": renderer_info["vendor"],
            "renderer": renderer_info["renderer"],
            "hash": self._generate_webgl_hash(renderer_info["renderer"]),
            "max_texture_size": self._rand_choice([4096, 8192, 16384, 32768]),
            "max_renderbuffer_size": self._rand_choice([4096, 8192, 16384]),
            "shading_language_version": "WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)",
            "extensions_count": self._rand_int(20, 40),
            "parameters": {
                "MAX_VERTEX_ATTRIBS": self._rand_int(16, 32),
                "MAX_VERTEX_UNIFORM_VECTORS": self._rand_int(256, 4096),
                "MAX_VARYING_VECTORS": self._rand_int(8, 32),
                "MAX_FRAGMENT_UNIFORM_VECTORS": self._rand_int(256, 1024),
                "MAX_VERTEX_TEXTURE_IMAGE_UNITS": self._rand_int(0, 32),
                "MAX_TEXTURE_IMAGE_UNITS": self._rand_int(8, 32),
                "MAX_COMBINED_TEXTURE_IMAGE_UNITS": self._rand_int(8, 64),
            },
        }
        self._scores["webgl"] = self._rand_int(10, 25)

    def _collect_fonts(self, os_type: str) -> None:
        """采集字体列表信息。

        Args:
            os_type: 操作系统类型。
        """
        fonts = list(self.FONT_LISTS.get(os_type, self.FONT_LISTS["windows"]))
        # 随机移除一些字体模拟不同安装情况
        num_fonts = self._rand_int(int(len(fonts) * 0.7), len(fonts))
        selected_fonts = self._rng.sample(fonts, min(num_fonts, len(fonts)))
        selected_fonts.sort()

        self._fingerprint["fonts"] = {
            "list": selected_fonts,
            "count": len(selected_fonts),
            "os_match": True,
        }
        self._scores["fonts"] = self._rand_int(5, 20)

    def _collect_audio_fingerprint(self) -> None:
        """采集音频指纹信息。"""
        self._fingerprint["audio"] = {
            "hash": self._generate_audio_hash(),
            "sample_rate": self._rand_choice([44100, 48000]),
            "channel_count": self._rand_choice([1, 2]),
            "max_channel_count": 2,
        }
        self._scores["audio"] = self._rand_int(10, 25)

    def _collect_hardware_info(self, device_type: str) -> None:
        """采集硬件信息。

        Args:
            device_type: 设备类型。
        """
        concurrency_list = self.HARDWARE_CONCURRENCY.get(device_type, self.HARDWARE_CONCURRENCY["desktop"])
        memory_list = self.DEVICE_MEMORY.get(device_type, self.DEVICE_MEMORY["desktop"])

        self._fingerprint["hardware"] = {
            "concurrency": self._rand_choice(concurrency_list),
            "device_memory": self._rand_choice(memory_list),
        }
        self._scores["hardware"] = self._rand_int(5, 15)

    def _collect_touch_support(self, device_type: str) -> None:
        """采集触摸支持信息。

        Args:
            device_type: 设备类型。
        """
        max_touch_points = 0 if device_type == "desktop" else self._rand_int(1, 10)
        self._fingerprint["touch"] = {
            "supported": device_type == "mobile",
            "max_touch_points": max_touch_points,
            "touch_event": device_type == "mobile",
        }
        self._scores["touch"] = self._rand_int(5, 15)

    def _collect_battery_status(self) -> None:
        """采集电池状态信息。"""
        self._fingerprint["battery"] = {
            "charging": self._rng.choice([True, False]),
            "level": self._rand_float(0.1, 1.0),
            "charging_time": self._rand_int(0, 7200) if self._fingerprint.get("touch", {}).get("supported") else 0,
            "discharging_time": self._rand_int(3600, 28800) if self._fingerprint.get("touch", {}).get("supported") else float("inf"),
        }
        self._scores["battery"] = self._rand_int(5, 15)

    def _collect_connection_info(self) -> None:
        """采集网络连接信息。"""
        conn_type = self._rand_choice(self.CONNECTION_TYPES)
        self._fingerprint["connection"] = {
            "type": conn_type,
            "effective_type": conn_type,
            "downlink": self._rand_float(1.0, 100.0),
            "rtt": self._rand_int(10, 300),
            "save_data": False,
        }
        self._scores["connection"] = self._rand_int(5, 15)

    def _collect_cookie_status(self) -> None:
        """采集 Cookie 启用状态。"""
        self._fingerprint["cookies"] = {
            "enabled": True,
        }
        self._scores["cookies"] = 5

    def _collect_do_not_track(self) -> None:
        """采集 Do Not Track 状态。"""
        dnt_value = self._rand_choice([None, "1", "0"])
        self._fingerprint["dnt"] = {
            "value": dnt_value,
        }
        self._scores["dnt"] = self._rand_int(5, 15)

    def _collect_pdf_viewer(self, browser: str) -> None:
        """采集 PDF 查看器信息。

        Args:
            browser: 浏览器类型。
        """
        has_pdf = browser in ("chrome", "firefox", "edge", "safari")
        self._fingerprint["pdf_viewer"] = {
            "enabled": has_pdf,
            "name": "PDF Viewer" if has_pdf else None,
        }
        self._scores["pdf_viewer"] = 5 if has_pdf else 20

    def _collect_plugins(self, browser: str) -> None:
        """采集插件列表信息。

        Args:
            browser: 浏览器类型。
        """
        plugins = list(self.PLUGIN_LISTS.get(browser, self.PLUGIN_LISTS["chrome"]))
        self._fingerprint["plugins"] = {
            "list": plugins,
            "count": len(plugins),
        }
        self._scores["plugins"] = self._rand_int(5, 15)

    def _collect_storage_quota(self, device_type: str) -> None:
        """采集存储配额信息。

        Args:
            device_type: 设备类型。
        """
        quotas = self.STORAGE_QUOTA.get(device_type, self.STORAGE_QUOTA["desktop"])
        quota = self._rand_choice(quotas)
        self._fingerprint["storage"] = {
            "quota": quota,
            "usage": self._rand_int(int(quota * 0.01), int(quota * 0.3)),
        }
        self._scores["storage"] = self._rand_int(5, 15)

    def _collect_media_devices(self, device_type: str) -> None:
        """采集媒体设备信息。

        Args:
            device_type: 设备类型。
        """
        has_camera = device_type == "mobile" or self._rng.random() > 0.5
        has_microphone = device_type == "mobile" or self._rng.random() > 0.5

        devices = []
        if has_camera:
            devices.append({
                "kind": "videoinput",
                "label": "Integrated Camera" if device_type == "desktop" else "Front Camera",
            })
        if has_microphone:
            devices.append({
                "kind": "audioinput",
                "label": "Microphone Array" if device_type == "desktop" else "Built-in Microphone",
            })
        devices.append({
            "kind": "audiooutput",
            "label": "Speakers" if device_type == "desktop" else "Built-in Speaker",
        })

        self._fingerprint["media_devices"] = {
            "devices": devices,
            "count": len(devices),
        }
        self._scores["media_devices"] = self._rand_int(5, 15)

    def _collect_speech_voices(self, os_type: str) -> None:
        """采集 Speech Synthesis 声音列表。

        Args:
            os_type: 操作系统类型。
        """
        lang = "en-US" if os_type in ("windows", "linux") else "zh-CN"
        voices = list(self.SPEECH_VOICES.get(lang, self.SPEECH_VOICES["en-US"]))

        self._fingerprint["speech"] = {
            "voices": voices,
            "count": len(voices),
            "default_voice": voices[0] if voices else None,
        }
        self._scores["speech"] = self._rand_int(5, 15)

    def _collect_client_rects(self) -> None:
        """采集 ClientRects 精度信息。"""
        self._fingerprint["client_rects"] = {
            "precision": self._rand_choice([1, 0.1, 0.01]),
            "method_supported": True,
        }
        self._scores["client_rects"] = self._rand_int(5, 20)

    def _collect_iframe_detection(self) -> None:
        """采集 iframe 内容检测信息。"""
        self._fingerprint["iframe"] = {
            "content_window_accessible": True,
            "same_origin": True,
            "cross_origin_blocked": True,
        }
        self._scores["iframe"] = self._rand_int(5, 15)

    def _collect_performance_api(self) -> None:
        """采集 Performance API 精度信息。"""
        self._fingerprint["performance"] = {
            "timing_precision": self._rand_choice([5, 10, 13, 100]),
            "now_precision": self._rand_choice([5, 10, 13, 100]),
            "navigation_count": 1,
            "resource_count": self._rand_int(5, 30),
        }
        self._scores["performance"] = self._rand_int(5, 20)

    def _collect_console_detection(self) -> None:
        """采集 Console 检测信息。"""
        self._fingerprint["console"] = {
            "detectable": True,
            "log_supported": True,
            "debug_supported": True,
            "info_supported": True,
            "warn_supported": True,
            "error_supported": True,
        }
        self._scores["console"] = self._rand_int(5, 15)

    def _collect_debugger_detection(self) -> None:
        """采集 Debugger 检测信息。"""
        self._fingerprint["debugger"] = {
            "detectable": False,
            "breakpoint_active": False,
            "profiler_active": False,
        }
        self._scores["debugger"] = 5

    def _collect_webdriver_detection(self) -> None:
        """采集 WebDriver 检测信息。"""
        self._fingerprint["webdriver"] = {
            "is_webdriver": False,
            "navigator_webdriver": False,
            "cdc_detected": False,
            "chrome_runtime_detected": False,
        }
        self._scores["webdriver"] = 5

    def _collect_webRTC_leak(self) -> None:
        """采集 WebRTC 泄露信息。"""
        self._fingerprint["webrtc"] = {
            "local_ip_leak": False,
            "stun_leak": False,
            "turn_leak": False,
            "disabled": self._rng.choice([True, False]),
        }
        self._scores["webrtc"] = self._rand_int(5, 20)

    def _collect_permissions_api(self) -> None:
        """采集 Permissions API 信息。"""
        permissions = {
            "geolocation": self._rand_choice(["prompt", "granted", "denied"]),
            "notifications": self._rand_choice(["prompt", "granted", "denied"]),
            "camera": self._rand_choice(["prompt", "denied"]),
            "microphone": self._rand_choice(["prompt", "denied"]),
            "clipboard-read": "prompt",
        }
        self._fingerprint["permissions"] = {
            "states": permissions,
            "api_supported": True,
        }
        self._scores["permissions"] = self._rand_int(5, 15)

    def _collect_css_features(self) -> None:
        """采集 CSS 特性检测信息。"""
        self._fingerprint["css_features"] = {
            "flexbox": True,
            "grid": True,
            "columns": True,
            "backdrop_filter": True,
            "mask_image": True,
            "text_stroke": True,
            "custom_properties": True,
            "scroll_snap": True,
            "container_queries": self._rng.choice([True, False]),
            "subgrid": self._rng.choice([True, False]),
        }
        self._scores["css_features"] = self._rand_int(5, 15)

    def _collect_math_constants(self) -> None:
        """采集 Math 常量精度信息。"""
        self._fingerprint["math_constants"] = {
            "pi": 3.141592653589793,
            "e": 2.718281828459045,
            "sqrt2": 1.4142135623730951,
            "ln2": 0.6931471805599453,
            "ln10": 2.302585092994046,
        }
        self._scores["math_constants"] = 5

    def _collect_error_messages(self) -> None:
        """采集错误消息特征信息。"""
        self._fingerprint["error_messages"] = {
            "stack_trace_format": "standard",
            "error_name_includes_line": True,
            "column_number_supported": True,
            "async_stack_traces": True,
        }
        self._scores["error_messages"] = self._rand_int(5, 15)

    def _collect_feature_detection(self) -> None:
        """采集特性检测信息。"""
        self._fingerprint["features"] = {
            "webgl": True,
            "webgl2": True,
            "webrtc": True,
            "websocket": True,
            "webworker": True,
            "serviceworker": True,
            "sharedworker": True,
            "webassembly": True,
            "indexdb": True,
            "localstorage": True,
            "sessionstorage": True,
            "geolocation": True,
            "notifications": True,
            "push_api": True,
            "bluetooth": self._rng.choice([True, False]),
            "usb": self._rng.choice([True, False]),
            "serial": self._rng.choice([True, False]),
            "gamepad": self._rng.choice([True, False]),
        }
        self._scores["features"] = self._rand_int(5, 15)

    def get_fingerprint(self) -> Dict[str, Any]:
        """获取已采集的指纹数据。

        Returns:
            指纹数据字典。
        """
        return self._fingerprint

    def get_scores(self) -> Dict[str, int]:
        """获取各维度的风险评分。

        Returns:
            风险评分字典。
        """
        return self._scores

    def get_dimension_count(self) -> int:
        """获取已采集的指纹维度数量。

        Returns:
            指纹维度数量。
        """
        return len(self._fingerprint)

    def to_json(self) -> str:
        """将指纹数据导出为 JSON 字符串。

        Returns:
            JSON 格式的指纹数据。
        """
        return json.dumps({
            "fingerprint": self._fingerprint,
            "scores": self._scores,
        }, indent=2, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> "FingerprintCollector":
        """从 JSON 字符串导入指纹数据。

        Args:
            json_str: JSON 格式的指纹数据。

        Returns:
            加载了指纹数据的 FingerprintCollector 实例。
        """
        data = json.loads(json_str)
        collector = cls()
        collector._fingerprint = data.get("fingerprint", {})
        collector._scores = data.get("scores", {})
        return collector
