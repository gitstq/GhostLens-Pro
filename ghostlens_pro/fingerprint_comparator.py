"""
GhostLens-Pro 指纹对比分析器

对比两个指纹配置的差异，计算指纹相似度百分比，
识别高风险差异维度，生成对比报告。
"""

import json
import time
from typing import Any, Dict, List, Optional, Tuple


class FingerprintComparator:
    """指纹对比分析器，负责对比和分析指纹配置之间的差异。"""

    # 各维度的权重（对指纹唯一性的贡献度）
    DIMENSION_WEIGHTS: Dict[str, float] = {
        "user_agent": 0.12,
        "canvas": 0.10,
        "webgl": 0.08,
        "fonts": 0.07,
        "audio": 0.06,
        "screen": 0.06,
        "platform": 0.05,
        "timezone": 0.04,
        "language": 0.04,
        "hardware": 0.04,
        "webgl": 0.08,
        "plugins": 0.03,
        "touch": 0.03,
        "storage": 0.02,
        "connection": 0.02,
        "cookies": 0.02,
        "dnt": 0.01,
        "pdf_viewer": 0.01,
        "media_devices": 0.02,
        "speech": 0.02,
        "client_rects": 0.02,
        "performance": 0.02,
        "webrtc": 0.02,
        "permissions": 0.01,
        "css_features": 0.01,
        "math_constants": 0.01,
        "error_messages": 0.01,
        "features": 0.01,
        "iframe": 0.01,
        "console": 0.01,
        "debugger": 0.01,
        "webdriver": 0.01,
        "battery": 0.01,
    }

    # 高风险差异维度
    HIGH_RISK_DIMENSIONS: List[str] = [
        "user_agent", "canvas", "webgl", "fonts", "audio",
        "platform", "screen", "hardware",
    ]

    def __init__(self) -> None:
        """初始化指纹对比分析器。"""
        self._result: Dict[str, Any] = {}

    def compare(self, fp1: Dict[str, Any], fp2: Dict[str, Any],
                name1: str = "Fingerprint A", name2: str = "Fingerprint B") -> Dict[str, Any]:
        """对比两个指纹配置。

        Args:
            fp1: 第一个指纹数据字典。
            fp2: 第二个指纹数据字典。
            name1: 第一个指纹的名称。
            name2: 第二个指纹的名称。

        Returns:
            包含相似度、差异详情和对比报告的字典。
        """
        fingerprint1 = fp1.get("fingerprint", {})
        fingerprint2 = fp2.get("fingerprint", {})

        # 获取所有维度
        all_dimensions = sorted(set(list(fingerprint1.keys()) + list(fingerprint2.keys())))

        # 对比各维度
        dimension_diffs = []
        total_weight = 0
        weighted_similarity = 0

        for dim in all_dimensions:
            val1 = fingerprint1.get(dim)
            val2 = fingerprint2.get(dim)

            similarity = self._calculate_dimension_similarity(dim, val1, val2)
            weight = self.DIMENSION_WEIGHTS.get(dim, 0.02)

            is_high_risk = dim in self.HIGH_RISK_DIMENSIONS
            diff_detail = self._get_diff_detail(dim, val1, val2)

            dimension_diffs.append({
                "dimension": dim,
                "similarity": similarity,
                "weight": weight,
                "is_high_risk": is_high_risk,
                "value1": self._safe_serialize(val1),
                "value2": self._safe_serialize(val2),
                "diff_detail": diff_detail,
                "is_different": similarity < 1.0,
            })

            weighted_similarity += similarity * weight
            total_weight += weight

        # 计算总体相似度
        overall_similarity = round(weighted_similarity / total_weight * 100, 1) if total_weight > 0 else 0

        # 识别高风险差异
        high_risk_diffs = [d for d in dimension_diffs if d["is_high_risk"] and d["similarity"] < 1.0]

        # 按相似度排序（差异最大的在前）
        dimension_diffs.sort(key=lambda x: x["similarity"])

        self._result = {
            "overall_similarity": overall_similarity,
            "name1": name1,
            "name2": name2,
            "dimension_count": len(all_dimensions),
            "different_count": sum(1 for d in dimension_diffs if d["is_different"]),
            "high_risk_diffs": high_risk_diffs,
            "dimension_diffs": dimension_diffs,
            "timestamp": time.time(),
            "version": "1.0.0",
        }

        return self._result

    def _calculate_dimension_similarity(self, dimension: str,
                                         val1: Any, val2: Any) -> float:
        """计算单个维度的相似度。

        Args:
            dimension: 维度名称。
            val1: 第一个值。
            val2: 第二个值。

        Returns:
            相似度（0.0-1.0）。
        """
        # 如果任一值为 None，视为完全不同
        if val1 is None or val2 is None:
            return 0.0 if not (val1 is None and val2 is None) else 1.0

        # 如果类型不同，视为完全不同
        if type(val1) != type(val2):
            return 0.0

        # 根据维度类型选择比较策略
        if isinstance(val1, dict):
            return self._compare_dicts(dimension, val1, val2)
        elif isinstance(val1, list):
            return self._compare_lists(dimension, val1, val2)
        elif isinstance(val1, (int, float)):
            return self._compare_numbers(dimension, val1, val2)
        elif isinstance(val1, str):
            return self._compare_strings(dimension, val1, val2)
        elif isinstance(val1, bool):
            return 1.0 if val1 == val2 else 0.0
        else:
            return 1.0 if val1 == val2 else 0.0

    def _compare_dicts(self, dimension: str, d1: Dict[str, Any],
                       d2: Dict[str, Any]) -> float:
        """比较两个字典的相似度。

        Args:
            dimension: 维度名称。
            d1: 第一个字典。
            d2: 第二个字典。

        Returns:
            相似度（0.0-1.0）。
        """
        all_keys = set(list(d1.keys()) + list(d2.keys()))
        if not all_keys:
            return 1.0

        # 对于哈希类维度，只比较哈希值
        if dimension in ("canvas", "audio", "webgl"):
            hash_keys = [k for k in all_keys if "hash" in k.lower()]
            if hash_keys:
                matching = sum(1 for k in hash_keys if d1.get(k) == d2.get(k))
                return matching / len(hash_keys)

        # 对于其他字典维度，比较所有键值对
        matching = 0
        for key in all_keys:
            v1 = d1.get(key)
            v2 = d2.get(key)
            if v1 == v2:
                matching += 1
            elif isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                # 数值类型允许小差异
                if abs(v1 - v2) / max(abs(v1), abs(v2), 1) < 0.1:
                    matching += 0.8

        return matching / len(all_keys)

    def _compare_lists(self, dimension: str, l1: List[Any],
                       l2: List[Any]) -> float:
        """比较两个列表的相似度。

        Args:
            dimension: 维度名称。
            l1: 第一个列表。
            l2: 第二个列表。

        Returns:
            相似度（0.0-1.0）。
        """
        if not l1 and not l2:
            return 1.0
        if not l1 or not l2:
            return 0.0

        set1 = set(str(v) for v in l1)
        set2 = set(str(v) for v in l2)

        if not set1 and not set2:
            return 1.0

        # Jaccard 相似度
        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0

    def _compare_numbers(self, dimension: str, n1: float,
                         n2: float) -> float:
        """比较两个数值的相似度。

        Args:
            dimension: 维度名称。
            n1: 第一个数值。
            n2: 第二个数值。

        Returns:
            相似度（0.0-1.0）。
        """
        if n1 == n2:
            return 1.0

        # 对于整数类型的维度（如屏幕分辨率），差异超过10%视为不同
        if dimension in ("screen",):
            max_val = max(abs(n1), abs(n2), 1)
            diff_ratio = abs(n1 - n2) / max_val
            return max(0.0, 1.0 - diff_ratio)

        # 对于其他数值，使用相对差异
        max_val = max(abs(n1), abs(n2), 1)
        diff_ratio = abs(n1 - n2) / max_val
        return max(0.0, 1.0 - diff_ratio)

    def _compare_strings(self, dimension: str, s1: str, s2: str) -> float:
        """比较两个字符串的相似度。

        Args:
            dimension: 维度名称。
            s1: 第一个字符串。
            s2: 第二个字符串。

        Returns:
            相似度（0.0-1.0）。
        """
        if s1 == s2:
            return 1.0

        # 对于哈希值，完全匹配或完全不匹配
        if dimension in ("canvas", "audio", "webgl") and len(s1) > 20:
            return 0.0

        # 对于 User-Agent，使用版本号比较
        if dimension == "user_agent":
            return self._compare_user_agents(s1, s2)

        # 对于其他字符串，使用简单的包含关系
        if s1 in s2 or s2 in s1:
            return 0.8

        # 使用最长公共子序列比例
        lcs_len = self._lcs_length(s1, s2)
        max_len = max(len(s1), len(s2))
        return lcs_len / max_len if max_len > 0 else 0.0

    def _compare_user_agents(self, ua1: str, ua2: str) -> float:
        """比较两个 User-Agent 字符串的相似度。

        Args:
            ua1: 第一个 User-Agent。
            ua2: 第二个 User-Agent。

        Returns:
            相似度（0.0-1.0）。
        """
        # 检查浏览器引擎是否相同
        if "AppleWebKit" in ua1 and "AppleWebKit" in ua2:
            engine_sim = 0.5
        elif "Gecko" in ua1 and "Gecko" in ua2:
            engine_sim = 0.5
        else:
            engine_sim = 0.0

        # 检查操作系统是否相同
        os_keywords = ["Windows", "Macintosh", "X11", "iPhone", "Android"]
        os_match = sum(1 for kw in os_keywords if kw in ua1 and kw in ua2)
        os_sim = min(os_match * 0.2, 0.3)

        # 检查浏览器是否相同
        browser_keywords = ["Chrome", "Firefox", "Safari", "Edg"]
        browser_match = sum(1 for kw in browser_keywords if kw in ua1 and kw in ua2)
        browser_sim = min(browser_match * 0.2, 0.2)

        return min(1.0, engine_sim + os_sim + browser_sim)

    @staticmethod
    def _lcs_length(s1: str, s2: str) -> int:
        """计算两个字符串的最长公共子序列长度。

        Args:
            s1: 第一个字符串。
            s2: 第二个字符串。

        Returns:
            LCS 长度。
        """
        m, n = len(s1), len(s2)
        # 优化空间复杂度
        if m < n:
            s1, s2 = s2, s1
            m, n = n, m

        prev = [0] * (n + 1)
        curr = [0] * (n + 1)

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    curr[j] = prev[j - 1] + 1
                else:
                    curr[j] = max(prev[j], curr[j - 1])
            prev, curr = curr, [0] * (n + 1)

        return prev[n]

    def _get_diff_detail(self, dimension: str, val1: Any, val2: Any) -> str:
        """获取维度差异的详细描述。

        Args:
            dimension: 维度名称。
            val1: 第一个值。
            val2: 第二个值。

        Returns:
            差异描述字符串。
        """
        if val1 is None and val2 is None:
            return "Both values are None"
        if val1 is None:
            return "Only present in fingerprint B"
        if val2 is None:
            return "Only present in fingerprint A"

        if isinstance(val1, dict) and isinstance(val2, dict):
            diffs = []
            all_keys = set(list(val1.keys()) + list(val2.keys()))
            for key in sorted(all_keys):
                v1 = val1.get(key)
                v2 = val2.get(key)
                if v1 != v2:
                    diffs.append(f"{key}: {v1!r} vs {v2!r}")
            return "; ".join(diffs) if diffs else "Identical"

        if isinstance(val1, list) and isinstance(val2, list):
            set1 = set(str(v) for v in val1)
            set2 = set(str(v) for v in val2)
            only_in_1 = set1 - set2
            only_in_2 = set2 - set1
            common = set1 & set2
            return f"Common: {len(common)}, Only in A: {len(only_in_1)}, Only in B: {len(only_in_2)}"

        return f"{val1!r} vs {val2!r}"

    @staticmethod
    def _safe_serialize(val: Any) -> Any:
        """安全地序列化值用于 JSON 输出。

        Args:
            val: 要序列化的值。

        Returns:
            可安全序列化的值。
        """
        if isinstance(val, (str, int, float, bool, type(None))):
            return val
        if isinstance(val, (list, tuple)):
            return [FingerprintComparator._safe_serialize(v) for v in val]
        if isinstance(val, dict):
            return {str(k): FingerprintComparator._safe_serialize(v) for k, v in val.items()}
        return str(val)

    def get_result(self) -> Dict[str, Any]:
        """获取对比结果。

        Returns:
            对比结果字典。
        """
        return self._result

    def to_json(self) -> str:
        """将对比结果导出为 JSON 字符串。

        Returns:
            JSON 格式的对比结果。
        """
        return json.dumps(self._result, indent=2, ensure_ascii=False, default=str)

    def summary_text(self) -> str:
        """生成文本格式的对比摘要。

        Returns:
            文本格式的对比摘要。
        """
        if not self._result:
            return "No comparison result available."

        similarity = self._result.get("overall_similarity", 0)
        name1 = self._result.get("name1", "A")
        name2 = self._result.get("name2", "B")
        diff_count = self._result.get("different_count", 0)
        total = self._result.get("dimension_count", 0)
        high_risk = self._result.get("high_risk_diffs", [])

        lines = [
            "=" * 60,
            "  GhostLens-Pro 指纹对比报告",
            "=" * 60,
            f"",
            f"  {name1} vs {name2}",
            f"",
            f"  总体相似度: {similarity}%",
            f"  差异维度数: {diff_count}/{total}",
            f"",
        ]

        if high_risk:
            lines.append("-" * 60)
            lines.append("  高风险差异维度:")
            for diff in high_risk:
                lines.append(
                    f"    - {diff['dimension']}: "
                    f"相似度 {diff['similarity'] * 100:.0f}% "
                    f"(权重: {diff['weight'] * 100:.0f}%)"
                )
                lines.append(f"      {diff['diff_detail']}")

        # 所有差异维度
        all_diffs = [d for d in self._result.get("dimension_diffs", []) if d["is_different"]]
        if all_diffs:
            lines.append("")
            lines.append("-" * 60)
            lines.append("  所有差异维度:")
            for diff in all_diffs:
                risk_marker = " [HIGH]" if diff["is_high_risk"] else ""
                lines.append(
                    f"    - {diff['dimension']}{risk_marker}: "
                    f"相似度 {diff['similarity'] * 100:.0f}%"
                )

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)

    def batch_compare(self, profiles: List[Dict[str, Any]],
                      base_index: int = 0) -> List[Dict[str, Any]]:
        """批量对比指纹配置。

        Args:
            profiles: 指纹配置列表。
            base_index: 基准配置的索引。

        Returns:
            对比结果列表。
        """
        if not profiles or base_index >= len(profiles):
            return []

        base = profiles[base_index]
        base_name = base.get("profile", {}).get("name", f"Profile {base_index}")

        results = []
        for i, profile in enumerate(profiles):
            if i == base_index:
                continue
            profile_name = profile.get("profile", {}).get("name", f"Profile {i}")
            result = self.compare(base, profile, base_name, profile_name)
            results.append(result)

        # 按相似度降序排列
        results.sort(key=lambda x: x["overall_similarity"], reverse=True)
        return results
