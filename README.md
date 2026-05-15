<p align="center">
  <h1 align="center">🔍👻🌐 GhostLens-Pro</h1>
  <p align="center">
    <strong>轻量级浏览器指纹智能分析与反检测评分引擎 CLI 工具</strong><br/>
    <em>Lightweight Browser Fingerprint Intelligence Analysis & Anti-Detection Scoring Engine CLI Tool</em>
  </p>
</p>

<p align="center">
  <a href="https://github.com/gitstq/GhostLens-Pro"><img src="https://img.shields.io/badge/GitHub-GhostLens--Pro-blue?logo=github" alt="GitHub"/></a>
  <a href="https://pypi.org/project/ghostlens-pro/"><img src="https://img.shields.io/badge/PyPI-ghostlens--pro-green?logo=pypi&logoColor=white" alt="PyPI"/></a>
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/License-MIT-brightgreen" alt="License: MIT"/>
  <img src="https://img.shields.io/badge/Dependencies-0%20External-orange" alt="Zero External Dependencies"/>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Cross Platform"/>
</p>

<p align="center">
  <a href="#简体中文">简体中文</a> &nbsp;|&nbsp;
  <a href="#繁體中文">繁體中文</a> &nbsp;|&nbsp;
  <a href="#english">English</a>
</p>

---

## 目录

- [简体中文](#简体中文)
- [繁體中文](#繁體中文)
- [English](#english)

---

<a id="简体中文"></a>

# 🇨🇳 简体中文

## 🎉 项目介绍

### 🎯 定位

GhostLens-Pro 是一款**轻量级浏览器指纹智能分析与反检测评分引擎**，以命令行工具（CLI）的形式提供服务。它专注于浏览器指纹的采集、分析、评分、生成和对比，帮助开发者和安全研究人员全面理解和评估浏览器指纹的隐私风险。

### 💡 核心价值

- **全方位指纹透视**：覆盖 32+ 指纹维度，从 User-Agent 到 WebGL、从 Canvas 到音频指纹，深入剖析浏览器身份标识的每一个角落。
- **智能反检测评分**：基于多维度加权算法，输出直观的 A+/A/B/C/D 等级评分，快速定位隐私薄弱环节。
- **一键生成逼真配置**：内置 12 套主流浏览器 + 操作系统模板，秒级生成高度一致的指纹配置文件。
- **零依赖纯 Python**：仅使用 Python 标准库，无需安装任何第三方包，即装即用。

### 🔥 解决的痛点

| 痛点 | GhostLens-Pro 的解决方案 |
|------|------------------------|
| 指纹维度多且分散，难以全面评估 | 一条命令采集 32+ 维度，输出完整报告 |
| 缺乏统一的反检测评分标准 | 多维度加权评分算法，A+~D 五级量化 |
| 手动构造指纹配置耗时且易出错 | 12 套内置模板 + 智能随机化，一键生成 |
| 指纹配置内部矛盾导致暴露 | 14 项一致性检查规则，自动发现矛盾 |
| 多配置之间差异难以量化 | 加权相似度算法 + 高风险差异识别 |
| 现有工具依赖重、体积大 | 纯标准库实现，零外部依赖 |

### ✨ 差异化亮点

- 🧬 **自研评分引擎**：不依赖任何第三方指纹检测服务，评分算法完全自主实现，支持离线使用。
- 🎨 **TUI 交互式仪表板**：基于 curses 的终端 UI，支持实时进度条、颜色编码和键盘导航，告别纯文本输出。
- 🔍 **14 项一致性校验**：从 UA 与平台匹配到字体与 OS 对应，从触摸支持到硬件范围，全面检测指纹配置的内部矛盾。
- 📊 **多格式报告导出**：支持终端文本、JSON、HTML 三种输出格式，满足自动化集成和人工审阅的不同需求。
- 🌱 **可复现的随机化**：通过 `--seed` 参数实现可复现的指纹生成，便于调试和回归测试。

### 🧠 灵感来源

GhostLens-Pro 的灵感来源于浏览器指纹追踪技术的快速发展与隐私保护需求之间的矛盾。随着 Canvas、WebGL、AudioContext 等高级指纹技术的普及，传统的隐私保护手段（如禁用 Cookie、使用无痕模式）已远远不够。我们希望为开发者和安全研究人员提供一个轻量、高效、易用的工具，帮助他们深入理解浏览器指纹的工作原理，评估指纹配置的隐私强度，并快速生成高质量的伪装配置。

---

## ✨ 核心特性

### 🔎 指纹采集引擎

- **32+ 指纹维度**：覆盖 User-Agent、屏幕信息、Canvas 指纹、WebGL 信息、字体列表、音频指纹、硬件信息、触摸支持、电池状态、网络连接、Cookie 状态、DNT、PDF 查看器、插件列表、存储配额、媒体设备、语音合成、ClientRects、iframe 检测、Performance API、Console 检测、Debugger 检测、WebDriver 检测、WebRTC 泄露、Permissions API、CSS 特性、Math 常量、错误消息、特性检测等。
- **每个维度附带风险评分**（0-100），直观展示各维度的隐私风险等级。
- **基于真实数据的模拟**：内置大量真实浏览器指纹数据模板，确保生成的指纹配置高度逼真。

### 📊 反检测评分引擎

- **综合评分算法**：基于 4 大风险分类（自动化检测、指纹唯一性、行为分析、网络特征）的加权计算，输出 0-100 的综合反检测评分。
- **五级评分等级**：A+（优秀，95+）、A（良好，85+）、B（中等，70+）、C（较差，50+）、D（危险，<50）。
- **4 大风险分类**：
  - 🤖 **自动化检测**（权重 35%）：WebDriver、Debugger、Console、Performance、ClientRects、iframe
  - 🎨 **指纹唯一性**（权重 25%）：Canvas、WebGL、Audio、Fonts、Math Constants、Error Messages、CSS Features
  - 🧩 **行为分析**（权重 20%）：Touch、Battery、Connection、Storage、Media Devices、Speech、Permissions
  - 🌐 **网络特征**（权重 20%）：WebRTC、Cookies、DNT、Features
- **智能改进建议**：针对高风险维度自动生成优先级排序的改进建议。

### 🛠️ 指纹配置生成器

- **12 套内置模板**：覆盖 Chrome/Firefox/Safari/Edge x Windows/macOS/Linux/iOS/Android 的主流组合。
- **智能随机化**：对 Canvas 哈希、存储使用量、连接信息等非关键参数进行随机化，避免生成千篇一律的配置。
- **可复现生成**：通过 `--seed` 参数实现确定性生成，便于调试和回归测试。
- **批量生成**：支持一次性生成多个指纹配置，满足大规模测试需求。

### ✅ 指纹一致性校验器

- **14 项一致性检查规则**：
  1. UA 与平台信息匹配
  2. 屏幕分辨率与设备类型匹配
  3. 字体列表与操作系统匹配
  4. WebGL 渲染器与操作系统匹配
  5. 触摸支持与设备类型匹配
  6. 硬件信息与设备类型匹配
  7. 插件列表与浏览器匹配
  8. 存储配额与设备类型匹配
  9. 颜色深度合理性
  10. 像素比与操作系统匹配
  11. WebDriver 检测状态
  12. Cookie 启用状态
  13. PDF 查看器与浏览器匹配
  14. 语言设置一致性
- **三级严重程度**：Critical（严重）、Warning（警告）、Info（提示）。
- **自动修复建议**：每个问题都附带具体的修复建议。

### 📐 指纹对比分析器

- **加权相似度计算**：基于各维度对指纹唯一性的贡献度进行加权，输出总体相似度百分比。
- **高风险差异识别**：自动标记 UA、Canvas、WebGL、Fonts、Audio、Platform、Screen、Hardware 等高风险差异维度。
- **多策略比较**：针对不同数据类型（字典、列表、数值、字符串）采用最优比较策略（Jaccard 相似度、LCS、相对差异等）。
- **批量对比**：支持以一个基准配置对比多个目标配置。

### 🖥️ TUI 仪表板

- **curses 终端 UI**：基于 Python 标准库 curses 实现，无需额外依赖。
- **实时进度条**：可视化展示评分进度和各分类得分。
- **颜色编码**：不同等级使用不同颜色（绿色=优秀、黄色=中等、红色=危险）。
- **键盘导航**：支持方向键、回车键、快捷键（S/F/C/H/R/Q）等操作。
- **多视图切换**：主菜单、评分视图、指纹数据视图、一致性视图、帮助视图。
- **优雅降级**：curses 不可用时自动回退到文本模式。

---

## 🚀 快速开始

### 📋 环境要求

- **Python** 3.8 或更高版本
- **操作系统**：Windows / macOS / Linux
- **外部依赖**：无（零外部依赖，仅使用标准库）

### 📦 安装方式

**方式一：通过 pip 直接从 GitHub 安装**

```bash
pip install git+https://github.com/gitstq/GhostLens-Pro.git
```

**方式二：克隆仓库后本地安装**

```bash
git clone https://github.com/gitstq/GhostLens-Pro.git
cd GhostLens-Pro
pip install .
```

**方式三：开发模式安装（推荐贡献者使用）**

```bash
git clone https://github.com/gitstq/GhostLens-Pro.git
cd GhostLens-Pro
pip install -e .
```

### 🎮 启动命令

安装完成后，在终端中输入以下命令即可启动：

```bash
ghostlens-pro --help
```

如果安装方式二或方式三，也可以通过以下方式启动：

```bash
python -m ghostlens_pro --help
```

### ⚡ 快速体验

```bash
# 执行完整指纹扫描与评分
ghostlens-pro scan

# 生成 Chrome on Windows 指纹配置
ghostlens-pro generate --browser chrome --os windows

# 一致性校验
ghostlens-pro check --input my_profile.json

# 指纹对比
ghostlens-pro compare --file1 profile1.json --file2 profile2.json

# 启动 TUI 仪表板
ghostlens-pro dashboard

# 生成 HTML 报告
ghostlens-pro report --html --output report.html

# 列出所有内置模板
ghostlens-pro list-profiles
```

---

## 📖 详细使用指南

### 🔧 CLI 子命令一览

| 命令 | 说明 | 常用参数 |
|------|------|---------|
| `scan` | 执行指纹采集与评分 | `--os`, `--browser`, `--device`, `--seed` |
| `score` | 对已有指纹配置进行评分 | `--input` |
| `generate` | 生成指纹配置文件 | `--template`, `--os`, `--browser`, `--device`, `--seed`, `--no-randomize` |
| `check` | 指纹一致性校验 | `--input` |
| `compare` | 指纹对比分析 | `--file1`, `--file2`, `--name1`, `--name2` |
| `dashboard` | 启动 TUI 仪表板 | 无 |
| `report` | 生成完整报告 | `--os`, `--browser`, `--device`, `--seed` |
| `list-profiles` | 列出内置模板 | 无 |

### 🌐 全局选项

| 选项 | 缩写 | 说明 |
|------|------|------|
| `--json` | - | 输出 JSON 格式 |
| `--html` | - | 输出 HTML 格式 |
| `--output` | `-o` | 指定输出文件路径 |
| `--verbose` | `-v` | 详细输出模式 |
| `--quiet` | `-q` | 静默模式，仅输出错误信息 |

### 📝 进阶用法

#### 1. 指纹扫描与评分

```bash
# 基本扫描（默认 Chrome + Windows + Desktop）
ghostlens-pro scan

# 指定目标环境
ghostlens-pro scan --os macos --browser safari --device desktop

# 使用随机种子确保可复现
ghostlens-pro scan --seed 42

# 输出 JSON 格式到文件
ghostlens-pro scan --json --output scan_result.json

# 详细模式
ghostlens-pro scan --verbose
```

#### 2. 指纹配置生成

```bash
# 使用内置模板生成
ghostlens-pro generate --template chrome_win10

# 自定义浏览器和操作系统组合
ghostlens-pro generate --browser firefox --os linux

# 生成移动端配置
ghostlens-pro generate --browser chrome --os android --device mobile

# 禁用随机化（使用模板默认值）
ghostlens-pro generate --template safari_macos --no-randomize

# 生成并保存到文件
ghostlens-pro generate --template edge_win10 --output my_edge_profile.json
```

#### 3. 一致性校验

```bash
# 校验指纹配置文件
ghostlens-pro check --input my_profile.json

# 校验并输出 JSON 格式
ghostlens-pro check --input my_profile.json --json --output check_result.json
```

#### 4. 指纹对比

```bash
# 对比两个指纹配置
ghostlens-pro compare --file1 profile_a.json --file2 profile_b.json

# 自定义名称
ghostlens-pro compare --file1 profile_a.json --file2 profile_b.json --name1 "Chrome Win10" --name2 "Firefox Linux"

# 输出 JSON 格式
ghostlens-pro compare --file1 profile_a.json --file2 profile_b.json --json --output compare_result.json
```

#### 5. 报告生成

```bash
# 生成 HTML 报告
ghostlens-pro report --html --output report.html

# 生成 JSON 报告
ghostlens-pro report --json --output report.json

# 指定目标环境生成报告
ghostlens-pro report --os macos --browser safari --html --output safari_report.html
```

#### 6. TUI 仪表板

```bash
# 启动交互式仪表板
ghostlens-pro dashboard

# 仪表板快捷键：
# UP/DOWN  - 导航菜单/滚动内容
# ENTER    - 选择菜单项
# S        - 扫描指纹
# F        - 查看指纹数据
# C        - 查看一致性检查
# R        - 返回主菜单
# H        - 显示帮助
# Q / ESC  - 退出
```

### 📋 内置模板列表

| 模板 ID | 名称 | 浏览器 | 操作系统 | 设备类型 |
|---------|------|--------|---------|---------|
| `chrome_win10` | Chrome on Windows 10 | Chrome | Windows | Desktop |
| `chrome_win11` | Chrome on Windows 11 | Chrome | Windows | Desktop |
| `chrome_macos` | Chrome on macOS | Chrome | macOS | Desktop |
| `chrome_linux` | Chrome on Linux | Chrome | Linux | Desktop |
| `firefox_win10` | Firefox on Windows 10 | Firefox | Windows | Desktop |
| `firefox_macos` | Firefox on macOS | Firefox | macOS | Desktop |
| `safari_macos` | Safari on macOS | Safari | macOS | Desktop |
| `edge_win10` | Edge on Windows 10 | Edge | Windows | Desktop |
| `chrome_ios` | Chrome on iOS | Chrome | iOS | Mobile |
| `chrome_android` | Chrome on Android | Chrome | Android | Mobile |
| `safari_ios` | Safari on iOS | Safari | iOS | Mobile |
| `chrome_android_pixel` | Chrome on Pixel 5 | Chrome | Android | Mobile |

### 🎯 典型使用场景

#### 场景一：隐私评估

你想了解当前浏览器指纹的隐私风险等级：

```bash
ghostlens-pro scan
```

#### 场景二：指纹伪装

你需要生成一个逼真的 Chrome on Windows 指纹配置用于测试：

```bash
ghostlens-pro generate --template chrome_win10 --output stealth_profile.json
ghostlens-pro check --input stealth_profile.json
```

#### 场景三：批量测试

你需要生成 10 个不同的指纹配置进行批量测试：

```bash
for i in $(seq 1 10); do
  ghostlens-pro generate --template chrome_win10 --seed $i --output "profile_${i}.json"
done
```

#### 场景四：配置对比

你需要对比两个指纹配置的差异：

```bash
ghostlens-pro compare --file1 profile_1.json --file2 profile_2.json --json --output diff.json
```

#### 场景五：生成报告

你需要生成一份 HTML 格式的完整分析报告：

```bash
ghostlens-pro report --html --output full_report.html
```

---

## 💡 设计思路与迭代规划

### 🏗️ 设计理念

1. **轻量至上**：零外部依赖，纯 Python 标准库实现，安装即用，不引入任何冗余。
2. **模块化架构**：采集、评分、生成、校验、对比五大引擎独立解耦，可单独使用也可组合调用。
3. **数据驱动**：所有指纹数据基于真实浏览器行为统计，确保生成的配置高度逼真。
4. **可扩展性**：清晰的模块接口和类型注解，便于社区贡献新的指纹维度和评分规则。
5. **安全合规**：本工具仅用于教育和研究目的，不鼓励或协助任何违法违规行为。

### 🔧 技术选型

| 技术决策 | 选择 | 原因 |
|---------|------|------|
| 语言 | Python 3.8+ | 生态丰富、开发效率高、跨平台支持好 |
| 外部依赖 | 无 | 降低安装门槛、避免版本冲突、提升可移植性 |
| CLI 框架 | argparse（标准库） | 无需额外依赖、功能完善、Python 官方推荐 |
| TUI 框架 | curses（标准库） | 原生支持、无额外依赖、终端兼容性好 |
| 数据格式 | JSON | 通用性强、可读性好、与前后端生态无缝对接 |

### 🗺️ 后续计划

- [ ] **Web 端可视化面板**：提供 Web UI，支持在线指纹分析和报告查看。
- [ ] **浏览器插件集成**：开发 Chrome/Firefox 插件，实现真实浏览器环境的指纹采集。
- [ ] **更多指纹维度**：增加 WebRTC ICE 候选、Battery API 详细信息、Speech Synthesis 指纹等。
- [ ] **机器学习评分**：引入 ML 模型，基于真实指纹数据库训练更精准的评分算法。
- [ ] **指纹对抗测试**：集成主流指纹检测服务（如 FingerprintJS、CreepJS）的测试能力。
- [ ] **配置导入导出**：支持从 Puppeteer Stealth、Playwright 等工具导入指纹配置。
- [ ] **多语言文档**：完善英文、日文等多语言文档。
- [ ] **CI/CD 集成**：支持在 CI/CD 流水线中进行指纹一致性自动化检查。

### 🤝 社区贡献方向

我们欢迎以下类型的贡献：

- 🐛 **Bug 修复**：修复已知的错误和异常。
- ✨ **新功能**：添加新的指纹维度、评分规则或 CLI 命令。
- 📚 **文档完善**：改进文档、添加使用示例、翻译多语言版本。
- 🧪 **测试覆盖**：增加单元测试和集成测试。
- 🎨 **UI 改进**：优化 TUI 仪表板的视觉效果和交互体验。
- 📊 **数据分析**：提供指纹数据的统计分析工具。

---

## 🤝 贡献指南

感谢你对 GhostLens-Pro 的关注！我们欢迎任何形式的贡献。

### 📌 PR 规范

1. **分支命名**：使用 `feature/xxx`、`fix/xxx`、`docs/xxx` 等前缀。
2. **提交信息**：遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：
   - `feat: 添加新的指纹维度`
   - `fix: 修复评分算法错误`
   - `docs: 更新 README 文档`
   - `test: 增加一致性校验器测试`
   - `refactor: 优化代码结构`
3. **代码风格**：遵循 PEP 8，所有函数和类必须有完整的 docstring，使用类型注解。
4. **测试要求**：所有 PR 必须通过现有测试，新增功能需附带对应测试。
5. **文档更新**：如果 PR 涉及功能变更，请同步更新 README 和 CLI 帮助信息。

### 📌 Issue 反馈规则

提交 Issue 时，请包含以下信息：

- **Python 版本**：`python --version`
- **操作系统**：Windows/macOS/Linux 及版本号
- **复现步骤**：详细描述如何复现问题
- **期望行为**：描述你期望的正确行为
- **实际行为**：描述实际发生的错误行为
- **错误信息**：粘贴完整的错误堆栈或日志

---

## 📄 开源协议

本项目基于 [MIT License](https://github.com/gitstq/GhostLens-Pro/blob/main/LICENSE) 开源。

```
MIT License

Copyright (c) 2024 GhostLens-Pro Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<a id="繁體中文"></a>

# 🇹🇼 繁體中文

## 🎉 專案介紹

### 🎯 定位

GhostLens-Pro 是一款**輕量級瀏覽器指紋智慧分析與反偵測評分引擎**，以命令列工具（CLI）的形式提供服務。它專注於瀏覽器指紋的採集、分析、評分、生成和對比，幫助開發者和安全研究人員全面理解和評估瀏覽器指紋的隱私風險。

### 💡 核心價值

- **全方位指紋透視**：覆蓋 32+ 指紋維度，從 User-Agent 到 WebGL、從 Canvas 到音訊指紋，深入剖析瀏覽器身份標識的每一個角落。
- **智慧反偵測評分**：基於多維度加權演算法，輸出直觀的 A+/A/B/C/D 等級評分，快速定位隱私薄弱環節。
- **一鍵生成逼真配置**：內建 12 套主流瀏覽器 + 作業系統模板，秒級生成高度一致的指紋配置檔案。
- **零依賴純 Python**：僅使用 Python 標準函式庫，無需安裝任何第三方套件，即裝即用。

### 🔥 解決的痛點

| 痛點 | GhostLens-Pro 的解決方案 |
|------|------------------------|
| 指紋維度多且分散，難以全面評估 | 一條命令採集 32+ 維度，輸出完整報告 |
| 缺乏統一的反偵測評分標準 | 多維度加權評分演算法，A+~D 五級量化 |
| 手動建構指紋配置耗時且易出錯 | 12 套內建模板 + 智慧隨機化，一鍵生成 |
| 指紋配置內部矛盾導致暴露 | 14 項一致性檢查規則，自動發現矛盾 |
| 多配置之間差異難以量化 | 加權相似度演算法 + 高風險差異識別 |
| 現有工具依賴重、體積大 | 純標準函式庫實作，零外部依賴 |

### ✨ 差異化亮點

- 🧬 **自研評分引擎**：不依賴任何第三方指紋偵測服務，評分演算法完全自主實作，支援離線使用。
- 🎨 **TUI 互動式儀表板**：基於 curses 的終端 UI，支援即時進度條、顏色編碼和鍵盤導航，告別純文字輸出。
- 🔍 **14 項一致性校驗**：從 UA 與平台匹配到字型與 OS 對應，從觸控支援到硬體範圍，全面檢測指紋配置的內部矛盾。
- 📊 **多格式報告匯出**：支援終端文字、JSON、HTML 三種輸出格式，滿足自動化整合和人工審閱的不同需求。
- 🌱 **可重現的隨機化**：透過 `--seed` 參數實作可重現的指紋生成，便於除錯和回歸測試。

### 🧠 靈感來源

GhostLens-Pro 的靈感來源於瀏覽器指紋追蹤技術的快速發展與隱私保護需求之間的矛盾。隨著 Canvas、WebGL、AudioContext 等高級指紋技術的普及，傳統的隱私保護手段（如停用 Cookie、使用無痕模式）已遠遠不夠。我們希望為開發者和安全研究人員提供一個輕量、高效、易用的工具，幫助他們深入理解瀏覽器指紋的工作原理，評估指紋配置的隱私強度，並快速生成高品質的偽裝配置。

---

## ✨ 核心特性

### 🔎 指紋採集引擎

- **32+ 指紋維度**：覆蓋 User-Agent、螢幕資訊、Canvas 指紋、WebGL 資訊、字型列表、音訊指紋、硬體資訊、觸控支援、電池狀態、網路連線、Cookie 狀態、DNT、PDF 檢視器、外掛列表、儲存配額、媒體裝置、語音合成、ClientRects、iframe 偵測、Performance API、Console 偵測、Debugger 偵測、WebDriver 偵測、WebRTC 洩漏、Permissions API、CSS 特性、Math 常數、錯誤訊息、特性偵測等。
- **每個維度附帶風險評分**（0-100），直觀展示各維度的隱私風險等級。
- **基於真實資料的模擬**：內建大量真實瀏覽器指紋資料模板，確保生成的指紋配置高度逼真。

### 📊 反偵測評分引擎

- **綜合評分演算法**：基於 4 大風險分類（自動化偵測、指紋唯一性、行為分析、網路特徵）的加權計算，輸出 0-100 的綜合反偵測評分。
- **五級評分等級**：A+（優秀，95+）、A（良好，85+）、B（中等，70+）、C（較差，50+）、D（危險，<50）。
- **4 大風險分類**：
  - 🤖 **自動化偵測**（權重 35%）：WebDriver、Debugger、Console、Performance、ClientRects、iframe
  - 🎨 **指紋唯一性**（權重 25%）：Canvas、WebGL、Audio、Fonts、Math Constants、Error Messages、CSS Features
  - 🧩 **行為分析**（權重 20%）：Touch、Battery、Connection、Storage、Media Devices、Speech、Permissions
  - 🌐 **網路特徵**（權重 20%）：WebRTC、Cookies、DNT、Features
- **智慧改進建議**：針對高風險維度自動生成優先級排序的改進建議。

### 🛠️ 指紋配置生成器

- **12 套內建模板**：覆蓋 Chrome/Firefox/Safari/Edge x Windows/macOS/Linux/iOS/Android 的主流組合。
- **智慧隨機化**：對 Canvas 雜湊、儲存使用量、連線資訊等非關鍵參數進行隨機化，避免生成千篇一律的配置。
- **可重現生成**：透過 `--seed` 參數實作確定性生成，便於除錯和回歸測試。
- **批次生成**：支援一次生成多個指紋配置，滿足大規模測試需求。

### ✅ 指紋一致性校驗器

- **14 項一致性檢查規則**：
  1. UA 與平台資訊匹配
  2. 螢幕解析度與裝置類型匹配
  3. 字型列表與作業系統匹配
  4. WebGL 渲染器與作業系統匹配
  5. 觸控支援與裝置類型匹配
  6. 硬體資訊與裝置類型匹配
  7. 外掛列表與瀏覽器匹配
  8. 儲存配額與裝置類型匹配
  9. 顏色深度合理性
  10. 像素比與作業系統匹配
  11. WebDriver 偵測狀態
  12. Cookie 啟用狀態
  13. PDF 檢視器與瀏覽器匹配
  14. 語言設定一致性
- **三級嚴重程度**：Critical（嚴重）、Warning（警告）、Info（提示）。
- **自動修復建議**：每個問題都附帶具體的修復建議。

### 📐 指紋對比分析器

- **加權相似度計算**：基於各維度對指紋唯一性的貢獻度進行加權，輸出總體相似度百分比。
- **高風險差異識別**：自動標記 UA、Canvas、WebGL、Fonts、Audio、Platform、Screen、Hardware 等高風險差異維度。
- **多策略比較**：針對不同資料型別（字典、列表、數值、字串）採用最優比較策略（Jaccard 相似度、LCS、相對差異等）。
- **批次對比**：支援以一個基準配置對比多個目標配置。

### 🖥️ TUI 儀表板

- **curses 終端 UI**：基於 Python 標準函式庫 curses 實作，無需額外依賴。
- **即時進度條**：視覺化展示評分進度和各分類得分。
- **顏色編碼**：不同等級使用不同顏色（綠色=優秀、黃色=中等、紅色=危險）。
- **鍵盤導航**：支援方向鍵、Enter 鍵、快速鍵（S/F/C/H/R/Q）等操作。
- **多檢視切換**：主選單、評分檢視、指紋資料檢視、一致性檢視、幫助檢視。
- **優雅降級**：curses 不可用時自動回退到文字模式。

---

## 🚀 快速開始

### 📋 環境需求

- **Python** 3.8 或更高版本
- **作業系統**：Windows / macOS / Linux
- **外部依賴**：無（零外部依賴，僅使用標準函式庫）

### 📦 安裝方式

**方式一：透過 pip 直接從 GitHub 安裝**

```bash
pip install git+https://github.com/gitstq/GhostLens-Pro.git
```

**方式二：複製倉庫後本機安裝**

```bash
git clone https://github.com/gitstq/GhostLens-Pro.git
cd GhostLens-Pro
pip install .
```

**方式三：開發模式安裝（推薦貢獻者使用）**

```bash
git clone https://github.com/gitstq/GhostLens-Pro.git
cd GhostLens-Pro
pip install -e .
```

### 🎮 啟動命令

安裝完成後，在終端中輸入以下命令即可啟動：

```bash
ghostlens-pro --help
```

如果使用方式二或方式三安裝，也可以透過以下方式啟動：

```bash
python -m ghostlens_pro --help
```

### ⚡ 快速體驗

```bash
# 執行完整指紋掃描與評分
ghostlens-pro scan

# 生成 Chrome on Windows 指紋配置
ghostlens-pro generate --browser chrome --os windows

# 一致性校驗
ghostlens-pro check --input my_profile.json

# 指紋對比
ghostlens-pro compare --file1 profile1.json --file2 profile2.json

# 啟動 TUI 儀表板
ghostlens-pro dashboard

# 生成 HTML 報告
ghostlens-pro report --html --output report.html

# 列出所有內建模板
ghostlens-pro list-profiles
```

---

## 📖 詳細使用指南

### 🔧 CLI 子命令一覽

| 命令 | 說明 | 常用參數 |
|------|------|---------|
| `scan` | 執行指紋採集與評分 | `--os`, `--browser`, `--device`, `--seed` |
| `score` | 對已有指紋配置進行評分 | `--input` |
| `generate` | 生成指紋配置檔案 | `--template`, `--os`, `--browser`, `--device`, `--seed`, `--no-randomize` |
| `check` | 指紋一致性校驗 | `--input` |
| `compare` | 指紋對比分析 | `--file1`, `--file2`, `--name1`, `--name2` |
| `dashboard` | 啟動 TUI 儀表板 | 無 |
| `report` | 生成完整報告 | `--os`, `--browser`, `--device`, `--seed` |
| `list-profiles` | 列出內建模板 | 無 |

### 🌐 全域選項

| 選項 | 縮寫 | 說明 |
|------|------|------|
| `--json` | - | 輸出 JSON 格式 |
| `--html` | - | 輸出 HTML 格式 |
| `--output` | `-o` | 指定輸出檔案路徑 |
| `--verbose` | `-v` | 詳細輸出模式 |
| `--quiet` | `-q` | 靜默模式，僅輸出錯誤資訊 |

### 📝 進階用法

#### 1. 指紋掃描與評分

```bash
# 基本掃描（預設 Chrome + Windows + Desktop）
ghostlens-pro scan

# 指定目標環境
ghostlens-pro scan --os macos --browser safari --device desktop

# 使用隨機種子確保可重現
ghostlens-pro scan --seed 42

# 輸出 JSON 格式到檔案
ghostlens-pro scan --json --output scan_result.json

# 詳細模式
ghostlens-pro scan --verbose
```

#### 2. 指紋配置生成

```bash
# 使用內建模板生成
ghostlens-pro generate --template chrome_win10

# 自訂瀏覽器和作業系統組合
ghostlens-pro generate --browser firefox --os linux

# 生成行動端配置
ghostlens-pro generate --browser chrome --os android --device mobile

# 停用隨機化（使用模板預設值）
ghostlens-pro generate --template safari_macos --no-randomize

# 生成並儲存到檔案
ghostlens-pro generate --template edge_win10 --output my_edge_profile.json
```

#### 3. 一致性校驗

```bash
# 校驗指紋配置檔案
ghostlens-pro check --input my_profile.json

# 校驗並輸出 JSON 格式
ghostlens-pro check --input my_profile.json --json --output check_result.json
```

#### 4. 指紋對比

```bash
# 對比兩個指紋配置
ghostlens-pro compare --file1 profile_a.json --file2 profile_b.json

# 自訂名稱
ghostlens-pro compare --file1 profile_a.json --file2 profile_b.json --name1 "Chrome Win10" --name2 "Firefox Linux"

# 輸出 JSON 格式
ghostlens-pro compare --file1 profile_a.json --file2 profile_b.json --json --output compare_result.json
```

#### 5. 報告生成

```bash
# 生成 HTML 報告
ghostlens-pro report --html --output report.html

# 生成 JSON 報告
ghostlens-pro report --json --output report.json

# 指定目標環境生成報告
ghostlens-pro report --os macos --browser safari --html --output safari_report.html
```

#### 6. TUI 儀表板

```bash
# 啟動互動式儀表板
ghostlens-pro dashboard

# 儀表板快速鍵：
# UP/DOWN  - 導航選單/滾動內容
# ENTER    - 選擇選單項目
# S        - 掃描指紋
# F        - 檢視指紋資料
# C        - 檢視一致性檢查
# R        - 返回主選單
# H        - 顯示幫助
# Q / ESC  - 退出
```

### 📋 內建模板列表

| 模板 ID | 名稱 | 瀏覽器 | 作業系統 | 裝置類型 |
|---------|------|--------|---------|---------|
| `chrome_win10` | Chrome on Windows 10 | Chrome | Windows | Desktop |
| `chrome_win11` | Chrome on Windows 11 | Chrome | Windows | Desktop |
| `chrome_macos` | Chrome on macOS | Chrome | macOS | Desktop |
| `chrome_linux` | Chrome on Linux | Chrome | Linux | Desktop |
| `firefox_win10` | Firefox on Windows 10 | Firefox | Windows | Desktop |
| `firefox_macos` | Firefox on macOS | Firefox | macOS | Desktop |
| `safari_macos` | Safari on macOS | Safari | macOS | Desktop |
| `edge_win10` | Edge on Windows 10 | Edge | Windows | Desktop |
| `chrome_ios` | Chrome on iOS | Chrome | iOS | Mobile |
| `chrome_android` | Chrome on Android | Chrome | Android | Mobile |
| `safari_ios` | Safari on iOS | Safari | iOS | Mobile |
| `chrome_android_pixel` | Chrome on Pixel 5 | Chrome | Android | Mobile |

### 🎯 典型使用場景

#### 場景一：隱私評估

你想了解目前瀏覽器指紋的隱私風險等級：

```bash
ghostlens-pro scan
```

#### 場景二：指紋偽裝

你需要生成一個逼真的 Chrome on Windows 指紋配置用於測試：

```bash
ghostlens-pro generate --template chrome_win10 --output stealth_profile.json
ghostlens-pro check --input stealth_profile.json
```

#### 場景三：批次測試

你需要生成 10 個不同的指紋配置進行批次測試：

```bash
for i in $(seq 1 10); do
  ghostlens-pro generate --template chrome_win10 --seed $i --output "profile_${i}.json"
done
```

#### 場景四：配置對比

你需要對比兩個指紋配置的差異：

```bash
ghostlens-pro compare --file1 profile_1.json --file2 profile_2.json --json --output diff.json
```

#### 場景五：生成報告

你需要生成一份 HTML 格式的完整分析報告：

```bash
ghostlens-pro report --html --output full_report.html
```

---

## 💡 設計思路與迭代規劃

### 🏗️ 設計理念

1. **輕量至上**：零外部依賴，純 Python 標準函式庫實作，安裝即用，不引入任何冗餘。
2. **模組化架構**：採集、評分、生成、校驗、對比五大引擎獨立解耦，可單獨使用也可組合呼叫。
3. **資料驅動**：所有指紋資料基於真實瀏覽器行為統計，確保生成的配置高度逼真。
4. **可擴展性**：清晰的模組介面和型別註解，便於社群貢獻新的指紋維度和評分規則。
5. **安全合規**：本工具僅用於教育和研究目的，不鼓勵或協助任何違法違規行為。

### 🔧 技術選型

| 技術決策 | 選擇 | 原因 |
|---------|------|------|
| 語言 | Python 3.8+ | 生態豐富、開發效率高、跨平台支援好 |
| 外部依賴 | 無 | 降低安裝門檻、避免版本衝突、提升可移植性 |
| CLI 框架 | argparse（標準函式庫） | 無需額外依賴、功能完善、Python 官方推薦 |
| TUI 框架 | curses（標準函式庫） | 原生支援、無額外依賴、終端相容性好 |
| 資料格式 | JSON | 通用性強、可讀性好、與前後端生態無縫對接 |

### 🗺️ 後續計劃

- [ ] **Web 端視覺化面板**：提供 Web UI，支援線上指紋分析和報告檢視。
- [ ] **瀏覽器外掛整合**：開發 Chrome/Firefox 外掛，實作真實瀏覽器環境的指紋採集。
- [ ] **更多指紋維度**：增加 WebRTC ICE 候選、Battery API 詳細資訊、Speech Synthesis 指紋等。
- [ ] **機器學習評分**：引入 ML 模型，基於真實指紋資料庫訓練更精準的評分演算法。
- [ ] **指紋對抗測試**：整合主流指紋偵測服務（如 FingerprintJS、CreepJS）的測試能力。
- [ ] **配置匯入匯出**：支援從 Puppeteer Stealth、Playwright 等工具匯入指紋配置。
- [ ] **多語言文件**：完善英文、日文等多語言文件。
- [ ] **CI/CD 整合**：支援在 CI/CD 流水線中進行指紋一致性自動化檢查。

### 🤝 社群貢獻方向

我們歡迎以下類型的貢獻：

- 🐛 **Bug 修復**：修復已知的錯誤和異常。
- ✨ **新功能**：添加新的指紋維度、評分規則或 CLI 命令。
- 📚 **文件完善**：改進文件、添加使用範例、翻譯多語言版本。
- 🧪 **測試覆蓋**：增加單元測試和整合測試。
- 🎨 **UI 改進**：優化 TUI 儀表板的視覺效果和互動體驗。
- 📊 **資料分析**：提供指紋資料的統計分析工具。

---

## 🤝 貢獻指南

感謝你對 GhostLens-Pro 的關注！我們歡迎任何形式的貢獻。

### 📌 PR 規範

1. **分支命名**：使用 `feature/xxx`、`fix/xxx`、`docs/xxx` 等前綴。
2. **提交資訊**：遵循 [Conventional Commits](https://www.conventionalcommits.org/) 規範：
   - `feat: 新增新的指紋維度`
   - `fix: 修復評分演算法錯誤`
   - `docs: 更新 README 文件`
   - `test: 增加一致性校驗器測試`
   - `refactor: 優化程式碼結構`
3. **程式碼風格**：遵循 PEP 8，所有函式和類別必須有完整的 docstring，使用型別註解。
4. **測試要求**：所有 PR 必須通過現有測試，新增功能需附帶對應測試。
5. **文件更新**：如果 PR 涉及功能變更，請同步更新 README 和 CLI 說明資訊。

### 📌 Issue 回饋規則

提交 Issue 時，請包含以下資訊：

- **Python 版本**：`python --version`
- **作業系統**：Windows/macOS/Linux 及版本號
- **重現步驟**：詳細描述如何重現問題
- **期望行為**：描述你期望的正確行為
- **實際行為**：描述實際發生的錯誤行為
- **錯誤資訊**：貼上完整的錯誤堆疊或日誌

---

## 📄 開源協議

本專案基於 [MIT License](https://github.com/gitstq/GhostLens-Pro/blob/main/LICENSE) 開源。

```
MIT License

Copyright (c) 2024 GhostLens-Pro Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<a id="english"></a>

# 🇬🇧 English

## 🎉 Introduction

### 🎯 What is GhostLens-Pro?

GhostLens-Pro is a **lightweight browser fingerprint intelligence analysis and anti-detection scoring engine** delivered as a Command Line Interface (CLI) tool. It focuses on browser fingerprint collection, analysis, scoring, generation, and comparison, helping developers and security researchers comprehensively understand and evaluate the privacy risks associated with browser fingerprints.

### 💡 Core Value

- **Comprehensive Fingerprint Insight**: Covers 32+ fingerprint dimensions, from User-Agent to WebGL, from Canvas to Audio fingerprints, providing an in-depth analysis of every aspect of browser identity.
- **Intelligent Anti-Detection Scoring**: Employs a multi-dimensional weighted algorithm to output intuitive A+/A/B/C/D grade scores, quickly pinpointing privacy vulnerabilities.
- **One-Click Realistic Profile Generation**: Ships with 12 built-in templates for mainstream browser + OS combinations, generating highly consistent fingerprint profiles in seconds.
- **Zero-Dependency Pure Python**: Built exclusively with the Python standard library, requiring no third-party packages -- install and run immediately.

### 🔥 Problems We Solve

| Problem | GhostLens-Pro Solution |
|---------|----------------------|
| Fingerprint dimensions are scattered and hard to evaluate comprehensively | One command collects 32+ dimensions with a complete report |
| Lack of a unified anti-detection scoring standard | Multi-dimensional weighted scoring algorithm with A+~D five-tier quantification |
| Manual fingerprint profile construction is time-consuming and error-prone | 12 built-in templates + smart randomization for one-click generation |
| Internal inconsistencies in fingerprint profiles lead to exposure | 14 consistency check rules to automatically detect contradictions |
| Differences between multiple profiles are hard to quantify | Weighted similarity algorithm + high-risk difference identification |
| Existing tools are heavy with many dependencies | Pure standard library implementation with zero external dependencies |

### ✨ Differentiating Highlights

- 🧬 **Self-Developed Scoring Engine**: No dependency on any third-party fingerprint detection services. The scoring algorithm is fully self-implemented and supports offline usage.
- 🎨 **Interactive TUI Dashboard**: Terminal UI based on curses with real-time progress bars, color coding, and keyboard navigation -- say goodbye to plain text output.
- 🔍 **14 Consistency Checks**: From UA-platform matching to font-OS correspondence, from touch support to hardware ranges, comprehensively detecting internal contradictions in fingerprint profiles.
- 📊 **Multi-Format Report Export**: Supports terminal text, JSON, and HTML output formats to meet the needs of both automated integration and manual review.
- 🌱 **Reproducible Randomization**: Achieve reproducible fingerprint generation via the `--seed` parameter, facilitating debugging and regression testing.

### 🧠 Inspiration

GhostLens-Pro was inspired by the growing tension between the rapid advancement of browser fingerprinting technologies and the need for privacy protection. As advanced fingerprinting techniques like Canvas, WebGL, and AudioContext have become widespread, traditional privacy measures (such as disabling cookies or using incognito mode) are no longer sufficient. We aim to provide developers and security researchers with a lightweight, efficient, and user-friendly tool to help them deeply understand how browser fingerprints work, evaluate the privacy strength of fingerprint profiles, and quickly generate high-quality stealth configurations.

---

## ✨ Core Features

### 🔎 Fingerprint Collection Engine

- **32+ Fingerprint Dimensions**: Covers User-Agent, Screen Info, Canvas Fingerprint, WebGL Info, Font List, Audio Fingerprint, Hardware Info, Touch Support, Battery Status, Network Connection, Cookie Status, DNT, PDF Viewer, Plugin List, Storage Quota, Media Devices, Speech Synthesis, ClientRects, iframe Detection, Performance API, Console Detection, Debugger Detection, WebDriver Detection, WebRTC Leak, Permissions API, CSS Features, Math Constants, Error Messages, Feature Detection, and more.
- **Risk Score per Dimension** (0-100), intuitively displaying the privacy risk level of each dimension.
- **Real-Data-Based Simulation**: Built-in extensive real browser fingerprint data templates ensure generated profiles are highly realistic.

### 📊 Anti-Detection Scoring Engine

- **Comprehensive Scoring Algorithm**: Weighted calculation based on 4 major risk categories (Automation Detection, Fingerprint Uniqueness, Behavioral Analysis, Network Characteristics), outputting a 0-100 overall anti-detection score.
- **Five-Tier Grading System**: A+ (Excellent, 95+), A (Good, 85+), B (Fair, 70+), C (Poor, 50+), D (Dangerous, <50).
- **4 Major Risk Categories**:
  - 🤖 **Automation Detection** (Weight 35%): WebDriver, Debugger, Console, Performance, ClientRects, iframe
  - 🎨 **Fingerprint Uniqueness** (Weight 25%): Canvas, WebGL, Audio, Fonts, Math Constants, Error Messages, CSS Features
  - 🧩 **Behavioral Analysis** (Weight 20%): Touch, Battery, Connection, Storage, Media Devices, Speech, Permissions
  - 🌐 **Network Characteristics** (Weight 20%): WebRTC, Cookies, DNT, Features
- **Smart Improvement Suggestions**: Automatically generates priority-ranked improvement suggestions for high-risk dimensions.

### 🛠️ Fingerprint Profile Generator

- **12 Built-in Templates**: Covers mainstream combinations of Chrome/Firefox/Safari/Edge x Windows/macOS/Linux/iOS/Android.
- **Smart Randomization**: Randomizes non-critical parameters like Canvas hashes, storage usage, and connection info to avoid generating identical profiles.
- **Reproducible Generation**: Achieve deterministic generation via the `--seed` parameter for debugging and regression testing.
- **Batch Generation**: Supports generating multiple fingerprint profiles at once for large-scale testing needs.

### ✅ Fingerprint Consistency Checker

- **14 Consistency Check Rules**:
  1. UA-Platform information matching
  2. Screen resolution vs. device type matching
  3. Font list vs. OS matching
  4. WebGL renderer vs. OS matching
  5. Touch support vs. device type matching
  6. Hardware info vs. device type matching
  7. Plugin list vs. browser matching
  8. Storage quota vs. device type matching
  9. Color depth validity
  10. Pixel ratio vs. OS matching
  11. WebDriver detection status
  12. Cookie enabled status
  13. PDF viewer vs. browser matching
  14. Language settings consistency
- **Three Severity Levels**: Critical, Warning, Info.
- **Auto-Fix Suggestions**: Each issue comes with specific remediation advice.

### 📐 Fingerprint Comparator

- **Weighted Similarity Calculation**: Weights each dimension by its contribution to fingerprint uniqueness, outputting an overall similarity percentage.
- **High-Risk Difference Identification**: Automatically flags high-risk differing dimensions including UA, Canvas, WebGL, Fonts, Audio, Platform, Screen, and Hardware.
- **Multi-Strategy Comparison**: Employs optimal comparison strategies (Jaccard similarity, LCS, relative difference, etc.) for different data types (dict, list, numeric, string).
- **Batch Comparison**: Supports comparing multiple target profiles against a single baseline profile.

### 🖥️ TUI Dashboard

- **curses Terminal UI**: Built on the Python standard library curses module, requiring no additional dependencies.
- **Real-Time Progress Bars**: Visual display of scoring progress and category scores.
- **Color Coding**: Different grades use different colors (green=excellent, yellow=fair, red=dangerous).
- **Keyboard Navigation**: Supports arrow keys, Enter, and shortcut keys (S/F/C/H/R/Q).
- **Multi-View Switching**: Main menu, Score view, Fingerprint data view, Consistency view, Help view.
- **Graceful Degradation**: Automatically falls back to text mode when curses is unavailable.

---

## 🚀 Quick Start

### 📋 Prerequisites

- **Python** 3.8 or higher
- **Operating System**: Windows / macOS / Linux
- **External Dependencies**: None (zero external dependencies, standard library only)

### 📦 Installation

**Option 1: Install directly from GitHub via pip**

```bash
pip install git+https://github.com/gitstq/GhostLens-Pro.git
```

**Option 2: Clone and install locally**

```bash
git clone https://github.com/gitstq/GhostLens-Pro.git
cd GhostLens-Pro
pip install .
```

**Option 3: Development mode (recommended for contributors)**

```bash
git clone https://github.com/gitstq/GhostLens-Pro.git
cd GhostLens-Pro
pip install -e .
```

### 🎮 Launch

After installation, run the following command in your terminal:

```bash
ghostlens-pro --help
```

If you installed using Option 2 or 3, you can also launch via:

```bash
python -m ghostlens_pro --help
```

### ⚡ Quick Demo

```bash
# Execute a full fingerprint scan with scoring
ghostlens-pro scan

# Generate a Chrome on Windows fingerprint profile
ghostlens-pro generate --browser chrome --os windows

# Run consistency check
ghostlens-pro check --input my_profile.json

# Compare two fingerprint profiles
ghostlens-pro compare --file1 profile1.json --file2 profile2.json

# Launch the TUI dashboard
ghostlens-pro dashboard

# Generate an HTML report
ghostlens-pro report --html --output report.html

# List all built-in templates
ghostlens-pro list-profiles
```

---

## 📖 Detailed Usage Guide

### 🔧 CLI Subcommands Overview

| Command | Description | Common Options |
|---------|-------------|---------------|
| `scan` | Execute fingerprint collection and scoring | `--os`, `--browser`, `--device`, `--seed` |
| `score` | Score an existing fingerprint profile | `--input` |
| `generate` | Generate a fingerprint profile | `--template`, `--os`, `--browser`, `--device`, `--seed`, `--no-randomize` |
| `check` | Check fingerprint consistency | `--input` |
| `compare` | Compare two fingerprint profiles | `--file1`, `--file2`, `--name1`, `--name2` |
| `dashboard` | Launch TUI dashboard | None |
| `report` | Generate a full report | `--os`, `--browser`, `--device`, `--seed` |
| `list-profiles` | List built-in templates | None |

### 🌐 Global Options

| Option | Short | Description |
|--------|-------|-------------|
| `--json` | - | Output in JSON format |
| `--html` | - | Output in HTML format |
| `--output` | `-o` | Specify output file path |
| `--verbose` | `-v` | Verbose output mode |
| `--quiet` | `-q` | Quiet mode, suppress non-error output |

### 📝 Advanced Usage

#### 1. Fingerprint Scanning & Scoring

```bash
# Basic scan (default: Chrome + Windows + Desktop)
ghostlens-pro scan

# Specify target environment
ghostlens-pro scan --os macos --browser safari --device desktop

# Use a random seed for reproducibility
ghostlens-pro scan --seed 42

# Output JSON format to a file
ghostlens-pro scan --json --output scan_result.json

# Verbose mode
ghostlens-pro scan --verbose
```

#### 2. Fingerprint Profile Generation

```bash
# Generate using a built-in template
ghostlens-pro generate --template chrome_win10

# Custom browser and OS combination
ghostlens-pro generate --browser firefox --os linux

# Generate a mobile profile
ghostlens-pro generate --browser chrome --os android --device mobile

# Disable randomization (use template defaults)
ghostlens-pro generate --template safari_macos --no-randomize

# Generate and save to a file
ghostlens-pro generate --template edge_win10 --output my_edge_profile.json
```

#### 3. Consistency Check

```bash
# Check a fingerprint profile file
ghostlens-pro check --input my_profile.json

# Check and output in JSON format
ghostlens-pro check --input my_profile.json --json --output check_result.json
```

#### 4. Fingerprint Comparison

```bash
# Compare two fingerprint profiles
ghostlens-pro compare --file1 profile_a.json --file2 profile_b.json

# Custom names
ghostlens-pro compare --file1 profile_a.json --file2 profile_b.json --name1 "Chrome Win10" --name2 "Firefox Linux"

# Output in JSON format
ghostlens-pro compare --file1 profile_a.json --file2 profile_b.json --json --output compare_result.json
```

#### 5. Report Generation

```bash
# Generate an HTML report
ghostlens-pro report --html --output report.html

# Generate a JSON report
ghostlens-pro report --json --output report.json

# Generate a report for a specific target environment
ghostlens-pro report --os macos --browser safari --html --output safari_report.html
```

#### 6. TUI Dashboard

```bash
# Launch the interactive dashboard
ghostlens-pro dashboard

# Dashboard shortcuts:
# UP/DOWN  - Navigate menu / Scroll content
# ENTER    - Select menu item
# S        - Scan fingerprint
# F        - View fingerprint data
# C        - View consistency check
# R        - Return to main menu
# H        - Show help
# Q / ESC  - Quit
```

### 📋 Built-in Templates

| Template ID | Name | Browser | OS | Device Type |
|-------------|------|---------|----|-------------|
| `chrome_win10` | Chrome on Windows 10 | Chrome | Windows | Desktop |
| `chrome_win11` | Chrome on Windows 11 | Chrome | Windows | Desktop |
| `chrome_macos` | Chrome on macOS | Chrome | macOS | Desktop |
| `chrome_linux` | Chrome on Linux | Chrome | Linux | Desktop |
| `firefox_win10` | Firefox on Windows 10 | Firefox | Windows | Desktop |
| `firefox_macos` | Firefox on macOS | Firefox | macOS | Desktop |
| `safari_macos` | Safari on macOS | Safari | macOS | Desktop |
| `edge_win10` | Edge on Windows 10 | Edge | Windows | Desktop |
| `chrome_ios` | Chrome on iOS | Chrome | iOS | Mobile |
| `chrome_android` | Chrome on Android | Chrome | Android | Mobile |
| `safari_ios` | Safari on iOS | Safari | iOS | Mobile |
| `chrome_android_pixel` | Chrome on Pixel 5 | Chrome | Android | Mobile |

### 🎯 Typical Use Cases

#### Use Case 1: Privacy Assessment

You want to evaluate the privacy risk level of your current browser fingerprint:

```bash
ghostlens-pro scan
```

#### Use Case 2: Fingerprint Stealth

You need to generate a realistic Chrome on Windows fingerprint profile for testing:

```bash
ghostlens-pro generate --template chrome_win10 --output stealth_profile.json
ghostlens-pro check --input stealth_profile.json
```

#### Use Case 3: Batch Testing

You need to generate 10 different fingerprint profiles for batch testing:

```bash
for i in $(seq 1 10); do
  ghostlens-pro generate --template chrome_win10 --seed $i --output "profile_${i}.json"
done
```

#### Use Case 4: Profile Comparison

You need to compare the differences between two fingerprint profiles:

```bash
ghostlens-pro compare --file1 profile_1.json --file2 profile_2.json --json --output diff.json
```

#### Use Case 5: Report Generation

You need to generate a comprehensive HTML analysis report:

```bash
ghostlens-pro report --html --output full_report.html
```

---

## 💡 Design Philosophy & Roadmap

### 🏗️ Design Principles

1. **Lightweight First**: Zero external dependencies, pure Python standard library implementation. Install and run with no bloat.
2. **Modular Architecture**: Five independent engines (Collection, Scoring, Generation, Checking, Comparison) are decoupled and can be used individually or in combination.
3. **Data-Driven**: All fingerprint data is based on real browser behavior statistics, ensuring generated profiles are highly realistic.
4. **Extensibility**: Clean module interfaces and type annotations make it easy for the community to contribute new fingerprint dimensions and scoring rules.
5. **Security Compliance**: This tool is intended for educational and research purposes only. We do not encourage or assist in any illegal activities.

### 🔧 Technical Choices

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Language | Python 3.8+ | Rich ecosystem, high development efficiency, excellent cross-platform support |
| External Dependencies | None | Lower installation barrier, avoid version conflicts, improve portability |
| CLI Framework | argparse (stdlib) | No extra dependencies, feature-complete, officially recommended by Python |
| TUI Framework | curses (stdlib) | Native support, no extra dependencies, good terminal compatibility |
| Data Format | JSON | Highly versatile, human-readable, seamless integration with frontend/backend ecosystems |

### 🗺️ Roadmap

- [ ] **Web Visualization Panel**: Provide a Web UI for online fingerprint analysis and report viewing.
- [ ] **Browser Extension Integration**: Develop Chrome/Firefox extensions for real browser environment fingerprint collection.
- [ ] **More Fingerprint Dimensions**: Add WebRTC ICE candidates, Battery API details, Speech Synthesis fingerprints, etc.
- [ ] **ML-Based Scoring**: Introduce ML models trained on real fingerprint databases for more accurate scoring.
- [ ] **Fingerprint Evasion Testing**: Integrate testing capabilities against mainstream fingerprint detection services (e.g., FingerprintJS, CreepJS).
- [ ] **Profile Import/Export**: Support importing fingerprint profiles from Puppeteer Stealth, Playwright, and other tools.
- [ ] **Multi-Language Documentation**: Complete documentation in English, Japanese, and other languages.
- [ ] **CI/CD Integration**: Support automated fingerprint consistency checks in CI/CD pipelines.

### 🤝 Community Contribution Areas

We welcome the following types of contributions:

- 🐛 **Bug Fixes**: Fix known errors and exceptions.
- ✨ **New Features**: Add new fingerprint dimensions, scoring rules, or CLI commands.
- 📚 **Documentation**: Improve docs, add usage examples, translate to other languages.
- 🧪 **Test Coverage**: Add unit tests and integration tests.
- 🎨 **UI Improvements**: Optimize the visual design and interaction experience of the TUI dashboard.
- 📊 **Data Analysis**: Provide statistical analysis tools for fingerprint data.

---

## 🤝 Contributing Guide

Thank you for your interest in GhostLens-Pro! We welcome contributions of all forms.

### 📌 PR Guidelines

1. **Branch Naming**: Use prefixes like `feature/xxx`, `fix/xxx`, `docs/xxx`.
2. **Commit Messages**: Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
   - `feat: add new fingerprint dimension`
   - `fix: correct scoring algorithm`
   - `docs: update README`
   - `test: add consistency checker tests`
   - `refactor: improve code structure`
3. **Code Style**: Follow PEP 8. All functions and classes must have complete docstrings with type annotations.
4. **Testing Requirements**: All PRs must pass existing tests. New features must include corresponding tests.
5. **Documentation Updates**: If a PR involves functional changes, please update the README and CLI help messages accordingly.

### 📌 Issue Reporting Guidelines

When submitting an issue, please include the following information:

- **Python Version**: `python --version`
- **Operating System**: Windows/macOS/Linux and version number
- **Steps to Reproduce**: Detailed description of how to reproduce the issue
- **Expected Behavior**: Describe what you expect the correct behavior to be
- **Actual Behavior**: Describe the actual erroneous behavior
- **Error Messages**: Paste the complete error stack trace or log output

---

## 📄 License

This project is licensed under the [MIT License](https://github.com/gitstq/GhostLens-Pro/blob/main/LICENSE).

```
MIT License

Copyright (c) 2024 GhostLens-Pro Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  <sub>Built with ❤️ by the GhostLens-Pro Team</sub><br/>
  <sub>If you find this project helpful, please consider giving it a ⭐ on <a href="https://github.com/gitstq/GhostLens-Pro">GitHub</a>!</sub>
</p>
