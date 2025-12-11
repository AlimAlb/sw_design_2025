from datetime import date
from typing import List, Optional
from commands.base import Command
from domain.models import Account, Category, Operation
from domain.types import AccountId, CategoryId, CategoryType, OperationType
from services.facades import AccountsFacade, AnalyticsFacade, CategoriesFacade, OperationsFacade


class CreateAccountCommand(Command):        
    def __init__(
        self,
        facade: AccountsFacade,
        name: str,
        initial_balance: float
    ) -> None:
        self._facade = facade
        self._name = name
        self._initial_balance = initial_balance
    
    def execute(self) -> Account:
        return self._facade.create_account(self._name, self._initial_balance)


class DeleteAccountCommand(Command):    
    def __init__(self, facade: AccountsFacade, account_id: AccountId) -> None:
        self._facade = facade
        self._account_id = account_id
    
    def execute(self) -> bool:
        return self._facade.delete_account(self._account_id)


class ListAccountsCommand(Command):
    def __init__(self, facade: AccountsFacade) -> None:
        self._facade = facade
    
    def execute(self) -> List[Account]:
        return self._facade.get_all_accounts()


class CreateCategoryCommand(Command):
    def __init__(self, facade: CategoriesFacade, name: str, category_type: CategoryType) -> None:
        self._facade = facade
        self._name = name
        self._category_type = category_type
    
    def execute(self) -> Category:
        return self._facade.create_category(self._name, self._category_type)


class DeleteCategoryCommand(Command):
    def __init__(self, facade: CategoriesFacade, category_id: CategoryId) -> None:
        self._facade = facade
        self._category_id = category_id
    
    def execute(self) -> bool:
        return self._facade.delete_category(self._category_id)


class ListCategoriesCommand(Command):
    def __init__(self, facade: CategoriesFacade) -> None:
        self._facade = facade
    
    def execute(self) -> List[Category]:
        return self._facade.get_all_categories()


class CreateOperationCommand(Command):
    def __init__(
        self,
        facade: OperationsFacade,
        operation_type: OperationType,
        amount: float,
        operation_date: date,
        category_id: CategoryId,
        account_id: AccountId,
        description: Optional[str] = None
    ) -> None:
        self._facade = facade
        self._operation_type = operation_type
        self._amount = amount
        self._operation_date = operation_date
        self._category_id = category_id
        self._account_id = account_id
        self._description = description
    
    def execute(self) -> Operation:
        return self._facade.create_operation(
            operation_type=self._operation_type,
            amount=self._amount,
            operation_date=self._operation_date,
            category_id=self._category_id,
            account_id=self._account_id,
            description=self._description
        )


class ListOperationsCommand(Command):
    def __init__(self, facade: OperationsFacade) -> None:
        self._facade = facade
    
    def execute(self) -> List[Operation]:
        return self._facade.get_all_operations()


class CalculateBalanceDifferenceCommand(Command):
    def __init__(
        self,
        facade: AnalyticsFacade,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> None:
        self._facade = facade
        self._start_date = start_date
        self._end_date = end_date
    
    def execute(self) -> float:
        return self._facade.calculate_balance_difference(
            self._start_date,
            self._end_date
        )


class GroupByCategoriesCommand(Command):
    def __init__(
        self,
        facade: AnalyticsFacade,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> None:
        self._facade = facade
        self._start_date = start_date
        self._end_date = end_date
    
    def execute(self) -> dict[str, float]:
        return self._facade.group_by_categories(
            self._start_date,
            self._end_date
        )



