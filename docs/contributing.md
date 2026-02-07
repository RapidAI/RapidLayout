---
comments: true
title: 贡献指南
hide:
  - navigation
  - toc
---

感谢你对 Rapid Layout 的关注与贡献！本文档说明如何参与项目的代码开发与文档贡献，包括环境准备、开发流程和提交流程。

## 前置要求

- Python >= 3.6（推荐 3.8+）
- Git
- 已注册的 GitHub 账号

---

## 一、克隆源码

从 Rapid Layout 主仓库克隆项目到本地：

```bash
git clone https://github.com/RapidAI/RapidLayout.git
cd RapidLayout
```

若网络受限，可先 Fork 到个人账号后再克隆（见后文「准备提交」部分）。

---

## 二、配置开发环境

建议使用虚拟环境，避免与系统 Python 冲突：

```bash
# 使用 venv
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# 或使用 conda
conda create -n rapidlayout python=3.10
conda activate rapidlayout
```

安装依赖（开发时建议可编辑安装以便本地修改生效）：

```bash
pip install -r requirements.txt
pip install pytest   # 运行单元测试需要
pip install -e .
```

如需使用 ONNX Runtime 等推理后端，请按 [安装文档](https://rapidai.github.io/RapidLayout/install_usage/installation/) 安装对应依赖。

---

## 三、安装代码格式化与 pre-commit 钩子

在已激活的虚拟环境中安装 pre-commit，并在**仓库根目录**启用 Git 提交前钩子，以便自动做代码格式检查与整理（如 black、autoflake 等）：

```bash
pip install pre-commit
pre-commit install
```

安装成功后，每次执行 `git commit` 时会自动运行配置好的格式化工具；若检查未通过，提交会被拒绝，请根据提示修改后再次提交。也可在提交前手动跑一遍：

```bash
pre-commit run --all-files
```

---

## 四、运行单元测试

在**仓库根目录**下执行：

```bash
# 运行全部测试
pytest tests/ -v

# 仅运行部分测试文件
pytest tests/test_main.py -v

# 查看测试覆盖率（需先安装 pytest-cov）
pytest tests/ -v --cov=rapid_layout
```

确认当前主分支在你本机环境下测试通过，再进行修改。

---

## 五、复现问题 / 增加新功能

### 反馈问题与建议

- **Bug 反馈**：在 [Issues](https://github.com/RapidAI/RapidLayout/issues) 中提交 Bug 报告，请尽量包含复现步骤、环境信息与报错信息。
- **功能建议**：在 Issues 中使用 Feature Request 模板描述你的需求或使用场景。
- **文档与示例**：发现文档错误或希望补充示例时，可直接提 Issue 或 PR。

### 复现 Bug

1. 在 [Issues](https://github.com/RapidAI/RapidLayout/issues) 中选定或创建对应 issue。
2. 根据 issue 描述与报错信息，在本地用仓库代码复现问题。
3. 在 `rapid_layout/` 或 `tests/` 下定位并修改代码，直到问题消失。

### 增加新功能

1. 与 maintainer 或现有 issue 讨论需求与实现方式（可选但推荐）。
2. 在 `rapid_layout/` 下实现新逻辑，保持与现有代码风格一致（项目使用 [black](https://github.com/psf/black) 等规范）。
3. 新功能应有对应单元测试覆盖。

---

## 六、编写对应单元测试

- 测试文件放在 **`tests/`** 下，命名建议 `test_*.py`。
- 使用 **pytest** 编写用例，可参考现有 `test_main.py`。
- 测试用图片等资源放在 `tests/test_files/`。
- 新增测试应：
    - 能稳定复现你要验证的行为（Bug 修复或新功能）；
    - 不依赖未在仓库或文档中说明的外部服务（必要时用 mock 或跳过）。

示例：

```python
# tests/test_xxx.py
import pytest
from pathlib import Path

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent
test_dir = cur_dir / "test_files"

def get_engine():
    from rapid_layout import RapidLayout
    return RapidLayout()

def test_your_new_feature():
    engine = get_engine()
    img_path = test_dir / "layout.jpg"
    result = engine(img_path)
    assert result is not None
    # 更多断言...
```

---

## 七、运行所有单元测试

在**仓库根目录**下再次全量跑测，确保无回归：

```bash
pytest tests/ -v
```

若有测试被跳过（如缺少某推理引擎），请确认你修改或新增的测试在现有环境下已执行并通过。

---

## 八、准备提交到仓库

### 8.1 Fork Rapid Layout 主仓库到个人账号

1. 打开 [Rapid Layout 主仓库](https://github.com/RapidAI/RapidLayout)。
2. 点击右上角 **Fork**，将仓库 fork 到你自己的 GitHub 账号下（例如 `https://github.com/你的用户名/RapidLayout`）。

### 8.2 将代码提交到个人 Fork

若最初是克隆的主仓库，需要添加你的 fork 为远程，并推送到 fork：

```bash
# 在项目根目录 RapidLayout 下执行
git remote add myfork https://github.com/你的用户名/RapidLayout.git
# 若已有 origin 且就是主仓库，可保留；推送时用 myfork

# 创建分支（推荐为每个 issue/功能单独分支）
git checkout -b fix/xxx   # 或 feat/xxx、docs/xxx

# 添加并提交修改
git add .
git status   # 确认只提交预期文件
git commit -m "fix: 简短描述"

# 推送到你的 fork
git push myfork fix/xxx
```

**请按约定式提交规范（Conventional Commits）书写 commit 信息**，便于维护者阅读与自动生成 Changelog。格式为：

```text
<类型>[可选范围]: <简短描述>

[可选正文]
[可选脚注]
```

常用类型示例：

| 类型       | 说明                   |
|------------|------------------------|
| `feat`     | 新功能                 |
| `fix`      | Bug 修复               |
| `docs`     | 文档变更               |
| `style`    | 代码格式（不影响逻辑） |
| `refactor` | 重构                   |
| `test`     | 测试相关               |
| `chore`    | 构建/工具等            |

示例：`fix: 修复某条件下版面结果为空`、`feat: 支持 xxx 输入格式`、`docs: 更新安装说明`。

### 8.3 向 Rapid Layout 主仓库提交 Pull Request（PR）

1. 打开你 fork 后的仓库页面（如 `https://github.com/你的用户名/RapidLayout`）。
2. 若刚推送分支，页面上通常会出现 **Compare & pull request**，点击即可；否则在 **Branches** 里选择你刚推送的分支，再点 **New pull request**。
3. 确认 **base 仓库** 为 `RapidAI/RapidLayout`、**base 分支** 为 `main`（或仓库默认主分支），**head 仓库** 为你的 fork、**head 分支** 为你的分支（如 `fix/xxx`）。
4. 填写 PR 标题和说明：
   - 标题：简要概括修改内容（如「Fix: 修复 xxx 问题」）。
   - 说明中建议包含：
     - 对应 Issue 编号（若有）：`Fixes #123` 或 `Related to #123`。
     - 修改原因与主要改动。
     - 如何验证：例如「在仓库根目录执行 `pytest tests/ -v` 通过」。
5. 提交 PR，等待 maintainer 审查；根据反馈再在本地修改并推送同一分支，PR 会自动更新。

---

## 流程小结

| 步骤 | 说明 |
|------|------|
| 1 | 克隆 Rapid Layout 源码 |
| 2 | 配置虚拟环境并安装依赖与 pytest，可编辑安装 `pip install -e .` |
| 3 | 安装 pre-commit（`pip install pre-commit`），在仓库根目录执行 `pre-commit install` |
| 4 | 运行单元测试（`pytest tests/ -v`），确认基线通过 |
| 5 | 复现问题或实现新功能 |
| 6 | 编写/补充对应单元测试 |
| 7 | 在仓库根目录运行全部测试并确认通过 |
| 8 | Fork 主仓库到个人账号 |
| 9 | 按约定式提交规范编写 commit，将修改提交并推送到个人 Fork 的对应分支 |
| 10 | 在主仓库创建 PR，从个人 Fork 分支指向主仓库 main |

---

## 文档本地预览

修改 `docs/` 下内容后，可使用 MkDocs 本地预览：

```bash
pip install mkdocs mkdocs-material
mkdocs serve
```

在浏览器中打开提示的地址（一般为 `http://127.0.0.1:8000`）即可查看效果。

---

## 其他说明

- **代码风格**：项目采用 [black](https://github.com/psf/black)、autoflake 等规范，已通过 pre-commit 钩子在提交时自动检查；也可在仓库根目录执行 `pre-commit run --all-files` 手动跑一遍。
- **文档**：更多安装与使用说明见 [Rapid Layout 文档](https://rapidai.github.io/RapidLayout/)。
- **问题与讨论**：Bug 与功能建议可通过 [GitHub Issues](https://github.com/RapidAI/RapidLayout/issues) 反馈。
- 提交 Issue 或 PR 时，请使用清晰、简洁的标题与描述，便于维护者处理。若你希望参与长期维护或较大功能开发，欢迎在 Issue 中说明，我们会与你沟通协作方式。

再次感谢你的贡献！
