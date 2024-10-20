# Nikiforov Vyacheslav

Установка зависимостей производится через Poetry.
Надо установить Poetry.
```
pip install Poetry
# Далее для первичной установки
poetry install
```

Для работы и запуска необходимо заполнить переменные окружения в env файле
```
База данных:
DB_HOST - адресс БД
DB_PORT - Порт
DB_NAME - Имя БД
DB_USER - Пользователь БД
DB_PASS - Пароль БД
Данные для настройки почтового сервиса:
MAIL_USERNAME - Имя пользователя 
MAIL_PASSWORD - Пароль
HOST - Хост
FROM_ADR - Адресс с которого будет приходить почта
Данные для создания токена
SECRET_KEY - секретный ключ генерации токена
ACCESS_TOKEN_EXPIRE_MINUTES - Время жизни токена
ALGORITHM - алгоритм шифрования
Данные пользователя администратора сайта
ADMINPASS - Пароль
ADMINMAIL - Почта
```

Работа с базой данных настроена через Alembic.
Для поднятия сервисов баз для локальной разработки нужно запустить команду:

```
make up
```

Для накатывания миграций, если файла alembic.ini ещё нет, нужно запустить в терминале команду:

```
alembic init migrations
```

После этого будет создана папка с миграциями и конфигурационный файл для алембика.

- В alembic.ini нужно задать адрес базы данных, в которую будем катать миграции.
- Дальше идём в папку с миграциями и открываем env.py, там вносим изменения.

- Дальше вводим: ```alembic revision --autogenerate -m "comment"``` - делается при любых изменениях моделей
- Будет создана миграция
- Дальше вводим: ```alembic upgrade heads```

После создание таблиц в БД необходимо импортировать тестовые данные для таблицы Product и создать пользователя admin.

```
data_import.py
```

Приложение готово к работе.
Вся документация и Swagger доступен по адресу:
```
http://127.0.0.1:8000/docs
```
Регистрация новых клиентов доступна свободно.
Далее необходимо авторизоваться на сервисе и получить токен для выполнения заказа.
Удаление или изменение доступно только для Администратора, созданного вначале.