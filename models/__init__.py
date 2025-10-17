"""
__init__.py do pacote models
"""

from .attributes import AttributeSystem, AttributeRule, SecondaryAttribute
from .level_system import LevelSystem, LevelConfig, EntityType, XPScalingType
from .races import RaceSystem, Race, SizeCategory, MovementRules
from .proficiency import ProficiencySystem, Proficiency, ProficiencyType
from .magic_system import MagicSystem, CasterType, ManaSystem, StaminaSystem
from .talents import TalentSystem, Talent, TalentType, TalentWeight
from .currency import CurrencySystem, Currency, ExchangeRate
from .conditions import ConditionSystem, Condition, StatusCondition, ConditionSeverity
from .elements import ElementSystem, ElementType, ResistanceLevel, ElementalResistance
from .armor_class import ACSystem, ArmorClass, MagicalAC
from .equipment import EquipmentSystem, Equipment, EquipmentTag, EquipmentSlot
from .languages import LanguageSystem, Language, LanguageProficiency

__all__ = [
    # Attributes
    'AttributeSystem', 'AttributeRule', 'SecondaryAttribute',
    # Levels
    'LevelSystem', 'LevelConfig', 'EntityType', 'XPScalingType',
    # Races
    'RaceSystem', 'Race', 'SizeCategory', 'MovementRules',
    # Proficiency
    'ProficiencySystem', 'Proficiency', 'ProficiencyType',
    # Magic
    'MagicSystem', 'CasterType', 'ManaSystem', 'StaminaSystem',
    # Talents
    'TalentSystem', 'Talent', 'TalentType', 'TalentWeight',
    # Currency
    'CurrencySystem', 'Currency', 'ExchangeRate',
    # Conditions
    'ConditionSystem', 'Condition', 'StatusCondition', 'ConditionSeverity',
    # Elements
    'ElementSystem', 'ElementType', 'ResistanceLevel', 'ElementalResistance',
    # Armor Class
    'ACSystem', 'ArmorClass', 'MagicalAC',
    # Equipment
    'EquipmentSystem', 'Equipment', 'EquipmentTag', 'EquipmentSlot',
    # Languages
    'LanguageSystem', 'Language', 'LanguageProficiency'
]
