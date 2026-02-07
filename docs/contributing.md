---
comments: true
title: 贡献指南
hide:
  - navigation
  - toc
---


感谢你对 Rapid Layout 的关注与贡献！欢迎通过以下方式参与项目。

## 贡献方式

### 反馈问题与建议

- **Bug 反馈**：在 [Issues](https://github.com/RapidAI/RapidLayout/issues) 中提交 Bug 报告，请尽量包含复现步骤、环境信息与报错信息。
- **功能建议**：在 Issues 中使用 Feature Request 模板描述你的需求或使用场景。
- **文档与示例**：发现文档错误或希望补充示例时，可直接提 Issue 或 PR。

### 提交代码（Pull Request）

1. **Fork 本仓库**，并在本地克隆你 Fork 后的仓库。
2. **创建分支**：从 `main` 拉取最新代码，建议使用独立分支进行修改，例如 `git checkout -b fix/xxx` 或 `feature/xxx`。
3. **开发与自测**：在本地完成修改与测试，确保不破坏现有行为。
4. **提交 PR**：将分支推送到你的 Fork，在 [RapidLayout](https://github.com/RapidAI/RapidLayout) 仓库中发起 Pull Request，并简要说明改动内容与原因。

我们会尽快 Review，必要时会与你讨论修改建议。

## 开发环境

### 环境准备

```bash linenums="1"
git clone https://github.com/RapidAI/RapidLayout.git
cd RapidLayout
pip install -r requirements.txt
pip install -e .
```

### 代码规范

项目使用 [black](https://github.com/psf/black) 做代码格式化，并配合 pre-commit 做提交前检查。建议在本地安装 pre-commit：

```bash linenums="1"
pip install pre-commit
pre-commit install
```

提交前会自动执行 `autoflake`（清理未使用导入与变量）和 `black` 格式化，请确保修改后的代码通过上述检查。

### 文档本地预览

修改 `docs/` 下内容后，可使用 MkDocs 本地预览：

```bash linenums="1"
pip install -r requirements.txt
mkdocs serve
```

在浏览器中打开提示的地址（一般为 `http://127.0.0.1:8000`）即可查看效果。

## 其他说明

- 提交 Issue 或 PR 时，请使用清晰、简洁的标题与描述，便于维护者处理。
- 若你希望参与长期维护或较大功能开发，欢迎在 Issue 中说明，我们会与你沟通协作方式。

再次感谢你的贡献！
