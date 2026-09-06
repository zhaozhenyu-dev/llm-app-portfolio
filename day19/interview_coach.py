"""
Day19：模拟面试打分教练（interview_coach）

复用 Day16 的 call_deepseek（Agent 外壳的模型调用），不重新造轮子：
  - gen_questions(jd)   ：给定岗位 JD，让 DeepSeek 出 3 道针对性面试题 + 评分要点
  - score_answer(jd, qa)：给定 JD + 候选人回答，让 DeepSeek 逐题打分(0-10) + 总评 + 建议

运行：
  python3 day19/interview_coach.py            # 交互模式：输入 JD → 答题 → 看评分
  python3 day19/interview_coach.py --selftest # 自测模式：用内置 JD + 假回答跑通闭环（无需手动输入）
"""
import os
import sys
import json

# 让本文件能 import 同仓库的 day16 外壳 call_deepseek
sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "day16"),
)
from agent_basic import call_deepseek


def _extract_json(text):
    """三保险抠 JSON：整段 → 扒 ```json 代码块 → 切 {…} 子串。"""
    if text is None:
        return None
    try:
        return json.loads(text)
    except Exception:
        pass
    import re
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass
    s, e = text.find("{"), text.rfind("}")
    if s != -1 and e != -1 and e > s:
        try:
            return json.loads(text[s:e + 1])
        except Exception:
            pass
    return None


def gen_questions(jd, api_key=None):
    """根据岗位 JD 生成针对性面试题 + 评分要点。"""
    messages = [
        {
            "role": "system",
            "content": "你是资深技术面试官。根据岗位 JD 设计 3 道针对性面试题，"
            "每题给 2 条评分要点。只输出 JSON，不要解释。",
        },
        {
            "role": "user",
            "content": (
                "岗位 JD：\n" + jd + "\n\n"
                '请输出 JSON：\n{\n'
                '  "questions": [\n'
                '    {"q": "题目", "points": ["评分要点1", "评分要点2"]}\n'
                "  ]\n}\n"
            ),
        },
    ]
    data, err = call_deepseek(messages, tools=None, api_key=api_key)
    if err:
        return None, err
    parsed = _extract_json(data["choices"][0]["message"].get("content", ""))
    if not isinstance(parsed, dict) or "questions" not in parsed:
        return None, "模型未返回合法 JSON"
    return parsed, None


def score_answer(jd, qa, api_key=None):
    """根据 JD + 候选人的问答记录打分。qa = [{"q":..., "a":...}, ...]"""
    payload = json.dumps(qa, ensure_ascii=False)
    messages = [
        {
            "role": "system",
            "content": "你是面试官，根据岗位 JD 和候选人的回答逐题打分(0-10)，"
            "给总分和建议。只输出 JSON，不要解释。",
        },
        {
            "role": "user",
            "content": (
                "岗位 JD：\n" + jd + "\n\n"
                "问答记录：\n" + payload + "\n\n"
                '请输出 JSON：\n{\n'
                '  "scores": [{"q": "题目", "score": 8, "comment": "点评"}],\n'
                '  "total": 24,\n'
                '  "advice": "改进建议"\n'
                "}\n"
            ),
        },
    ]
    data, err = call_deepseek(messages, tools=None, api_key=api_key)
    if err:
        return None, err
    parsed = _extract_json(data["choices"][0]["message"].get("content", ""))
    if not isinstance(parsed, dict) or "scores" not in parsed:
        return None, "模型未返回合法 JSON"
    return parsed, None


def _selftest():
    """内置 JD + 假回答，跑通出题→打分闭环，验证模型调用与降级。"""
    jd = (
        "Python 开发实习生：要求 Python、FastAPI、SQL、LangChain；"
        "本科及以上；能独立写 API、做简单 RAG 应用。"
    )
    print("=== [自测] 出题 ===")
    qs, err = gen_questions(jd, api_key=os.getenv("DEEPSEEK_API_KEY"))
    if err:
        print("出题失败：", err)
        return
    for i, item in enumerate(qs["questions"], 1):
        print(f"{i}. {item['q']}")
        print("   要点：", "；".join(item.get("points", [])))

    # 假回答（模拟候选人）
    qa = [{"q": item["q"], "a": "我做过类似项目，用 Python 写过 API，会用 SQL 和 LangChain。"} for item in qs["questions"]]
    print("\n=== [自测] 打分 ===")
    result, err = score_answer(jd, qa, api_key=os.getenv("DEEPSEEK_API_KEY"))
    if err:
        print("打分失败：", err)
        return
    for s in result["scores"]:
        print(f"{s['q']} → {s['score']}/10：{s.get('comment', '')}")
    print(f"总分：{result.get('total')}/30")
    print("建议：", result.get("advice", ""))


def _interactive():
    jd = input("岗位 JD（或粘贴简要要求）：\n")
    qs, err = gen_questions(jd, api_key=os.getenv("DEEPSEEK_API_KEY"))
    if err:
        print("出题失败：", err)
        return
    print("\n=== 模拟面试题 ===")
    for i, item in enumerate(qs["questions"], 1):
        print(f"{i}. {item['q']}")
        print("   评分要点：", "；".join(item.get("points", [])))
    print("\n请依次回答（每行一题）：")
    qa = []
    for item in qs["questions"]:
        a = input("你的回答：")
        qa.append({"q": item["q"], "a": a})
    result, err = score_answer(jd, qa, api_key=os.getenv("DEEPSEEK_API_KEY"))
    if err:
        print("打分失败：", err)
        return
    print("\n=== 评分 ===")
    for s in result["scores"]:
        print(f"{s['q']} → {s['score']}/10：{s.get('comment', '')}")
    print(f"总分：{result.get('total')}/30")
    print("建议：", result.get("advice", ""))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        _selftest()
    else:
        _interactive()
