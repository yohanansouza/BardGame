"""
Sistema de Classe de Armadura (AC)
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class ArmorType(Enum):
    """Tipos de armadura"""
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"
    SHIELD = "shield"
    NATURAL = "natural"


class ACCalculationType(Enum):
    """Tipo de cálculo de AC"""
    BASE_PLUS_DEX = "base_plus_dex"  # AC base + modificador de Destreza
    BASE_PLUS_LIMITED_DEX = "base_plus_limited_dex"  # AC base + Dex (max +2)
    FLAT = "flat"  # AC fixo
    FORMULA = "formula"  # Fórmula customizada


@dataclass
class ArmorClass:
    """Definição de classe de armadura"""
    base_ac: int
    calculation_type: ACCalculationType = ACCalculationType.BASE_PLUS_DEX
    max_dex_bonus: Optional[int] = None
    attribute_bonuses: Dict[str, float] = field(default_factory=dict)  # {attr: multiplier}
    flat_bonuses: int = 0
    formula: str = ""  # Para cálculo customizado


@dataclass
class MagicalAC:
    """Classe de Armadura Mágica separada"""
    enabled: bool = False
    base_mac: int = 10
    primary_attribute: str = "intelligence"  # Atributo principal para MAC
    attribute_multiplier: float = 1.0
    additional_bonuses: int = 0


class ACSystem:
    """Gerenciador do sistema de Classe de Armadura"""
    
    def __init__(self):
        self.physical_ac_enabled: bool = True
        self.magical_ac_enabled: bool = False
        self.magical_ac = MagicalAC()
        self.armor_types: Dict[str, int] = self._init_armor_base_values()
    
    def _init_armor_base_values(self) -> Dict[str, int]:
        """Inicializa valores base de armaduras"""
        return {
            # Armaduras leves
            "padded": 11,
            "leather": 11,
            "studded_leather": 12,
            
            # Armaduras médias
            "hide": 12,
            "chain_shirt": 13,
            "scale_mail": 14,
            "breastplate": 14,
            "half_plate": 15,
            
            # Armaduras pesadas
            "ring_mail": 14,
            "chain_mail": 16,
            "splint": 17,
            "plate": 18,
            
            # Escudos
            "shield": 2,  # Bônus adicional
            
            # Natural
            "unarmored": 10
        }
    
    def calculate_physical_ac(
        self,
        armor_config: ArmorClass,
        attributes: Dict[str, int],
        additional_bonuses: int = 0
    ) -> int:
        """Calcula AC física"""
        ac = armor_config.base_ac
        
        if armor_config.calculation_type == ACCalculationType.FLAT:
            return ac + additional_bonuses
        
        # Adicionar modificador de destreza
        dex_modifier = self._calculate_modifier(attributes.get("dexterity", 10))
        
        if armor_config.calculation_type == ACCalculationType.BASE_PLUS_DEX:
            ac += dex_modifier
        elif armor_config.calculation_type == ACCalculationType.BASE_PLUS_LIMITED_DEX:
            max_dex = armor_config.max_dex_bonus or 2
            ac += min(dex_modifier, max_dex)
        
        # Adicionar bônus de outros atributos
        for attr, multiplier in armor_config.attribute_bonuses.items():
            attr_value = attributes.get(attr, 10)
            attr_modifier = self._calculate_modifier(attr_value)
            ac += int(attr_modifier * multiplier)
        
        # Adicionar bônus flat
        ac += armor_config.flat_bonuses
        ac += additional_bonuses
        
        return ac
    
    def calculate_magical_ac(
        self,
        attributes: Dict[str, int],
        additional_bonuses: int = 0
    ) -> int:
        """Calcula AC mágica"""
        if not self.magical_ac.enabled:
            return 0
        
        mac = self.magical_ac.base_mac
        
        # Adicionar modificador do atributo primário
        primary_attr = attributes.get(self.magical_ac.primary_attribute, 10)
        attr_modifier = self._calculate_modifier(primary_attr)
        mac += int(attr_modifier * self.magical_ac.attribute_multiplier)
        
        # Adicionar bônus adicionais
        mac += self.magical_ac.additional_bonuses
        mac += additional_bonuses
        
        return mac
    
    def _calculate_modifier(self, attribute_value: int) -> int:
        """Calcula modificador de atributo (D&D style)"""
        return (attribute_value - 10) // 2
    
    def create_armor_config(
        self,
        armor_name: str,
        armor_type: ArmorType,
        additional_modifiers: Dict = None
    ) -> ArmorClass:
        """Cria configuração de armadura"""
        base_ac = self.armor_types.get(armor_name, 10)
        
        config = ArmorClass(base_ac=base_ac)
        
        # Configurar baseado no tipo
        if armor_type == ArmorType.LIGHT:
            config.calculation_type = ACCalculationType.BASE_PLUS_DEX
        elif armor_type == ArmorType.MEDIUM:
            config.calculation_type = ACCalculationType.BASE_PLUS_LIMITED_DEX
            config.max_dex_bonus = 2
        elif armor_type == ArmorType.HEAVY:
            config.calculation_type = ACCalculationType.FLAT
        
        if additional_modifiers:
            config.flat_bonuses = additional_modifiers.get('flat_bonuses', 0)
            config.attribute_bonuses = additional_modifiers.get('attribute_bonuses', {})
        
        return config
    
    def to_json(self) -> str:
        """Exporta sistema para JSON"""
        data = {
            'physical_ac_enabled': self.physical_ac_enabled,
            'magical_ac_enabled': self.magical_ac_enabled,
            'magical_ac': {
                'enabled': self.magical_ac.enabled,
                'base_mac': self.magical_ac.base_mac,
                'primary_attribute': self.magical_ac.primary_attribute,
                'attribute_multiplier': self.magical_ac.attribute_multiplier,
                'additional_bonuses': self.magical_ac.additional_bonuses
            },
            'armor_types': self.armor_types
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
            
            system.physical_ac_enabled = data.get('physical_ac_enabled', True)
            system.magical_ac_enabled = data.get('magical_ac_enabled', False)
            
            mac_data = data.get('magical_ac', {})
            system.magical_ac = MagicalAC(
                enabled=mac_data.get('enabled', False),
                base_mac=mac_data.get('base_mac', 10),
                primary_attribute=mac_data.get('primary_attribute', 'intelligence'),
                attribute_multiplier=mac_data.get('attribute_multiplier', 1.0),
                additional_bonuses=mac_data.get('additional_bonuses', 0)
            )
            
            if 'armor_types' in data:
                system.armor_types = data['armor_types']
            
            return system
