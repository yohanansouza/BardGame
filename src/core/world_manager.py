"""
Gerenciador de Mundo - Integra todos os sistemas de regras
"""
import json
import os
from typing import Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime

from models import (
    AttributeSystem, LevelSystem, RaceSystem, ProficiencySystem,
    MagicSystem, TalentSystem, CurrencySystem, ConditionSystem,
    ElementSystem, ACSystem, EquipmentSystem, LanguageSystem
)


@dataclass
class WorldMetadata:
    """Metadados do mundo"""
    name: str
    creator: str  # Game Master
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_modified: str = field(default_factory=lambda: datetime.now().isoformat())
    description: str = ""
    version: str = "1.0"
    player_count: int = 0
    session_count: int = 0


class WorldManager:
    """Gerenciador central do mundo de jogo"""
    
    def __init__(self, world_name: str = "New World", gm_name: str = "Game Master"):
        self.metadata = WorldMetadata(name=world_name, creator=gm_name)
        
        # Inicializar todos os sistemas
        self.attributes = AttributeSystem()
        self.levels = LevelSystem()
        self.races = RaceSystem()
        self.proficiencies = ProficiencySystem()
        self.magic = MagicSystem()
        self.talents = TalentSystem()
        self.currency = CurrencySystem()
        self.conditions = ConditionSystem()
        self.elements = ElementSystem()
        self.armor_class = ACSystem()
        self.equipment = EquipmentSystem()
        self.languages = LanguageSystem()
        
        # Configurações de layout do GM
        self.gm_layout: Dict = {}
    
    def save_world(self, directory: str):
        """Salva todo o mundo em arquivos JSON separados"""
        world_dir = os.path.join(directory, self.metadata.name.replace(' ', '_'))
        os.makedirs(world_dir, exist_ok=True)
        
        # Atualizar timestamp
        self.metadata.last_modified = datetime.now().isoformat()
        
        # Salvar metadados
        metadata_path = os.path.join(world_dir, 'metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump({
                'name': self.metadata.name,
                'creator': self.metadata.creator,
                'created_at': self.metadata.created_at,
                'last_modified': self.metadata.last_modified,
                'description': self.metadata.description,
                'version': self.metadata.version,
                'player_count': self.metadata.player_count,
                'session_count': self.metadata.session_count
            }, f, indent=2, ensure_ascii=False)
        
        # Salvar cada sistema em arquivo separado
        rules_dir = os.path.join(world_dir, 'rules')
        os.makedirs(rules_dir, exist_ok=True)
        
        self.attributes.save_to_file(os.path.join(rules_dir, 'attributes.json'))
        self.levels.save_to_file(os.path.join(rules_dir, 'levels.json'))
        self.races.save_to_file(os.path.join(rules_dir, 'races.json'))
        self.proficiencies.save_to_file(os.path.join(rules_dir, 'proficiencies.json'))
        self.magic.save_to_file(os.path.join(rules_dir, 'magic.json'))
        self.talents.save_to_file(os.path.join(rules_dir, 'talents.json'))
        self.currency.save_to_file(os.path.join(rules_dir, 'currency.json'))
        self.conditions.save_to_file(os.path.join(rules_dir, 'conditions.json'))
        self.elements.save_to_file(os.path.join(rules_dir, 'elements.json'))
        self.armor_class.save_to_file(os.path.join(rules_dir, 'armor_class.json'))
        self.equipment.save_to_file(os.path.join(rules_dir, 'equipment.json'))
        self.languages.save_to_file(os.path.join(rules_dir, 'languages.json'))
        
        # Salvar layout do GM
        layout_path = os.path.join(world_dir, 'gm_layout.json')
        with open(layout_path, 'w', encoding='utf-8') as f:
            json.dump(self.gm_layout, f, indent=2, ensure_ascii=False)
        
        print(f"Mundo '{self.metadata.name}' salvo em: {world_dir}")
        return world_dir
    
    @classmethod
    def load_world(cls, world_path: str) -> 'WorldManager':
        """Carrega um mundo de arquivos JSON"""
        # Carregar metadados
        metadata_path = os.path.join(world_path, 'metadata.json')
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata_data = json.load(f)
        
        world = cls(metadata_data['name'], metadata_data['creator'])
        world.metadata = WorldMetadata(**metadata_data)
        
        # Carregar sistemas
        rules_dir = os.path.join(world_path, 'rules')
        
        world.attributes = AttributeSystem.load_from_file(
            os.path.join(rules_dir, 'attributes.json'))
        world.levels = LevelSystem.load_from_file(
            os.path.join(rules_dir, 'levels.json'))
        world.races = RaceSystem.load_from_file(
            os.path.join(rules_dir, 'races.json'))
        world.proficiencies = ProficiencySystem.load_from_file(
            os.path.join(rules_dir, 'proficiencies.json'))
        world.magic = MagicSystem.load_from_file(
            os.path.join(rules_dir, 'magic.json'))
        world.talents = TalentSystem.load_from_file(
            os.path.join(rules_dir, 'talents.json'))
        world.currency = CurrencySystem.load_from_file(
            os.path.join(rules_dir, 'currency.json'))
        world.conditions = ConditionSystem.load_from_file(
            os.path.join(rules_dir, 'conditions.json'))
        world.elements = ElementSystem.load_from_file(
            os.path.join(rules_dir, 'elements.json'))
        world.armor_class = ACSystem.load_from_file(
            os.path.join(rules_dir, 'armor_class.json'))
        world.equipment = EquipmentSystem.load_from_file(
            os.path.join(rules_dir, 'equipment.json'))
        world.languages = LanguageSystem.load_from_file(
            os.path.join(rules_dir, 'languages.json'))
        
        # Carregar layout do GM
        layout_path = os.path.join(world_path, 'gm_layout.json')
        if os.path.exists(layout_path):
            with open(layout_path, 'r', encoding='utf-8') as f:
                world.gm_layout = json.load(f)
        
        print(f"Mundo '{world.metadata.name}' carregado de: {world_path}")
        return world
    
    def export_world_summary(self) -> Dict:
        """Exporta um resumo do mundo"""
        return {
            'metadata': {
                'name': self.metadata.name,
                'creator': self.metadata.creator,
                'created_at': self.metadata.created_at,
                'last_modified': self.metadata.last_modified,
                'description': self.metadata.description
            },
            'systems': {
                'attributes': {
                    'primary_count': len(self.attributes.primary_attributes),
                    'secondary_count': len(self.attributes.secondary_attributes)
                },
                'levels': {
                    'enabled': self.levels.enabled,
                    'entity_types': len(self.levels.level_configs),
                    'reborn_enabled': self.levels.reborn_config.enabled
                },
                'races': {
                    'count': len(self.races.races)
                },
                'proficiencies': {
                    'count': len(self.proficiencies.proficiencies)
                },
                'magic': {
                    'spell_tables': len(self.magic.spell_slot_tables),
                    'mana_enabled': self.magic.mana_system.enabled,
                    'stamina_enabled': self.magic.stamina_system.enabled
                },
                'talents': {
                    'count': len(self.talents.talents),
                    'max_per_character': self.talents.build_rules.max_talents
                },
                'currency': {
                    'currencies': len(self.currency.currencies),
                    'base_currency': self.currency.base_currency
                },
                'conditions': {
                    'count': len(self.conditions.conditions)
                },
                'elements': {
                    'count': len(self.elements.elements),
                    'interactions': len(self.elements.interactions)
                },
                'equipment': {
                    'count': len(self.equipment.equipment_database)
                },
                'languages': {
                    'count': len(self.languages.languages)
                }
            }
        }
    
    def validate_world(self) -> Dict:
        """Valida configuração do mundo"""
        warnings = []
        errors = []
        
        # Validar sistema de níveis
        if not self.levels.enabled:
            if self.levels.attribute_warnings:
                warnings.extend(self.levels.attribute_warnings)
        
        # Verificar se há pelo menos uma moeda
        if not self.currency.currencies:
            errors.append("Nenhuma moeda definida no sistema")
        
        # Verificar se moeda base existe
        if self.currency.base_currency not in self.currency.currencies:
            errors.append(f"Moeda base '{self.currency.base_currency}' não existe")
        
        return {
            'valid': len(errors) == 0,
            'warnings': warnings,
            'errors': errors
        }
