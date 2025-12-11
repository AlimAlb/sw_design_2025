from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Dict, List
import json
import csv
from io import StringIO
import yaml 
from domain.models import Account, Category, Operation
from domain.types import AccountId, CategoryId, OperationId, CategoryType, OperationType


class DataImporter(ABC):
    def import_data(self, file_path: str) -> Dict[str, List[Any]]:
        raw_data = self._read_file(file_path)
        parsed_data = self._parse_data(raw_data)
        return parsed_data
    
    @abstractmethod
    def _read_file(self, file_path: str) -> str:
        pass


    @abstractmethod
    def _parse_data(self, raw_data: str) -> Dict[str, List[Any]]:
        pass


class JSONImporter(DataImporter):
    def _read_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _parse_data(self, raw_data: str) -> Dict[str, List[Any]]:
        data = json.loads(raw_data)
        result: Dict[str, List[Any]] = {
            'accounts': [],
            'categories': [],
            'operations': []
        }


        for acc_data in data.get('accounts', []):
            account = Account(
                id=AccountId(acc_data['id']),
                name=acc_data['name'],
                balance=float(acc_data['balance'])
            )
            result['accounts'].append(account)
        for cat_data in data.get('categories', []):
            category = Category(
                id=CategoryId(cat_data['id']),
                name=cat_data['name'],
                category_type=CategoryType(cat_data['category_type'])
            )
            result['categories'].append(category)
        
        for op_data in data.get('operations', []):
            operation = Operation(
                id=OperationId(op_data['id']),
                operation_type=OperationType(op_data['operation_type']),
                amount=float(op_data['amount']),
                date=date.fromisoformat(op_data['date']),
                category_id=CategoryId(op_data['category_id']),
                account_id=AccountId(op_data['account_id']),
                description=op_data.get('description')
            )
            result['operations'].append(operation)
        return result


class CSVImporter(DataImporter):
    def _read_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _parse_data(self, raw_data: str) -> Dict[str, List[Any]]:
        result: Dict[str, List[Any]] = {
            'accounts': [],
            'categories': [],
            'operations': []
        }
        
        reader = csv.DictReader(StringIO(raw_data))
        
        for row in reader:
            entity_type = row.get('type', '').lower()
            
            if entity_type == 'account':
                account = Account(
                    id=AccountId(int(row['id'])),
                    name=row['name'],
                    balance=float(row['balance'])
                )
                result['accounts'].append(account)
            
            elif entity_type == 'category':
                category = Category(
                    id=CategoryId(int(row['id'])),
                    name=row['name'],
                    category_type=CategoryType(row['category_type'])
                )
                result['categories'].append(category)
            
            elif entity_type == 'operation':
                operation = Operation(
                    id=OperationId(int(row['id'])),
                    operation_type=OperationType(row['operation_type']),
                    amount=float(row['amount']),
                    date=date.fromisoformat(row['date']),
                    category_id=CategoryId(int(row['category_id'])),
                    account_id=AccountId(int(row['account_id'])),
                    description=row.get('description') or None
                )
                result['operations'].append(operation)
        
        return result


class YAMLImporter(DataImporter):
    def _read_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _parse_data(self, raw_data: str) -> Dict[str, List[Any]]:
        data = yaml.safe_load(raw_data)
        
        result: Dict[str, List[Any]] = {
            'accounts': [],
            'categories': [],
            'operations': []
        }
        

        for acc_data in data.get('accounts', []):
            account = Account(
                id=AccountId(acc_data['id']),
                name=acc_data['name'],
                balance=float(acc_data['balance'])
            )
            result['accounts'].append(account)
        

        for cat_data in data.get('categories', []):
            category = Category(
                id=CategoryId(cat_data['id']),
                name=cat_data['name'],
                category_type=CategoryType(cat_data['category_type'])
            )
            result['categories'].append(category)
        

        for op_data in data.get('operations', []):
            operation = Operation(
                id=OperationId(op_data['id']),
                operation_type=OperationType(op_data['operation_type']),
                amount=float(op_data['amount']),
                date=date.fromisoformat(op_data['date']),
                category_id=CategoryId(op_data['category_id']),
                account_id=AccountId(op_data['account_id']),
                description=op_data.get('description')
            )
            result['operations'].append(operation)

        
        return result



