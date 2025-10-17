"""
Sistema de Magia/Spell Slots/Stamina
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class CasterType(Enum):
    """Tipos de conjuradores"""
    FULL_CASTER = "full_caster"
    HALF_CASTER = "half_caster"
    THIRD_CASTER = "third_caster"
    MANA_BASED = "mana_based"
    STAMINA_BASED = "stamina_based"
    CUSTOM = "custom"


class ManaScaling(Enum):
    """Tipos de escalamento de mana"""
    LEVEL_BASED = "level_based"
    ATTRIBUTE_BASED = "attribute_based"
    HYBRID = "hybrid"
    MANUAL = "manual"


@dataclass
class SpellSlotTable:
    """Tabela de slots de magia por nível"""
    name: str
    caster_type: CasterType
    slots_by_level: Dict[int, Dict[int, int]] = field(default_factory=dict)  # {char_level: {spell_level: slots}}


@dataclass
class ManaSystem:
    """Sistema baseado em mana"""
    enabled: bool = False
    scaling: ManaScaling = ManaScaling.LEVEL_BASED
    base_mana: int = 100
    mana_per_level: int = 10
    primary_attribute: Optional[str] = None  # Para attribute_based
    attribute_multiplier: float = 5.0
    regeneration_rate: int = 10  # Mana por descanso curto


@dataclass
class StaminaSystem:
    """Sistema baseado em stamina"""
    enabled: bool = False
    base_stamina: int = 100
    stamina_per_level: int = 5
    stamina_per_attribute: Dict[str, float] = field(default_factory=dict)  # {attr_name: multiplier}
    regeneration_rate: int = 20


@dataclass
class AlternativeResource:
    """Recursos alternativos (Ki, Aura, etc)"""
    name: str
    max_value: int
    scaling_attribute: Optional[str] = None
    regeneration_rules: Dict = field(default_factory=dict)


class MagicSystem:
    """Gerenciador do sistema de magia"""
    
    def __init__(self):
        self.spell_slot_tables: Dict[str, SpellSlotTable] = {}
        self.mana_system = ManaSystem()
        self.stamina_system = StaminaSystem()
        self.alternative_resources: Dict[str, AlternativeResource] = {}
        self._init_default_tables()
    
    def _init_default_tables(self):
        """Inicializa tabelas padrão de spell slots"""
        # Full Caster (baseado em D&D 5e)
        full_caster = SpellSlotTable(
            name="Full Caster",
            caster_type=CasterType.FULL_CASTER
        )
        
        full_caster.slots_by_level = {
            1: {1: 2},
            2: {1: 3},
            3: {1: 4, 2: 2},
            4: {1: 4, 2: 3},
            5: {1: 4, 2: 3, 3: 2},
            6: {1: 4, 2: 3, 3: 3},
            7: {1: 4, 2: 3, 3: 3, 4: 1},
            8: {1: 4, 2: 3, 3: 3, 4: 2},
            9: {1: 4, 2: 3, 3: 3, 4: 3, 5: 1},
            10: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2},
            11: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1},
            12: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1},
            13: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1},
            14: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1},
            15: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1},
            16: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1},
            17: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1, 9: 1},
            18: {1: 4, 2: 3, 3: 3, 4: 3, 5: 3, 6: 1, 7: 1, 8: 1, 9: 1},
            19: {1: 4, 2: 3, 3: 3, 4: 3, 5: 3, 6: 2, 7: 1, 8: 1, 9: 1},
            20: {1: 4, 2: 3, 3: 3, 4: 3, 5: 3, 6: 2, 7: 2, 8: 1, 9: 1}
        }
        
        self.add_spell_slot_table(full_caster)
        
        # Half Caster
        half_caster = SpellSlotTable(
            name="Half Caster",
            caster_type=CasterType.HALF_CASTER
        )
        
        half_caster.slots_by_level = {
            2: {1: 2},
            3: {1: 3},
            5: {1: 4, 2: 2},
            7: {1: 4, 2: 3},
            9: {1: 4, 2: 3, 3: 2},
            11: {1: 4, 2: 3, 3: 3},
            13: {1: 4, 2: 3, 3: 3, 4: 1},
            15: {1: 4, 2: 3, 3: 3, 4: 2},
            17: {1: 4, 2: 3, 3: 3, 4: 3, 5: 1},
            19: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2}
        }
        
        self.add_spell_slot_table(half_caster)
    
    def add_spell_slot_table(self, table: SpellSlotTable):
        """Adiciona uma tabela de spell slots"""
        self.spell_slot_tables[table.name] = table
    
    def get_spell_slots(self, table_name: str, character_level: int) -> Dict[int, int]:
        """Retorna os spell slots disponíveis para um nível"""
        table = self.spell_slot_tables.get(table_name)
        if not table:
            return {}
        return table.slots_by_level.get(character_level, {})
    
    def calculate_mana(self, level: int, attributes: Dict[str, int] = None) -> int:
        """Calcula total de mana"""
        if not self.mana_system.enabled:
            return 0
        
        mana = self.mana_system.base_mana
        
        if self.mana_system.scaling == ManaScaling.LEVEL_BASED:
            mana += level * self.mana_system.mana_per_level
        
        elif self.mana_system.scaling == ManaScaling.ATTRIBUTE_BASED:
            if attributes and self.mana_system.primary_attribute:
                attr_value = attributes.get(self.mana_system.primary_attribute, 0)
                mana = int(attr_value * self.mana_system.attribute_multiplier)
        
        elif self.mana_system.scaling == ManaScaling.HYBRID:
            mana += level * self.mana_system.mana_per_level
            if attributes and self.mana_system.primary_attribute:
                attr_value = attributes.get(self.mana_system.primary_attribute, 0)
                mana += int(attr_value * self.mana_system.attribute_multiplier)
        
        return mana
    
    def calculate_stamina(self, level: int, attributes: Dict[str, int] = None) -> int:
        """Calcula total de stamina"""
        if not self.stamina_system.enabled:
            return 0
        
        stamina = self.stamina_system.base_stamina + (level * self.stamina_system.stamina_per_level)
        
        if attributes:
            for attr_name, multiplier in self.stamina_system.stamina_per_attribute.items():
                attr_value = attributes.get(attr_name, 0)
                stamina += int(attr_value * multiplier)
        
        return stamina
    
    def add_alternative_resource(self, resource: AlternativeResource):
        """Adiciona recurso alternativo (Ki, Aura, etc)"""
        self.alternative_resources[resource.name] = resource
    
    def to_json(self) -> str:
        """Exporta sistema para JSON"""
        data = {
            'spell_slot_tables': {
                name: {
                    'name': table.name,
                    'caster_type': table.caster_type.value,
                    'slots_by_level': {
                        str(lvl): slots for lvl, slots in table.slots_by_level.items()
                    }
                }
                for name, table in self.spell_slot_tables.items()
            },
            'mana_system': {
                'enabled': self.mana_system.enabled,
                'scaling': self.mana_system.scaling.value,
                'base_mana': self.mana_system.base_mana,
                'mana_per_level': self.mana_system.mana_per_level,
                'primary_attribute': self.mana_system.primary_attribute,
                'attribute_multiplier': self.mana_system.attribute_multiplier,
                'regeneration_rate': self.mana_system.regeneration_rate
            },
            'stamina_system': {
                'enabled': self.stamina_system.enabled,
                'base_stamina': self.stamina_system.base_stamina,
                'stamina_per_level': self.stamina_system.stamina_per_level,
                'stamina_per_attribute': self.stamina_system.stamina_per_attribute,
                'regeneration_rate': self.stamina_system.regeneration_rate
            },
            'alternative_resources': {
                name: {
                    'name': res.name,
                    'max_value': res.max_value,
                    'scaling_attribute': res.scaling_attribute,
                    'regeneration_rules': res.regeneration_rules
                }
                for name, res in self.alternative_resources.items()
            }
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
            
            # Limpar tabelas padrão se necessário
            system.spell_slot_tables.clear()
            
            # Carregar tabelas de spell slots
            for name, table_data in data.get('spell_slot_tables', {}).items():
                table = SpellSlotTable(
                    name=table_data['name'],
                    caster_type=CasterType(table_data['caster_type']),
                    slots_by_level={
                        int(lvl): slots for lvl, slots in table_data['slots_by_level'].items()
                    }
                )
                system.add_spell_slot_table(table)
            
            # Carregar sistema de mana
            mana_data = data.get('mana_system', {})
            system.mana_system = ManaSystem(
                enabled=mana_data.get('enabled', False),
                scaling=ManaScaling(mana_data.get('scaling', 'level_based')),
                base_mana=mana_data.get('base_mana', 100),
                mana_per_level=mana_data.get('mana_per_level', 10),
                primary_attribute=mana_data.get('primary_attribute'),
                attribute_multiplier=mana_data.get('attribute_multiplier', 5.0),
                regeneration_rate=mana_data.get('regeneration_rate', 10)
            )
            
            # Carregar sistema de stamina
            stamina_data = data.get('stamina_system', {})
            system.stamina_system = StaminaSystem(
                enabled=stamina_data.get('enabled', False),
                base_stamina=stamina_data.get('base_stamina', 100),
                stamina_per_level=stamina_data.get('stamina_per_level', 5),
                stamina_per_attribute=stamina_data.get('stamina_per_attribute', {}),
                regeneration_rate=stamina_data.get('regeneration_rate', 20)
            )
            
            # Carregar recursos alternativos
            for name, res_data in data.get('alternative_resources', {}).items():
                resource = AlternativeResource(
                    name=res_data['name'],
                    max_value=res_data['max_value'],
                    scaling_attribute=res_data.get('scaling_attribute'),
                    regeneration_rules=res_data.get('regeneration_rules', {})
                )
                system.add_alternative_resource(resource)
            
            return system
