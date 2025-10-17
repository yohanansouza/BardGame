"""
Sistema de Talentos/Boons
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class TalentWeight(Enum):
    """Peso/Custo do talento"""
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class TalentType(Enum):
    """Tipo/Categoria do talento"""
    COMBAT = "combat"
    DISCOVERY = "discovery"
    RACIAL = "racial"
    MAGIC = "magic"
    SOCIAL = "social"
    CRAFT = "craft"
    SURVIVAL = "survival"


@dataclass
class TalentRequirement:
    """Requisitos para adquirir um talento"""
    min_level: int = 1
    required_attributes: Dict[str, int] = field(default_factory=dict)
    required_talents: List[str] = field(default_factory=list)
    required_race: Optional[str] = None
    required_class: Optional[str] = None


@dataclass
class TalentEffect:
    """Efeito de um talento"""
    attribute_bonuses: Dict[str, int] = field(default_factory=dict)
    skill_bonuses: Dict[str, int] = field(default_factory=dict)
    special_abilities: List[str] = field(default_factory=list)
    damage_bonus: int = 0
    ac_bonus: int = 0
    save_bonuses: Dict[str, int] = field(default_factory=dict)


@dataclass
class Talent:
    """Definição de um talento"""
    name: str
    talent_type: TalentType
    weight: TalentWeight
    description: str
    requirements: TalentRequirement = field(default_factory=TalentRequirement)
    effects: TalentEffect = field(default_factory=TalentEffect)
    max_stacks: int = 1  # Quantas vezes pode ser pego


@dataclass
class TalentBuildRules:
    """Regras para construção de talentos"""
    max_talents: int = 3
    max_points: int = 6  # Total de pontos de peso permitido
    allow_duplicates: bool = False
    type_restrictions: Dict[str, int] = field(default_factory=dict)  # {type: max_count}


class TalentSystem:
    """Gerenciador do sistema de talentos"""
    
    def __init__(self):
        self.talents: Dict[str, Talent] = {}
        self.build_rules = TalentBuildRules()
    
    def add_talent(self, talent: Talent):
        """Adiciona um talento ao sistema"""
        self.talents[talent.name] = talent
    
    def get_talent(self, name: str) -> Optional[Talent]:
        """Retorna um talento pelo nome"""
        return self.talents.get(name)
    
    def validate_talent_build(self, selected_talents: List[str]) -> Dict:
        """Valida se uma seleção de talentos é válida"""
        if len(selected_talents) > self.build_rules.max_talents:
            return {
                'valid': False,
                'error': f'Máximo de {self.build_rules.max_talents} talentos permitido'
            }
        
        total_weight = 0
        type_counts = {}
        
        for talent_name in selected_talents:
            talent = self.get_talent(talent_name)
            if not talent:
                return {'valid': False, 'error': f'Talento {talent_name} não encontrado'}
            
            total_weight += talent.weight.value
            
            talent_type = talent.talent_type.value
            type_counts[talent_type] = type_counts.get(talent_type, 0) + 1
        
        if total_weight > self.build_rules.max_points:
            return {
                'valid': False,
                'error': f'Total de pontos ({total_weight}) excede o máximo ({self.build_rules.max_points})'
            }
        
        # Verificar restrições por tipo
        for talent_type, count in type_counts.items():
            max_allowed = self.build_rules.type_restrictions.get(talent_type, float('inf'))
            if count > max_allowed:
                return {
                    'valid': False,
                    'error': f'Máximo de {max_allowed} talentos do tipo {talent_type} permitido'
                }
        
        return {'valid': True, 'total_weight': total_weight}
    
    def check_requirements(self, talent_name: str, character_data: Dict) -> bool:
        """Verifica se personagem atende requisitos de um talento"""
        talent = self.get_talent(talent_name)
        if not talent:
            return False
        
        req = talent.requirements
        
        # Verificar nível
        if character_data.get('level', 0) < req.min_level:
            return False
        
        # Verificar atributos
        char_attributes = character_data.get('attributes', {})
        for attr, min_value in req.required_attributes.items():
            if char_attributes.get(attr, 0) < min_value:
                return False
        
        # Verificar talentos prerequisitos
        char_talents = character_data.get('talents', [])
        for required_talent in req.required_talents:
            if required_talent not in char_talents:
                return False
        
        # Verificar raça
        if req.required_race and character_data.get('race') != req.required_race:
            return False
        
        # Verificar classe
        if req.required_class and character_data.get('class') != req.required_class:
            return False
        
        return True
    
    def get_talents_by_type(self, talent_type: TalentType) -> List[Talent]:
        """Retorna todos talentos de um tipo específico"""
        return [t for t in self.talents.values() if t.talent_type == talent_type]
    
    def calculate_total_effects(self, talent_names: List[str]) -> TalentEffect:
        """Calcula efeitos totais de múltiplos talentos"""
        total_effect = TalentEffect()
        
        for talent_name in talent_names:
            talent = self.get_talent(talent_name)
            if not talent:
                continue
            
            # Somar bônus de atributos
            for attr, bonus in talent.effects.attribute_bonuses.items():
                total_effect.attribute_bonuses[attr] = \
                    total_effect.attribute_bonuses.get(attr, 0) + bonus
            
            # Somar bônus de skills
            for skill, bonus in talent.effects.skill_bonuses.items():
                total_effect.skill_bonuses[skill] = \
                    total_effect.skill_bonuses.get(skill, 0) + bonus
            
            # Adicionar habilidades especiais
            total_effect.special_abilities.extend(talent.effects.special_abilities)
            
            # Somar outros bônus
            total_effect.damage_bonus += talent.effects.damage_bonus
            total_effect.ac_bonus += talent.effects.ac_bonus
            
            # Somar bônus de salvamento
            for save, bonus in talent.effects.save_bonuses.items():
                total_effect.save_bonuses[save] = \
                    total_effect.save_bonuses.get(save, 0) + bonus
        
        return total_effect
    
    def to_json(self) -> str:
        """Exporta sistema para JSON"""
        data = {
            'talents': {
                name: {
                    'name': talent.name,
                    'talent_type': talent.talent_type.value,
                    'weight': talent.weight.value,
                    'description': talent.description,
                    'requirements': {
                        'min_level': talent.requirements.min_level,
                        'required_attributes': talent.requirements.required_attributes,
                        'required_talents': talent.requirements.required_talents,
                        'required_race': talent.requirements.required_race,
                        'required_class': talent.requirements.required_class
                    },
                    'effects': {
                        'attribute_bonuses': talent.effects.attribute_bonuses,
                        'skill_bonuses': talent.effects.skill_bonuses,
                        'special_abilities': talent.effects.special_abilities,
                        'damage_bonus': talent.effects.damage_bonus,
                        'ac_bonus': talent.effects.ac_bonus,
                        'save_bonuses': talent.effects.save_bonuses
                    },
                    'max_stacks': talent.max_stacks
                }
                for name, talent in self.talents.items()
            },
            'build_rules': {
                'max_talents': self.build_rules.max_talents,
                'max_points': self.build_rules.max_points,
                'allow_duplicates': self.build_rules.allow_duplicates,
                'type_restrictions': self.build_rules.type_restrictions
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
            
            # Carregar regras de construção
            rules_data = data.get('build_rules', {})
            system.build_rules = TalentBuildRules(
                max_talents=rules_data.get('max_talents', 3),
                max_points=rules_data.get('max_points', 6),
                allow_duplicates=rules_data.get('allow_duplicates', False),
                type_restrictions=rules_data.get('type_restrictions', {})
            )
            
            # Carregar talentos
            for name, talent_data in data.get('talents', {}).items():
                requirements = TalentRequirement(
                    min_level=talent_data['requirements'].get('min_level', 1),
                    required_attributes=talent_data['requirements'].get('required_attributes', {}),
                    required_talents=talent_data['requirements'].get('required_talents', []),
                    required_race=talent_data['requirements'].get('required_race'),
                    required_class=talent_data['requirements'].get('required_class')
                )
                
                effects = TalentEffect(
                    attribute_bonuses=talent_data['effects'].get('attribute_bonuses', {}),
                    skill_bonuses=talent_data['effects'].get('skill_bonuses', {}),
                    special_abilities=talent_data['effects'].get('special_abilities', []),
                    damage_bonus=talent_data['effects'].get('damage_bonus', 0),
                    ac_bonus=talent_data['effects'].get('ac_bonus', 0),
                    save_bonuses=talent_data['effects'].get('save_bonuses', {})
                )
                
                talent = Talent(
                    name=talent_data['name'],
                    talent_type=TalentType(talent_data['talent_type']),
                    weight=TalentWeight(talent_data['weight']),
                    description=talent_data['description'],
                    requirements=requirements,
                    effects=effects,
                    max_stacks=talent_data.get('max_stacks', 1)
                )
                system.add_talent(talent)
            
            return system
