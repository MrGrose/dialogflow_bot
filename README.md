# Мультиплатформенный чат-бот на базе Dialogflow

## Описание
Этот проект - мультибот для Telegram и ВКонтакте, который использует [DialogFlow](https://dialogflow.cloud.google.com/) для обработки естественного языка.

В Telegram бот отвечает на вопросы пользователей, если знает ответ.

В ВКонтакте бот отвечает только если знает ответ - если не знает, он молчит (чтобы не мешать операторам).

## Структура файлов

- text_questions.json - база вопросов и ответов для обучения Dialogflow.

- create_intent.py - скрипт для загрузки intents (намерений) в Dialogflow.

- dialog_flow_bot.py - обёртка для работы с Dialogflow: функция распознавания намерения.

- tg_bot.py - Telegram-бот.

- vk_bot.py - ВКонтакте-бот.


## Описание
1. `text_questions.json`

Файл с вопросами и ответами для обучения Dialogflow. 

Пример:

```json
{
  "Устройство на работу": {
    "questions": [
      "Как устроиться к вам на работу?",
      "Как устроиться к вам?",
      ...
    ],
    "answer": "Если вы хотите устроиться к нам, напишите на почту ..."
  },
  ...
}
```
2. `create_intent.py`

- Скрипт для массовой загрузки intents в Dialogflow из файла text_questions.json.
- Читает вопросы и ответы из text_questions.json.
- Создаёт intents в Dialogflow через API.

3. `dialog_flow_bot.py`
- Отправляет текст пользователя в Dialogflow.
- Если бот не понял вопрос (is_fallback=True), возвращает None.
- Если есть ответ, возвращает текст ответа.

4. `tg_bot.py`
Telegram-бот:
- Читает переменные из .env.
- Принимает сообщения, отправляет их в Dialogflow.
- Если есть ответ - отправляет его пользователю.
- Если нет ответа - молчит (или можно добавить шаблонный ответ).
- Логирует ошибки и события в указанный чат.

5. `vk_bot.py`
ВКонтакте-бот:

- Читает переменные из .env.
- Слушает входящие сообщения через LongPoll.
- Отправляет сообщения в Dialogflow.
- Если есть ответ - отправляет его пользователю.
- Если нет ответа (is_fallback=True) - молчит (ничего не отправляет).


## Установка
1. Установите зависимости:

```text
pip install -r requirements.txt
```

requirements.txt cодержит:
- environs - для работы с переменными окружения
- google-cloud-dialogflow - для интеграции с Dialogflow
- python-telegram-bot - для Telegram-бота
- vk-api - для VK-бота

2. Создайте файл .env с такими переменными:

```text
TG_TOKEN=<токен Telegram-бота>
TG_CHAT_ID=<ваш Telegram chat id для логов>
VK_GROUP_TOKEN=<токен группы VK>
GOOGLE_APPLICATION_CREDENTIALS=<путь до JSON-файла сервисного аккаунта Dialogflow>
```
3. Запустите скрипт create_intent.py он создаст новый Intents в DialogFlow с вопросами на ответы из списка text_questions.json

```python
python create_intent.py
```

4. Запуск Телеграмм и Вконтакте ботов.
```python
python tg_bot.py

python vk_bot.py
```

## Как обучить Dialogflow новым вопросам
Добавьте новые вопросы и ответы в text_questions.json по образцу.

Запустите python create_intent.py - intents будут загружены в Dialogflow.

## Пример работы
Пользователь пишет вопрос в Telegram или VK.

Бот отправляет вопрос в Dialogflow.

Если есть подходящий intent - бот отвечает.

Если нет - в Telegram можно отправить шаблонный ответ, в VK бот молчит.

`Telegramm bot` 

![bot](https://private-user-images.githubusercontent.com/147311692/444301737-dc86fea3-2b5f-4431-93a6-c13fdb0facc6.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDczNDUyNDYsIm5iZiI6MTc0NzM0NDk0NiwicGF0aCI6Ii8xNDczMTE2OTIvNDQ0MzAxNzM3LWRjODZmZWEzLTJiNWYtNDQzMS05M2E2LWMxM2ZkYjBmYWNjNi5naWY_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNTE1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDUxNVQyMTM1NDZaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0yYjFhYjk4ZTQ5ZWUxNzlmYmExZTU4MjVmN2JhNWMwNmJiZWQxNDYwZjNmZTIzZTRkMTgxOWNhYmI0MjJiMDE3JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.YQkCFStlX0HZPvcvCYCNq3Ipi1rvL4ghuUwLXEw4W_w)

`VK bot:`

![vk](https://private-user-images.githubusercontent.com/147311692/444304262-3937f101-4c23-4324-9050-c039e8a8728c.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDczNDU4MzgsIm5iZiI6MTc0NzM0NTUzOCwicGF0aCI6Ii8xNDczMTE2OTIvNDQ0MzA0MjYyLTM5MzdmMTAxLTRjMjMtNDMyNC05MDUwLWMwMzllOGE4NzI4Yy5naWY_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNTE1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDUxNVQyMTQ1MzhaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0zY2U0NzhiZjQwYzI3NTlmZjQ5ZDA2YjM4YWNhMjJjZmY3YTllZWQyNTJmZDAwYWNlZDIyNDI1NTIzMmEzOTg1JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.Zsc0cAf3VQg0vZx02VV2yCoGGQoohsGUkFgj80w5avY) 