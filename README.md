# Engineer Platform

Платформа для публикации записей пользователей с бесплатным и платным доступом. Регистрация по номеру телефона с OTP через Firebase. Подписки на авторов через Stripe. Фронтенд на Bootstrap. Полностью контейнеризировано с Docker и Docker Compose.

## Основные возможности

- Регистрация и вход по номеру телефона (OTP через Firebase Authentication)
- Публикация бесплатных и платных постов (текст + изображения до 10 МБ + YouTube embed)
- Подписка на авторов (1/3/6/9/12 месяцев, автопродление, цены настраиваются платформой)
- Доступ к платным постам только для активных подписчиков автора
- Жалобы на посты + модерация (роль модератора)
- Уведомления внутри сайта (о новых платных постах от подписанных авторов)
- Выбор тем оформления (light/dark + премиум для подписчиков)
- Поиск и фильтры постов (по заголовку, тегам, бесплатные/платные)
- Полный Docker + Nginx для production-like окружения
- Тесты с покрытием >85%

## Технологический стек

- Backend: Django 6.0.1 + PostgreSQL
- Frontend: Bootstrap 5 + Django templates
- Аутентификация: Firebase Phone Auth (OTP)
- Платежи: Stripe (recurring subscriptions)
- Токены: JWT (djangorestframework-simplejwt)
- Тестирование: pytest + coverage (≥85%)
- Контейнеризация: Docker + Docker Compose + Nginx
- Качество кода: black, isort, flake8, mypy, pre-commit

## Структура проекта
```bash
Engineer_platform/
├── core/                     # контекст-процессоры, утилиты
├── engineer_platform/        # настройки проекта
├── users/                    # пользователи, аутентификация
├── posts/                    # посты, теги, жалобы
├── payments/                 # подписки, Stripe
├── notifications/            # уведомления
├── themes/                   # темы оформления
├── templates/                # шаблоны
├── static/                   # статика (css, js)
├── media/                    # загруженные изображения
├── fixtures/                 # начальные данные
├── nginx.conf                # конфиг Nginx
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── pytest.ini / pyproject.toml
└── README.md
```


## Установка и запуск локально

1. **Клонируй репозиторий**

   ```bash
   git clone https://github.com/Couguar-lab/Engineer_platform
   cd Engineer_platform
   ```
   
2. **Создай виртуальное окружение**

   ```bash
    python -m venv venv
    .\venv\Scripts\activate
   ```
   
3. **Установи зависимости**

   ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
   ```
   
4. **Настрой .env**

    Скопируй .env.example в .env и заполни все переменные (Stripe keys, Firebase config, DB creds).

5.  **Сделай миграции и собери статику**

   ```bash
    python manage.py migrate
    python manage.py collectstatic --noinput
   ```
   
6.  **Загрузи начальные данные (фикстуры)**

   ```bash
    python manage.py loaddata fixtures/initial_data.json
   ```
   
7.  **Запусти сервер**

   ```bash
    python manage.py runserver
   ```
   Сайт: http://localhost:8000

## Запуск в Docker (рекомендуемый способ)

1. **Убедись, что Docker Desktop запущен**
2. **Собери и запусти**

   ```bash
    docker-compose up -d --build
    ```
3. **Проверь статус**

   ```bash
    docker-compose ps
   ```
   Должны быть Up: db, web, nginx

4. Сайт доступен по

    http://localhost (порт 80 через Nginx)

**добавлен деплой на виртуальную машину яндекс**