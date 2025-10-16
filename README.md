# 🌍 GeoGame - Географическая игра на Django

Увлекательная географическая игра с интерактивными картами, созданная на Django. Проверьте свои знания о достопримечательностях мира и соревнуйтесь с друзьями!

## 🎮 Демо версия

**Статическая версия (работает на GitHub Pages):** [Играть онлайн](https://yourusername.github.io/practicegis-master/static_game.html)

**Полная Django версия:** Требует развертывания на сервере (см. инструкции ниже)

## ✨ Возможности

- 🗺️ **Интерактивные карты** с использованием библиотеки Folium
- 🎯 **Умная система очков** на основе формулы Haversine
- 👤 **Система профилей** с отслеживанием статистики
- 🎮 **Режимы игры**: одиночная игра и многопользовательские баттлы
- 💡 **Визуальные подсказки** с изображениями достопримечательностей
- 📱 **Адаптивный дизайн** для всех устройств

## 🚀 Быстрый старт

### Статическая версия (для GitHub Pages)

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/yourusername/practicegis-master.git
   cd practicegis-master
   ```

2. **Откройте `static_game.html` в браузере** - игра готова!

### Полная Django версия

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/yourusername/practicegis-master.git
   cd practicegis-master
   ```

2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте базу данных:**
   ```bash
   cd gis
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Запустите сервер:**
   ```bash
   python manage.py runserver
   ```

6. **Откройте браузер:** http://127.0.0.1:8000

## 🌐 Развертывание на GitHub Pages

### Автоматическое развертывание

1. **Активируйте GitHub Pages:**
   - Перейдите в Settings → Pages
   - Выберите источник: "GitHub Actions"

2. **Настройте репозиторий:**
   - Файлы уже настроены для автоматического развертывания
   - При каждом push в main/master ветку будет создаваться новая версия

3. **Доступ к сайту:**
   - URL: `https://yourusername.github.io/practicegis-master/`

### Ручное развертывание

Если автоматическое развертывание не работает:

```bash
# Установите GitHub Pages Deploy Action
npm install -g gh-pages

# Разверните статическую версию
gh-pages -d . -b gh-pages
```

## ☁️ Развертывание на других платформах

### Heroku

1. **Создайте `Procfile`:**
   ```
   web: gunicorn gis.wsgi --log-file -
   ```

2. **Настройте переменные окружения:**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com
   ```

3. **Разверните:**
   ```bash
   git push heroku main
   ```

### Railway

1. **Подключите GitHub репозиторий**
2. **Настройте переменные окружения:**
   - `SECRET_KEY`: ваш секретный ключ Django
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: ваш домен Railway

3. **Разверните автоматически**

### Render

1. **Создайте новый Web Service**
2. **Подключите GitHub репозиторий**
3. **Настройте:**
   - Build Command: `pip install -r requirements.txt && cd gis && python manage.py collectstatic --noinput`
   - Start Command: `cd gis && gunicorn gis.wsgi`

## 📁 Структура проекта

```
practicegis-master/
├── gis/                    # Django приложение
│   ├── game/              # Основное приложение игры
│   │   ├── models.py      # Модели данных
│   │   ├── views.py       # Представления
│   │   ├── templates/     # HTML шаблоны
│   │   └── static/        # Статические файлы
│   ├── media/             # Загруженные изображения
│   └── manage.py          # Django управление
├── static_game.html       # Статическая версия игры
├── requirements.txt       # Python зависимости
├── .github/workflows/     # GitHub Actions
└── README.md             # Этот файл
```

## 🛠️ Технологии

- **Backend:** Django 4.2, Python 3.11+
- **Frontend:** HTML5, CSS3, JavaScript, Leaflet.js
- **Карты:** Folium, OpenStreetMap
- **База данных:** SQLite (разработка), PostgreSQL (продакшн)
- **Развертывание:** GitHub Pages, Heroku, Railway, Render

## 🎯 Как играть

1. **Посмотрите на изображение** достопримечательности
2. **Нажмите на карту** в том месте, где, по вашему мнению, находится объект
3. **Получите очки** в зависимости от точности вашего ответа:
   - 1000 очков: менее 1 км
   - 900-999 очков: 1-5 км
   - 800-899 очков: 5-15 км
   - И так далее...

## 📊 Система очков

Игра использует формулу Haversine для точного расчета расстояния между вашим ответом и правильным местоположением. Чем ближе ваш ответ к реальному месту, тем больше очков вы получите!

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 👨‍💻 Автор

Создано с ❤️ для изучения географии и веб-разработки.

## 🔗 Полезные ссылки

- [Django Documentation](https://docs.djangoproject.com/)
- [Folium Documentation](https://python-visualization.github.io/folium/)
- [Leaflet.js Documentation](https://leafletjs.com/)
- [GitHub Pages Documentation](https://pages.github.com/)

---

**Наслаждайтесь игрой! 🌍🎮**
