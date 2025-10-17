"""
Sistema de Níveis e Experiência
"""
import json
import math
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class XPScalingType(Enum):
    """Tipos de escalamento de XP"""
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    S_CURVE = "s_curve"
    MULTIPLICATION = "multiplication"
    MANUAL = "manual"


class EntityType(Enum):
    """Tipos de entidades com níveis"""
    PLAYER = "player"
    NPC = "npc"
    MONSTER = "monster"


@dataclass
class LevelConfig:
    """Configuração de níveis para um tipo de entidade"""
    entity_type: EntityType
    max_level: int
    scaling_type: XPScalingType
    base_xp: int = 100
    scaling_factor: float = 1.5
    reset_xp_on_levelup: bool = True
    manual_xp_table: List[int] = field(default_factory=list)
    attribute_bonuses_per_level: Dict[str, int] = field(default_factory=dict)


@dataclass
class RebornConfig:
    """Configuração do sistema de Reborn"""
    enabled: bool = False
    max_rebirths: int = 0
    bonuses_per_rebirth: Dict[str, float] = field(default_factory=dict)
    level_reset_to: int = 1


@dataclass
class MultiLevelConfig:
    """Configuração para múltiplos sistemas de nível"""
    enabled: bool = False
    level_types: List[str] = field(default_factory=list)  # ["combat", "magic", "crafting"]
    xp_distribution_mode: str = "manual"  # "manual", "auto_by_usage"


class LevelSystem:
    """Gerenciador do sistema de níveis"""
    
    def __init__(self):
        self.enabled: bool = True
        self.level_configs: Dict[EntityType, LevelConfig] = {}
        self.reborn_config: RebornConfig = RebornConfig()
        self.multi_level_config: MultiLevelConfig = MultiLevelConfig()
        self.attribute_warnings: List[str] = []
    
    def set_enabled(self, enabled: bool):
        """Ativa ou desativa o sistema de níveis"""
        self.enabled = enabled
        if not enabled:
            self.check_attribute_dependencies()
    
    def check_attribute_dependencies(self):
        """Verifica se há atributos que dependem do sistema de níveis"""
        # TODO: Integrar com sistema de atributos para verificar dependências
        self.attribute_warnings = []
        if not self.enabled:
            self.attribute_warnings.append("AVISO: Sistema de níveis desativado, mas há atributos que dependem dele!")
    
    def add_level_config(self, config: LevelConfig):
        """Adiciona configuração de nível para um tipo de entidade"""
        self.level_configs[config.entity_type] = config
    
    def calculate_xp_for_level(self, level: int, config: LevelConfig) -> int:
        """Calcula XP necessário para atingir um nível"""
        if config.scaling_type == XPScalingType.MANUAL:
            if level <= len(config.manual_xp_table):
                return config.manual_xp_table[level - 1]
            return config.manual_xp_table[-1] if config.manual_xp_table else 0
        
        elif config.scaling_type == XPScalingType.LINEAR:
            return config.base_xp * level
        
        elif config.scaling_type == XPScalingType.EXPONENTIAL:
            return int(config.base_xp * (config.scaling_factor ** (level - 1)))
        
        elif config.scaling_type == XPScalingType.S_CURVE:
            # Curva sigmoide
            x = level / config.max_level
            sigmoid = 1 / (1 + math.exp(-10 * (x - 0.5)))
            return int(config.base_xp * sigmoid * config.max_level)
        
        elif config.scaling_type == XPScalingType.MULTIPLICATION:
            return config.base_xp * level * config.scaling_factor
        
        return 0
    
    def generate_xp_table(self, config: LevelConfig) -> Dict[int, int]:
        """Gera tabela completa de XP para todos os níveis"""
        return {
            level: self.calculate_xp_for_level(level, config)
            for level in range(1, config.max_level + 1)
        }
    
    def perform_rebirth(self, current_level: int, rebirth_count: int) -> Dict:
        """Executa um renascimento"""
        if not self.reborn_config.enabled:
            return {"success": False, "message": "Sistema de Reborn desabilitado"}
        
        if rebirth_count >= self.reborn_config.max_rebirths:
            return {"success": False, "message": "Limite de Rebirths atingido"}
        
        bonuses = {
            key: value * (rebirth_count + 1)
            for key, value in self.reborn_config.bonuses_per_rebirth.items()
        }
        
        return {
            "success": True,
            "new_level": self.reborn_config.level_reset_to,
            "bonuses": bonuses,
            "rebirth_count": rebirth_count + 1
        }
    
    def to_json(self) -> str:
        """Exporta sistema de níveis para JSON"""
        data = {
            'enabled': self.enabled,
            'level_configs': {
                entity_type.value: {
                    'entity_type': config.entity_type.value,
                    'max_level': config.max_level,
                    'scaling_type': config.scaling_type.value,
                    'base_xp': config.base_xp,
                    'scaling_factor': config.scaling_factor,
                    'reset_xp_on_levelup': config.reset_xp_on_levelup,
                    'manual_xp_table': config.manual_xp_table,
                    'attribute_bonuses_per_level': config.attribute_bonuses_per_level
                }
                for entity_type, config in self.level_configs.items()
            },
            'reborn_config': {
                'enabled': self.reborn_config.enabled,
                'max_rebirths': self.reborn_config.max_rebirths,
                'bonuses_per_rebirth': self.reborn_config.bonuses_per_rebirth,
                'level_reset_to': self.reborn_config.level_reset_to
            },
            'multi_level_config': {
                'enabled': self.multi_level_config.enabled,
                'level_types': self.multi_level_config.level_types,
                'xp_distribution_mode': self.multi_level_config.xp_distribution_mode
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
            system.enabled = data.get('enabled', True)
            
            # Carregar configs de nível
            for entity_type_str, config_data in data.get('level_configs', {}).items():
                config = LevelConfig(
                    entity_type=EntityType(config_data['entity_type']),
                    max_level=config_data['max_level'],
                    scaling_type=XPScalingType(config_data['scaling_type']),
                    base_xp=config_data.get('base_xp', 100),
                    scaling_factor=config_data.get('scaling_factor', 1.5),
                    reset_xp_on_levelup=config_data.get('reset_xp_on_levelup', True),
                    manual_xp_table=config_data.get('manual_xp_table', []),
                    attribute_bonuses_per_level=config_data.get('attribute_bonuses_per_level', {})
                )
                system.add_level_config(config)
            
            # Carregar config de reborn
            reborn_data = data.get('reborn_config', {})
            system.reborn_config = RebornConfig(
                enabled=reborn_data.get('enabled', False),
                max_rebirths=reborn_data.get('max_rebirths', 0),
                bonuses_per_rebirth=reborn_data.get('bonuses_per_rebirth', {}),
                level_reset_to=reborn_data.get('level_reset_to', 1)
            )
            
            # Carregar config multi-level
            multi_data = data.get('multi_level_config', {})
            system.multi_level_config = MultiLevelConfig(
                enabled=multi_data.get('enabled', False),
                level_types=multi_data.get('level_types', []),
                xp_distribution_mode=multi_data.get('xp_distribution_mode', 'manual')
            )
            
            return system
