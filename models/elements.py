"""
Sistema de Elementos
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class ElementType(Enum):
    """Tipos de elementos"""
    FIRE = "fire"
    WATER = "water"
    EARTH = "earth"
    AIR = "air"
    LIGHTNING = "lightning"
    ICE = "ice"
    POISON = "poison"
    HOLY = "holy"
    DARK = "dark"
    PSYCHIC = "psychic"


class ResistanceLevel(Enum):
    """Níveis de resistência"""
    VULNERABLE = -1  # Recebe dobro de dano
    NORMAL = 0
    RESISTANT = 1  # Recebe metade do dano
    IMMUNE = 2  # Não recebe dano


@dataclass
class ElementInteraction:
    """Interação entre elementos"""
    attacking_element: ElementType
    defending_element: ElementType
    damage_multiplier: float = 1.0
    additional_effects: List[str] = field(default_factory=list)


@dataclass
class ElementalResistance:
    """Resistência elemental de uma entidade"""
    element: ElementType
    resistance_level: ResistanceLevel
    percentage: float = 0.0  # -100 a 200 (vulnerável a imune+)


class ElementSystem:
    """Gerenciador do sistema de elementos"""
    
    def __init__(self):
        self.elements: Dict[str, ElementType] = {e.value: e for e in ElementType}
        self.interactions: List[ElementInteraction] = []
        self.max_resistance_player: float = 75.0  # % máxima para players
        self.max_resistance_monster: float = 100.0  # % máxima para monstros
        self.allow_immunity_player: bool = False
        self.allow_immunity_monster: bool = True
        self._init_default_interactions()
    
    def _init_default_interactions(self):
        """Inicializa interações padrão entre elementos"""
        default_interactions = [
            # Fogo
            ElementInteraction(ElementType.FIRE, ElementType.ICE, 1.5, ["melt"]),
            ElementInteraction(ElementType.FIRE, ElementType.WATER, 0.5, []),
            ElementInteraction(ElementType.FIRE, ElementType.EARTH, 1.0, []),
            
            # Água
            ElementInteraction(ElementType.WATER, ElementType.FIRE, 1.5, ["extinguish"]),
            ElementInteraction(ElementType.WATER, ElementType.LIGHTNING, 0.5, ["conduct"]),
            ElementInteraction(ElementType.WATER, ElementType.EARTH, 1.0, ["mud"]),
            
            # Terra
            ElementInteraction(ElementType.EARTH, ElementType.AIR, 0.5, []),
            ElementInteraction(ElementType.EARTH, ElementType.LIGHTNING, 1.0, []),
            
            # Ar
            ElementInteraction(ElementType.AIR, ElementType.EARTH, 1.5, []),
            ElementInteraction(ElementType.AIR, ElementType.FIRE, 1.25, ["spread_flames"]),
            
            # Relâmpago
            ElementInteraction(ElementType.LIGHTNING, ElementType.WATER, 1.5, ["shock"]),
            ElementInteraction(ElementType.LIGHTNING, ElementType.EARTH, 0.75, ["ground"]),
            
            # Gelo
            ElementInteraction(ElementType.ICE, ElementType.FIRE, 0.5, []),
            ElementInteraction(ElementType.ICE, ElementType.WATER, 1.0, ["freeze"]),
            
            # Sagrado/Sombrio
            ElementInteraction(ElementType.HOLY, ElementType.DARK, 1.5, ["purify"]),
            ElementInteraction(ElementType.DARK, ElementType.HOLY, 1.5, ["corrupt"])
        ]
        
        for interaction in default_interactions:
            self.add_interaction(interaction)
    
    def add_interaction(self, interaction: ElementInteraction):
        """Adiciona uma interação entre elementos"""
        self.interactions.append(interaction)
    
    def get_interaction(
        self,
        attacking: ElementType,
        defending: ElementType
    ) -> Optional[ElementInteraction]:
        """Retorna interação entre dois elementos"""
        for interaction in self.interactions:
            if (interaction.attacking_element == attacking and
                interaction.defending_element == defending):
                return interaction
        return None
    
    def calculate_damage(
        self,
        base_damage: int,
        attacking_element: ElementType,
        target_resistances: List[ElementalResistance]
    ) -> Dict:
        """Calcula dano final considerando resistências"""
        final_damage = base_damage
        applied_effects = []
        
        # Verificar resistência ao elemento atacante
        resistance = None
        for res in target_resistances:
            if res.element == attacking_element:
                resistance = res
                break
        
        if resistance:
            if resistance.resistance_level == ResistanceLevel.IMMUNE:
                return {
                    'damage': 0,
                    'blocked': True,
                    'message': f'Imune a {attacking_element.value}'
                }
            elif resistance.resistance_level == ResistanceLevel.VULNERABLE:
                final_damage *= 2
            elif resistance.resistance_level == ResistanceLevel.RESISTANT:
                final_damage //= 2
            
            # Aplicar porcentagem adicional
            final_damage = int(final_damage * (1 - resistance.percentage / 100))
        
        # Verificar interações com elementos que o alvo possui
        for target_res in target_resistances:
            interaction = self.get_interaction(attacking_element, target_res.element)
            if interaction:
                final_damage = int(final_damage * interaction.damage_multiplier)
                applied_effects.extend(interaction.additional_effects)
        
        return {
            'damage': max(0, final_damage),
            'blocked': False,
            'effects': applied_effects,
            'original_damage': base_damage
        }
    
    def validate_resistance(
        self,
        resistance: ElementalResistance,
        is_player: bool
    ) -> Dict:
        """Valida se uma resistência é permitida"""
        max_res = self.max_resistance_player if is_player else self.max_resistance_monster
        allow_immunity = self.allow_immunity_player if is_player else self.allow_immunity_monster
        
        if resistance.resistance_level == ResistanceLevel.IMMUNE and not allow_immunity:
            return {
                'valid': False,
                'error': f'Imunidade não permitida para {"players" if is_player else "monstros"}'
            }
        
        if resistance.percentage > max_res:
            return {
                'valid': False,
                'error': f'Resistência máxima é {max_res}%'
            }
        
        return {'valid': True}
    
    def to_json(self) -> str:
        """Exporta sistema para JSON"""
        data = {
            'elements': [e.value for e in ElementType],
            'interactions': [
                {
                    'attacking_element': inter.attacking_element.value,
                    'defending_element': inter.defending_element.value,
                    'damage_multiplier': inter.damage_multiplier,
                    'additional_effects': inter.additional_effects
                }
                for inter in self.interactions
            ],
            'settings': {
                'max_resistance_player': self.max_resistance_player,
                'max_resistance_monster': self.max_resistance_monster,
                'allow_immunity_player': self.allow_immunity_player,
                'allow_immunity_monster': self.allow_immunity_monster
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
            
            # Carregar configurações
            settings = data.get('settings', {})
            system.max_resistance_player = settings.get('max_resistance_player', 75.0)
            system.max_resistance_monster = settings.get('max_resistance_monster', 100.0)
            system.allow_immunity_player = settings.get('allow_immunity_player', False)
            system.allow_immunity_monster = settings.get('allow_immunity_monster', True)
            
            # Limpar interações padrão
            system.interactions.clear()
            
            # Carregar interações
            for inter_data in data.get('interactions', []):
                interaction = ElementInteraction(
                    attacking_element=ElementType(inter_data['attacking_element']),
                    defending_element=ElementType(inter_data['defending_element']),
                    damage_multiplier=inter_data.get('damage_multiplier', 1.0),
                    additional_effects=inter_data.get('additional_effects', [])
                )
                system.add_interaction(interaction)
            
            return system
