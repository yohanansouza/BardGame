"""
Sistema de Proficiências
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class ProficiencyType(Enum):
    """Tipos de proficiência"""
    WEAPON = "weapon"
    ARMOR = "armor"
    TOOL = "tool"
    SKILL = "skill"
    SAVING_THROW = "saving_throw"


@dataclass
class ProficiencyLevel:
    """Nível de proficiência"""
    name: str
    bonus: int
    damage_multiplier: float = 1.0
    ac_bonus: int = 0
    special_effects: List[str] = field(default_factory=list)


@dataclass
class Proficiency:
    """Definição de uma proficiência"""
    name: str
    proficiency_type: ProficiencyType
    levels: List[ProficiencyLevel] = field(default_factory=list)
    requirements: Dict = field(default_factory=dict)
    description: str = ""


class ProficiencySystem:
    """Gerenciador do sistema de proficiências"""
    
    def __init__(self):
        self.proficiencies: Dict[str, Proficiency] = {}
        self.proficiency_levels: List[ProficiencyLevel] = self._init_default_levels()
    
    def _init_default_levels(self) -> List[ProficiencyLevel]:
        """Inicializa níveis padrão de proficiência"""
        return [
            ProficiencyLevel(name="Novice", bonus=0, damage_multiplier=1.0),
            ProficiencyLevel(name="Apprentice", bonus=2, damage_multiplier=1.1),
            ProficiencyLevel(name="Journeyman", bonus=4, damage_multiplier=1.25),
            ProficiencyLevel(name="Expert", bonus=6, damage_multiplier=1.5),
            ProficiencyLevel(name="Master", bonus=8, damage_multiplier=2.0)
        ]
    
    def add_proficiency(self, proficiency: Proficiency):
        """Adiciona uma proficiência"""
        self.proficiencies[proficiency.name] = proficiency
    
    def get_proficiency(self, name: str) -> Optional[Proficiency]:
        """Retorna uma proficiência pelo nome"""
        return self.proficiencies.get(name)
    
    def get_bonus(self, proficiency_name: str, level: int) -> int:
        """Retorna o bônus de uma proficiência em determinado nível"""
        proficiency = self.get_proficiency(proficiency_name)
        if not proficiency or level >= len(proficiency.levels):
            return 0
        return proficiency.levels[level].bonus
    
    def calculate_proficiency_bonus(self, character_level: int) -> int:
        """Calcula bônus de proficiência baseado no nível do personagem"""
        return 2 + ((character_level - 1) // 4)
    
    def to_json(self) -> str:
        """Exporta sistema para JSON"""
        data = {
            'proficiencies': {
                name: {
                    'name': prof.name,
                    'proficiency_type': prof.proficiency_type.value,
                    'levels': [
                        {
                            'name': lvl.name,
                            'bonus': lvl.bonus,
                            'damage_multiplier': lvl.damage_multiplier,
                            'ac_bonus': lvl.ac_bonus,
                            'special_effects': lvl.special_effects
                        }
                        for lvl in prof.levels
                    ],
                    'requirements': prof.requirements,
                    'description': prof.description
                }
                for name, prof in self.proficiencies.items()
            },
            'default_levels': [
                {
                    'name': lvl.name,
                    'bonus': lvl.bonus,
                    'damage_multiplier': lvl.damage_multiplier,
                    'ac_bonus': lvl.ac_bonus,
                    'special_effects': lvl.special_effects
                }
                for lvl in self.proficiency_levels
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
            
            # Carregar níveis padrão
            if 'default_levels' in data:
                system.proficiency_levels = [
                    ProficiencyLevel(
                        name=lvl['name'],
                        bonus=lvl['bonus'],
                        damage_multiplier=lvl.get('damage_multiplier', 1.0),
                        ac_bonus=lvl.get('ac_bonus', 0),
                        special_effects=lvl.get('special_effects', [])
                    )
                    for lvl in data['default_levels']
                ]
            
            # Carregar proficiências
            for name, prof_data in data.get('proficiencies', {}).items():
                levels = [
                    ProficiencyLevel(
                        name=lvl['name'],
                        bonus=lvl['bonus'],
                        damage_multiplier=lvl.get('damage_multiplier', 1.0),
                        ac_bonus=lvl.get('ac_bonus', 0),
                        special_effects=lvl.get('special_effects', [])
                    )
                    for lvl in prof_data.get('levels', [])
                ]
                
                proficiency = Proficiency(
                    name=prof_data['name'],
                    proficiency_type=ProficiencyType(prof_data['proficiency_type']),
                    levels=levels,
                    requirements=prof_data.get('requirements', {}),
                    description=prof_data.get('description', '')
                )
                system.add_proficiency(proficiency)
            
            return system
