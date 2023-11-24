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
```
*В проекте есть шаблон файла .env - `.env_example`

### Шаг 6: Применение миграций
1. Выполнить команду
```bash
python manage.py migrate
```

### Шаг 7: Заполение базы данных
1. Добавить курсы
```bash
python3 manage.py loaddata courses.json
```
2. Добавить уроки
```bash
python3 manage.py loaddata lessons.json
```
3. Создать суперпользователя
```bash
python3 manage.py сsu
```
4. Создать пользователей
```bash
python3 manage.py loaddata users.json
```
5. Добавить платежи
```bash
python3 manage.py loaddata payments.json
```

### Шаг 8: Запуск сервера Django
1. Открыть новое окно терминала

2. Запустить сервер
```bash
python manage.py runserver
```