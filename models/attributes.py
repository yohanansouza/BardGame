"""
Sistema de Atributos - Primários e Secundários
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class AttributeRule:
    """Regras para um atributo específico"""
    name: str
    is_primary: bool
    is_mandatory: bool
    base_value: int = 0
    min_value: int = 0
    max_value: int = 100
    increase_rules: List[str] = field(default_factory=list)  # "level_up", "training", etc
    linked_secondaries: List[str] = field(default_factory=list)


@dataclass
class SecondaryAttribute:
    """Atributo secundário derivado de primários"""
    name: str
    formula: str  # Ex: "strength * 2 + dexterity"
    parent_attributes: List[str] = field(default_factory=list)
    class_modifiers: Dict[str, float] = field(default_factory=dict)


class AttributeSystem:
    """Gerenciador do sistema de atributos"""
    
    def __init__(self):
        self.primary_attributes: Dict[str, AttributeRule] = {}
        self.secondary_attributes: Dict[str, SecondaryAttribute] = {}
    
    def add_primary_attribute(self, attr: AttributeRule):
        """Adiciona um atributo primário"""
        self.primary_attributes[attr.name] = attr
    
    def add_secondary_attribute(self, attr: SecondaryAttribute):
        """Adiciona um atributo secundário"""
        self.secondary_attributes[attr.name] = attr
    
    def calculate_secondary(self, secondary_name: str, primary_values: Dict[str, int]) -> int:
        """Calcula o valor de um atributo secundário baseado nos primários"""
        if secondary_name not in self.secondary_attributes:
            return 0
        
        secondary = self.secondary_attributes[secondary_name]
        # Implementar parser de fórmula
        # TODO: Usar eval com segurança ou criar parser próprio
        return 0
    
    def validate_mandatory_attributes(self, attributes: Dict[str, int]) -> bool:
        """Valida se todos atributos obrigatórios estão presentes"""
        for name, attr in self.primary_attributes.items():
            if attr.is_mandatory and name not in attributes:
                return False
        return True
    
    def to_json(self) -> str:
        """Exporta sistema de atributos para JSON"""
        data = {
            'primary': {name: attr.__dict__ for name, attr in self.primary_attributes.items()},
            'secondary': {name: attr.__dict__ for name, attr in self.secondary_attributes.items()}
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    @classmethod
    def from_json(cls, json_str: str):
        """Importa sistema de atributos de JSON"""
        data = json.loads(json_str)
        system = cls()
        
        for name, attr_data in data.get('primary', {}).items():
            system.add_primary_attribute(AttributeRule(**attr_data))
        
        for name, attr_data in data.get('secondary', {}).items():
            system.add_secondary_attribute(SecondaryAttribute(**attr_data))
        
        return system
    
    def save_to_file(self, filepath: str):
        """Salva sistema em arquivo JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    @classmethod
    def load_from_file(cls, filepath: str):
        """Carrega sistema de arquivo JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return cls.from_json(f.read())
