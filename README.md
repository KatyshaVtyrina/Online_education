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
3. Склонировать проект
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
DB_USER=имя пользователя (postgres)
DB_PASSWORD=пароль
DB_NAME=название базы данных (education)
SECRET_KEY=секретный ключ 
STRIPE_SECRET_KEY=ключ для аутентификации в сервисе stripe
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
3.Добавить уроки
```bash
python3 manage.py loaddata lessons.json
```

### Шаг 8: Запуск сервера Django
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

## Просмотр документации
### Swagger
```bash
http://127.0.0.1:8000/swagger/
```
### Redoc
```bash
http://127.0.0.1:8000/redoc/
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