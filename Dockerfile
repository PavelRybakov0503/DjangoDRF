FROM python:3.12

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt
#     apt-get install -y gcc libpg-dev && \
#     apt-get update && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
