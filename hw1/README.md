# HW1 — ERP для зоопарка

Домашнее задание #1. Программа моделирует зоопарк: добавление животных, учёт инвентаря, проверка животных ветеринарной клиникой и простое консольное меню для работы.

## Структура проекта
- README.md — описание 
- hw1/
  - animal_classes.py — модели животных (`Animal`, `Herbo`, `Predator`, конкретные виды)
  - inventory_classes.py — инвентарь (`Thing`, `Table`, `Computer`)
  - vet_clinic.py — проверка животных (`Vetclinic`)
  - zoo.py — хранение списка животных/инвентаря, расчёт корма, загрузка/сохранение состояния
  - ui.py — консольный интерфейс и обработка команд
  - main.py — точка входа, запуск UI и регистрация зависимостей
  - di_container.py — DI‑контейнер для создания объектов
  - interfaces.py — протоколы `IAlive`, `IInventory`
  - data/
    - animals.plk, inventory.plk — сериализованное состояние зоопарка
  - tests/ — модульные тесты (`unittest`)
  - requirements.txt — нужен только для прогона тестов (сама программа работает без внешних пакетов)

## Как запустить
Требуется Python 3.14, дополнительных пакетов нет.
1) Откройте терминал в корне репозитория.
2) Выполните:
```
python3.14 hw1/main.py
```
   или, находясь в каталоге `hw1`:
```
cd hw1
python3.14 main.py
```
3) Состояние сохраняется в `hw1/data/animals.plk` и `hw1/data/inventory.plk` (при необходимости удалите эти файлы для сброса).

## Окружение и тесты
Создать venv и поставить зависимости из `requirements.txt`:
```
cd hw1
python3.14 -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
Запуск тестов (из корня проекта или из `hw1`):
```
python3.14 -m unittest discover -s hw1/tests
```
С покрытием (coverage из requirements):
```
python3.14 -m coverage run -m unittest discover -s hw1/tests -p "test_*.py"
python3.14 -m coverage report
```
Текущее покрытие: 96% (292 строк, 13 пропусков).
```
Name                         Stmts   Miss  Cover
------------------------------------------------
animal_classes.py               35      0   100%
di_container.py                 28      1    96%
interfaces.py                    3      0   100%
inventory_classes.py            19      0   100%
tests/test_animals.py           16      1    94%
tests/test_di_container.py      38      1    97%
tests/test_inventory.py         17      1    94%
tests/test_zoo.py               51      1    98%
vet_clinic.py                    8      0   100%
zoo.py                          77      8    90%
------------------------------------------------
TOTAL                          292     13    96%
```

## Как устроен DI‑контейнер (`hw1/di_container.py`)
- Контейнер хранит спецификацию регистраций: `register(cls, singleton=True|False)` помечает тип как `SINGLETON` или `SCOPED`.
- `resolve(cls, **kwargs)`:
  - Для `SINGLETON` создаёт объект один раз и возвращает ту же ссылку; для потомков `Thing` при повторном resolve увеличивает количество предметов через `add(number)`.
  - Для `SCOPED` создаёт новый объект на каждый запрос и дополнительно прогоняет его через единственный экземпляр `Vetclinic.inspect`. Возвращает кортеж `(bool, obj)`, где `bool` — прошёл ли проверку.
- В `main.py` регистрируются все зависимости: животные как `SCOPED`, а `Table`, `Computer`, `Vetclinic`, `Zoo`, `UI` как `SINGLETON`. Далее контейнер создаёт `Zoo` и `Vetclinic`, а сами животные/инвентарь создаются по запросу из UI через `di.resolve(...)`.

## Использованные принципы SOLID
- S (Single Responsibility): каждый модуль отвечает за свою подсистему — модели животных, инвентарь, зоопарк, UI, контейнер зависимостей, клиника.
- O (Open/Closed): новые животные и предметы добавляются наследованием от базовых классов без изменения существующего кода.
- L (Liskov Substitution): работа строится через протоколы `IAlive` и `IInventory`, объекты, реализующие эти контракты, взаимозаменяемы в `Zoo` и UI.
- I (Interface Segregation): интерфейсы разбиты на узкие протоколы (`IAlive` и `IInventory`), клиенты используют только необходимые свойства.
- D (Dependency Inversion): точка входа зависит от абстракций и настраивает конкретные реализации через DI‑контейнер; проверки здоровья делегированы `Vetclinic`, а создание объектов отделено от их использования.
