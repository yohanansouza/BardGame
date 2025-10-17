"""
Sistema de Raças
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class SizeCategory(Enum):
    """Categorias de tamanho"""
    TINY = "tiny"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    HUGE = "huge"
    GARGANTUAN = "gargantuan"


@dataclass
class MovementRules:
    """Regras de movimentação"""
    base_speed: int = 30  # pés ou metros
    climb_speed: Optional[int] = None
    swim_speed: Optional[int] = None
    fly_speed: Optional[int] = None
    burrow_speed: Optional[int] = None


@dataclass
class Race:
    """Definição de uma raça"""
    name: str
    size: SizeCategory
    movement: MovementRules
    attribute_modifiers: Dict[str, int] = field(default_factory=dict)
    available_talents: List[str] = field(default_factory=list)
    racial_abilities: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    age_range: tuple = (0, 100)
    height_range: tuple = (150, 180)  # cm
    weight_range: tuple = (50, 90)  # kg
    special_rules: Dict = field(default_factory=dict)


class RaceSystem:
    """Gerenciador do sistema de raças"""
    
    def __init__(self):
        self.races: Dict[str, Race] = {}
        self.size_modifiers: Dict[SizeCategory, Dict] = self._init_size_modifiers()
    
    def _init_size_modifiers(self) -> Dict[SizeCategory, Dict]:
        """Inicializa modificadores padrão por tamanho"""
        return {
            SizeCategory.TINY: {"ac_bonus": 2, "stealth_bonus": 4, "strength_penalty": -4},
            SizeCategory.SMALL: {"ac_bonus": 1, "stealth_bonus": 2, "strength_penalty": -2},
            SizeCategory.MEDIUM: {"ac_bonus": 0, "stealth_bonus": 0, "strength_penalty": 0},
            SizeCategory.LARGE: {"ac_bonus": -1, "stealth_bonus": -2, "strength_bonus": 2},
            SizeCategory.HUGE: {"ac_bonus": -2, "stealth_bonus": -4, "strength_bonus": 4},
            SizeCategory.GARGANTUAN: {"ac_bonus": -4, "stealth_bonus": -8, "strength_bonus": 8}
        }
    
    def add_race(self, race: Race):
        """Adiciona uma raça ao sistema"""
        self.races[race.name] = race
    
    def get_race(self, name: str) -> Optional[Race]:
        """Retorna uma raça pelo nome"""
        return self.races.get(name)
    
    def get_size_modifiers(self, size: SizeCategory) -> Dict:
        """Retorna modificadores de tamanho"""
        return self.size_modifiers.get(size, {})
    
    def calculate_total_modifiers(self, race_name: str) -> Dict:
        """Calcula todos os modificadores de uma raça"""
        race = self.get_race(race_name)
        if not race:
            return {}
        
        modifiers = race.attribute_modifiers.copy()
        size_mods = self.get_size_modifiers(race.size)
        
        # Combinar modificadores
        for key, value in size_mods.items():
            if key in modifiers:
                modifiers[key] += value
            else:
                modifiers[key] = value
        
        return modifiers
    
    def to_json(self) -> str:
        """Exporta sistema de raças para JSON"""
        data = {
            'races': {
                name: {
                    'name': race.name,
                    'size': race.size.value,
                    'movement': {
                        'base_speed': race.movement.base_speed,
                        'climb_speed': race.movement.climb_speed,
                        'swim_speed': race.movement.swim_speed,
                        'fly_speed': race.movement.fly_speed,
                        'burrow_speed': race.movement.burrow_speed
                    },
                    'attribute_modifiers': race.attribute_modifiers,
                    'available_talents': race.available_talents,
                    'racial_abilities': race.racial_abilities,
                    'languages': race.languages,
                    'age_range': race.age_range,
                    'height_range': race.height_range,
                    'weight_range': race.weight_range,
                    'special_rules': race.special_rules
                }
                for name, race in self.races.items()
            },
            'size_modifiers': {
                size.value: mods for size, mods in self.size_modifiers.items()
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
            
            for name, race_data in data.get('races', {}).items():
                movement = MovementRules(
                    base_speed=race_data['movement']['base_speed'],
                    climb_speed=race_data['movement'].get('climb_speed'),
                    swim_speed=race_data['movement'].get('swim_speed'),
                    fly_speed=race_data['movement'].get('fly_speed'),
                    burrow_speed=race_data['movement'].get('burrow_speed')
                )
                
                race = Race(
                    name=race_data['name'],
                    size=SizeCategory(race_data['size']),
                    movement=movement,
                    attribute_modifiers=race_data.get('attribute_modifiers', {}),
                    available_talents=race_data.get('available_talents', []),
                    racial_abilities=race_data.get('racial_abilities', []),
                    languages=race_data.get('languages', []),
                    age_range=tuple(race_data.get('age_range', [0, 100])),
                    height_range=tuple(race_data.get('height_range', [150, 180])),
                    weight_range=tuple(race_data.get('weight_range', [50, 90])),
                    special_rules=race_data.get('special_rules', {})
                )
                system.add_race(race)
            
            if 'size_modifiers' in data:
                system.size_modifiers = {
                    SizeCategory(size): mods
                    for size, mods in data['size_modifiers'].items()
                }
            
            return system
