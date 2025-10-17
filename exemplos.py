"""
Exemplos de uso dos sistemas do BardGame
"""
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.world_manager import WorldManager
from models import (
    AttributeRule, SecondaryAttribute,
    LevelConfig, EntityType, XPScalingType,
    Race, SizeCategory, MovementRules,
    Talent, TalentType, TalentWeight, TalentRequirement, TalentEffect,
    Currency,
    Condition, ConditionSeverity, StatusEffect
)


def exemplo_criar_mundo():
    """Exemplo: Criando um novo mundo"""
    print("=== Criando Novo Mundo ===\n")
    
    # Criar mundo
    mundo = WorldManager("Reino de Eldoria", "Mestre Gandalf")
    mundo.metadata.description = "Um reino de alta fantasia medieval"
    
    # 1. Configurar Atributos
    print("1. Configurando Atributos...")
    
    # Atributos primários
    forca = AttributeRule(
        name="Força",
        is_primary=True,
        is_mandatory=True,
        base_value=10,
        min_value=1,
        max_value=20,
        increase_rules=["level_up", "training"]
    )
    mundo.attributes.add_primary_attribute(forca)
    
    destreza = AttributeRule(
        name="Destreza",
        is_primary=True,
        is_mandatory=True,
        base_value=10,
        min_value=1,
        max_value=20
    )
    mundo.attributes.add_primary_attribute(destreza)
    
    # Atributo secundário
    vida = SecondaryAttribute(
        name="Pontos de Vida",
        formula="strength * 5 + 50",
        parent_attributes=["Força"]
    )
    mundo.attributes.add_secondary_attribute(vida)
    
    print(f"   - Atributos primários: {len(mundo.attributes.primary_attributes)}")
    print(f"   - Atributos secundários: {len(mundo.attributes.secondary_attributes)}\n")
    
    # 2. Configurar Sistema de Níveis
    print("2. Configurando Sistema de Níveis...")
    
    # Config para jogadores
    config_player = LevelConfig(
        entity_type=EntityType.PLAYER,
        max_level=20,
        scaling_type=XPScalingType.EXPONENTIAL,
        base_xp=100,
        scaling_factor=1.5,
        reset_xp_on_levelup=True
    )
    mundo.levels.add_level_config(config_player)
    
    # Configurar Reborn
    mundo.levels.reborn_config.enabled = True
    mundo.levels.reborn_config.max_rebirths = 3
    mundo.levels.reborn_config.bonuses_per_rebirth = {"Força": 2, "Destreza": 2}
    
    print(f"   - Nível máximo (Player): {config_player.max_level}")
    print(f"   - Reborn habilitado: {mundo.levels.reborn_config.enabled}\n")
    
    # 3. Criar Raças
    print("3. Criando Raças...")
    
    humano = Race(
        name="Humano",
        size=SizeCategory.MEDIUM,
        movement=MovementRules(base_speed=30),
        attribute_modifiers={"Força": 1, "Destreza": 1},
        languages=["Common"],
        age_range=(0, 100),
        height_range=(160, 190),
        weight_range=(60, 100)
    )
    mundo.races.add_race(humano)
    
    elfo = Race(
        name="Elfo",
        size=SizeCategory.MEDIUM,
        movement=MovementRules(base_speed=35),
        attribute_modifiers={"Destreza": 2},
        languages=["Common", "Elvish"],
        racial_abilities=["Visão na Penumbra"],
        age_range=(0, 750),
        height_range=(150, 180),
        weight_range=(45, 75)
    )
    mundo.races.add_race(elfo)
    
    print(f"   - Raças criadas: {len(mundo.races.races)}\n")
    
    # 4. Criar Talentos
    print("4. Criando Talentos...")
    
    talento_forte = Talent(
        name="Força Brutal",
        talent_type=TalentType.COMBAT,
        weight=TalentWeight.MEDIUM,
        description="Aumenta seu dano em combate corpo a corpo",
        requirements=TalentRequirement(min_level=3, required_attributes={"Força": 13}),
        effects=TalentEffect(
            attribute_bonuses={"Força": 2},
            damage_bonus=2
        )
    )
    mundo.talents.add_talent(talento_forte)
    
    talento_agil = Talent(
        name="Reflexos Rápidos",
        talent_type=TalentType.COMBAT,
        weight=TalentWeight.SMALL,
        description="Melhora sua esquiva",
        effects=TalentEffect(ac_bonus=1, attribute_bonuses={"Destreza": 1})
    )
    mundo.talents.add_talent(talento_agil)
    
    print(f"   - Talentos criados: {len(mundo.talents.talents)}\n")
    
    # 5. Configurar Moedas
    print("5. Configurando Sistema de Moedas...")
    
    # Moedas já vêm com padrão D&D, mas podemos adicionar custom
    mundo.currency.add_currency(
        Currency("Cristal Arcano", "ca", 5000, 0.05, "Moeda rara de magia")
    )
    
    print(f"   - Total de moedas: {len(mundo.currency.currencies)}\n")
    
    # 6. Criar Condições Customizadas
    print("6. Criando Condições...")
    
    congelado = Condition(
        name="Congelado",
        severity=ConditionSeverity.SEVERE,
        description="Coberto de gelo, movimento reduzido",
        effects=StatusEffect(
            movement_modifier=0.5,
            ac_modifier=-2,
            damage_over_time=2
        ),
        duration_type="rounds",
        default_duration=3,
        removable_by=["fire", "magic"]
    )
    mundo.conditions.add_condition(congelado)
    
    print(f"   - Condições disponíveis: {len(mundo.conditions.conditions)}\n")
    
    # 7. Salvar Mundo
    print("7. Salvando Mundo...")
    mundo_path = mundo.save_world("data/worlds")
    print(f"   - Mundo salvo em: {mundo_path}\n")
    
    # 8. Validar Mundo
    print("8. Validando Mundo...")
    validacao = mundo.validate_world()
    if validacao['valid']:
        print("   ✓ Mundo válido!")
    else:
        print("   ✗ Erros encontrados:")
        for erro in validacao['errors']:
            print(f"     - {erro}")
    
    if validacao['warnings']:
        print("   ⚠ Avisos:")
        for aviso in validacao['warnings']:
            print(f"     - {aviso}")
    
    print("\n=== Mundo Criado com Sucesso! ===\n")
    
    return mundo


def exemplo_usar_sistemas():
    """Exemplo: Usando os sistemas"""
    print("\n=== Testando Sistemas ===\n")
    
    # Criar mundo de teste
    mundo = WorldManager("Mundo de Teste", "GM Teste")
    
    # Adicionar atributo
    mundo.attributes.add_primary_attribute(
        AttributeRule("Força", True, True, 10, 1, 20)
    )
    
    # Testar cálculo de XP
    from models import LevelConfig, EntityType, XPScalingType
    
    config = LevelConfig(
        entity_type=EntityType.PLAYER,
        max_level=10,
        scaling_type=XPScalingType.EXPONENTIAL,
        base_xp=100,
        scaling_factor=1.5
    )
    
    print("Tabela de XP (Exponencial):")
    tabela_xp = mundo.levels.generate_xp_table(config)
    for nivel, xp in tabela_xp.items():
        print(f"   Nível {nivel}: {xp} XP")
    
    print("\n" + "="*50 + "\n")
    
    # Testar conversão de moedas
    print("Conversão de Moedas:")
    resultado = mundo.currency.convert(100, "Gold", "Silver")
    if resultado['success']:
        print(f"   100 Gold = {resultado['converted_amount']} Silver")
    
    print("\n" + "="*50 + "\n")
    
    # Testar validação de talento
    print("Validação de Build de Talentos:")
    
    from models import Talent, TalentType, TalentWeight
    
    mundo.talents.add_talent(Talent("Talento A", TalentType.COMBAT, TalentWeight.LARGE, "Desc"))
    mundo.talents.add_talent(Talent("Talento B", TalentType.COMBAT, TalentWeight.MEDIUM, "Desc"))
    mundo.talents.add_talent(Talent("Talento C", TalentType.COMBAT, TalentWeight.SMALL, "Desc"))
    
    # Validar build (3 + 2 + 1 = 6 pontos, dentro do limite)
    validacao = mundo.talents.validate_talent_build(["Talento A", "Talento B", "Talento C"])
    print(f"   Build válido: {validacao['valid']}")
    if 'total_weight' in validacao:
        print(f"   Total de pontos: {validacao['total_weight']}/6")
    
    print("\n=== Testes Concluídos ===\n")


def exemplo_carregar_mundo():
    """Exemplo: Carregando um mundo salvo"""
    print("\n=== Carregando Mundo Existente ===\n")
    
    mundo_path = "data/worlds/Reino_de_Eldoria"
    
    if os.path.exists(mundo_path):
        mundo = WorldManager.load_world(mundo_path)
        
        # Exibir resumo
        resumo = mundo.export_world_summary()
        
        print(f"Nome: {resumo['metadata']['name']}")
        print(f"Criador: {resumo['metadata']['creator']}")
        print(f"\nSistemas:")
        for sistema, info in resumo['systems'].items():
            print(f"  {sistema}:")
            for chave, valor in info.items():
                print(f"    - {chave}: {valor}")
        
        print("\n=== Mundo Carregado ===\n")
    else:
        print(f"Mundo não encontrado em: {mundo_path}")
        print("Execute exemplo_criar_mundo() primeiro!\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print(" BardGame - Exemplos de Uso ".center(60, "="))
    print("="*60 + "\n")
    
    # Executar exemplos
    mundo = exemplo_criar_mundo()
    exemplo_usar_sistemas()
    
    # Descomente para testar carregamento
    # exemplo_carregar_mundo()
    
    print("\n" + "="*60)
    print(" Fim dos Exemplos ".center(60, "="))
    print("="*60 + "\n")
