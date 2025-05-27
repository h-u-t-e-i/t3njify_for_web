# ベースイメージは安定版の Python 3.10 を使用
FROM python:3.10-slim

# 作業ディレクトリを作成
WORKDIR /app

# distutils を手動インストール（必要な場合がある）
RUN apt-get update && apt-get install -y python3-distutils ffmpeg

# requirements.txt をコピーしてインストール
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

# アプリコードとデータをコピー
COPY . .

# Streamlit をポート指定で起動
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
