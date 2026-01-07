# Лабораторная работа 5, Django REST Framework: (микро)сервисы
## Яблонская Евгения, ИВТ-1.2

## Описание
Проект расширяет стандартное Django‑приложение для голосований (`polls`) микросервисами аналитики на базе Django REST Framework (DRF). Реализована статистика, экспорт данных и визуализация результатов опросов.

## Функциональность

1. **Статистика по голосованиям**  
   - Общее число голосов.  
   - Количество голосов за каждый вариант.  
   - Процентное соотношение.  

2. **Экспорт данных**  
   - JSON (API‑ответ).  
   - CSV (скачивание файла).  

3. **Визуализация**  
   - Графики в формате PNG (base64 в JSON‑ответе).  

4. **Поиск и отображение**  
   - Фильтрация голосований по названию/дате.  
   - Динамическая загрузка статистики и графиков на фронтенде.  

## Структура

- `polls/` — основное приложение (голосования).  
- `poll_analytics/` — микросервисы аналитики (DRF).  
- `templates/polls/analytics.html` — страница поиска и отображения статистики.  

## Установка

1. Установите зависимости:  
   ```bash
   pip install django djangorestframework matplotlib
   ```

2. Настройте `settings.py`:  
   - Добавьте `'rest_framework'` и `'poll_analytics'` в `INSTALLED_APPS`.  
   - Укажите `BASE_DIR` и `TEMPLATES` (см. пример в документации).  

3. Выполните миграции:  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Запустите сервер:  
   ```bash
   python manage.py runserver
   ```

## API‑эндпоинты

- **`GET /api/analytics/stats/<id>/**` — статистика по голосованию.  
- **`GET /api/analytics/export/<id>/<format>/**` — экспорт (формат: `json` или `csv`).  
- **`GET /api/analytics/chart/<id>/**` — график в base64.  
- **`GET /polls/api/search/?q=<query>`** — поиск голосований.  

## Использование

1. Откройте страницу аналитики:  
   ```
   http://127.0.0.1:8000/polls/analytics/
   ```
2. Введите поисковый запрос (название или дату).  
3. Кликните на результат — загрузится статистика и график.  

## Требования

- Python 3.8+  
- Django 4.0+  
- Django REST Framework  
- Matplotlib (для графиков)  

## Результаты:

http://127.0.0.1:8000/api/analytics/stats/1/
<img width="1516" height="897" alt="image" src="https://github.com/user-attachments/assets/87f42922-5a4e-4777-add3-f9839009f26a" />

http://127.0.0.1:8000/api/analytics/export/1/csv/
<img width="1602" height="144" alt="image" src="https://github.com/user-attachments/assets/52d6be91-8a1f-436c-be2c-9527cf394a9b" />
<img width="1581" height="200" alt="image" src="https://github.com/user-attachments/assets/9fa70ced-bfba-4341-b32d-6056fe22e657" />

http://127.0.0.1:8000/api/analytics/chart/<id>/
<img width="1579" height="582" alt="image" src="https://github.com/user-attachments/assets/4ae74c42-f86c-4342-9fb9-1b04f06a43b5" />

http://127.0.0.1:8000/polls/api/search/?q=<query>
<img width="610" height="353" alt="image" src="https://github.com/user-attachments/assets/c2cafbc4-0800-49de-b36d-a554c0258779" />

