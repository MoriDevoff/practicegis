# ⚡ Быстрый старт - Развертывание GeoGame

## 🎯 Выберите ваш вариант развертывания

### 🌐 Вариант 1: GitHub Pages (Рекомендуется для демо)
**Статическая версия игры - работает сразу без сервера**

1. **Загрузите файлы на GitHub:**
   ```bash
   git add .
   git commit -m "Add deployment files"
   git push origin main
   ```

2. **Активируйте GitHub Pages:**
   - Repository → Settings → Pages
   - Source: "GitHub Actions"
   - Сохраните

3. **Готово!** Ваш сайт будет доступен по адресу:
   ```
   https://yourusername.github.io/practicegis-master/
   ```

### 🚂 Вариант 2: Railway (Рекомендуется для полной версии)
**Полная Django версия с базой данных**

1. **Перейдите на Railway:** https://railway.app/
2. **Нажмите "Deploy from GitHub repo"**
3. **Выберите ваш репозиторий**
4. **Настройте переменные:**
   ```
   SECRET_KEY: your-secret-key-here
   DEBUG: False
   ALLOWED_HOSTS: your-app.railway.app
   ```
5. **Готово!** Railway автоматически развернет ваше приложение

### 🟣 Вариант 3: Heroku
**Классический выбор для Django приложений**

```bash
# Установите Heroku CLI
heroku login
heroku create your-geogame-app
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
git push heroku main
heroku run python manage.py migrate
```

---

## 🎮 Что вы получите

### Статическая версия (GitHub Pages)
- ✅ Работает сразу без настройки
- ✅ Интерактивная карта с Leaflet.js
- ✅ 10 встроенных достопримечательностей
- ✅ Система подсчета очков
- ✅ Адаптивный дизайн

### Полная Django версия (Railway/Heroku)
- ✅ Все функции статической версии
- ✅ Система регистрации и авторизации
- ✅ Сохранение результатов игр
- ✅ Профили игроков со статистикой
- ✅ Админ-панель для управления данными
- ✅ Загрузка собственных изображений

---

## 📁 Важные файлы

- `static_game.html` - Статическая версия игры
- `requirements.txt` - Зависимости Python
- `Procfile` - Конфигурация для Heroku
- `.github/workflows/deploy.yml` - Автоматическое развертывание
- `README.md` - Подробная документация
- `DEPLOYMENT.md` - Полное руководство по развертыванию

---

## 🆘 Нужна помощь?

1. **Прочитайте** `DEPLOYMENT.md` для подробных инструкций
2. **Создайте issue** с тегом `[DEPLOYMENT]` в GitHub
3. **Проверьте** логи развертывания в настройках платформы

---

**Выберите подходящий вариант и начните играть! 🎮🌍**
