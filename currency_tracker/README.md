REST API для отслеживания курсов валют. Позволяет:
- Управлять пользователями (CRUD)
- Подписывать пользователей на валюты
- Получать актуальные курсы из API Центробанка РФ

## 🚀 Запуск проекта

### 1. Клонировать репозиторий
```bash
git clone <ссылка на ваш репозиторий>
cd currency_tracker
2. Создать виртуальное окружение
bash
python -m venv venv
3. Активировать окружение
Windows:

bash
venv\Scripts\activate
Mac/Linux:

bash
source venv/bin/activate
4. Установить зависимости
bash
pip install -r requirements.txt
5. Запустить сервер
bash
uvicorn app.main:app --reload
Сервер будет доступен по адресу: http://127.0.0.1:8000

📖 Документация API
Интерактивная документация доступна после запуска по адресу:
http://127.0.0.1:8000/docs

Основные эндпоинты
Метод	Эндпоинт	Описание
POST	/users/	Создать пользователя
GET	/users/	Получить список всех пользователей
GET	/users/{user_id}	Получить пользователя с его подписками
PUT	/users/{user_id}	Обновить email пользователя
DELETE	/users/{user_id}	Удалить пользователя
POST	/subscriptions/	Подписать пользователя на валюту
DELETE	/subscriptions/	Отписать пользователя от валюты
POST	/currencies/update	Обновить список валют из ЦБ РФ
GET	/currencies/	Список всех валют
GET	/currencies/{code}/rate	Получить текущий курс валюты
Пример запроса (через curl)
Создать пользователя:

bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "ivan", "email": "ivan@example.com"}'
Подписаться на USD:

bash
curl -X POST "http://localhost:8000/subscriptions/" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "currency_code": "USD"}'
Узнать курс USD:

bash
curl "http://localhost:8000/currencies/USD/rate"
🛠 Используемые технологии
FastAPI

SQLAlchemy (async)

SQLite (aiosqlite)

uvicorn

httpx

Pydantic

xml.etree.ElementTree (парсинг XML ЦБ РФ)

📌 Примечания
При первом запуске база данных (currency_tracker.db) создаётся автоматически.

Перед подпиской на валюту необходимо выполнить POST /currencies/update, чтобы загрузить список валют из ЦБ РФ.

👨‍💻 Автор
Кожевников Александр Николаевич Ивт 3 курс