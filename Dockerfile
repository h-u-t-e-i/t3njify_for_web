# ベースイメージ（Python 3.10系）
FROM python:3.10-slim

# 必要パッケージのインストール（ffmpeg, unzip）
RUN apt-get update && \
    apt-get install -y ffmpeg unzip && \
    apt-get clean

# 作業ディレクトリを作成
WORKDIR /app

# アプリケーションファイルをコピー
COPY . /app

# 依存関係をインストール
RUN pip install --upgrade pip && pip install -r requirements.txt

# ポート指定（Streamlitのデフォルト）
EXPOSE 8501

# Streamlitを起動
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]