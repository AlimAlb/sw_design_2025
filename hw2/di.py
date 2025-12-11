from domain.factory import DomainFactory
from persistence.proxy import AccountRepositoryProxy
from persistence.repositories import AccountRepository, CategoryRepository, OperationRepository
from services.facades import AccountsFacade, AnalyticsFacade, CategoriesFacade, OperationsFacade


class DIContainer:
    def __init__(self) -> None:
        self._factory = DomainFactory()
        self._account_repository = AccountRepository()
        self._category_repository = CategoryRepository()
        self._operation_repository = OperationRepository()
        self._account_repository_proxy = AccountRepositoryProxy(self._account_repository)
        self._accounts_facade = AccountsFacade(
            factory=self._factory,
            repository=self._account_repository_proxy
        )
        self._categories_facade = CategoriesFacade(
            factory=self._factory,
            repository=self._category_repository
        )
        self._operations_facade = OperationsFacade(
            factory=self._factory,
            operation_repository=self._operation_repository,
            account_facade=self._accounts_facade,
            category_facade=self._categories_facade
        )
        self._analytics_facade = AnalyticsFacade(
            operation_repository=self._operation_repository,
            category_facade=self._categories_facade
        )
    
    @property
    def accounts_facade(self) -> AccountsFacade:
        """Get accounts facade."""
        return self._accounts_facade
    
    @property
    def categories_facade(self) -> CategoriesFacade:
        """Get categories facade."""
        return self._categories_facade
    
    @property
    def operations_facade(self) -> OperationsFacade:
        """Get operations facade."""
        return self._operations_facade
    
    @property
    def analytics_facade(self) -> AnalyticsFacade:
        """Get analytics facade."""
        return self._analytics_facade



