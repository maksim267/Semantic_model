FROM python:3.12.8

WORKDIR /app

RUN pip install --upgrade pip
#http://localhost:8000/docs
# COPY requirements.txt ./
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python","main.py"]
#docker build . -t api_model_tonal после изменения в файлах запустить в терминале
#docker run -p 8000:8000 -e HF_API_TOKEN="hf_ваш API TOKEN" api_model_tonal запуск приложения
