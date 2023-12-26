# Online Education

## Описание

SPA-приложение, результатом создания которого будет бэкенд-сервер, возвращающий клиенту JSON-структуры.

## Данные

**Cущности проекта:**

- Пользователи
- Курсы
- Уроки
- Платежи



## Подготовка к работе с проектом

### Шаг 1: Клонирование проекта
1. Зайти в терминал
2. С помощью команды `cd` перейти в директорию, где будет находиться проект
3. Клонировать проект
```bash
git clone https://github.com/KatyshaVtyrina/Online_education.git
```

### Шаг 2: Настройка виртуального окружения

1. Создать виртуальное окружение
```bash
python3 -m venv venv
```
2. Активировать виртуальное окружение
```bash
source venv/bin/activate
```

### Шаг 3: Установка зависимостей
1. Перейти в каталог проекта
```bash
cd Online_education
```
2. Установить зависимости проекта из файла`requirements.txt`
```bash
pip install -r requirements.txt
```

### Шаг 4: Установка и настройка PostgreSQL
1. Установить PostreSQL
```bash
brew install postgres
```
2. Подключиться к PostgreSQL от имени пользователя postgres
```bash
psql -U postgres 
```
3. Создать базу данных `education`
```bash
CREATE DATABASE education;
```
4. Выйти
```bash
\q
```

### Шаг 5: Настройка окружения
1. В директории проекта создать файл `.env`

3. Записать в файл следующие настройки
```bash
POSTGRES_DB=название базы данных (education)
POSTGRES_USER=имя пользователя(postgres)
POSTGRES_PASSWORD=пароль
POSTGRES_HOST=хост (localhost) 
POSTGRES_PORT=5432
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"

# через Docker
POSTGRES_HOST = db
CELERY_BROKER_URL="redis://redis:6379/0"
CELERY_RESULT_BACKEND="redis://redis:6379/0"

SECRET_KEY=секретный ключ 
STRIPE_SECRET_KEY=ключ для аутентификации в сервисе stripe
EMAIL_HOST_USER=адрес электронной почты для аутенфикации на почтовом сервере
EMAIL_HOST_PASSWORD=пароль для аутенфикации на почтовом сервере
```
*В проекте есть шаблон файла .env - `.env_example`

### Шаг 6: Применение миграций
1. Выполнить команду
```bash
python manage.py migrate
```

### Шаг 7: Заполнение базы данных
1. Создать пользователей и суперпользователя
```bash
python3 manage.py create_users
```
2. Добавить курсы
```bash
python3 manage.py loaddata courses.json
```
3. Добавить уроки
```bash
python3 manage.py loaddata lessons.json
```
### Шаг 8: Установка и настройка Redis
1. Установить
```bash
brew install redis
```
2. Запустить в отдельном окне терминала 
```bash
redis-server
```
### Шаг 9: Запуск celery
1. Открыть новое окно терминала
2. Из каталога проекта запустить celery командой
```bash
celery -A config worker -l info
```
### Шаг 10: Запуск celery-beat
1. Открыть новое окно терминала
2. Из каталога проекта запустить celery-beat командой
```bash
celery -A config beat -l info 
```
### Шаг 11: Запуск сервера Django
1. Открыть новое окно терминала

2. Запустить сервер
```bash
python manage.py runserver
```

## Запуск тестов

### Для запуска тестов выполнить команду
```bash
 coverage3 run --source='.' manage.py test
```
### Результат покрытия тестами
```bash
 coverage_result.png
```

## Работа с проектом с помощью Docker

1. Выполнить Шаги 1 и 5 Подготовки к проекту
2. Чтобы создать образ, выполнить команду в терминале
```bash
docker-compose build  
```
3. Запуск проекта
```bash
docker-compose up
```
4. Заполнение базы данных
```bash
docker-compose exec app python3 manage.py create_users
docker-compose exec app python3 manage.py loaddata courses.json
docker-compose exec app python3 manage.py loaddata lessons.json
```
5. Запуск тестов 
```bash
docker-compose exec app coverage3 run --source='.' manage.py test
```

## Работа с сервисом stripe через Postman
1. Получить токен
```bash
POST: http://localhost:8000/users/token/
```
2. Подключить авторизацию по токену
3. Создать платеж
```bash
POST: http://localhost:8000/payment/create/
body: {"course": <id курса>} 
```
4. Посмотреть детальную информацию по платежу
```bash
GET: http://localhost:8000/payment/<pk>/
```
5. Перейдя по ссылке для оплаты, совершить тестовый платеж
```bash
Тестовые данные: https://stripe.com/docs/terminal/references/testing#standard-test-cards
```

## Просмотр документации
### Swagger
```bash
http://127.0.0.1:8000/swagger/
```
### Redoc
```bash
http://127.0.0.1:8000/redoc/
```

## Просмотр документации c помощью Docker
### Swagger
```bash
http://localhost:8000/swagger/
```
### Redoc
```bash
http://localhost:8000/redoc/
```