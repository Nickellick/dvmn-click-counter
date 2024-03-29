# Обрезка ссылок с помощью Битли

Данный проект умеет создавать сокращённые ссылки (и показывать статистику по существующим!) с помощью сервиса [bit.ly](https://bit.ly)
# Как установить

Перед установкой требуется
[создать акканут на bit.ly](https://bitly.com/a/sign_up?rd=%2Forganization%2Fdefault%2Fsubscription%3Ftier%3Dstarter%26billing%3Dannual%26suppress_blocking%3Dfalse%26payment_form%3Dtrue)
(бесплатного аккаунта будет достаточно), после чего получить ключ разработчика. Для этого нужно зайти в настройки аккаунта, и в пункте `API`
ввесть пароль и нажать на кнопку `Generate Token`

Пример ключа: **(Важно! Это всего лишь пример, ключ не работает!)**

```
abcd1efgh2345ijk6789lm1no2345p6q7rs89t01
```

(Набор букв и цифр, а также их порядок могут быть абсолютно случайными)

Далее ключ можно разместить в системе двумя способами:

1) Создать переменную среды `BITLY_DVMN_TOKEN` и присвоить ей значение ключа. Для Linux это команда

        export BITLY_DVMN_TOKEN=<значение_ключа_без_скобок>

2) Создать файл `.env` в корне проекта, и вписать туда

        BITLY_DVMN_TOKEN=<значение_ключа_без_скобок>


`Python3` должен быть уже установлен. Затем используйте `pip` (или `pip3`, есть конфликт с `Python2`) для установки зависимостей:

```pip install -r requirements.txt```

# Запуск

Для запуска введите в папке с проектом

```
python main.py <ссылка_без_треугольных_скобок>
```

или 

```
python3 main.py <ссылка_без_треугольных_скобок>
```

Текст с помощью можно вызвать при помощи аргумента `-h` или `--help`
```
python main.py -h
```

# Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.