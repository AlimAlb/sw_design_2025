from abc import ABC, abstractmethod
from typing import Any, List
import json
import csv
import yaml

from domain.models import Account, Category, Operation

class ExportVisitor(ABC):
    @abstractmethod
    def visit_account(self, account: Account) -> Any:
        pass
    
    @abstractmethod
    def visit_category(self, category: Category) -> Any:
        pass
    
    @abstractmethod
    def visit_operation(self, operation: Operation) -> Any:
        pass
    
    @abstractmethod
    def write_to_file(self, file_path: str, accounts: List[Account], categories: List[Category], operations: List[Operation]) -> None:
        pass


class JSONExportVisitor(ExportVisitor):
    def visit_account(self, account: Account) -> dict[str, Any]:
        return {
            'id': account.id,
            'name': account.name,
            'balance': account.balance
        }
    
    def visit_category(self, category: Category) -> dict[str, Any]:
        return {
            'id': category.id,
            'name': category.name,
            'category_type': category.category_type.value
        }
    
    def visit_operation(self, operation: Operation) -> dict[str, Any]:
        return {
            'id': operation.id,
            'operation_type': operation.operation_type.value,
            'amount': operation.amount,
            'date': operation.date.isoformat(),
            'category_id': operation.category_id,
            'account_id': operation.account_id,
            'description': operation.description
        }
    
    def write_to_file(self, file_path: str, accounts: List[Account], categories: List[Category], operations: List[Operation]) -> None:
        data = {
            'accounts': [self.visit_account(acc) for acc in accounts],
            'categories': [self.visit_category(cat) for cat in categories],
            'operations': [self.visit_operation(op) for op in operations]
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


class CSVExportVisitor(ExportVisitor):    
    def visit_account(self, account: Account) -> list[Any]:
        return ['account', account.id, account.name, account.balance, '', '', '', '', '', '', '']
    
    def visit_category(self, category: Category) -> list[Any]:
        return ['category', category.id, category.name, '', category.category_type.value, '', '', '', '', '', '']
    
    def visit_operation(self, operation: Operation) -> list[Any]:
        return [
            'operation',
            operation.id,
            '',
            '',
            '',
            operation.operation_type.value,
            operation.amount,
            operation.date.isoformat(),
            operation.category_id,
            operation.account_id,
            operation.description or ''
        ]
    
    def write_to_file(self, file_path: str, accounts: List[Account], categories: List[Category], operations: List[Operation]) -> None:
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['type', 'id', 'name', 'balance', 'category_type', 'operation_type', 'amount', 'date', 'category_id', 'account_id', 'description'])
            for account in accounts:
                writer.writerow(self.visit_account(account))

            for category in categories:
                writer.writerow(self.visit_category(category))
            
            for operation in operations:
                writer.writerow(self.visit_operation(operation))


class YAMLExportVisitor(ExportVisitor):    
    def visit_account(self, account: Account) -> dict[str, Any]:
        return {
            'id': account.id,
            'name': account.name,
            'balance': account.balance
        }
    
    def visit_category(self, category: Category) -> dict[str, Any]:
        return {
            'id': category.id,
            'name': category.name,
            'category_type': category.category_type.value
        }
    
    def visit_operation(self, operation: Operation) -> dict[str, Any]:
        return {
            'id': operation.id,
            'operation_type': operation.operation_type.value,
            'amount': operation.amount,
            'date': operation.date.isoformat(),
            'category_id': operation.category_id,
            'account_id': operation.account_id,
            'description': operation.description
        }
    
    def write_to_file(self, file_path: str, accounts: List[Account], categories: List[Category], operations: List[Operation]) -> None:
        data = {
            'accounts': [self.visit_account(acc) for acc in accounts],
            'categories': [self.visit_category(cat) for cat in categories],
            'operations': [self.visit_operation(op) for op in operations]
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


class DataExporter:    
    def __init__(self, visitor: ExportVisitor) -> None:
        self._visitor = visitor
    
    def export_accounts(self, accounts: List[Account]) -> List[Any]:
        return [self._visitor.visit_account(acc) for acc in accounts]
    
    def export_categories(self, categories: List[Category]) -> List[Any]:
        return [self._visitor.visit_category(cat) for cat in categories]
    
    def export_operations(self, operations: List[Operation]) -> List[Any]:
        return [self._visitor.visit_operation(op) for op in operations]
    
    def export_all(self, accounts: List[Account], categories: List[Category], operations: List[Operation]) -> dict[str, List[Any]]:
        return {
            'accounts': self.export_accounts(accounts),
            'categories': self.export_categories(categories),
            'operations': self.export_operations(operations)
        }
    
    def export_to_file(self, file_path: str, accounts: List[Account], categories: List[Category], operations: List[Operation]) -> None:
        self._visitor.write_to_file(file_path, accounts, categories, operations)



