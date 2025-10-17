"""
Sistema de Línguas e Criptografia
"""
import json
import random
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field


@dataclass
class Language:
    """Definição de uma língua"""
    name: str
    script: str  # Sistema de escrita
    difficulty: int = 1  # 1-10, quão difícil é aprender
    description: str = ""
    related_languages: List[str] = field(default_factory=list)  # Línguas similares
    speakers: List[str] = field(default_factory=list)  # Raças que falam


@dataclass
class LanguageProficiency:
    """Proficiência em uma língua"""
    language_name: str
    speak_percentage: float = 0.0  # 0-100%
    read_percentage: float = 0.0  # 0-100%
    write_percentage: float = 0.0  # 0-100%
    understand_percentage: float = 0.0  # 0-100%


class LanguageSystem:
    """Gerenciador do sistema de línguas"""
    
    def __init__(self):
        self.languages: Dict[str, Language] = {}
        self.unknown_text_marker = "[Língua Desconhecida]"
        self.cipher_characters = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        self._init_default_languages()
    
    def _init_default_languages(self):
        """Inicializa línguas padrão"""
        default_languages = [
            Language(
                name="Common",
                script="Latin",
                difficulty=1,
                description="Língua comum falada pela maioria das raças",
                speakers=["Human", "Halfling"]
            ),
            Language(
                name="Elvish",
                script="Elvish",
                difficulty=3,
                description="Língua melódica dos elfos",
                related_languages=["Sylvan"],
                speakers=["Elf", "Half-Elf"]
            ),
            Language(
                name="Dwarvish",
                script="Runic",
                difficulty=4,
                description="Língua áspera dos anões",
                speakers=["Dwarf"]
            ),
            Language(
                name="Draconic",
                script="Draconic",
                difficulty=5,
                description="Língua antiga dos dragões",
                speakers=["Dragon", "Dragonborn"]
            ),
            Language(
                name="Orcish",
                script="Dwarvish",
                difficulty=2,
                description="Língua dos orcs",
                speakers=["Orc", "Half-Orc"]
            ),
            Language(
                name="Infernal",
                script="Infernal",
                difficulty=6,
                description="Língua dos diabos e do inferno",
                speakers=["Devil", "Tiefling"]
            ),
            Language(
                name="Celestial",
                script="Celestial",
                difficulty=6,
                description="Língua dos seres celestiais",
                speakers=["Angel", "Aasimar"]
            ),
            Language(
                name="Abyssal",
                script="Infernal",
                difficulty=5,
                description="Língua caótica dos demônios",
                speakers=["Demon"]
            )
        ]
        
        for language in default_languages:
            self.add_language(language)
    
    def add_language(self, language: Language):
        """Adiciona uma língua ao sistema"""
        self.languages[language.name] = language
    
    def get_language(self, name: str) -> Optional[Language]:
        """Retorna uma língua pelo nome"""
        return self.languages.get(name)
    
    def encrypt_text(
        self,
        text: str,
        language_name: str,
        proficiency: LanguageProficiency
    ) -> str:
        """Criptografa texto baseado na proficiência"""
        language = self.get_language(language_name)
        if not language:
            return self.unknown_text_marker
        
        # Se não tem proficiência nenhuma, retorna marcador
        if proficiency.read_percentage == 0:
            return self.unknown_text_marker
        
        # Se proficiência é 100%, retorna texto original
        if proficiency.read_percentage >= 100:
            return text
        
        # Calcular quantos caracteres cifrar
        words = text.split()
        encrypted_words = []
        
        for word in words:
            # Chance de entender cada palavra baseado na proficiência
            if random.random() * 100 < proficiency.read_percentage:
                encrypted_words.append(word)
            else:
                # Cifrar palavra
                encrypted_word = self._cipher_word(word, proficiency.read_percentage)
                encrypted_words.append(encrypted_word)
        
        return ' '.join(encrypted_words)
    
    def _cipher_word(self, word: str, proficiency: float) -> str:
        """Cifra uma palavra baseado na proficiência"""
        if proficiency >= 75:
            # Alta proficiência: apenas alguns caracteres cifrados
            result = list(word)
            num_to_cipher = max(1, len(word) // 4)
            indices = random.sample(range(len(word)), min(num_to_cipher, len(word)))
            for i in indices:
                result[i] = random.choice(self.cipher_characters)
            return ''.join(result)
        
        elif proficiency >= 50:
            # Média proficiência: metade cifrada
            result = list(word)
            for i in range(0, len(word), 2):
                result[i] = random.choice(self.cipher_characters)
            return ''.join(result)
        
        elif proficiency >= 25:
            # Baixa proficiência: mantém algumas letras
            result = []
            for char in word:
                if random.random() < 0.3:
                    result.append(char)
                else:
                    result.append(random.choice(self.cipher_characters))
            return ''.join(result)
        
        else:
            # Muito baixa: tudo cifrado
            return ''.join(random.choice(self.cipher_characters) for _ in word)
    
    def decrypt_text(
        self,
        encrypted_text: str,
        original_text: str,
        proficiency: LanguageProficiency
    ) -> Dict:
        """Tenta decifrar texto"""
        if encrypted_text == self.unknown_text_marker:
            return {
                'success': False,
                'text': self.unknown_text_marker,
                'percentage_understood': 0
            }
        
        # Calcular quantas palavras foram decifradas
        encrypted_words = encrypted_text.split()
        original_words = original_text.split()
        
        if len(encrypted_words) != len(original_words):
            return {'success': False, 'error': 'Textos não correspondem'}
        
        understood_count = sum(
            1 for enc, orig in zip(encrypted_words, original_words)
            if enc == orig
        )
        
        percentage = (understood_count / len(original_words)) * 100
        
        return {
            'success': True,
            'text': encrypted_text,
            'percentage_understood': percentage,
            'words_understood': understood_count,
            'total_words': len(original_words)
        }
    
    def learn_language(
        self,
        proficiency: LanguageProficiency,
        study_hours: int,
        intelligence_modifier: int = 0
    ) -> LanguageProficiency:
        """Aumenta proficiência em uma língua com estudo"""
        language = self.get_language(proficiency.language_name)
        if not language:
            return proficiency
        
        # Calcular ganho baseado em dificuldade e inteligência
        base_gain = study_hours / language.difficulty
        intelligence_bonus = intelligence_modifier * 0.1
        total_gain = base_gain * (1 + intelligence_bonus)
        
        # Atualizar proficiências
        proficiency.read_percentage = min(100, proficiency.read_percentage + total_gain)
        proficiency.understand_percentage = min(100, proficiency.understand_percentage + total_gain * 0.8)
        proficiency.speak_percentage = min(100, proficiency.speak_percentage + total_gain * 0.6)
        proficiency.write_percentage = min(100, proficiency.write_percentage + total_gain * 0.5)
        
        return proficiency
    
    def get_related_language_bonus(
        self,
        known_language: str,
        target_language: str
    ) -> float:
        """Retorna bônus de aprendizado se línguas são relacionadas"""
        target = self.get_language(target_language)
        if not target:
            return 0.0
        
        if known_language in target.related_languages:
            return 0.25  # 25% bônus
        
        # Verificar se compartilham mesmo sistema de escrita
        known = self.get_language(known_language)
        if known and known.script == target.script:
            return 0.15  # 15% bônus
        
        return 0.0
    
    def to_json(self) -> str:
        """Exporta sistema para JSON"""
        data = {
            'languages': {
                name: {
                    'name': lang.name,
                    'script': lang.script,
                    'difficulty': lang.difficulty,
                    'description': lang.description,
                    'related_languages': lang.related_languages,
                    'speakers': lang.speakers
                }
                for name, lang in self.languages.items()
            },
            'settings': {
                'unknown_text_marker': self.unknown_text_marker,
                'cipher_characters': self.cipher_characters
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
            
            # Limpar línguas padrão
            system.languages.clear()
            
            # Carregar configurações
            settings = data.get('settings', {})
            system.unknown_text_marker = settings.get('unknown_text_marker', '[Língua Desconhecida]')
            system.cipher_characters = settings.get('cipher_characters', system.cipher_characters)
            
            # Carregar línguas
            for name, lang_data in data.get('languages', {}).items():
                language = Language(
                    name=lang_data['name'],
                    script=lang_data['script'],
                    difficulty=lang_data.get('difficulty', 1),
                    description=lang_data.get('description', ''),
                    related_languages=lang_data.get('related_languages', []),
                    speakers=lang_data.get('speakers', [])
                )
                system.add_language(language)
            
            return system
