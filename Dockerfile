FROM python:3.14-slim

# resolved buffer issue with logs 
ENV PYTHONUNBUFFERED=1  

WORKDIR /app

COPY requirements.txt .


# install package for voice_client to play audio file
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

COPY . . 

CMD ["python", "main.py"]