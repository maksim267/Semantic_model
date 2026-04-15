Sentiment Classifier API

Небольшое FastAPI-приложение для классификации тональности текста с использованием Hugging Face Inference API и внутреннего кэширования (lru_cache).


Структура проекта

project/
│── main.py              # FastAPI приложение
│── requirements.txt     # зависимости
│── README.md            # инструкция по запуску
│── tests/
│    └── test_all.py     # unit-тесты
│    └── __init__.py     #проект пакетом
│── Dockerfile           # контейнеризация


Запуск приложения:

1) Получить HF_API Token:
    а. Перейти в профиль Hugging Face в раздел "Access Tokens" (https://huggingface.co/settings/tokens)
    b. Нажать "Create new token" 
    c. Выбрать разрешение "Make calls to Inference Providers" и нажать "Create token"
    d. Скопировать выданный токен (hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx)

2) Запуск через Docker:
    a. Построить Docker-образ командой через PowerShell с помощью команды: 
        docker build -t api_model_tonal
    b. Запустить контейнер через PowerShell с помощью команды:
        docker run -p 8000:8000 -e HF_API_TOKEN="hf_полученный_вами_токен" api_model_tonal

3) Отправка запроса через веб-приложение:
    a. Откройте встроенную документацию FastAPI по адресу http://localhost:8000/docs
    b. Найдите метод POST /classify
    с. Нажмите “Try it out”
    d. В поле ввода замените значение: "test":"your text in English"
    e. Нажмите “Execute”, чтобы отправить запрос к API.

3) Отправка запроса через терминал PowerShell:
    a. Откройте новый терминал и введите команду предварительно заменив значение text = "your text in English":
        Invoke-RestMethod -Uri "http://localhost:8000/classify" `
                        -Method POST `
                        -Body (@{ text = "your text in English" } | ConvertTo-Json) `
                        -ContentType "application/json"

4) Просмотр Responses:
    a. Response body -> labels, список классов тональности отсортированных по уверенности модели
    b. Response body -> scores показана числовая уверенность модели для каждого класса (от 0 до 1)
    с. Response body -> cached Показывает, был ли ответ получен из кэша (true) или вычислен заново (false)

5) При необходимости повторного запроса проделайте шаги 3.d и 3.e (3.a при работе из терминала)


Запуск тестов:
1) Выполните 1 и 2 пункт раздела "Запуск приложения"
2) В новом терминале PowerShell введите команду:
 docker exec -it (docker ps -q | Select-Object -First 1) pytest -v
3) В качестве логов будут показаны проверки валидации, кэширования, внешнего API, позитивной нейтральной и негативной классификации

