FROM python:alpine
WORKDIR /app/si3mshady
COPY . .
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["python","app.py"]