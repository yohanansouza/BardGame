"""
Sistema de Status e Condições
"""
import json
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


class ConditionSeverity(Enum):
    """Severidade da condição"""
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


@dataclass
class StatusEffect:
    """Efeito de status aplicado"""
    attribute_modifiers: Dict[str, int] = field(default_factory=dict)
    movement_modifier: float = 1.0  # Multiplicador de movimento
    ac_modifier: int = 0
    attack_modifier: int = 0
    save_modifiers: Dict[str, int] = field(default_factory=dict)
    damage_over_time: int = 0
    heal_over_time: int = 0
    prevents_actions: Set[str] = field(default_factory=set)  # {"attack", "cast", "move"}
    grants_advantage: Set[str] = field(default_factory=set)
    grants_disadvantage: Set[str] = field(default_factory=set)


@dataclass
class Condition:
    """Definição de uma condição"""
    name: str
    severity: ConditionSeverity
    description: str
    effects: StatusEffect = field(default_factory=StatusEffect)
    duration_type: str = "rounds"  # "rounds", "minutes", "hours", "permanent", "until_condition"
    default_duration: int = 1
    can_stack: bool = False
    max_stacks: int = 1
    removable_by: List[str] = field(default_factory=list)  # ["rest", "magic", "antidote"]
    incompatible_with: List[str] = field(default_factory=list)  # Condições que se cancelam
    icon: str = ""


@dataclass
class StatusCondition:
    """Instância de uma condição aplicada a uma entidade"""
    condition_name: str
    remaining_duration: int
    stacks: int = 1
    source: str = ""  # Quem/o que aplicou a condição


class ConditionSystem:
    """Gerenciador do sistema de condições"""
    
    def __init__(self):
        self.conditions: Dict[str, Condition] = {}
        self._init_default_conditions()
    
    def _init_default_conditions(self):
        """Inicializa condições padrão (baseado em D&D 5e)"""
        default_conditions = [
            Condition(
                name="Blinded",
                severity=ConditionSeverity.MODERATE,
                description="Cego, não pode ver",
                effects=StatusEffect(
                    grants_disadvantage={"attack", "perception"},
                    ac_modifier=-2
                )
            ),
            Condition(
                name="Charmed",
                severity=ConditionSeverity.MINOR,
                description="Encantado, não pode atacar o encantador",
                effects=StatusEffect(
                    prevents_actions={"attack_charmer"}
                )
            ),
            Condition(
                name="Frightened",
                severity=ConditionSeverity.MINOR,
                description="Amedrontado",
                effects=StatusEffect(
                    grants_disadvantage={"attack", "ability_check"},
                    movement_modifier=0.5
                )
            ),
            Condition(
                name="Paralyzed",
                severity=ConditionSeverity.SEVERE,
                description="Paralisado, não pode se mover ou agir",
                effects=StatusEffect(
                    prevents_actions={"move", "attack", "cast"},
                    ac_modifier=-5
                )
            ),
            Condition(
                name="Poisoned",
                severity=ConditionSeverity.MODERATE,
                description="Envenenado",
                effects=StatusEffect(
                    grants_disadvantage={"attack", "ability_check"},
                    damage_over_time=5
                ),
                can_stack=True,
                max_stacks=5,
                removable_by=["antidote", "rest"]
            ),
            Condition(
                name="Stunned",
                severity=ConditionSeverity.SEVERE,
                description="Atordoado",
                effects=StatusEffect(
                    prevents_actions={"move", "attack"},
                    ac_modifier=-2
                )
            ),
            Condition(
                name="Unconscious",
                severity=ConditionSeverity.CRITICAL,
                description="Inconsciente",
                effects=StatusEffect(
                    prevents_actions={"move", "attack", "cast", "speak"},
                    ac_modifier=-5
                ),
                duration_type="until_condition"
            ),
            Condition(
                name="Bleeding",
                severity=ConditionSeverity.MODERATE,
                description="Sangrando",
                effects=StatusEffect(
                    damage_over_time=3
                ),
                can_stack=True,
                max_stacks=10,
                removable_by=["healing", "bandage"]
            ),
            Condition(
                name="Burning",
                severity=ConditionSeverity.MODERATE,
                description="Em chamas",
                effects=StatusEffect(
                    damage_over_time=5
                ),
                can_stack=True,
                max_stacks=5,
                removable_by=["water", "magic"]
            )
        ]
        
        for condition in default_conditions:
            self.add_condition(condition)
    
    def add_condition(self, condition: Condition):
        """Adiciona uma condição ao sistema"""
        self.conditions[condition.name] = condition
    
    def get_condition(self, name: str) -> Optional[Condition]:
        """Retorna uma condição pelo nome"""
        return self.conditions.get(name)
    
    def apply_condition(
        self,
        active_conditions: List[StatusCondition],
        condition_name: str,
        duration: Optional[int] = None,
        source: str = ""
    ) -> Dict:
        """Aplica uma condição a uma entidade"""
        condition = self.get_condition(condition_name)
        if not condition:
            return {'success': False, 'error': 'Condição não encontrada'}
        
        # Verificar incompatibilidades
        for active in active_conditions:
            if active.condition_name in condition.incompatible_with:
                # Remover condição incompatível
                active_conditions.remove(active)
        
        # Verificar se já existe e pode empilhar
        existing = None
        for active in active_conditions:
            if active.condition_name == condition_name:
                existing = active
                break
        
        if existing:
            if condition.can_stack and existing.stacks < condition.max_stacks:
                existing.stacks += 1
                return {'success': True, 'message': 'Condição empilhada', 'stacks': existing.stacks}
            else:
                # Renovar duração
                existing.remaining_duration = duration or condition.default_duration
                return {'success': True, 'message': 'Duração renovada'}
        
        # Adicionar nova condição
        new_condition = StatusCondition(
            condition_name=condition_name,
            remaining_duration=duration or condition.default_duration,
            stacks=1,
            source=source
        )
        active_conditions.append(new_condition)
        
        return {'success': True, 'message': 'Condição aplicada'}
    
    def remove_condition(
        self,
        active_conditions: List[StatusCondition],
        condition_name: str,
        remove_all_stacks: bool = False
    ) -> bool:
        """Remove uma condição"""
        for i, active in enumerate(active_conditions):
            if active.condition_name == condition_name:
                if remove_all_stacks or active.stacks <= 1:
                    active_conditions.pop(i)
                else:
                    active.stacks -= 1
                return True
        return False
    
    def update_conditions(self, active_conditions: List[StatusCondition]) -> List[Dict]:
        """Atualiza duração das condições e retorna efeitos"""
        effects = []
        to_remove = []
        
        for i, active in enumerate(active_conditions):
            condition = self.get_condition(active.condition_name)
            if not condition:
                continue
            
            # Aplicar efeitos
            if condition.effects.damage_over_time > 0:
                effects.append({
                    'type': 'damage',
                    'amount': condition.effects.damage_over_time * active.stacks,
                    'source': active.condition_name
                })
            
            if condition.effects.heal_over_time > 0:
                effects.append({
                    'type': 'heal',
                    'amount': condition.effects.heal_over_time * active.stacks,
                    'source': active.condition_name
                })
            
            # Decrementar duração
            if condition.duration_type in ["rounds", "minutes", "hours"]:
                active.remaining_duration -= 1
                if active.remaining_duration <= 0:
                    to_remove.append(i)
        
        # Remover condições expiradas
        for i in reversed(to_remove):
            active_conditions.pop(i)
        
        return effects
    
    def calculate_total_effects(self, active_conditions: List[StatusCondition]) -> StatusEffect:
        """Calcula efeitos totais de todas condições ativas"""
        total = StatusEffect()
        
        for active in active_conditions:
            condition = self.get_condition(active.condition_name)
            if not condition:
                continue
            
            effects = condition.effects
            
            # Somar modificadores de atributos
            for attr, mod in effects.attribute_modifiers.items():
                total.attribute_modifiers[attr] = \
                    total.attribute_modifiers.get(attr, 0) + (mod * active.stacks)
            
            # Multiplicar movimento (usar menor)
            total.movement_modifier = min(total.movement_modifier, effects.movement_modifier)
            
            # Somar modificadores
            total.ac_modifier += effects.ac_modifier * active.stacks
            total.attack_modifier += effects.attack_modifier * active.stacks
            
            # Somar DoT/HoT
            total.damage_over_time += effects.damage_over_time * active.stacks
            total.heal_over_time += effects.heal_over_time * active.stacks
            
            # Unir sets
            total.prevents_actions.update(effects.prevents_actions)
            total.grants_advantage.update(effects.grants_advantage)
            total.grants_disadvantage.update(effects.grants_disadvantage)
        
        return total
    
    def to_json(self) -> str:
        """Exporta sistema para JSON"""
        data = {
            'conditions': {
                name: {
                    'name': cond.name,
                    'severity': cond.severity.value,
                    'description': cond.description,
                    'effects': {
                        'attribute_modifiers': cond.effects.attribute_modifiers,
                        'movement_modifier': cond.effects.movement_modifier,
                        'ac_modifier': cond.effects.ac_modifier,
                        'attack_modifier': cond.effects.attack_modifier,
                        'save_modifiers': cond.effects.save_modifiers,
                        'damage_over_time': cond.effects.damage_over_time,
                        'heal_over_time': cond.effects.heal_over_time,
                        'prevents_actions': list(cond.effects.prevents_actions),
                        'grants_advantage': list(cond.effects.grants_advantage),
                        'grants_disadvantage': list(cond.effects.grants_disadvantage)
                    },
                    'duration_type': cond.duration_type,
                    'default_duration': cond.default_duration,
                    'can_stack': cond.can_stack,
                    'max_stacks': cond.max_stacks,
                    'removable_by': cond.removable_by,
                    'incompatible_with': cond.incompatible_with,
                    'icon': cond.icon
                }
                for name, cond in self.conditions.items()
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
            
            system.conditions.clear()
            
            for name, cond_data in data.get('conditions', {}).items():
                effects = StatusEffect(
                    attribute_modifiers=cond_data['effects'].get('attribute_modifiers', {}),
                    movement_modifier=cond_data['effects'].get('movement_modifier', 1.0),
                    ac_modifier=cond_data['effects'].get('ac_modifier', 0),
                    attack_modifier=cond_data['effects'].get('attack_modifier', 0),
                    save_modifiers=cond_data['effects'].get('save_modifiers', {}),
                    damage_over_time=cond_data['effects'].get('damage_over_time', 0),
                    heal_over_time=cond_data['effects'].get('heal_over_time', 0),
                    prevents_actions=set(cond_data['effects'].get('prevents_actions', [])),
                    grants_advantage=set(cond_data['effects'].get('grants_advantage', [])),
                    grants_disadvantage=set(cond_data['effects'].get('grants_disadvantage', []))
                )
                
                condition = Condition(
                    name=cond_data['name'],
                    severity=ConditionSeverity(cond_data['severity']),
                    description=cond_data['description'],
                    effects=effects,
                    duration_type=cond_data.get('duration_type', 'rounds'),
                    default_duration=cond_data.get('default_duration', 1),
                    can_stack=cond_data.get('can_stack', False),
                    max_stacks=cond_data.get('max_stacks', 1),
                    removable_by=cond_data.get('removable_by', []),
                    incompatible_with=cond_data.get('incompatible_with', []),
                    icon=cond_data.get('icon', '')
                )
                system.add_condition(condition)
            
            return system
