# 项目 3（JD 匹配助手）Docker 镜像
# 基于 day18/app.py 的 Streamlit 演示，依赖仅 streamlit + requests，轻量。
FROM python:3.11-slim

WORKDIR /app

# 先拷依赖清单，利用 Docker 层缓存（依赖不变就不重装）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷整个仓库：day18 应用 + day16 外壳（jd_match_agent 会跨目录 import call_deepseek）都要
COPY . .

EXPOSE 8501

# Streamlit 必须监听 0.0.0.0 才能被容器外访问
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

CMD ["streamlit", "run", "day18/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
