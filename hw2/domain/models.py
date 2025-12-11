from dataclasses import dataclass
from datetime import date
from typing import Optional
from domain.types import AccountId, CategoryId, OperationId, OperationType, CategoryType

@dataclass
class Account:
    id: AccountId
    name: str
    balance: float


@dataclass
class Category:
    id: CategoryId
    name: str
    category_type: CategoryType


@dataclass
class Operation:
    id: OperationId
    operation_type: OperationType
    amount: float
    date: date
    category_id: CategoryId
    account_id: AccountId
    description: Optional[str] = None

