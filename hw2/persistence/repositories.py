from typing import Dict, List, Optional
from domain.models import Account, Category, Operation
from domain.types import AccountId, CategoryId, OperationId
from datetime import date

class AccountRepository:
    def __init__(self) -> None:
        self._accounts: Dict[AccountId, Account] = {}
    
    def create(self, account: Account) -> Account:
        self._accounts[account.id] = account
        return account


    def get_by_id(self, account_id: AccountId) -> Optional[Account]:
        return self._accounts.get(account_id)
    
    def get_all(self) -> List[Account]:
        return list(self._accounts.values())
    
    def delete(self, account_id: AccountId) -> bool:
        if account_id in self._accounts:
            del self._accounts[account_id]
            return True
        return False
    
    def update(self, account: Account) -> Account:
        self._accounts[account.id] = account
        return account


class CategoryRepository:
    def __init__(self) -> None:
        self._categories: Dict[CategoryId, Category] = {}

    
    def create(self, category: Category) -> Category:
        self._categories[category.id] = category
        return category
    
    def get_by_id(self, category_id: CategoryId) -> Optional[Category]:
        return self._categories.get(category_id)
    
    def get_all(self) -> List[Category]:
        return list(self._categories.values())
    
    def delete(self, category_id: CategoryId) -> bool:
        if category_id in self._categories:
            del self._categories[category_id]
            return True
        return False


class OperationRepository:
    def __init__(self) -> None:
        self._operations: Dict[OperationId, Operation] = {}
    
    def create(self, operation: Operation) -> Operation:
        self._operations[operation.id] = operation
        return operation
    
    
    def get_by_id(self, operation_id: OperationId) -> Optional[Operation]:
        return self._operations.get(operation_id)
    
    def get_all(self) -> List[Operation]:
        return list(self._operations.values())
    
    def get_by_account(self, account_id: AccountId) -> List[Operation]:
        return [ op for op in self._operations.values() if op.account_id == account_id]
    

    def get_by_date_range(self, start_date: Optional["date"], end_date: Optional["date"]) -> List[Operation]:
        operations = list(self._operations.values())
        if start_date is not None:
            operations = [op for op in operations if op.date >= start_date]
        if end_date is not None:
            operations = [op for op in operations if op.date <= end_date]
        
        return operations



