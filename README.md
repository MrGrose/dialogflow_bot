# Мультиплатформенный чат-бот на базе Dialogflow

## Описание
Этот проект - мультибот для Telegram и ВКонтакте, который использует [DialogFlow](https://dialogflow.cloud.google.com/) для обработки естественного языка.

В Telegram бот отвечает на вопросы пользователей, если знает ответ.

В ВКонтакте бот отвечает только если знает ответ - если не знает, он молчит (чтобы не мешать операторам).

## Подготовка Google Cloud и Dialogflow
1. Зарегистрируйтесь в Google Cloud
    - Создайте учётную запись на платформе Google Cloud, если у вас её ещё нет.

2. Создайте новый проект
    - В консоли [Google Cloud](https://console.cloud.google.com/projectcreate?previousPage=%2Fwelcome%3Fproject%3Dregal-fortress-361907&organizationId=0) создайте новый проект.
    - Сохраните его идентификатор (Project ID) - он понадобится для интеграции с Dialogflow.

3. Создайте агента в Dialogflow
    - Перейдите в сервис [Dialogflow](https://dialogflow.cloud.google.com/#/newAgent). В левом верхнем углу выберите регион размещения агента - выбирайте только Global.
    - Затем нажмите кнопку для создания нового агента.

4. Привяжите проект Google Cloud к агенту Dialogflow
    - Введите название для вашего агента.
    - После этого нажмите на кнопку выбора проекта Google и укажите тот Project ID, который вы создали ранее.
    - Завершите создание агента.

5. Создайте сервисный аккаунт и получите ключ
    - Откройте раздел [Service accounts](https://console.cloud.google.com/iam-admin/serviceaccounts?project=regal-fortress-361907&inv=1&invt=AbxfhA) в Google Cloud.
    - Нажмите Create service account, задайте имя и продолжайте.
    - На этапе выбора роли выберите Owner в разделе Currently used, затем завершите создание.

6. Скачайте JSON-ключ
    - После создания сервисного аккаунта выберите его, кликните по трём точкам справа и выберите Manage Keys.
    - Далее нажмите Add Keys → Create new key, выберите формат JSON и скачайте файл.
    - Сохраните этот файл в папку вашего проекта.

7. Настройте переменные окружения
  - Откройте файл .env в корне вашего проекта.
  - В строке GOOGLE_APPLICATION_CREDENTIALS укажите имя скачанного JSON-файла, например:

    ```text
    GOOGLE_APPLICATION_CREDENTIALS=firm-champion-459914-h1-f4f4ac94d573.json
    ```

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
3. Запуск скрипта create_intent.py для создания Intents в DialogFlow. Данный скрипт автоматически создаёт новый Intent в DialogFlow, используя вопросы из файла text_questions.json (или другого файла с вопросами, если указать свой).

Как использовать
```bash
python create_intent.py -c путь/к/вашему/google.json
```
 - `-c или --credentials` - обязательный параметр, указывающий путь к вашему файлу с учетными данными Google (например, google.json).

Если вы хотите использовать другой файл с вопросами, укажите его через параметр -q:

```bash
python create_intent.py -c путь/к/вашему/google.json -q путь/к/вашим_вопросам.json
```
- `-q или --questions`- необязательный параметр, по умолчанию используется text_questions.json. Здесь указывается путь к JSON-файлу с вопросами.

Аргументы командной строки
- `-c, --credentials` - путь к JSON-файлу с учетными данными Google (обязательно).

- `-q, --questions` - путь к JSON-файлу с вопросами (по умолчанию text_questions.json).

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