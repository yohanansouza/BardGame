"""
Sistema de Moedas e Economia
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Currency:
    """Definição de uma moeda"""
    name: str
    abbreviation: str
    base_value: float  # Valor em relação à moeda base
    weight: float = 0.01  # kg por moeda
    description: str = ""


@dataclass
class ExchangeRate:
    """Taxa de câmbio entre moedas"""
    from_currency: str
    to_currency: str
    rate: float
    fee_percentage: float = 0.0  # Taxa de conversão


class CurrencySystem:
    """Gerenciador do sistema de moedas"""
    
    def __init__(self):
        self.currencies: Dict[str, Currency] = {}
        self.base_currency: Optional[str] = None
        self.exchange_rates: List[ExchangeRate] = []
        self._init_default_currencies()
    
    def _init_default_currencies(self):
        """Inicializa moedas padrão (baseado em D&D)"""
        default_currencies = [
            Currency("Copper", "cp", 1, 0.01, "Moeda de cobre"),
            Currency("Silver", "sp", 10, 0.01, "Moeda de prata"),
            Currency("Electrum", "ep", 50, 0.01, "Moeda de electrum"),
            Currency("Gold", "gp", 100, 0.01, "Moeda de ouro"),
            Currency("Platinum", "pp", 1000, 0.01, "Moeda de platina")
        ]
        
        for currency in default_currencies:
            self.add_currency(currency)
        
        self.base_currency = "Copper"
    
    def add_currency(self, currency: Currency):
        """Adiciona uma moeda ao sistema"""
        self.currencies[currency.name] = currency
    
    def set_base_currency(self, currency_name: str):
        """Define a moeda base do sistema"""
        if currency_name in self.currencies:
            self.base_currency = currency_name
    
    def add_exchange_rate(self, rate: ExchangeRate):
        """Adiciona uma taxa de câmbio"""
        self.exchange_rates.append(rate)
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> Dict:
        """Converte valores entre moedas"""
        if from_currency not in self.currencies or to_currency not in self.currencies:
            return {'success': False, 'error': 'Moeda não encontrada'}
        
        # Converter para moeda base
        from_curr = self.currencies[from_currency]
        to_curr = self.currencies[to_currency]
        
        base_value = amount * from_curr.base_value
        converted_amount = base_value / to_curr.base_value
        
        # Verificar se há taxa de câmbio específica
        fee = 0.0
        for rate in self.exchange_rates:
            if rate.from_currency == from_currency and rate.to_currency == to_currency:
                converted_amount = amount * rate.rate
                fee = converted_amount * (rate.fee_percentage / 100)
                break
        
        return {
            'success': True,
            'original_amount': amount,
            'original_currency': from_currency,
            'converted_amount': converted_amount - fee,
            'target_currency': to_currency,
            'fee': fee,
            'fee_percentage': rate.fee_percentage if 'rate' in locals() else 0
        }
    
    def calculate_weight(self, currency_amounts: Dict[str, float]) -> float:
        """Calcula peso total de moedas"""
        total_weight = 0.0
        for currency_name, amount in currency_amounts.items():
            if currency_name in self.currencies:
                total_weight += self.currencies[currency_name].weight * amount
        return total_weight
    
    def convert_to_base(self, currency_amounts: Dict[str, float]) -> float:
        """Converte todas moedas para valor base"""
        total = 0.0
        for currency_name, amount in currency_amounts.items():
            if currency_name in self.currencies:
                total += self.currencies[currency_name].base_value * amount
        return total
    
    def optimize_currency(self, base_value: float) -> Dict[str, int]:
        """Otimiza distribuição de moedas para menor quantidade"""
        # Ordenar moedas por valor (maior primeiro)
        sorted_currencies = sorted(
            self.currencies.items(),
            key=lambda x: x[1].base_value,
            reverse=True
        )
        
        result = {}
        remaining = base_value
        
        for name, currency in sorted_currencies:
            if remaining <= 0:
                break
            
            count = int(remaining // currency.base_value)
            if count > 0:
                result[name] = count
                remaining -= count * currency.base_value
        
        return result
    
    def to_json(self) -> str:
        """Exporta sistema para JSON"""
        data = {
            'base_currency': self.base_currency,
            'currencies': {
                name: {
                    'name': curr.name,
                    'abbreviation': curr.abbreviation,
                    'base_value': curr.base_value,
                    'weight': curr.weight,
                    'description': curr.description
                }
                for name, curr in self.currencies.items()
            },
            'exchange_rates': [
                {
                    'from_currency': rate.from_currency,
                    'to_currency': rate.to_currency,
                    'rate': rate.rate,
                    'fee_percentage': rate.fee_percentage
                }
                for rate in self.exchange_rates
            ]
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def save_to_file(self, filepath: str):
        """Salva sistema em arquivo JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    @classmethod
    def load_from_file(cls, filepath: str):
        """Carrega sistema de arquivo JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            system = cls()
            
            # Limpar moedas padrão se necessário
            system.currencies.clear()
            
            # Carregar moedas
            for name, curr_data in data.get('currencies', {}).items():
                currency = Currency(
                    name=curr_data['name'],
                    abbreviation=curr_data['abbreviation'],
                    base_value=curr_data['base_value'],
                    weight=curr_data.get('weight', 0.01),
                    description=curr_data.get('description', '')
                )
                system.add_currency(currency)
            
            # Definir moeda base
            if 'base_currency' in data:
                system.base_currency = data['base_currency']
            
            # Carregar taxas de câmbio
            for rate_data in data.get('exchange_rates', []):
                rate = ExchangeRate(
                    from_currency=rate_data['from_currency'],
                    to_currency=rate_data['to_currency'],
                    rate=rate_data['rate'],
                    fee_percentage=rate_data.get('fee_percentage', 0.0)
                )
                system.add_exchange_rate(rate)
            
            return system
