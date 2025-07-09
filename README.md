## Инструкция по запуску:
1. Клонируйте репозиторий\
  `git clone https://github.com/wanychto/django_training.git` \
  `cd /django_training`

2. Настройте переменные окружения
Для этого, используя шаблон .env-example, создайте новый файл .env и вставьте свои значения в переменные.

3. Запустите через docker-compose.\
  `docker-compose up --build`

4. Откройте http://localhost:8000

## Переменные окружения:
DJANGO_SECRET_KEY- это криптографический ключ, который используется для различных операций безопасности в приложении. Получить его можно с помощью:\
  `from django.core.management.utils import get_random_secret_key`\
  `get_random_secret_key()`\
DEBUG - режим отладки джанго, по умолчанию стоит False, менять его не нужно.\
DJANGO_LOGLEVEL - уровень логирования сообщений. По умолчанию стоит INFO, оно будет показывать общую информацию о поведении приложения.\
DJANGO_ALLOWED_HOSTS- список разрешённых доменов для работы с джанго.\
DATABASE_USERNAME - имя пользователя для подключения к базе данных.\
DATABASE_PASSWORD - пароль для подключения к базе данных.\
DATABASE_NAME - название базы данных.
