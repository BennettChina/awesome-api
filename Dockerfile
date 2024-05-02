FROM python:3.12-slim

LABEL maintainer="Bennett <bennett_aisa@outlook.com>"

WORKDIR /app

COPY requirements.txt ./
RUN uname -a && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "api.index:app", "--host", "0.0.0.0", "--port", "80"]
