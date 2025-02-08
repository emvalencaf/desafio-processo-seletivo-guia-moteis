FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN prisma generate 

EXPOSE 8080

CMD ["fastapi", "run", "app.py"]