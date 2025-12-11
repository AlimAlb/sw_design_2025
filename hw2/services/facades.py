from datetime import date
from typing import Dict, List, Optional
from domain.factory import DomainFactory
from domain.models import Account, Category, Operation
from domain.types import AccountId, CategoryId, OperationId, CategoryType, OperationType
from persistence.proxy import AccountRepositoryProxy
from persistence.repositories import CategoryRepository, OperationRepository

class AccountsFacade:    
    def __init__(self, factory: DomainFactory, repository: AccountRepositoryProxy) -> None:
        self._factory = factory
        self._repository = repository
    
    def create_account(self, name: str, initial_balance: float) -> Account:
        account = self._factory.create_account(name, initial_balance)
        return self._repository.create(account)
    
    def delete_account(self, account_id: AccountId) -> bool:
        return self._repository.delete(account_id)
    
    def get_all_accounts(self) -> List[Account]:
        return self._repository.get_all()
    
    def get_account(self, account_id: AccountId) -> Optional[Account]:
        return self._repository.get_by_id(account_id)
    
    def update_account_balance(self, account_id: AccountId, new_balance: float) -> None:
        account = self._repository.get_by_id(account_id)
        if account:
            account.balance = new_balance
            self._repository.update(account)


class CategoriesFacade:
    def __init__(self, factory: DomainFactory, repository: CategoryRepository) -> None:
        self._factory = factory
        self._repository = repository
    
    def create_category(self, name: str, category_type: CategoryType) -> Category:
        category = self._factory.create_category(name, category_type)
        return self._repository.create(category)
    
    def delete_category(self, category_id: CategoryId) -> bool:
        return self._repository.delete(category_id)
    
    def get_all_categories(self) -> List[Category]:
        return self._repository.get_all()
    
    def get_category(self, category_id: CategoryId) -> Optional[Category]:
        return self._repository.get_by_id(category_id)


class OperationsFacade:
    def __init__(self, factory: DomainFactory, operation_repository: OperationRepository, account_facade: AccountsFacade, category_facade: CategoriesFacade) -> None:
        self._factory = factory
        self._operation_repository = operation_repository
        self._account_facade = account_facade
        self._category_facade = category_facade
    
    def create_operation( self, operation_type: OperationType, amount: float, operation_date: date, category_id: CategoryId, account_id: AccountId, description: Optional[str] = None) -> Operation:
        account = self._account_facade.get_account(account_id)
        if account is None:
            raise ValueError(f"Account with ID {account_id} not found")
        
        
        category = self._category_facade.get_category(category_id)
        if category is None:
            raise ValueError(f"Category with ID {category_id} not found")
        
        if operation_type == OperationType.INCOME and category.category_type != CategoryType.INCOME:
            raise ValueError("Category type must be INCOME for income operations")
        if operation_type == OperationType.EXPENSE and category.category_type != CategoryType.EXPENSE:
            raise ValueError("Category type must be EXPENSE for expense operations")
        
        operation = self._factory.create_operation(
            operation_type=operation_type,
            amount=amount,
            operation_date=operation_date,
            category_id=category_id,
            account_id=account_id,
            description=description
        )
        if operation_type == OperationType.INCOME:
            new_balance = account.balance + amount
        else:
            new_balance = account.balance - amount
        self._account_facade.update_account_balance(account_id, new_balance)
        return self._operation_repository.create(operation)
    
    def get_all_operations(self) -> List[Operation]:
        return self._operation_repository.get_all()
    
    def get_operations_by_account(self, account_id: AccountId) -> List[Operation]:
        return self._operation_repository.get_by_account(account_id)


class AnalyticsFacade:
    def __init__(self, operation_repository: OperationRepository, category_facade: CategoriesFacade) -> None:
        self._operation_repository = operation_repository
        self._category_facade = category_facade
    
    def calculate_balance_difference( self,start_date: Optional[date] = None, end_date: Optional[date] = None) -> float:
        operations = self._operation_repository.get_by_date_range(start_date, end_date)
        income = sum(
            op.amount for op in operations
            if op.operation_type == OperationType.INCOME
        )
        expenses = sum(
            op.amount for op in operations
            if op.operation_type == OperationType.EXPENSE
        )
        
        return income - expenses
    
    def group_by_categories(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Dict[str, float]:
        operations = self._operation_repository.get_by_date_range(start_date, end_date)
        
        result: Dict[str, float] = {}
        
        for operation in operations:
            category = self._category_facade.get_category(operation.category_id)
            if category:
                category_name = category.name
                if category_name not in result:
                    result[category_name] = 0.0
                
                if operation.operation_type == OperationType.INCOME:
                    result[category_name] += operation.amount
                else:  # EXPENSE
                    result[category_name] -= operation.amount
        
        return result



