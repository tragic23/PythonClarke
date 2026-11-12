FROM python:3.14-slim

# resolved buffer issue with logs 
ENV PYTHONUNBUFFERED=1  

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 
COPY . . 
CMD ["python", "main.py"]