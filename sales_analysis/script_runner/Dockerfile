# Exact base image format from the official docs
FROM python:3

# Same working directory as documentation
WORKDIR /usr/src/app

# 1. Copy requirements first (optimized layer caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy all other files (including scripts)
COPY . .

# 3. Set entrypoint to hello.py (matches "./your-daemon-or-script.py" in docs)
CMD ["python", "./scripts/hello.py"]
