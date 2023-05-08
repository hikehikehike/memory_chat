FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENV PORT=8000
ENV WORKERS_PER_CORE=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
