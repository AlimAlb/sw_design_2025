from datetime import date
from typing import Optional
from domain.models import Account, Category, Operation
from domain.types import AccountId, CategoryId, OperationId, CategoryType, OperationType


class DomainFactory:
    def __init__(self) -> None:
        self._account_id_counter = 0
        self._category_id_counter = 0
        self._operation_id_counter = 0
    
    def create_account(self, name: str, initial_balance: float) -> Account:
        if not name or not name.strip():
            raise ValueError("Account name cannot be empty")
        
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        
        account_id = AccountId(self._account_id_counter)
        self._account_id_counter += 1
        
        return Account(
            id=account_id,
            name=name.strip(),
            balance=initial_balance
        )
    
    def create_category(self, name: str, category_type: CategoryType) -> Category:
        if not name or not name.strip():
            raise ValueError("Category name cannot be empty")

        category_id = CategoryId(self._category_id_counter)
        self._category_id_counter += 1        
        return Category(
            id=category_id,
            name=name.strip(),
            category_type=category_type
        )
    
    def create_operation(self,operation_type: OperationType, amount: float, operation_date: date,
    category_id: CategoryId, account_id: AccountId, description: Optional[str] = None) -> Operation:        
        if amount <= 0:
            raise ValueError("Operation amount must be greater than 0")
        
        operation_id = OperationId(self._operation_id_counter)
        self._operation_id_counter += 1
        return Operation(
            id=operation_id,
            operation_type=operation_type,
            amount=amount,
            date=operation_date,
            category_id=category_id,
            account_id=account_id,
            description=description.strip() if description else None
        )



