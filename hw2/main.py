from datetime import date
from typing import Optional

from commands.concrete import (
    CalculateBalanceDifferenceCommand,
    CreateAccountCommand,
    CreateCategoryCommand,
    CreateOperationCommand,
    DeleteAccountCommand,
    DeleteCategoryCommand,
    GroupByCategoriesCommand,
    ListAccountsCommand,
    ListCategoriesCommand,
    ListOperationsCommand
)
from di import DIContainer
from domain.types import AccountId, CategoryId, CategoryType, OperationType
from io_layer.exporters import CSVExportVisitor, DataExporter, JSONExportVisitor, YAMLExportVisitor
from io_layer.importers import CSVImporter, JSONImporter, YAMLImporter


class ConsoleMenu:
    def __init__(self, container: DIContainer) -> None:
        self._container = container
    
    def run(self) -> None:
        while True:
            self._print_menu()
            choice = input("Выберите действие: ").strip()
            
            if choice == "0":
                print("Выход из приложения.")
                break
            
            try:
                self._handle_choice(choice)
            except Exception as e:
                print(f"Ошибка: {e}")
            
            input("\nНажмите Enter для продолжения...")
    
    def _print_menu(self) -> None:
        print("\n" + "=" * 50)
        print("Управление финансами")
        print("=" * 50)
        print("1. Управление счетами")
        print("2. Управление категориями")
        print("3. Управление операциями")
        print("4. Аналитика")
        print("5. Импорт данных")
        print("6. Экспорт данных")
        print("0. Выход")
        print("=" * 50)
    
    def _handle_choice(self, choice: str) -> None:
        if choice == "1":
            self._handle_accounts_menu()
        elif choice == "2":
            self._handle_categories_menu()
        elif choice == "3":
            self._handle_operations_menu()
        elif choice == "4":
            self._handle_analytics_menu()
        elif choice == "5":
            self._handle_import_menu()
        elif choice == "6":
            self._handle_export_menu()
        else:
            print("Неверный выбор!")
    
    def _handle_accounts_menu(self) -> None:
        print("\n--- Управление счетами ---")
        print("1. Создать счёт")
        print("2. Удалить счёт")
        print("3. Просмотреть все счета")
        
        choice = input("Выберите действие: ").strip()
        facade = self._container.accounts_facade
        
        if choice == "1":
            name = input("Введите имя счёта: ").strip()
            try:
                balance = float(input("Введите начальный баланс: "))
                command = CreateAccountCommand(facade, name, balance)
                account = command.execute()
                print(f"Счёт создан: {account.name} (ID: {account.id}, Баланс: {account.balance})")
            except ValueError as e:
                print(f"Ошибка: {e}")
        
        elif choice == "2":
            accounts = facade.get_all_accounts()
            if not accounts:
                print("Нет счетов для удаления.")
                return
            
            print("\nДоступные счета:")
            for acc in accounts:
                print(f"  ID: {acc.id}, Имя: {acc.name}, Баланс: {acc.balance}")
            
            try:
                account_id = AccountId(int(input("Введите ID счёта для удаления: ")))
                command = DeleteAccountCommand(facade, account_id)
                if command.execute():
                    print("Счёт удалён.")
                else:
                    print("Счёт не найден.")
            except ValueError:
                print("Неверный ID.")
        
        elif choice == "3":
            command = ListAccountsCommand(facade)
            accounts = command.execute()
            
            if not accounts:
                print("Нет счетов.")
            else:
                print("\nВсе счета:")
                for acc in accounts:
                    print(f"  ID: {acc.id}, Имя: {acc.name}, Баланс: {acc.balance}")
    
    def _handle_categories_menu(self) -> None:
        print("\n--- Управление категориями ---")
        print("1. Создать категорию дохода")
        print("2. Создать категорию расхода")
        print("3. Удалить категорию")
        print("4. Просмотреть все категории")
        
        choice = input("Выберите действие: ").strip()
        
        facade = self._container.categories_facade
        
        if choice == "1":
            name = input("Введите имя категории: ").strip()
            try:
                command = CreateCategoryCommand(facade, name, CategoryType.INCOME)
                category = command.execute()
                print(f"Категория создана: {category.name} (ID: {category.id}, Тип: доход)")
            except ValueError as e:
                print(f"Ошибка: {e}")
        
        elif choice == "2":
            name = input("Введите имя категории: ").strip()
            try:
                command = CreateCategoryCommand(facade, name, CategoryType.EXPENSE)
                category = command.execute()
                print(f"Категория создана: {category.name} (ID: {category.id}, Тип: расход)")
            except ValueError as e:
                print(f"Ошибка: {e}")
        
        elif choice == "3":
            categories = facade.get_all_categories()
            if not categories:
                print("Нет категорий для удаления.")
                return
            
            print("\nДоступные категории:")
            for cat in categories:
                print(f"  ID: {cat.id}, Имя: {cat.name}, Тип: {cat.category_type.value}")
            
            try:
                category_id = CategoryId(int(input("Введите ID категории для удаления: ")))
                command = DeleteCategoryCommand(facade, category_id)
                if command.execute():
                    print("Категория удалена.")
                else:
                    print("Категория не найдена.")
            except ValueError:
                print("Неверный ID.")
        
        elif choice == "4":
            command = ListCategoriesCommand(facade)
            categories = command.execute()
            
            if not categories:
                print("Нет категорий.")
            else:
                print("\nВсе категории:")
                for cat in categories:
                    print(f"  ID: {cat.id}, Имя: {cat.name}, Тип: {cat.category_type.value}")
    
    def _handle_operations_menu(self) -> None:
        print("\n--- Управление операциями ---")
        print("1. Создать операцию")
        print("2. Просмотреть все операции")
        
        choice = input("Выберите действие: ").strip()
        
        facade = self._container.operations_facade
        
        if choice == "1":
            accounts = self._container.accounts_facade.get_all_accounts()
            if not accounts:
                print("Сначала создайте счёт.")
                return
            
            print("\nДоступные счета:")
            for acc in accounts:
                print(f"  ID: {acc.id}, Имя: {acc.name}")
            
            try:
                account_id = AccountId(int(input("Введите ID счёта: ")))
            except ValueError:
                print("Неверный ID счёта.")
                return
            
            categories = self._container.categories_facade.get_all_categories()
            if not categories:
                print("Сначала создайте категорию.")
                return
            
            print("\nДоступные категории:")
            for cat in categories:
                print(f"  ID: {cat.id}, Имя: {cat.name}, Тип: {cat.category_type.value}")
            
            try:
                category_id = CategoryId(int(input("Введите ID категории: ")))
            except ValueError:
                print("Неверный ID категории.")
                return
            
            print("\nТип операции:")
            print("1. Доход")
            print("2. Расход")
            op_type_choice = input("Выберите тип: ").strip()
            
            if op_type_choice == "1":
                operation_type = OperationType.INCOME
            elif op_type_choice == "2":
                operation_type = OperationType.EXPENSE
            else:
                print("Неверный выбор типа.")
                return
            
            try:
                amount = float(input("Введите сумму (> 0): "))
            except ValueError:
                print("Неверная сумма.")
                return
            
            
            date_str = input("Введите дату (YYYY-MM-DD) или нажмите Enter для сегодня: ").strip()
            if date_str:
                try:
                    operation_date = date.fromisoformat(date_str)
                except ValueError:
                    print("Неверный формат даты.")
                    return
            else:
                operation_date = date.today()
            
            
            description = input("Введите описание (опционально): ").strip() or None
            
            try:
                command = CreateOperationCommand(
                    facade,
                    operation_type,
                    amount,
                    operation_date,
                    category_id,
                    account_id,
                    description
                )
                operation = command.execute()
                account = self._container.accounts_facade.get_account(account_id)
                print(f"Операция создана (ID: {operation.id})")
                if account:
                    print(f"Новый баланс счёта '{account.name}': {account.balance}")
            except ValueError as e:
                print(f"Ошибка: {e}")
        
        elif choice == "2":
            command = ListOperationsCommand(facade)
            operations = command.execute()
            
            if not operations:
                print("Нет операций.")
            else:
                print("\nВсе операции:")
                for op in operations:
                    op_type_str = "Доход" if op.operation_type == OperationType.INCOME else "Расход"
                    desc = f", Описание: {op.description}" if op.description else ""
                    print(
                        f"  ID: {op.id}, Тип: {op_type_str}, Сумма: {op.amount}, "
                        f"Дата: {op.date}, Счёт: {op.account_id}, "
                        f"Категория: {op.category_id}{desc}"
                    )
    
    def _handle_analytics_menu(self) -> None:
        print("\n--- Аналитика ---")
        print("1. Разница доходы - расходы")
        print("2. Группировка по категориям")
        
        choice = input("Выберите действие: ").strip()
        
        facade = self._container.analytics_facade
        
        # Date range
        start_date: Optional[date] = None
        end_date: Optional[date] = None
        
        use_period = input("Использовать период? (y/n): ").strip().lower() == 'y'
        if use_period:
            start_str = input("Начальная дата (YYYY-MM-DD) или Enter для пропуска: ").strip()
            if start_str:
                try:
                    start_date = date.fromisoformat(start_str)
                except ValueError:
                    print("Неверный формат даты, период не будет использован.")
            
            end_str = input("Конечная дата (YYYY-MM-DD) или Enter для пропуска: ").strip()
            if end_str:
                try:
                    end_date = date.fromisoformat(end_str)
                except ValueError:
                    print("Неверный формат даты, период не будет использован.")
        
        if choice == "1":
            command = CalculateBalanceDifferenceCommand(facade, start_date, end_date)
            difference = command.execute()
            period_str = f" за период {start_date} - {end_date}" if start_date or end_date else ""
            print(f"\nРазница доходы - расходы{period_str}: {difference:.2f}")
        
        elif choice == "2":
            command = GroupByCategoriesCommand(facade, start_date, end_date)
            grouped = command.execute()
            
            if not grouped:
                print("Нет данных для группировки.")
            else:
                period_str = f" за период {start_date} - {end_date}" if start_date or end_date else ""
                print(f"\nГруппировка по категориям{period_str}:")
                for category_name, total in grouped.items():
                    print(f"  {category_name}: {total:.2f}")
    
    def _handle_import_menu(self) -> None:
        print("\n--- Импорт данных ---")
        print("1. Импорт из JSON")
        print("2. Импорт из CSV")
        print("3. Импорт из YAML")
        
        choice = input("Выберите формат: ").strip()
        file_path = input("Введите путь к файлу: ").strip()
        
        try:
            if choice == "1":
                importer = JSONImporter()
            elif choice == "2":
                importer = CSVImporter()
            elif choice == "3":
                importer = YAMLImporter()
            else:
                print("Неверный выбор формата.")
                return
            
            data = importer.import_data(file_path)
            
            
            accounts_facade = self._container.accounts_facade
            for account in data.get('accounts', []):
                
                existing = accounts_facade.get_account(account.id)
                if not existing:
                    accounts_facade.create_account(account.name, account.balance)
                    print(f"Импортирован счёт: {account.name}")
            
            categories_facade = self._container.categories_facade
            for category in data.get('categories', []):
                existing = categories_facade.get_category(category.id)
                if not existing:
                    categories_facade.create_category(category.name, category.category_type)
                    print(f"Импортирована категория: {category.name}")
            
            operations_facade = self._container.operations_facade
            for operation in data.get('operations', []):
                try:
                    operations_facade.create_operation(
                        operation.operation_type,
                        operation.amount,
                        operation.date,
                        operation.category_id,
                        operation.account_id,
                        operation.description
                    )
                    print(f"Импортирована операция: ID {operation.id}")
                except ValueError as e:
                    print(f"Ошибка импорта операции {operation.id}: {e}")
            
            print("Импорт завершён.")
        
        except Exception as e:
            print(f"Ошибка импорта: {e}")
    
    def _handle_export_menu(self) -> None:
        print("\n--- Экспорт данных ---")
        print("1. Экспорт в JSON")
        print("2. Экспорт в CSV")
        print("3. Экспорт в YAML")
        
        choice = input("Выберите формат: ").strip()
        
        if choice not in ["1", "2", "3"]:
            print("Неверный выбор формата.")
            return
        
        format_map = {"1": "json", "2": "csv", "3": "yaml"}
        format_type = format_map[choice]
        format_ext = format_type
        
        file_path = input(f"Введите путь к файлу для экспорта ({format_ext.upper()}): ").strip()
        
        if not file_path:
            print("Путь к файлу не указан.")
            return
        
        try:
            accounts = self._container.accounts_facade.get_all_accounts()
            categories = self._container.categories_facade.get_all_categories()
            operations = self._container.operations_facade.get_all_operations()
            
            if format_type == 'json':
                visitor = JSONExportVisitor()
            elif format_type == 'csv':
                visitor = CSVExportVisitor()
            elif format_type == 'yaml':
                visitor = YAMLExportVisitor()
            else:
                print("Неверный формат экспорта.")
                return
            
            exporter = DataExporter(visitor)
            exporter.export_to_file(file_path, accounts, categories, operations)
            
            print(f"Данные экспортированы в {file_path} (формат: {format_ext.upper()})")
        
        except Exception as e:
            print(f"Ошибка экспорта: {e}")


def main() -> None:
    container = DIContainer()
    menu = ConsoleMenu(container)
    menu.run()


if __name__ == "__main__":
    main()



