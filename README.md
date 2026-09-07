# AI 应用作品集 · LLM Apps

3 个已上线的 Python 大模型应用：RAG 知识库问答、Agent 应用（ReAct + function calling）、结构化文本生成，均配备 pytest 单元测试、GitHub Actions CI 与 Docker 镜像构建校验。

[![CI](https://github.com/zhaozhenyu-dev/llm-app-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/zhaozhenyu-dev/llm-app-portfolio/actions/workflows/ci.yml)

> CI 每次提交自动执行两项校验：① `pytest` 单元测试（mock 拦截外部 API）；② Docker 镜像构建校验，确保 `Dockerfile` 始终可构建。

## 🚀 在线 Demo

| 项目 | 说明 | 链接 |
|------|------|------|
| **AI 周报助手** | 把手写流水账一键转成格式规范、重点突出的周报 | [打开 Demo](https://llm-app-portfolio-fgcfrtkcnslqpa2mnpvgfy.streamlit.app) |
| **RAG 求职资料助手** | 用中文语义向量检索私有资料，让大模型「只依据资料作答」并标注 `[编号]` 出处，缓解幻觉；检索评估最优命中 10/10（10 道测试题 × 6 组 chunk/top-k 参数对比） | [打开 Demo](https://llm-app-portfolio-sdya3nmbqzg6rglk9b2nmt.streamlit.app) |
| **JD 匹配助手** | 基于 Agent（ReAct + function calling）自动解析 JD 与简历，用确定性算法算匹配度并给出提升建议 | [打开 Demo](https://llm-app-portfolio-n7tdupvpwauyydgtvbjrar.streamlit.app) |

## 🛠 技术栈

`Python` · `Agent (ReAct + function calling)` · `DeepSeek API (OpenAI 兼容)` · `LangChain` · `FastEmbed (bge-small-zh-v1.5)` · `FAISS` · `Streamlit` · `pytest` · `GitHub Actions (CI)` · `Docker`

## 📂 代码结构

- `day9/`：**AI 周报助手**（项目 1）—— Streamlit + DeepSeek API + pytest + 云端部署
- `day14/`：**RAG 求职资料助手**（项目 2）—— 语义向量检索 / TF-IDF 兜底降级 + pytest + GitHub Actions CI
- `day16/`：**通用 Agent 外壳** —— 封装的 ReAct + function calling Agent 循环（示例工具：安全计算器 / 天气查询）
- `day18/`：**JD 匹配助手**（项目 3）—— 复用 Agent 外壳 + `parse_profile` / `score_match` 两个工具 + Streamlit 界面
- `day19/`：**工程化收尾** —— Dockerfile（python:3.11-slim 分层构建）+ 模拟面试打分脚本 `interview_coach.py`
- 其余 `dayN/` 目录为基础模块与功能验证代码（HTTP/API、文件处理、类与对象等）

## ✨ 项目亮点

- **项目 2 采用「语义为主、TF-IDF 兜底」降级链路**：语义检索依赖异常时自动切换，保障问答服务不中断。
- **纯逻辑与界面解耦**：`rag_lib.py` 不依赖 Web 框架，核心 RAG 逻辑可独立测试、可复用。
- **测试与 CI**：编写 pytest 单元测试（用 mock 拦截外部 API），并配置 GitHub Actions，每次提交自动跑测试 + Docker 镜像构建校验（单元测试 + 容器化双重保障）。
- **可溯源答案**：约束大模型「仅依据检索资料作答 + 用 `[编号]` 标注来源」，答案可溯源、缓解幻觉。
- **检索效果可量化**：用 10 道测试题 × 6 组 chunk/top-k 参数对比评估检索效果，最优命中 10/10 并记录调优依据，避免「凭感觉调参」。
- **项目 3 复用通用 Agent 外壳**：同一套 ReAct + function calling 循环复用，只替换工具表（`parse_profile` 解析 JD/简历 + `score_match` 确定性打分），体现工程抽象与模块复用能力。
- **确定性打分不幻觉**：`score_match` 用加权公式（技能 0.6 / 经验 0.25 / 学历 0.15）算匹配度，同输入必同输出，把"可能对"变成"一定对"。

## 🏃 本地运行

### JD 匹配助手（day18）
```bash
git clone https://github.com/zhaozhenyu-dev/llm-app-portfolio.git
cd llm-app-portfolio
pip install -r requirements.txt
export DEEPSEEK_API_KEY="sk-你的key"
streamlit run day18/app.py
```
浏览器打开 http://localhost:8501 ，粘贴 JD + 简历，点「匹配」即可看到匹配报告。

### 用 Docker 跑 JD 匹配助手
```bash
docker build -t jd-match .
docker run -e DEEPSEEK_API_KEY="sk-你的key" -p 8501:8501 jd-match
```
镜像基于 `python:3.11-slim`，仅装 `streamlit` + `requests`，轻量；容器内 Streamlit 监听 `0.0.0.0:8501`。

### 模拟面试打分（day19）
```bash
python3 day19/interview_coach.py --selftest   # 自测：内置 JD + 假回答跑通出题→打分
python3 day19/interview_coach.py              # 交互：输入 JD → 逐题回答 → 看评分
```

## 📌 备注

代码按开发阶段归档（`dayN` 目录）；三个在线 Demo 均可直接访问体验。

> 作者：[@zhaozhenyu-dev](https://github.com/zhaozhenyu-dev)
