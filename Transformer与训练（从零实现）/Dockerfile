# Dockerfile — 从零实现 Transformer 训练/推理镜像
# 构建：  docker build -t char-gpt .
# 训练：  docker run --rm -v "$(pwd)/checkpoints:/app/checkpoints" char-gpt python train.py --config config.yaml
# 生成：  docker run --rm -it -v "$(pwd)/checkpoints:/app/checkpoints" char-gpt python generate.py --prompt "清华" --length 300

# --- 构建阶段 ---
FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- 运行阶段 ---
FROM python:3.11-slim

WORKDIR /app

# 从构建阶段复制 site-packages（避免重新下载）
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# 复制源码
COPY . .

# 非 root 运行
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# checkpoints 挂载点
VOLUME ["/app/checkpoints"]

# 默认命令：打印用法
CMD ["python", "train.py", "--help"]
