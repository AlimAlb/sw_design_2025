from enum import Enum
from typing import NewType

AccountId = NewType("AccountId", int)
CategoryId = NewType("CategoryId", int)
OperationId = NewType("OperationId", int)


class OperationType(Enum):
    INCOME = "income"
    EXPENSE = "expense"




class CategoryType(Enum):
    INCOME = "income"
    EXPENSE = "expense"



