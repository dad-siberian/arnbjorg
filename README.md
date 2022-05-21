# arnbjorg

Бот-помощник службы поддержки. Отвечает на часто задаваемые вопросы в Telegram и в группе ВКонтакте.

|Пример Telegram бота:|Пример Vk бота:|
|--|--|
|![Telegram bot](https://dvmn.org/filer/canonical/1569214094/323/)|![VK bot](https://dvmn.org/filer/canonical/1569214089/322/)|


## Установка

1. Скачать код

```
git clone https://github.com/dad-siberian/arnbjorg.git

```

2. Создать виртуальное окружение:

```
python3 -m venv venv
source venv/bin/activate
```

3. Установить зависимости командой

```
pip install -r requirements.txt
```

## Настройка

Настройки берутся из переменных окружения. Чтобы их определить, создайте файл `.env` в корне проекта и запишите туда данные в формате: `ПЕРЕМЕННАЯ=значение`.

- `TELEGRAM_TOKEN` - токен, полученный у телеграм бота [@BotFather](https://telegram.me/BotFather) ([инструкция](https://botcreators.ru/blog/kak-sozdat-svoego-bota-v-botfather/)).
- `TG_CHAT_ID` - Telegram id администратора ботов для получения системных оповещений. Можно узнать, написав в Telegram специальному боту: [@userinfobot](https://t.me/userinfobot)
- `VK_TOKEN` - токен группы ВК. Для его получения пройдите в управление своей группы. В разделе "Работа с API" нажмите на кнопку "Создать ключ". Отметьте галочками первые два пункта (Разрешить приложению доступ к управлению сообществом и Разрешить приложению доступ к сообщениям сообществом) и создайте ключ кнопкой "Создать" (необходимо смс подтверждение)
- `GOOGLE_APPLICATION_CREDENTIALS` - имя файла с ключом Google Cloud Platform.
  Например:

```
GOOGLE_APPLICATION_CREDENTIALS=august-terminus-350016-311dfea51f94.json
```

Для его получения необходимо:

1. [создать](https://cloud.google.com/dialogflow/es/docs/quick/build-agent) Агента в DialogFlow.
2. [создать](https://cloud.google.com/dialogflow/es/docs/quick/setup) service-account с доступом к DialogFlow. Файл с ключом необходимо поместить в корень проекта.

## Обучение бота тренировочными фразами

1. Внести в файл `questions.json` тренировочные фразы с ответами в формате:

```
{
    "Забыл пароль": {
        "questions": [
            "Не помню пароль",
            "Не могу войти",
            "Проблемы со входом",
            "Забыл пароль",
            "Забыл логин",
            "Восстановить пароль",
            "Как восстановить пароль",
            "Неправильный логин или пароль",
            "Ошибка входа",
            "Не могу войти в аккаунт"
        ],
        "answer": "Если вы не можете войти на сайт, воспользуйтесь кнопкой «Забыли пароль?» под формой входа. Вам на почту прийдёт письмо с дальнейшими инструкциями. Проверьте папку «Спам», иногда письма попадают в неё."
    },
    ...
}
```

Ещё пример тренировочных фраз - [questions](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json)

2. Запустить скрипт командой:

```
pytnon DialogFlow.py
```

## Запуск ботов

1. Запуск Телеграм бота:

```
pytnon arnbjorg_telegram_bot.py
```

2. Запуск VK бота:

```
pytnon arnbjorg_vk_bot.py
```

## Запуск бота на сервере

Для постоянной работы бота необходимо запустить на сервере, например на [Heroku: Cloud Application Platform](https://www.heroku.com).
На сайте есть подробная [инструкция](https://devcenter.heroku.com/articles/getting-started-with-python).


Переменные окружения передаются на сервер командой
```
heroku config:set TELEGRAM_TOKEN={telegram token}
```

Для работы с Heroku на территории РФ может понадобиться VPN

## Цели проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
