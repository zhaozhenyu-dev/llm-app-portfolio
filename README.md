# python-20days

赵振宇的「AI 应用岗 近期集中开发」代码仓库 —— 从 Python 入门，到做出 3 个可在线演示的 AI 应用项目。

## 🚀 在线 Demo

| 项目 | 说明 | 链接 |
|------|------|------|
| **项目 1：AI 周报助手** | 把手写流水账一键转成格式规范、重点突出的周报 | [打开 Demo](https://python-20days-dcxzqfevfgkkkvqfevfgkkqvapxmvjuz.streamlit.app) |
| **项目 2：RAG 求职资料助手** | 用中文语义向量检索私有资料，让大模型「只依据资料作答」并标注 `[编号]` 出处，缓解幻觉 | [打开 Demo](https://python-20days-p3gwguohddqctexdntivccy.streamlit.app) |
| **项目 3：JD 匹配助手** | 基于 Agent（ReAct + function calling）自动解析 JD 与简历，用确定性算法算匹配度并给出提升建议 | [打开 Demo](https://python-20days-cj6vyfw4oseypfg9ppwepz.streamlit.app) |

## 🛠 技术栈

`Python` · `Agent (ReAct + function calling)` · `DeepSeek API (OpenAI 兼容)` · `LangChain` · `FastEmbed (bge-small-zh-v1.5)` · `FAISS` · `Streamlit` · `pytest` · `GitHub Actions (CI)`

## 📂 学习路线与目录

- `day1` ~ `day5`：Python 基础语法、列表/字典、函数、异常处理 + 文件读写 + JSON、类与对象
- `day6` ~ `day9`：requests + HTTP API、DeepSeek API 调用、简历润色智能体、面试问答智能体
- `day10`：AI 周报助手 MVP（项目 1）+ Git 进阶 + Streamlit Cloud 部署 + pytest 测试
- `day11` ~ `day13`：RAG 原理、语义向量 / TF-IDF 对比、LangChain + FAISS 实战
- `day14`：RAG 求职资料助手（项目 2）+ 语义为主 / TF-IDF 兜底降级 + pytest + GitHub Actions CI + Streamlit Cloud 部署
- `day16`：Agent 与工具调用入门——手写 ReAct + function calling（calculator 安全 eval + get_weather Open-Meteo 中文适配），理解"大模型只是 Agent 的脑"
- `day17`：项目 3 架构设计——把 Day16 通用 Agent 外壳当"万能插座"，设计两个求职工具
- `day18`：JD 匹配助手（项目 3）MVP——复用 Day16 外壳 + 插 `parse_profile` / `score_match` 两工具，Streamlit Cloud 部署上线

## ✨ 项目亮点

- **项目 2 采用「语义为主、TF-IDF 兜底」降级链路**：语义检索依赖异常时自动切换，保障问答服务不中断。
- **纯逻辑与界面解耦**：`rag_lib.py` 不依赖 Web 框架，核心 RAG 逻辑可独立测试、可复用。
- **测试与 CI**：编写 pytest 单元测试（用 mock 拦截外部 API），并配置 GitHub Actions，每次提交自动跑测试。
- **可溯源答案**：约束大模型「仅依据检索资料作答 + 用 `[编号]` 标注来源」，答案可溯源、缓解幻觉。
- **项目 3 复用 Day16 Agent 外壳**：Day16 手写的通用 ReAct + function calling 循环一行不重写，只替换工具表（`parse_profile` 解析 JD/简历 + `score_match` 确定性打分），Agent 从玩具升级成求职产品。
- **确定性打分不幻觉**：`score_match` 用加权公式（技能 0.6 / 经验 0.25 / 学历 0.15）算匹配度，同输入必同输出，把"可能对"变成"一定对"。

## 📌 备注

仓库为学习实践产物，代码按天归档；三个在线 Demo 均可直接访问体验。

> 仓库作者：[@zhaozhenyu-dev](https://github.com/zhaozhenyu-dev)
