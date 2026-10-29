# Clipdeck

Десктопное приложение для Windows: публикует одно видео сразу на группу TikTok-аккаунтов и показывает статистику роликов.

## Возможности

**Аккаунты**
- Вход через браузер (интерфейс не замирает, вход можно отменить) или по кукам (`sessionid`, `tt-target-idc`).
- Массовый импорт списка: вставьте строки `логин  sessionid  tt-target-idc` — порядок полей и разделитель любые, данные из Excel тоже подходят.
- Группы по тегам, массовая смена тега и удаление, поиск по аккаунтам и фильтр по тегу.

**Публикация**
- Одно видео на все аккаунты выбранной группы.
- Подпись и хэштеги в одном поле, счётчик до 2200 символов.
- Пауза между аккаунтами (настраивается в «Настройках»), остановка на полпути.
- Журнал с причиной ошибки по каждому аккаунту, кнопки «Повторить ошибки» и «Скопировать журнал».
- История публикаций в базе: что, когда и на какой аккаунт ушло, с текстом ошибки.

**Статистика**
- Просмотры, лайки, комментарии, репосты и подписчики по аккаунтам и по каждому ролику.
- Прирост с прошлого обновления, пометки «Растёт», «Без роста», «Нет просмотров».
- Обновление вручную или автоматически (15, 30 минут, час), история за 30 дней.
- Экспорт в CSV (Excel открывает без настройки кодировки).

**Соединение и обслуживание**
- Необязательный прокси (SOCKS5 или HTTP) для всех запросов, проверка IP в настройках.
- Проверка окружения: Node.js, Chrome, пакеты, файлы куков — видно, чего не хватает.
- Все данные (база, куки, настройки) лежат локально рядом с программой.

## Требования

Windows, Python 3.10+, Google Chrome, Node.js.

## Запуск из исходников

```bash
python -m venv venv
venv\Scripts\pip install -r requirements.txt
cd tiktok_uploader\tiktok-signature
npm install
npx playwright install chromium
cd ..\..
venv\Scripts\python main.py
```

Скопируйте `.env.example` в `.env`, если нужен прокси.

Проверка, что всё на месте: `venv\Scripts\python main.py --selftest` — результат в `selftest.log`
(то же самое доступно в приложении: «Настройки» → «Проверить окружение»).

## Сборка exe

```bash
venv\Scripts\pip install pyinstaller
venv\Scripts\python -m PyInstaller --noconfirm --clean --windowed --onedir --name Clipdeck ^
  --icon src/ui/assets/icon.ico ^
  --add-data "src/ui/assets;src/ui/assets" ^
  --add-data "tiktok_uploader/tiktok-signature;tiktok_uploader/tiktok-signature" ^
  --collect-data fake_useragent ^
  --collect-submodules undetected_chromedriver ^
  --hidden-import tiktok_uploader.tiktok --hidden-import tiktok_uploader.stats ^
  --exclude-module playwright --exclude-module aiohttp --exclude-module tkinter main.py
```

Рядом с `Clipdeck.exe` создаются `data/`, `CookiesDir/` и `.env`. Проверка сборки: `Clipdeck.exe --selftest` пишет `selftest.log`.

## Тесты

```bash
venv\Scripts\pip install pytest
venv\Scripts\python -m pytest tests -q
```

`tests/smoke_gui.py` поднимает интерфейс в offscreen-режиме и проверяет, что страницы собираются и база отвечает.

## Если что-то не работает

| Симптом | Причина и решение |
| --- | --- |
| «Не удалось загрузить модуль загрузки» | не хватает пакета из `requirements.txt` — установите его |
| «Node.js не найден в PATH» | установите Node.js и перезапустите программу (или запустите из новой консоли) |
| Статистика падает с ошибкой playwright | в `tiktok_uploader\tiktok-signature` не выполнен `npm install` / `npx playwright install chromium` |
| Вход через браузер не открывается | Chrome не найден или устарел: проверьте в «Настройках» → «Проверить окружение» |
| «сессия недействительна» | куки протухли, войдите в аккаунт заново |

## Ограничения

- Программа работает через неофициальные запросы TikTok, после его обновлений что-то может перестать работать.
- TikTok может блокировать публикацию на уровне аккаунта или региона.
- Массовая публикация одного видео на много аккаунтов повышает риск ограничений. Используйте только свои аккаунты и соблюдайте правила платформы.
- Куки аккаунтов хранятся в открытом виде в `CookiesDir/`. Не публикуйте эту папку и не передавайте её другим.

## Лицензия и авторство

MIT, см. [LICENSE](LICENSE). Проект основан на [TikTokAutoUploader](https://github.com/y1ki/TikTokAutoUploader) (Y1ki) и использует [tiktok-signature](https://github.com/carcabot/tiktok-signature) (CarcaBot).
