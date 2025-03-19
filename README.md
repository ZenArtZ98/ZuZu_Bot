# Telegram-бот для добавления сайтов в краулер

Этот проект представляет собой Telegram-бота, который позволяет пользователям загружать Excel-файлы с информацией о сайтах (название, URL, XPath), сохранять данные в SQLite базу данных и рассчитывать среднюю цену товаров по каждому сайту.

## Описание
Бот принимает Excel-файлы с тремя колонками:
- `title` — название сайта.
- `url` — ссылка на сайт.
- `xpath` — XPath-путь к элементу с ценой.

После загрузки файла бот:
1. Выводит содержимое файла.
2. Сохраняет данные в локальную базу SQLite (`sites.db`).
3. Парсит цены с указанных сайтов и рассчитывает среднюю цену для каждого сайта.

## Требования
- **Операционная система**: Windows, Linux или macOS.
- **Python**: версия 3.8 или выше.
- **Git**: для клонирования репозитория.
- **Telegram-аккаунт**: для создания и настройки бота.

## Установка

### 1. Установка Python
Если Python не установлен:
1. Скачайте установщик с [официального сайта](https://www.python.org/downloads/).
2. Установите Python, убедитесь, что опция "Add Python to PATH" включена.
3. Проверьте версию в терминале:
   ```bash
   python --version
   ```
   Ожидаемый вывод: Python 3.x.x.

### 2. Установка Git
Если Git не установлен:
1. Скачайте и установите Git с [официального сайта](https://git-scm.com/).
2. Проверьте установку:
   ```bash
   git --version
   ```

### 3. Клонирование репозитория
Склонируйте этот репозиторий на свой компьютер:
```bash
git clone https://github.com/ZenArtZ98/ZuZu_Bot.git
cd tg_bot
```
### 4. Создание виртуального окружения
Создайте виртуальное окружение для изоляции зависимостей:
```bash
python -m venv .venv
```
Активируйте его:
- На Windows:
  ```bash
  .venv\Scripts\activate
  ```
- На Linux/Mac:
  ```bash
  source .venv/bin/activate
  ```
После активации в начале строки терминала появится `(.venv)`.

### 5. Установка зависимостей
Установите необходимые библиотеки из файла `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Настройка бота

### 1. Получение api_id и api_hash
1. Перейдите на [my.telegram.org](https://my.telegram.org/).
2. Войдите, используя свой номер телефона Telegram.
3. Перейдите в раздел **API development tools**.
4. Заполните форму и нажмите **Create application**.
5. Сохраните `api_id` и `api_hash`.

### 2. Получение bot_token
1. Откройте Telegram и найдите бота `@BotFather`.
2. Отправьте команду `/start`, затем `/newbot`.
3. Следуйте инструкциям для создания бота.
4. После успешного создания @BotFather пришлет `bot_token`.

### 3. Заполнение данных в коде
Откройте файл `bot.py` и укажите свои значения:
```python
api_id = "YOUR_API_ID"
api_hash = "YOUR_API_HASH"
bot_token = "YOUR_BOT_TOKEN"
```
Сохраните файл.

## Запуск бота
1. Убедитесь, что вы находитесь в папке `tg_bot` и виртуальное окружение активировано.
2. Запустите бота:
   ```bash
   python bot.py
   ```
3. В терминале появится сообщение `Бот запущен!`.

## Использование
1. Откройте Telegram и найдите своего бота.
2. Отправьте команду `/start`.
3. Нажмите кнопку **Загрузить файл**.
4. Прикрепите Excel-файл с данными.

Пример содержимого файла:
1.xlsx

После загрузки файла бот:
- Выведет содержимое.
- Сохранит данные в `sites.db`.
- Спарсит цены и покажет среднюю цену.

