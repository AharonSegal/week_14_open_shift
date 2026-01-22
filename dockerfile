FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# copy application code
COPY app ./app

EXPOSE 8000

# run the fastapi application with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]