# Консольное приложение «Управление финансами»
## Описание проекта
Приложение позволяет:
- Управлять банковскими счетами (создание, удаление, просмотр)
- Управлять категориями доходов и расходов
- Создавать финансовые операции (доходы/расходы) с автоматическим обновлением баланса счетов
- Анализировать финансовые данные (разница доходов и расходов, группировка по категориям)
- Импортировать данные из JSON, CSV, YAML
- Экспортировать данные в JSON, CSV, YAML

## Структура проекта

```
hw2/
├── main.py                 # Точка входа, консольное меню
├── di.py                   # DI-контейнер
│
├── domain/                 # Доменный слой
│   ├── __init__.py
│   ├── types.py           # Перечисления и типы (AccountId, CategoryId, OperationType)
│   ├── models.py          # Dataclass-модели (Account, Category, Operation)
│   └── factory.py         # Фабрика для создания доменных объектов (Factory pattern)
│
├── persistence/            # Слой персистентности
│   ├── __init__.py
│   └── repositories.py    # In-memory репозитории (AccountRepository, CategoryRepository, OperationRepository)
│
├── services/               # Слой сервисов
│   ├── __init__.py
│   └── facades.py         # Фасады для работы с доменом (Facade pattern): AccountsFacade, CategoriesFacade
│                           # OperationsFacade, AnalyticsFacade                           
│                           
│
├── commands/               # Слой команд
│   ├── __init__.py
│   ├── base.py            # Интерфейс Command (Command pattern)
│   ├── concrete.py        # Конкретные команды (CreateAccountCommand, ListOperationsCommand и т.д.)
│   └── decorators.py      # Декоратор для измерения времени (Decorator pattern)
│
└── io_layer/              # Слой ввода/вывода
    ├── __init__.py
    ├── importers.py       # Импортеры данных (Template Method pattern): JSONImporter, CSVImporter, YAMLImporter
    └── exporters.py       # Экспортеры данных (Visitor pattern): JSONExportVisitor, DataExporter
```

## Реализованные паттерны проектирования

### 1. Фабрика - `domain/factory.py`  
Создание доменных объектов (Account, Category, Operation) с валидацией и автоматической генерацией ID.

### 2. Фасад - `services/facades.py`  
 Упрощение работы с доменом через высокоуровневые интерфейсы. Инкапсулирует работу с репозиториями и бизнес-логику.

### 3. Команда - `commands/base.py`, `commands/concrete.py`  
 Инкапсуляция запросов как объектов. Каждая операция (создание счёта, удаление категории и т.д.) представлена отдельной командой.

### 4. Декоратор - `commands/decorators.py`  
 Добавление функциональности измерения времени выполнения команд без изменения их структуры.

### 5. Шаблонный метод - `io_layer/importers.py`  
 Определение алгоритма импорта данных  с возможностью переопределения шагов для разных форматов (JSON, CSV, YAML).

### 6. Посетитель - `io_layer/exporters.py`  
Разделение алгоритма экспорта от структуры данных. Разные посетители могут экспортировать в разные форматы.

### 7. DI Container - `di.py`
 Централизованное управление зависимостями. Все компоненты создаются и связываются в одном месте.

## Принципы SOLID

### 1. Single Responsibility Principle 
- **Facades** (`services/facades.py`): Каждый фасад отвечает только за свою область (AccountsFacade — только за счета, CategoriesFacade — только за категории).
- **Repositories** (`persistence/repositories.py`): Каждый репозиторий отвечает только за работу с одним типом сущности.
- **Commands** (`commands/concrete.py`): Каждая команда выполняет только одну операцию.
- **Importers/Exporters** (`io_layer/`): Каждый класс отвечает только за один формат или одну операцию.

### 2. Open/Closed Principle 
- **DataImporter** (`io_layer/importers.py`): Базовый класс закрыт для модификации, но открыт для расширения через наследование (JSONImporter, CSVImporter, YAMLImporter).
- **ExportVisitor** (`io_layer/exporters.py`): Можно добавить новые форматы экспорта, не изменяя существующий код.
- **Command** (`commands/base.py`): Можно добавлять новые команды, не изменяя интерфейс Command.

### 3. Liskov Substitution Principle 
- Все подклассы `DataImporter` могут использоваться вместо базового класса.
- Все подклассы `Command` могут использоваться через общий интерфейс.

### 4. Interface Segregation Principle 
- **Command** (`commands/base.py`): Минимальный интерфейс с одним методом `execute()`.
- **ExportVisitor** (`io_layer/exporters.py`): Раздельные методы для каждого типа сущности (visit_account, visit_category, visit_operation).

### 5. Dependency Inversion Principle 
- Все зависимости передаются через конструкторы (dependency injection).
- **DI Container** (`di.py`): Централизованное управление зависимостями.
- Фасады зависят от абстракций (репозитории, фабрика), а не от конкретных реализаций.
- Команды зависят от фасадов, а не от репозиториев напрямую.

## Принципы GRASP

### 1. Information Expert
- **DomainFactory**: Знает, как создавать и валидировать доменные объекты.
- **Repositories**: Знают, как хранить и извлекать данные.
- **Facades**: Знают бизнес-логику и координируют работу репозиториев.

### 2. Creator 
- **DomainFactory**: Создаёт доменные объекты (Account, Category, Operation).
- **DIContainer**: Создаёт все компоненты системы и управляет их зависимостями.

### 3. Low Coupling 
- Слои изолированы друг от друга (domain не зависит от persistence, services не зависит от commands).
- Зависимости передаются через конструкторы (dependency injection).
- Использование абстракций (интерфейсов) вместо конкретных классов.

### 4. High Cohesion 
- **domain/**: Все классы связаны с доменной моделью.
- **persistence/**: Все классы связаны с хранением данных.
- **services/**: Все фасады связаны с бизнес-логикой.
- **commands/**: Все команды связаны с выполнением операций.

### 5. Controller 
- **Facades**: Управляют бизнес-логикой и координируют работу между компонентами.
- **Commands**: Инкапсулируют сценарии использования (создание счёта, удаление категории и т.д.).
- **ConsoleMenu**: Управляет пользовательским интерфейсом и делегирует выполнение командам.

### 6. Polymorphism 
- **DataImporter**: Разные импортеры обрабатывают разные форматы через единый интерфейс.
- **ExportVisitor**: Разные посетители могут экспортировать в разные форматы.
- **Command**: Разные команды выполняются через единый интерфейс.

## Требования
- Python 3.11+
- Стандартная библиотека Python и PyYAML

Для установки опциональных зависимостей (PyYAML): <br/>
Убедитесь, что установлен Python 3.11 или выше. Далее установка необходимых пакетов (он по сути один)
```bash
pip install -r requirements.txt
```

Из корневой директории проекта `hw2/`:
```bash
python main.py
```

