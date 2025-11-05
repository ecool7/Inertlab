# Inertlab Site (Flask)

Современный сайт производителя инерциальных модулей IMU на Flask + Tailwind (CDN).

## Запуск локально

1. Создайте виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Запустите приложение:

```bash
python app.py
```

Откройте `http://127.0.0.1:8000`.

## Структура
- `app.py` — входная точка Flask и роуты
- `templates/` — Jinja-шаблоны (`base.html`, `index.html`, `products.html`, `about.html`, `contact.html`)
- `static/` — статические файлы (CSS/JS/логотип)

## Деплой (gunicorn)

```bash
gunicorn -w 2 -b 0.0.0.0:8000 app:app
```

## Примечания
- Tailwind, AOS подключены через CDN для быстрого старта.
- Для офлайн-сборки дизайна можно внедрить локальную сборку Tailwind позднее.
