FROM python:alpine
WORKDIR /app/si3mshady
COPY . .
RUN pip install -r requirements.txt
CMD ["python","app.py"]