"""
Sistema de Equipamentos
"""
import json
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


class EquipmentTag(Enum):
    """Tags de equipamento"""
    EQUIPPABLE = "equippable"
    CONSUMABLE = "consumable"
    QUEST_ITEM = "quest_item"
    CRAFTING_MATERIAL = "crafting_material"
    MAGICAL = "magical"
    CURSED = "cursed"
    UNIQUE = "unique"
    TRADEABLE = "tradeable"


class EquipmentSlot(Enum):
    """Slots de equipamento"""
    HEAD = "head"
    NECK = "neck"
    SHOULDERS = "shoulders"
    CHEST = "chest"
    BACK = "back"
    WRIST = "wrist"
    HANDS = "hands"
    WAIST = "waist"
    LEGS = "legs"
    FEET = "feet"
    RING_1 = "ring_1"
    RING_2 = "ring_2"
    MAIN_HAND = "main_hand"
    OFF_HAND = "off_hand"
    TWO_HAND = "two_hand"


class DamageType(Enum):
    """Tipos de dano"""
    SLASHING = "slashing"
    PIERCING = "piercing"
    BLUDGEONING = "bludgeoning"
    FIRE = "fire"
    COLD = "cold"
    LIGHTNING = "lightning"
    POISON = "poison"
    ACID = "acid"
    PSYCHIC = "psychic"
    RADIANT = "radiant"
    NECROTIC = "necrotic"


@dataclass
class ItemRequirements:
    """Requisitos para usar um item"""
    min_level: int = 1
    required_attributes: Dict[str, int] = field(default_factory=dict)
    required_proficiencies: List[str] = field(default_factory=list)
    required_race: Optional[str] = None
    required_class: Optional[str] = None


@dataclass
class WeaponStats:
    """Estatísticas de arma"""
    damage_dice: str  # "1d8", "2d6", etc
    damage_type: DamageType
    attack_bonus: int = 0
    critical_range: int = 20
    critical_multiplier: float = 2.0
    range: Optional[int] = None  # Para armas à distância
    properties: List[str] = field(default_factory=list)  # "finesse", "versatile", etc


@dataclass
class ArmorStats:
    """Estatísticas de armadura"""
    ac_bonus: int
    max_dex_bonus: Optional[int] = None
    armor_type: str = "light"
    magical_ac_bonus: int = 0
    stealth_disadvantage: bool = False


@dataclass
class Equipment:
    """Definição de um equipamento"""
    name: str
    description: str
    tags: Set[EquipmentTag] = field(default_factory=set)
    slot: Optional[EquipmentSlot] = None
    weight: float = 0.0
    value: int = 0  # Em moeda base
    max_stack: int = 1
    rarity: str = "common"  # common, uncommon, rare, epic, legendary
    
    # Estatísticas
    weapon_stats: Optional[WeaponStats] = None
    armor_stats: Optional[ArmorStats] = None
    
    # Modificadores
    attribute_modifiers: Dict[str, int] = field(default_factory=dict)
    skill_modifiers: Dict[str, int] = field(default_factory=dict)
    
    # Efeitos especiais
    on_equip_effects: List[str] = field(default_factory=list)
    on_use_effects: List[str] = field(default_factory=list)
    charges: Optional[int] = None
    
    # Requisitos
    requirements: ItemRequirements = field(default_factory=ItemRequirements)
    
    # Visual
    icon: str = ""
    model: str = ""


class EquipmentSystem:
    """Gerenciador do sistema de equipamentos"""
    
    def __init__(self):
        self.equipment_database: Dict[str, Equipment] = {}
        self.rarity_colors: Dict[str, str] = {
            "common": "#FFFFFF",
            "uncommon": "#00FF00",
            "rare": "#0000FF",
            "epic": "#A335EE",
            "legendary": "#FF8000"
        }
    
    def add_equipment(self, equipment: Equipment):
        """Adiciona equipamento ao banco de dados"""
        self.equipment_database[equipment.name] = equipment
    
    def get_equipment(self, name: str) -> Optional[Equipment]:
        """Retorna equipamento pelo nome"""
        return self.equipment_database.get(name)
    
    def create_weapon(
        self,
        name: str,
        damage_dice: str,
        damage_type: DamageType,
        **kwargs
    ) -> Equipment:
        """Cria uma arma"""
        weapon_stats = WeaponStats(
            damage_dice=damage_dice,
            damage_type=damage_type,
            attack_bonus=kwargs.get('attack_bonus', 0),
            critical_range=kwargs.get('critical_range', 20),
            critical_multiplier=kwargs.get('critical_multiplier', 2.0),
            range=kwargs.get('range'),
            properties=kwargs.get('properties', [])
        )
        
        equipment = Equipment(
            name=name,
            description=kwargs.get('description', ''),
            tags={EquipmentTag.EQUIPPABLE},
            slot=EquipmentSlot.MAIN_HAND,
            weapon_stats=weapon_stats,
            weight=kwargs.get('weight', 1.0),
            value=kwargs.get('value', 10),
            rarity=kwargs.get('rarity', 'common')
        )
        
        self.add_equipment(equipment)
        return equipment
    
    def create_armor(
        self,
        name: str,
        ac_bonus: int,
        armor_type: str,
        **kwargs
    ) -> Equipment:
        """Cria uma armadura"""
        armor_stats = ArmorStats(
            ac_bonus=ac_bonus,
            armor_type=armor_type,
            max_dex_bonus=kwargs.get('max_dex_bonus'),
            magical_ac_bonus=kwargs.get('magical_ac_bonus', 0),
            stealth_disadvantage=kwargs.get('stealth_disadvantage', False)
        )
        
        equipment = Equipment(
            name=name,
            description=kwargs.get('description', ''),
            tags={EquipmentTag.EQUIPPABLE},
            slot=kwargs.get('slot', EquipmentSlot.CHEST),
            armor_stats=armor_stats,
            weight=kwargs.get('weight', 5.0),
            value=kwargs.get('value', 50),
            rarity=kwargs.get('rarity', 'common')
        )
        
        self.add_equipment(equipment)
        return equipment
    
    def create_consumable(
        self,
        name: str,
        effects: List[str],
        **kwargs
    ) -> Equipment:
        """Cria um consumível"""
        equipment = Equipment(
            name=name,
            description=kwargs.get('description', ''),
            tags={EquipmentTag.CONSUMABLE},
            on_use_effects=effects,
            max_stack=kwargs.get('max_stack', 99),
            weight=kwargs.get('weight', 0.1),
            value=kwargs.get('value', 5),
            rarity=kwargs.get('rarity', 'common')
        )
        
        self.add_equipment(equipment)
        return equipment
    
    def check_requirements(
        self,
        equipment_name: str,
        character_data: Dict
    ) -> Dict:
        """Verifica se personagem atende requisitos do equipamento"""
        equipment = self.get_equipment(equipment_name)
        if not equipment:
            return {'can_equip': False, 'reason': 'Equipamento não encontrado'}
        
        req = equipment.requirements
        
        # Verificar nível
        if character_data.get('level', 0) < req.min_level:
            return {
                'can_equip': False,
                'reason': f'Nível mínimo: {req.min_level}'
            }
        
        # Verificar atributos
        char_attributes = character_data.get('attributes', {})
        for attr, min_value in req.required_attributes.items():
            if char_attributes.get(attr, 0) < min_value:
                return {
                    'can_equip': False,
                    'reason': f'{attr} mínimo: {min_value}'
                }
        
        # Verificar proficiências
        char_proficiencies = character_data.get('proficiencies', [])
        for prof in req.required_proficiencies:
            if prof not in char_proficiencies:
                return {
                    'can_equip': False,
                    'reason': f'Proficiência necessária: {prof}'
                }
        
        # Verificar raça
        if req.required_race and character_data.get('race') != req.required_race:
            return {
                'can_equip': False,
                'reason': f'Apenas {req.required_race} podem usar'
            }
        
        # Verificar classe
        if req.required_class and character_data.get('class') != req.required_class:
            return {
                'can_equip': False,
                'reason': f'Apenas {req.required_class} podem usar'
            }
        
        return {'can_equip': True}
    
    def get_items_by_tag(self, tag: EquipmentTag) -> List[Equipment]:
        """Retorna todos itens com uma tag específica"""
        return [
            item for item in self.equipment_database.values()
            if tag in item.tags
        ]
    
    def get_items_by_rarity(self, rarity: str) -> List[Equipment]:
        """Retorna todos itens de uma raridade"""
        return [
            item for item in self.equipment_database.values()
            if item.rarity == rarity
        ]
    
    def to_json(self) -> str:
        """Exporta sistema para JSON"""
        data = {
            'equipment': {
                name: {
                    'name': eq.name,
                    'description': eq.description,
                    'tags': [tag.value for tag in eq.tags],
                    'slot': eq.slot.value if eq.slot else None,
                    'weight': eq.weight,
                    'value': eq.value,
                    'max_stack': eq.max_stack,
                    'rarity': eq.rarity,
                    'weapon_stats': {
                        'damage_dice': eq.weapon_stats.damage_dice,
                        'damage_type': eq.weapon_stats.damage_type.value,
                        'attack_bonus': eq.weapon_stats.attack_bonus,
                        'critical_range': eq.weapon_stats.critical_range,
                        'critical_multiplier': eq.weapon_stats.critical_multiplier,
                        'range': eq.weapon_stats.range,
                        'properties': eq.weapon_stats.properties
                    } if eq.weapon_stats else None,
                    'armor_stats': {
                        'ac_bonus': eq.armor_stats.ac_bonus,
                        'max_dex_bonus': eq.armor_stats.max_dex_bonus,
                        'armor_type': eq.armor_stats.armor_type,
                        'magical_ac_bonus': eq.armor_stats.magical_ac_bonus,
                        'stealth_disadvantage': eq.armor_stats.stealth_disadvantage
                    } if eq.armor_stats else None,
                    'attribute_modifiers': eq.attribute_modifiers,
                    'skill_modifiers': eq.skill_modifiers,
                    'on_equip_effects': eq.on_equip_effects,
                    'on_use_effects': eq.on_use_effects,
                    'charges': eq.charges,
                    'requirements': {
                        'min_level': eq.requirements.min_level,
                        'required_attributes': eq.requirements.required_attributes,
                        'required_proficiencies': eq.requirements.required_proficiencies,
                        'required_race': eq.requirements.required_race,
                        'required_class': eq.requirements.required_class
                    },
                    'icon': eq.icon,
                    'model': eq.model
                }
                for name, eq in self.equipment_database.items()
            },
            'rarity_colors': self.rarity_colors
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
            
            if 'rarity_colors' in data:
                system.rarity_colors = data['rarity_colors']
            
            for name, eq_data in data.get('equipment', {}).items():
                # Carregar weapon_stats se existir
                weapon_stats = None
                if eq_data.get('weapon_stats'):
                    ws = eq_data['weapon_stats']
                    weapon_stats = WeaponStats(
                        damage_dice=ws['damage_dice'],
                        damage_type=DamageType(ws['damage_type']),
                        attack_bonus=ws.get('attack_bonus', 0),
                        critical_range=ws.get('critical_range', 20),
                        critical_multiplier=ws.get('critical_multiplier', 2.0),
                        range=ws.get('range'),
                        properties=ws.get('properties', [])
                    )
                
                # Carregar armor_stats se existir
                armor_stats = None
                if eq_data.get('armor_stats'):
                    ars = eq_data['armor_stats']
                    armor_stats = ArmorStats(
                        ac_bonus=ars['ac_bonus'],
                        max_dex_bonus=ars.get('max_dex_bonus'),
                        armor_type=ars.get('armor_type', 'light'),
                        magical_ac_bonus=ars.get('magical_ac_bonus', 0),
                        stealth_disadvantage=ars.get('stealth_disadvantage', False)
                    )
                
                # Carregar requirements
                req_data = eq_data.get('requirements', {})
                requirements = ItemRequirements(
                    min_level=req_data.get('min_level', 1),
                    required_attributes=req_data.get('required_attributes', {}),
                    required_proficiencies=req_data.get('required_proficiencies', []),
                    required_race=req_data.get('required_race'),
                    required_class=req_data.get('required_class')
                )
                
                equipment = Equipment(
                    name=eq_data['name'],
                    description=eq_data['description'],
                    tags={EquipmentTag(tag) for tag in eq_data.get('tags', [])},
                    slot=EquipmentSlot(eq_data['slot']) if eq_data.get('slot') else None,
                    weight=eq_data.get('weight', 0.0),
                    value=eq_data.get('value', 0),
                    max_stack=eq_data.get('max_stack', 1),
                    rarity=eq_data.get('rarity', 'common'),
                    weapon_stats=weapon_stats,
                    armor_stats=armor_stats,
                    attribute_modifiers=eq_data.get('attribute_modifiers', {}),
                    skill_modifiers=eq_data.get('skill_modifiers', {}),
                    on_equip_effects=eq_data.get('on_equip_effects', []),
                    on_use_effects=eq_data.get('on_use_effects', []),
                    charges=eq_data.get('charges'),
                    requirements=requirements,
                    icon=eq_data.get('icon', ''),
                    model=eq_data.get('model', '')
                )
                system.add_equipment(equipment)
            
            return system
