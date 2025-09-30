FROM python:3.11

WORKDIR /app

# prevents python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

#prevents python from buffering stdin/stdout
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run the bot
CMD ["python", "bot_root.py"]