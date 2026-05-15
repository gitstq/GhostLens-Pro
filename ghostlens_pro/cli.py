"""
GhostLens-Pro CLI 主入口

使用 argparse 实现完整的命令行界面，支持指纹采集、评分、
配置生成、一致性校验、指纹对比和 TUI 仪表板等功能。
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional

from . import __version__
from .fingerprint_collector import FingerprintCollector
from .detection_scorer import DetectionScorer
from .profile_generator import ProfileGenerator
from .consistency_checker import ConsistencyChecker
from .fingerprint_comparator import FingerprintComparator


def cmd_scan(args: argparse.Namespace) -> int:
    """执行指纹采集与评分命令。

    Args:
        args: 命令行参数。

    Returns:
        退出码。
    """
    verbose = args.verbose
    quiet = args.quiet

    if not quiet:
        print("GhostLens-Pro - Fingerprint Scanner")
        print("=" * 50)

    collector = FingerprintCollector(seed=args.seed)
    if verbose:
        print(f"[*] Collecting fingerprints (OS: {args.os}, Browser: {args.browser}, Device: {args.device})...")

    fingerprint_data = collector.collect_all(
        os_type=args.os,
        browser=args.browser,
        device_type=args.device,
    )

    if verbose:
        print(f"[*] Collected {collector.get_dimension_count()} fingerprint dimensions")

    # 评分
    scorer = DetectionScorer()
    report = scorer.score(fingerprint_data)

    # 一致性校验
    checker = ConsistencyChecker()
    consistency = checker.check(fingerprint_data)

    # 输出结果
    if args.json:
        output = {
            "fingerprint": fingerprint_data,
            "score_report": report,
            "consistency": consistency,
        }
        _output_json(output, args.output)
    elif args.html:
        _output_html(scorer.to_html(), args.output)
    else:
        if not quiet:
            print(scorer.summary_text())
            print()
            print(checker.summary_text())

    return 0


def cmd_score(args: argparse.Namespace) -> int:
    """执行评分分析命令。

    Args:
        args: 命令行参数。

    Returns:
        退出码。
    """
    if not args.input:
        print("Error: --input is required for score command", file=sys.stderr)
        return 1

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            fingerprint_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        return 1

    scorer = DetectionScorer()
    report = scorer.score(fingerprint_data)

    if args.json:
        _output_json(report, args.output)
    elif args.html:
        _output_html(scorer.to_html(), args.output)
    else:
        print(scorer.summary_text())

    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    """执行指纹配置生成命令。

    Args:
        args: 命令行参数。

    Returns:
        退出码。
    """
    quiet = args.quiet

    gen = ProfileGenerator(seed=args.seed)

    try:
        profile = gen.generate(
            template_name=args.template,
            browser=args.browser,
            os_type=args.os,
            device_type=args.device,
            randomize=not args.no_randomize,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json or not args.output:
        output_path = args.output
        if output_path:
            gen.export_json(profile, output_path)
            if not quiet:
                print(f"Profile saved to: {output_path}")
        else:
            print(json.dumps(profile, indent=2, ensure_ascii=False))
    else:
        gen.export_json(profile, args.output)
        if not quiet:
            print(f"Profile saved to: {args.output}")

    return 0


def cmd_check(args: argparse.Namespace) -> int:
    """执行一致性校验命令。

    Args:
        args: 命令行参数。

    Returns:
        退出码。
    """
    if not args.input:
        print("Error: --input is required for check command", file=sys.stderr)
        return 1

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            fingerprint_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        return 1

    checker = ConsistencyChecker()
    result = checker.check(fingerprint_data)

    if args.json:
        _output_json(result, args.output)
    else:
        print(checker.summary_text())

    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    """执行指纹对比命令。

    Args:
        args: 命令行参数。

    Returns:
        退出码。
    """
    if not args.file1 or not args.file2:
        print("Error: --file1 and --file2 are required for compare command", file=sys.stderr)
        return 1

    try:
        with open(args.file1, "r", encoding="utf-8") as f:
            fp1 = json.load(f)
        with open(args.file2, "r", encoding="utf-8") as f:
            fp2 = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: File not found: {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        return 1

    comparator = FingerprintComparator()
    result = comparator.compare(fp1, fp2, args.name1, args.name2)

    if args.json:
        _output_json(result, args.output)
    else:
        print(comparator.summary_text())

    return 0


def cmd_dashboard(args: argparse.Namespace) -> int:
    """启动 TUI 仪表板命令。

    Args:
        args: 命令行参数。

    Returns:
        退出码。
    """
    from .tui_dashboard import TUIDashboard
    dashboard = TUIDashboard()
    dashboard.run()
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    """生成报告命令。

    Args:
        args: 命令行参数。

    Returns:
        退出码。
    """
    # 执行完整采集和评分
    collector = FingerprintCollector(seed=args.seed)
    fingerprint_data = collector.collect_all(
        os_type=args.os,
        browser=args.browser,
        device_type=args.device,
    )

    scorer = DetectionScorer()
    report = scorer.score(fingerprint_data)

    checker = ConsistencyChecker()
    consistency = checker.check(fingerprint_data)

    if args.html:
        _output_html(scorer.to_html(), args.output or "report.html")
    elif args.json:
        full_report = {
            "fingerprint": fingerprint_data,
            "score_report": report,
            "consistency": consistency,
        }
        _output_json(full_report, args.output or "report.json")
    else:
        print(scorer.summary_text())
        print()
        print(checker.summary_text())

    return 0


def cmd_list_profiles(args: argparse.Namespace) -> int:
    """列出内置配置模板命令。

    Args:
        args: 命令行参数。

    Returns:
        退出码。
    """
    gen = ProfileGenerator()
    templates = gen.list_templates()

    if args.json:
        _output_json(templates, args.output)
    else:
        print("GhostLens-Pro - Built-in Profile Templates")
        print("=" * 60)
        print(f"{'ID':<25} {'Browser':<10} {'OS':<10} {'Device':<10}")
        print("-" * 60)
        for tmpl in templates:
            print(f"{tmpl['id']:<25} {tmpl['browser']:<10} {tmpl['os_type']:<10} {tmpl['device_type']:<10}")
        print()
        print(f"Total: {len(templates)} templates")
        print()
        print("Usage: ghostlens-pro generate --template <ID>")

    return 0


def _output_json(data: Any, filepath: Optional[str] = None) -> None:
    """输出 JSON 数据。

    Args:
        data: 要输出的数据。
        filepath: 输出文件路径。如果为None，输出到stdout。
    """
    content = json.dumps(data, indent=2, ensure_ascii=False)
    if filepath:
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"JSON report saved to: {filepath}")
    else:
        print(content)


def _output_html(content: str, filepath: Optional[str] = None) -> None:
    """输出 HTML 数据。

    Args:
        content: HTML 内容。
        filepath: 输出文件路径。如果为None，输出到stdout。
    """
    if filepath:
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"HTML report saved to: {filepath}")
    else:
        print(content)


def build_parser() -> argparse.ArgumentParser:
    """构建 CLI 参数解析器。

    Returns:
        配置好的 ArgumentParser 实例。
    """
    parser = argparse.ArgumentParser(
        prog="ghostlens-pro",
        description="GhostLens-Pro - Lightweight Browser Fingerprint Manager & Anti-Detection Engine",
        epilog="Example: ghostlens-pro scan --os windows --browser chrome",
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    # 全局选项（放在子命令之前）
    parser.add_argument("--json", action="store_true", default=False,
                        help="Output in JSON format")
    parser.add_argument("--html", action="store_true", default=False,
                        help="Output in HTML format")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Output file path")
    parser.add_argument("--verbose", "-v", action="store_true", default=False,
                        help="Verbose output")
    parser.add_argument("--quiet", "-q", action="store_true", default=False,
                        help="Quiet mode, suppress non-error output")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # scan 命令
    scan_parser = subparsers.add_parser("scan", help="Execute fingerprint collection and scoring")
    scan_parser.add_argument("--os", type=str, default="windows",
                             choices=["windows", "macos", "linux", "ios", "android"],
                             help="Target operating system")
    scan_parser.add_argument("--browser", type=str, default="chrome",
                             choices=["chrome", "firefox", "safari", "edge"],
                             help="Target browser")
    scan_parser.add_argument("--device", type=str, default="desktop",
                             choices=["desktop", "mobile"],
                             help="Target device type")
    scan_parser.add_argument("--seed", type=int, default=None,
                             help="Random seed for reproducible results")

    # score 命令
    score_parser = subparsers.add_parser("score", help="Score an existing fingerprint profile")
    score_parser.add_argument("--input", "-i", type=str, required=True,
                              help="Input fingerprint JSON file")

    # generate 命令
    gen_parser = subparsers.add_parser("generate", help="Generate a fingerprint profile")
    gen_parser.add_argument("--template", "-t", type=str, default=None,
                            help="Profile template name")
    gen_parser.add_argument("--os", type=str, default=None,
                            choices=["windows", "macos", "linux", "ios", "android"],
                            help="Target operating system")
    gen_parser.add_argument("--browser", type=str, default=None,
                            choices=["chrome", "firefox", "safari", "edge"],
                            help="Target browser")
    gen_parser.add_argument("--device", type=str, default=None,
                            choices=["desktop", "mobile"],
                            help="Target device type")
    gen_parser.add_argument("--seed", type=int, default=None,
                            help="Random seed for reproducible results")
    gen_parser.add_argument("--no-randomize", action="store_true", default=False,
                            help="Disable non-critical parameter randomization")

    # check 命令
    check_parser = subparsers.add_parser("check", help="Check fingerprint consistency")
    check_parser.add_argument("--input", "-i", type=str, required=True,
                              help="Input fingerprint JSON file")

    # compare 命令
    compare_parser = subparsers.add_parser("compare", help="Compare two fingerprint profiles")
    compare_parser.add_argument("--file1", "-f1", type=str, required=True,
                                help="First fingerprint JSON file")
    compare_parser.add_argument("--file2", "-f2", type=str, required=True,
                                help="Second fingerprint JSON file")
    compare_parser.add_argument("--name1", type=str, default="Fingerprint A",
                                help="Name for first fingerprint")
    compare_parser.add_argument("--name2", type=str, default="Fingerprint B",
                                help="Name for second fingerprint")

    # dashboard 命令
    subparsers.add_parser("dashboard", help="Launch TUI dashboard")

    # report 命令
    report_parser = subparsers.add_parser("report", help="Generate a full report")
    report_parser.add_argument("--os", type=str, default="windows",
                               choices=["windows", "macos", "linux", "ios", "android"],
                               help="Target operating system")
    report_parser.add_argument("--browser", type=str, default="chrome",
                               choices=["chrome", "firefox", "safari", "edge"],
                               help="Target browser")
    report_parser.add_argument("--device", type=str, default="desktop",
                               choices=["desktop", "mobile"],
                               help="Target device type")
    report_parser.add_argument("--seed", type=int, default=None,
                               help="Random seed for reproducible results")

    # list-profiles 命令
    subparsers.add_parser("list-profiles", help="List built-in profile templates")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """CLI 主入口函数。

    Args:
        argv: 命令行参数列表。如果为None，使用 sys.argv。

    Returns:
        退出码。
    """
    parser = build_parser()

    # 使用 parse_known_args 处理全局选项和子命令参数的混合
    if argv is None:
        argv = sys.argv[1:]

    # 分离全局选项和子命令参数
    global_options = {"--json": False, "--html": False, "--output": None,
                      "--verbose": False, "--quiet": False,
                      "-o": None, "-v": False, "-q": False}

    filtered_argv = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("--json",):
            global_options["--json"] = True
        elif arg in ("--html",):
            global_options["--html"] = True
        elif arg in ("--verbose", "-v"):
            global_options["--verbose"] = True
        elif arg in ("--quiet", "-q"):
            global_options["--quiet"] = True
        elif arg in ("--output", "-o"):
            if i + 1 < len(argv):
                global_options["--output"] = argv[i + 1]
                i += 1
        else:
            filtered_argv.append(arg)
        i += 1

    args = parser.parse_args(filtered_argv)

    # 将全局选项注入到 args 中
    args.json = global_options["--json"] or getattr(args, "json", False)
    args.html = global_options["--html"] or getattr(args, "html", False)
    args.output = global_options["--output"] or getattr(args, "output", None)
    args.verbose = global_options["--verbose"] or getattr(args, "verbose", False)
    args.quiet = global_options["--quiet"] or getattr(args, "quiet", False)

    if not args.command:
        parser.print_help()
        return 0

    command_map = {
        "scan": cmd_scan,
        "score": cmd_score,
        "generate": cmd_generate,
        "check": cmd_check,
        "compare": cmd_compare,
        "dashboard": cmd_dashboard,
        "report": cmd_report,
        "list-profiles": cmd_list_profiles,
    }

    handler = command_map.get(args.command)
    if handler:
        try:
            return handler(args)
        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            return 130
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 1
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
