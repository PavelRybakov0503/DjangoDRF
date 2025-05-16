# Используем официальный образ Nginx
FROM nginx:latest

# Копируем файл конфигурации Nginx в контейнер
COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /app/staticfiles

# Открываем порт 80 для HTTP-трафика
EXPOSE 80