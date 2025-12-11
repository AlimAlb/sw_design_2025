from typing import List, Optional
from domain.models import Account
from domain.types import AccountId
from persistence.repositories import AccountRepository


class AccountRepositoryProxy:
    def __init__(self, repository: AccountRepository) -> None:
        self._repository = repository
    

    def create(self, account: Account) -> Account:
        result = self._repository.create(account)
        print(f"[LOG] Created account: {account.name} (ID: {account.id})")
        return result
    
    def get_by_id(self, account_id: AccountId) -> Optional[Account]:
        return self._repository.get_by_id(account_id)
    
    def get_all(self) -> List[Account]:
        accounts = self._repository.get_all()
        print(f"[LOG] Retrieved {len(accounts)} accounts")
        return accounts
    

    
    def delete(self, account_id: AccountId) -> bool:
        account = self._repository.get_by_id(account_id)
        result = self._repository.delete(account_id)
        if result and account:
            print(f"[LOG] Deleted account: {account.name} (ID: {account_id})")
        return result
    
    def update(self, account: Account) -> Account:
        result = self._repository.update(account)
        print(f"[LOG] Updated account: {account.name} (ID: {account.id})")
        return result



