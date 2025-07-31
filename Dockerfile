# Use official Python image
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    fonts-liberation \
    xdg-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Download Chrome for Testing and ChromeDriver (latest stable)
RUN CFT_VERSION=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | \
    python3 -c "import sys, json; print(json.load(sys.stdin)['channels']['Stable']['version'])") && \
    CFT_URL="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CFT_VERSION}/linux64/chrome-linux64.zip" && \
    DRIVER_URL="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CFT_VERSION}/linux64/chromedriver-linux64.zip" && \
    wget -O /tmp/chrome.zip "$CFT_URL" && \
    wget -O /tmp/chromedriver.zip "$DRIVER_URL" && \
    unzip /tmp/chrome.zip -d /opt/ && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    ln -s /opt/chrome-linux64/chrome /usr/bin/google-chrome && \
    ln -s /opt/chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    rm /tmp/chrome.zip /tmp/chromedriver.zip

ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
