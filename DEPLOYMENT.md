# 🚀 Руководство по развертыванию GeoGame

Это руководство поможет вам развернуть вашу географическую игру на различных платформах.

## 📋 Содержание

1. [GitHub Pages (Статическая версия)](#github-pages-статическая-версия)
2. [Heroku (Полная Django версия)](#heroku-полная-django-версия)
3. [Railway (Полная Django версия)](#railway-полная-django-версия)
4. [Render (Полная Django версия)](#render-полная-django-версия)
5. [Vercel (Статическая версия)](#vercel-статическая-версия)
6. [Netlify (Статическая версия)](#netlify-статическая-версия)

---

## 🌐 GitHub Pages (Статическая версия)

### Преимущества
- ✅ Бесплатно
- ✅ Простое развертывание
- ✅ Автоматические обновления
- ✅ Поддержка HTTPS

### Недостатки
- ❌ Только статические файлы
- ❌ Нет серверной логики

### Пошаговая инструкция

1. **Активируйте GitHub Pages:**
   ```
   Repository → Settings → Pages
   Source: GitHub Actions
   ```

2. **Настройте автоматическое развертывание:**
   - Файл `.github/workflows/deploy.yml` уже настроен
   - При каждом push в main ветку будет автоматически развертываться новая версия

3. **Доступ к сайту:**
   ```
   https://yourusername.github.io/practicegis-master/
   ```

4. **Ручное развертывание (если нужно):**
   ```bash
   npm install -g gh-pages
   gh-pages -d . -b gh-pages
   ```

---

## 🟣 Heroku (Полная Django версия)

### Преимущества
- ✅ Поддержка Django
- ✅ Автоматическое развертывание
- ✅ Простая настройка базы данных
- ✅ Масштабируемость

### Недостатки
- ❌ Ограниченное бесплатное время
- ❌ Может "засыпать" при неактивности

### Пошаговая инструкция

1. **Установите Heroku CLI:**
   ```bash
   # Windows
   winget install Heroku.HerokuCLI
   
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Войдите в Heroku:**
   ```bash
   heroku login
   ```

3. **Создайте приложение:**
   ```bash
   heroku create your-geogame-app
   ```

4. **Настройте переменные окружения:**
   ```bash
   heroku config:set SECRET_KEY="your-super-secret-key-here"
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS="your-geogame-app.herokuapp.com"
   ```

5. **Настройте базу данных PostgreSQL:**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

6. **Разверните приложение:**
   ```bash
   git push heroku main
   ```

7. **Выполните миграции:**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

8. **Откройте приложение:**
   ```bash
   heroku open
   ```

---

## 🚂 Railway (Полная Django версия)

### Преимущества
- ✅ Простое развертывание
- ✅ Автоматическая настройка базы данных
- ✅ Хорошая документация

### Пошаговая инструкция

1. **Перейдите на Railway:**
   ```
   https://railway.app/
   ```

2. **Подключите GitHub:**
   - Нажмите "Deploy from GitHub repo"
   - Выберите ваш репозиторий

3. **Настройте переменные окружения:**
   ```
   SECRET_KEY: your-super-secret-key-here
   DEBUG: False
   ALLOWED_HOSTS: your-app.railway.app
   ```

4. **Railway автоматически:**
   - Установит зависимости
   - Настроит базу данных PostgreSQL
   - Развернет приложение

5. **Выполните миграции:**
   ```bash
   railway run python manage.py migrate
   railway run python manage.py createsuperuser
   ```

---

## 🎨 Render (Полная Django версия)

### Преимущества
- ✅ Бесплатный план
- ✅ Автоматическое развертывание
- ✅ Встроенная база данных

### Пошаговая инструкция

1. **Перейдите на Render:**
   ```
   https://render.com/
   ```

2. **Создайте новый Web Service:**
   - Connect GitHub repository
   - Выберите ваш репозиторий

3. **Настройте параметры:**
   ```
   Name: geogame
   Environment: Python 3
   Build Command: pip install -r requirements.txt && cd gis && python manage.py collectstatic --noinput
   Start Command: cd gis && gunicorn gis.wsgi
   ```

4. **Настройте переменные окружения:**
   ```
   SECRET_KEY: your-super-secret-key-here
   DEBUG: False
   ALLOWED_HOSTS: your-app.onrender.com
   ```

5. **Создайте базу данных PostgreSQL:**
   - New → PostgreSQL
   - Подключите к вашему Web Service

6. **Разверните приложение**

---

## ▲ Vercel (Статическая версия)

### Преимущества
- ✅ Очень быстрое развертывание
- ✅ Отличная производительность
- ✅ Автоматические обновления

### Пошаговая инструкция

1. **Установите Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Войдите в Vercel:**
   ```bash
   vercel login
   ```

3. **Разверните проект:**
   ```bash
   vercel
   ```

4. **Настройте в веб-интерфейсе:**
   - Connect GitHub repository
   - Настройте автоматическое развертывание

---

## 🟢 Netlify (Статическая версия)

### Преимущества
- ✅ Простое развертывание
- ✅ Формы и функции
- ✅ CDN по всему миру

### Пошаговая инструкция

1. **Перейдите на Netlify:**
   ```
   https://netlify.com/
   ```

2. **Подключите GitHub:**
   - New site from Git
   - Connect to GitHub
   - Выберите ваш репозиторий

3. **Настройте параметры:**
   ```
   Build command: (оставьте пустым)
   Publish directory: ./
   ```

4. **Настройте переменные окружения (если нужно):**
   ```
   Site settings → Environment variables
   ```

---

## 🔧 Общие настройки для продакшн

### Переменные окружения

Для всех платформ с Django необходимо настроить:

```bash
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:password@host:port/database
```

### Генерация секретного ключа

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Настройка домена

1. **Купите домен** (например, на Namecheap, GoDaddy)
2. **Настройте DNS записи:**
   ```
   A record: @ → IP адрес вашего хостинга
   CNAME: www → your-app.herokuapp.com
   ```

### SSL сертификат

Большинство платформ автоматически предоставляют SSL сертификаты:
- GitHub Pages: ✅
- Heroku: ✅
- Railway: ✅
- Render: ✅
- Vercel: ✅
- Netlify: ✅

---

## 📊 Сравнение платформ

| Платформа | Тип | Бесплатно | Простота | Производительность | Рекомендация |
|-----------|-----|-----------|----------|-------------------|--------------|
| GitHub Pages | Статический | ✅ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Для демо |
| Heroku | Django | ⚠️ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Для разработки |
| Railway | Django | ✅ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **Лучший выбор** |
| Render | Django | ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Альтернатива |
| Vercel | Статический | ✅ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Для статики |
| Netlify | Статический | ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Для статики |

---

## 🚨 Решение проблем

### Ошибка "No module named 'django'"
```bash
pip install -r requirements.txt
```

### Ошибка базы данных
```bash
python manage.py migrate
```

### Ошибка статических файлов
```bash
python manage.py collectstatic --noinput
```

### Ошибка "ALLOWED_HOSTS"
Добавьте ваш домен в `ALLOWED_HOSTS` в settings.py

### Ошибка "SECRET_KEY"
Установите переменную окружения `SECRET_KEY`

---

## 📞 Поддержка

Если у вас возникли проблемы:

1. **Проверьте логи:**
   ```bash
   heroku logs --tail
   railway logs
   ```

2. **Проверьте переменные окружения:**
   ```bash
   heroku config
   railway variables
   ```

3. **Обратитесь к документации платформы**

4. **Создайте issue в GitHub репозитории**

---

**Удачного развертывания! 🚀**
