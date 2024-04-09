# Use an official lightweight Python image.
FROM python:3.9-slim

WORKDIR /app

COPY ./src /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /app/

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]