"""
GhostLens-Pro TUI 仪表板

使用标准库 curses 实现终端 UI 仪表板，提供实时指纹采集进度、
可视化评分结果和交互式菜单导航。
"""

import curses
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

from .fingerprint_collector import FingerprintCollector
from .detection_scorer import DetectionScorer
from .profile_generator import ProfileGenerator
from .consistency_checker import ConsistencyChecker


class TUIDashboard:
    """TUI 仪表板，使用 curses 实现终端用户界面。"""

    # 颜色对定义
    COLOR_PAIRS = {
        "header": 1,
        "highlight": 2,
        "success": 3,
        "warning": 4,
        "danger": 5,
        "info": 6,
        "progress_bar": 7,
        "progress_bg": 8,
        "menu_selected": 9,
        "menu_normal": 10,
        "border": 11,
        "grade_a_plus": 12,
        "grade_a": 13,
        "grade_b": 14,
        "grade_c": 15,
        "grade_d": 16,
    }

    def __init__(self) -> None:
        """初始化 TUI 仪表板。"""
        self._stdscr: Optional[Any] = None
        self._current_menu_index: int = 0
        self._current_view: str = "main_menu"
        self._fingerprint_data: Optional[Dict[str, Any]] = None
        self._score_report: Optional[Dict[str, Any]] = None
        self._consistency_result: Optional[Dict[str, Any]] = None
        self._scroll_offset: int = 0
        self._status_message: str = ""
        self._status_time: float = 0

    def run(self) -> None:
        """启动 TUI 仪表板主循环。"""
        try:
            self._stdscr = curses.initscr()
            curses.start_color()
            curses.use_default_colors()
            curses.cbreak()
            curses.noecho()
            curses.curs_set(0)
            self._stdscr.keypad(True)
            self._stdscr.timeout(100)

            self._init_colors()
            self._main_loop()
        except curses.error as e:
            # curses 不可用时回退到简单文本模式
            self._fallback_mode(str(e))
        finally:
            self._cleanup()

    def _init_colors(self) -> None:
        """初始化颜色对。"""
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)       # header
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)        # highlight
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)       # success
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)      # warning
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)         # danger
        curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)        # info
        curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)       # progress_bar
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)       # progress_bg
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_WHITE)       # menu_selected
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)      # menu_normal
        curses.init_pair(11, curses.COLOR_BLUE, curses.COLOR_BLACK)       # border
        curses.init_pair(12, curses.COLOR_GREEN, curses.COLOR_BLACK)      # grade_a_plus
        curses.init_pair(13, curses.COLOR_CYAN, curses.COLOR_BLACK)       # grade_a
        curses.init_pair(14, curses.COLOR_YELLOW, curses.COLOR_BLACK)     # grade_b
        curses.init_pair(15, curses.COLOR_MAGENTA, curses.COLOR_BLACK)    # grade_c
        curses.init_pair(16, curses.COLOR_RED, curses.COLOR_BLACK)        # grade_d

    def _cleanup(self) -> None:
        """清理 curses 环境。"""
        try:
            if self._stdscr:
                curses.nocbreak()
                self._stdscr.keypad(False)
                curses.echo()
                curses.curs_set(1)
                curses.endwin()
        except curses.error:
            pass

    def _main_loop(self) -> None:
        """TUI 主循环。"""
        while True:
            self._draw()
            key = self._stdscr.getch()

            if key == ord('q') or key == 27:  # q or ESC
                break
            elif key == curses.KEY_UP:
                self._handle_up()
            elif key == curses.KEY_DOWN:
                self._handle_down()
            elif key == curses.KEY_LEFT:
                self._handle_left()
            elif key == curses.KEY_RIGHT:
                self._handle_right()
            elif key == ord('\n') or key == curses.KEY_ENTER:
                self._handle_enter()
            elif key == ord('r'):
                self._current_view = "main_menu"
                self._current_menu_index = 0
            elif key == ord('s'):
                self._current_view = "score_view"
            elif key == ord('f'):
                self._current_view = "fingerprint_view"
            elif key == ord('c'):
                self._current_view = "consistency_view"
            elif key == ord('h'):
                self._current_view = "help_view"

    def _handle_up(self) -> None:
        """处理向上导航。"""
        if self._current_view == "main_menu":
            self._current_menu_index = max(0, self._current_menu_index - 1)
        elif self._scroll_offset > 0:
            self._scroll_offset -= 1

    def _handle_down(self) -> None:
        """处理向下导航。"""
        if self._current_view == "main_menu":
            self._current_menu_index = min(5, self._current_menu_index + 1)
        else:
            self._scroll_offset += 1

    def _handle_left(self) -> None:
        """处理向左导航。"""
        if self._current_view != "main_menu":
            self._current_view = "main_menu"
            self._current_menu_index = 0

    def _handle_right(self) -> None:
        """处理向右导航。"""
        pass

    def _handle_enter(self) -> None:
        """处理回车键。"""
        if self._current_view == "main_menu":
            self._execute_menu_action(self._current_menu_index)

    def _execute_menu_action(self, index: int) -> None:
        """执行菜单操作。

        Args:
            index: 菜单项索引。
        """
        if index == 0:
            self._action_scan()
        elif index == 1:
            self._action_generate()
        elif index == 2:
            if self._fingerprint_data:
                self._current_view = "score_view"
            else:
                self._set_status("请先执行指纹采集 (Scan)")
        elif index == 3:
            if self._fingerprint_data:
                self._current_view = "consistency_view"
            else:
                self._set_status("请先执行指纹采集 (Scan)")
        elif index == 4:
            self._current_view = "fingerprint_view"
        elif index == 5:
            self._current_view = "help_view"

    def _action_scan(self) -> None:
        """执行指纹采集操作。"""
        self._set_status("正在采集指纹...")
        self._draw()

        collector = FingerprintCollector()
        self._fingerprint_data = collector.collect_all()

        scorer = DetectionScorer()
        self._score_report = scorer.score(self._fingerprint_data)

        checker = ConsistencyChecker()
        self._consistency_result = checker.check(self._fingerprint_data)

        score = self._score_report.get("overall_score", 0)
        grade = self._score_report.get("grade", "N/A")
        self._set_status(f"采集完成! 评分: {score}/100 ({grade})")
        self._current_view = "score_view"

    def _action_generate(self) -> None:
        """执行指纹生成操作。"""
        self._set_status("正在生成指纹配置...")
        self._draw()

        gen = ProfileGenerator()
        self._fingerprint_data = gen.generate(template_name="chrome_win10", randomize=True)

        scorer = DetectionScorer()
        self._score_report = scorer.score(self._fingerprint_data)

        checker = ConsistencyChecker()
        self._consistency_result = checker.check(self._fingerprint_data)

        score = self._score_report.get("overall_score", 0)
        grade = self._score_report.get("grade", "N/A")
        self._set_status(f"生成完成! 评分: {score}/100 ({grade})")
        self._current_view = "score_view"

    def _set_status(self, message: str) -> None:
        """设置状态栏消息。

        Args:
            message: 状态消息。
        """
        self._status_message = message
        self._status_time = time.time()

    def _draw(self) -> None:
        """绘制当前视图。"""
        if not self._stdscr:
            return

        self._stdscr.clear()
        max_y, max_x = self._stdscr.getmaxyx()

        if self._current_view == "main_menu":
            self._draw_main_menu(max_y, max_x)
        elif self._current_view == "score_view":
            self._draw_score_view(max_y, max_x)
        elif self._current_view == "fingerprint_view":
            self._draw_fingerprint_view(max_y, max_x)
        elif self._current_view == "consistency_view":
            self._draw_consistency_view(max_y, max_x)
        elif self._current_view == "help_view":
            self._draw_help_view(max_y, max_x)

        self._draw_status_bar(max_y, max_x)
        self._stdscr.refresh()

    def _draw_main_menu(self, max_y: int, max_x: int) -> None:
        """绘制主菜单。

        Args:
            max_y: 终端最大行数。
            max_x: 终端最大列数。
        """
        # 标题
        title = "GhostLens-Pro - Browser Fingerprint Manager"
        self._draw_centered_text(max_y // 2 - 8, title, self.COLOR_PAIRS["header"])

        subtitle = "Lightweight Anti-Detection Engine v1.0.0"
        self._draw_centered_text(max_y // 2 - 6, subtitle, self.COLOR_PAIRS["info"])

        # 菜单项
        menu_items = [
            "[1] Scan Fingerprint",
            "[2] Generate Profile",
            "[3] View Score Report",
            "[4] View Consistency Check",
            "[5] View Fingerprint Data",
            "[6] Help",
        ]

        start_y = max_y // 2 - 3
        for i, item in enumerate(menu_items):
            y = start_y + i
            if i == self._current_menu_index:
                color = self.COLOR_PAIRS["menu_selected"]
                self._draw_centered_text(y, f"  > {item}  ", color)
            else:
                color = self.COLOR_PAIRS["menu_normal"]
                self._draw_centered_text(y, f"    {item}  ", color)

        # 底部提示
        hint = "Use UP/DOWN to navigate, ENTER to select, Q to quit"
        self._draw_centered_text(max_y - 4, hint, self.COLOR_PAIRS["info"])

    def _draw_score_view(self, max_y: int, max_x: int) -> None:
        """绘制评分视图。

        Args:
            max_y: 终端最大行数。
            max_x: 终端最大列数。
        """
        self._draw_header("Score Report")

        if not self._score_report:
            self._draw_centered_text(max_y // 2, "No score data available. Press S to scan first.",
                                     self.COLOR_PAIRS["warning"])
            return

        score = self._score_report.get("overall_score", 0)
        grade = self._score_report.get("grade", "N/A")
        grade_desc = self._score_report.get("grade_description", "")

        # 评分圆圈（文本表示）
        y = 3
        score_text = f"Overall Score: {score}/100  Grade: {grade} ({grade_desc})"
        grade_color = self._get_grade_color(grade)
        self._stdscr.addstr(y, 2, score_text, curses.color_pair(grade_color))

        # 进度条
        y += 2
        bar_width = min(max_x - 4, 60)
        self._draw_progress_bar(y, 2, bar_width, score / 100.0)

        # 风险分类
        y += 3
        self._stdscr.addstr(y, 2, "Risk Categories:", curses.color_pair(self.COLOR_PAIRS["header"]))
        y += 1

        category_names = {
            "automation_detection": "Automation Detection",
            "fingerprint_uniqueness": "Fingerprint Uniqueness",
            "behavioral_analysis": "Behavioral Analysis",
            "network_characteristics": "Network Characteristics",
        }

        for cat_key, cat_data in self._score_report.get("category_scores", {}).items():
            if y >= max_y - 3:
                break
            cat_name = category_names.get(cat_key, cat_key)
            anti_score = cat_data.get("anti_detection_score", 0)
            self._stdscr.addstr(y, 4, f"{cat_name}:", curses.color_pair(self.COLOR_PAIRS["info"]))
            bar_x = 35
            bar_w = min(max_x - bar_x - 4, 30)
            self._draw_progress_bar(y, bar_x, bar_w, anti_score / 100.0)
            self._stdscr.addstr(y, bar_x + bar_w + 2, f"{anti_score:.0f}%",
                                curses.color_pair(self.COLOR_PAIRS["menu_normal"]))
            y += 1

        # 高风险维度
        y += 1
        if y < max_y - 3:
            self._stdscr.addstr(y, 2, "High Risk Dimensions (score > 30):",
                                curses.color_pair(self.COLOR_PAIRS["danger"]))
            y += 1
            for dim in self._score_report.get("dimension_details", []):
                if y >= max_y - 3:
                    break
                if dim["risk_score"] > 30:
                    risk_color = self.COLOR_PAIRS["danger"] if dim["risk_score"] > 50 else self.COLOR_PAIRS["warning"]
                    self._stdscr.addstr(y, 4, f"{dim['dimension']}: risk={dim['risk_score']}, anti_detect={dim['anti_detection_score']}",
                                        curses.color_pair(risk_color))
                    y += 1

    def _draw_fingerprint_view(self, max_y: int, max_x: int) -> None:
        """绘制指纹数据视图。

        Args:
            max_y: 终端最大行数。
            max_x: 终端最大列数。
        """
        self._draw_header("Fingerprint Data")

        if not self._fingerprint_data:
            self._draw_centered_text(max_y // 2, "No fingerprint data. Press S to scan first.",
                                     self.COLOR_PAIRS["warning"])
            return

        fingerprint = self._fingerprint_data.get("fingerprint", {})
        y = 3
        for key, value in fingerprint.items():
            if y >= max_y - 3:
                break
            if isinstance(value, dict):
                display_val = str(value)[:max_x - 30]
            else:
                display_val = str(value)[:max_x - 30]
            self._stdscr.addstr(y, 2, f"{key}:", curses.color_pair(self.COLOR_PAIRS["info"]))
            self._stdscr.addstr(y, 25, display_val, curses.color_pair(self.COLOR_PAIRS["menu_normal"]))
            y += 1

    def _draw_consistency_view(self, max_y: int, max_x: int) -> None:
        """绘制一致性校验视图。

        Args:
            max_y: 终端最大行数。
            max_x: 终端最大列数。
        """
        self._draw_header("Consistency Check")

        if not self._consistency_result:
            self._draw_centered_text(max_y // 2, "No consistency data. Press S to scan first.",
                                     self.COLOR_PAIRS["warning"])
            return

        score = self._consistency_result.get("consistency_score", 0)
        grade = self._consistency_result.get("grade", "unknown")

        y = 3
        grade_color = self.COLOR_PAIRS["success"] if score >= 85 else self.COLOR_PAIRS["warning"] if score >= 70 else self.COLOR_PAIRS["danger"]
        self._stdscr.addstr(y, 2, f"Consistency Score: {score}/100 (Grade: {grade})",
                            curses.color_pair(grade_color))

        # 进度条
        y += 2
        bar_width = min(max_x - 4, 60)
        self._draw_progress_bar(y, 2, bar_width, score / 100.0)

        # 检查结果
        y += 2
        checks = self._consistency_result.get("checks", {})
        self._stdscr.addstr(y, 2, "Check Results:", curses.color_pair(self.COLOR_PAIRS["header"]))
        y += 1

        for check_name, check_data in checks.items():
            if y >= max_y - 3:
                break
            passed = check_data.get("passed", False)
            status = "PASS" if passed else "FAIL"
            color = self.COLOR_PAIRS["success"] if passed else self.COLOR_PAIRS["danger"]
            self._stdscr.addstr(y, 4, f"[{status}] {check_name}", curses.color_pair(color))
            y += 1

        # 问题列表
        issues = self._consistency_result.get("issues", [])
        if issues and y < max_y - 3:
            y += 1
            self._stdscr.addstr(y, 2, f"Issues Found: {len(issues)}",
                                curses.color_pair(self.COLOR_PAIRS["warning"]))
            y += 1
            for issue in issues:
                if y >= max_y - 3:
                    break
                severity = issue.get("severity", "info")
                desc = issue.get("description", "")[:max_x - 20]
                color = self.COLOR_PAIRS["danger"] if severity == "critical" else self.COLOR_PAIRS["warning"]
                self._stdscr.addstr(y, 4, f"[{severity.upper()}] {desc}", curses.color_pair(color))
                y += 1

    def _draw_help_view(self, max_y: int, max_x: int) -> None:
        """绘制帮助视图。

        Args:
            max_y: 终端最大行数。
            max_x: 终端最大列数。
        """
        self._draw_header("Help - Keyboard Shortcuts")

        help_items = [
            ("UP/DOWN", "Navigate menu items / Scroll content"),
            ("ENTER", "Select menu item"),
            ("S", "Scan fingerprint"),
            ("F", "View fingerprint data"),
            ("C", "View consistency check"),
            ("R", "Return to main menu"),
            ("H", "Show this help"),
            ("Q / ESC", "Quit"),
        ]

        y = 3
        for key, desc in help_items:
            if y >= max_y - 3:
                break
            self._stdscr.addstr(y, 4, f"{key:>12}", curses.color_pair(self.COLOR_PAIRS["highlight"]))
            self._stdscr.addstr(y, 18, f" - {desc}", curses.color_pair(self.COLOR_PAIRS["menu_normal"]))
            y += 1

    def _draw_header(self, title: str) -> None:
        """绘制视图标题栏。

        Args:
            title: 标题文本。
        """
        if not self._stdscr:
            return
        max_x = self._stdscr.getmaxyx()[1]
        header_text = f" {title} "
        self._stdscr.addstr(0, 0, header_text, curses.color_pair(self.COLOR_PAIRS["header"]))
        # 填充剩余空间
        remaining = max_x - len(header_text)
        if remaining > 0:
            self._stdscr.addstr(0, len(header_text), "-" * remaining,
                                curses.color_pair(self.COLOR_PAIRS["border"]))

    def _draw_status_bar(self, max_y: int, max_x: int) -> None:
        """绘制底部状态栏。

        Args:
            max_y: 终端最大行数。
            max_x: 终端最大列数。
        """
        if not self._stdscr:
            return

        y = max_y - 1
        status = self._status_message or "Ready | Press H for help, Q to quit"
        status = status[:max_x - 2]
        self._stdscr.addstr(y, 0, status, curses.color_pair(self.COLOR_PAIRS["info"]))

    def _draw_centered_text(self, y: int, text: str, color_pair: int) -> None:
        """绘制居中文本。

        Args:
            y: 行号。
            text: 文本内容。
            color_pair: 颜色对。
        """
        if not self._stdscr:
            return
        max_x = self._stdscr.getmaxyx()[1]
        x = max(0, (max_x - len(text)) // 2)
        try:
            self._stdscr.addstr(y, x, text, curses.color_pair(color_pair))
        except curses.error:
            pass

    def _draw_progress_bar(self, y: int, x: int, width: int, ratio: float) -> None:
        """绘制进度条。

        Args:
            y: 行号。
            x: 列号。
            width: 进度条宽度。
            ratio: 填充比例 (0.0-1.0)。
        """
        if not self._stdscr:
            return
        ratio = max(0.0, min(1.0, ratio))
        filled = int(width * ratio)
        empty = width - filled

        # 背景条
        if empty > 0:
            try:
                self._stdscr.addstr(y, x, " " * empty, curses.color_pair(self.COLOR_PAIRS["progress_bg"]))
            except curses.error:
                pass

        # 填充条
        if filled > 0:
            color = self.COLOR_PAIRS["success"] if ratio >= 0.85 else self.COLOR_PAIRS["warning"] if ratio >= 0.7 else self.COLOR_PAIRS["danger"]
            try:
                self._stdscr.addstr(y, x, "#" * filled, curses.color_pair(color))
            except curses.error:
                pass

    def _get_grade_color(self, grade: str) -> int:
        """根据评分等级获取颜色对。

        Args:
            grade: 评分等级。

        Returns:
            颜色对编号。
        """
        grade_colors = {
            "A+": self.COLOR_PAIRS["grade_a_plus"],
            "A": self.COLOR_PAIRS["grade_a"],
            "B": self.COLOR_PAIRS["grade_b"],
            "C": self.COLOR_PAIRS["grade_c"],
            "D": self.COLOR_PAIRS["grade_d"],
        }
        return grade_colors.get(grade, self.COLOR_PAIRS["menu_normal"])

    def _fallback_mode(self, error: str) -> None:
        """curses 不可用时的回退模式。

        Args:
            error: 错误信息。
        """
        print(f"\nGhostLens-Pro TUI Dashboard")
        print(f"=" * 50)
        print(f"Warning: TUI mode unavailable: {error}")
        print(f"Falling back to text mode...\n")

        # 执行指纹采集
        print("Collecting fingerprint...")
        collector = FingerprintCollector()
        self._fingerprint_data = collector.collect_all()

        scorer = DetectionScorer()
        self._score_report = scorer.score(self._fingerprint_data)
        print(scorer.summary_text())

        checker = ConsistencyChecker()
        self._consistency_result = checker.check(self._fingerprint_data)
        print()
        print(checker.summary_text())
