"""
Cliente WebSocket para conectar ao servidor
"""
import asyncio
import websockets
import json
import logging
from typing import Callable, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GameClient:
    """Cliente de jogo com WebSocket"""
    
    def __init__(self, host: str = 'localhost', port: int = 5000):
        self.uri = f"ws://{host}:{port}"
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.connected = False
        self.role: Optional[str] = None  # 'gm' ou 'player'
        self.name: Optional[str] = None
        
        # Callbacks para diferentes tipos de mensagens
        self.message_handlers: dict[str, Callable] = {}
    
    def register_handler(self, message_type: str, handler: Callable):
        """Registra handler para tipo de mensagem"""
        self.message_handlers[message_type] = handler
    
    async def connect(self):
        """Conecta ao servidor"""
        try:
            self.websocket = await websockets.connect(self.uri)
            self.connected = True
            logger.info(f"Conectado ao servidor: {self.uri}")
            return True
        except Exception as e:
            logger.error(f"Erro ao conectar: {e}")
            self.connected = False
            return False
    
    async def disconnect(self):
        """Desconecta do servidor"""
        if self.websocket:
            await self.websocket.close()
            self.connected = False
            logger.info("Desconectado do servidor")
    
    async def send_message(self, message_type: str, data: dict = None):
        """Envia mensagem ao servidor"""
        if not self.connected or not self.websocket:
            logger.error("Não conectado ao servidor")
            return False
        
        message = {
            'type': message_type,
            **(data or {})
        }
        
        try:
            await self.websocket.send(json.dumps(message))
            return True
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            return False
    
    async def register_as_gm(self):
        """Registra como Game Master"""
        success = await self.send_message('register_gm')
        if success:
            self.role = 'gm'
            logger.info("Registrado como GM")
        return success
    
    async def register_as_player(self, player_name: str):
        """Registra como jogador"""
        success = await self.send_message('register_player', {'name': player_name})
        if success:
            self.role = 'player'
            self.name = player_name
            logger.info(f"Registrado como jogador: {player_name}")
        return success
    
    async def update_world(self, world_data: dict):
        """Atualiza dados do mundo (apenas GM)"""
        if self.role != 'gm':
            logger.error("Apenas GM pode atualizar o mundo")
            return False
        
        return await self.send_message('update_world', {'world_data': world_data})
    
    async def send_chat_message(self, message: str):
        """Envia mensagem de chat"""
        import time
        return await self.send_message('chat_message', {
            'sender': self.name or self.role or 'Unknown',
            'message': message,
            'timestamp': time.time()
        })
    
    async def roll_dice(self, dice: str, result: int):
        """Envia resultado de rolagem de dados"""
        return await self.send_message('dice_roll', {
            'sender': self.name or self.role or 'Unknown',
            'dice': dice,
            'result': result
        })
    
    async def update_character(self, character_data: dict):
        """Envia atualização de personagem"""
        return await self.send_message('character_update', {
            'sender': self.name,
            'character': character_data
        })
    
    async def ping(self):
        """Envia ping ao servidor"""
        return await self.send_message('ping')
    
    async def receive_messages(self):
        """Recebe mensagens do servidor"""
        if not self.connected or not self.websocket:
            return
        
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    msg_type = data.get('type')
                    
                    # Chamar handler se existir
                    if msg_type in self.message_handlers:
                        self.message_handlers[msg_type](data)
                    else:
                        logger.info(f"Mensagem recebida ({msg_type}): {data}")
                
                except json.JSONDecodeError:
                    logger.error("Erro ao decodificar mensagem")
        
        except websockets.exceptions.ConnectionClosed:
            logger.info("Conexão fechada pelo servidor")
            self.connected = False
    
    async def run(self):
        """Executa o cliente"""
        if await self.connect():
            await self.receive_messages()


# Exemplo de uso
async def example_gm_client():
    """Exemplo de cliente GM"""
    client = GameClient()
    
    # Registrar handlers
    def on_player_join(data):
        print(f"Jogador entrou: {data}")
    
    client.register_handler('registration_success', on_player_join)
    
    # Conectar
    if await client.connect():
        await client.register_as_gm()
        
        # Atualizar mundo
        await client.update_world({'world_name': 'Meu Mundo', 'version': '1.0'})
        
        # Enviar mensagem
        await client.send_chat_message("Bem-vindos à sessão!")
        
        # Receber mensagens
        await client.receive_messages()


async def example_player_client():
    """Exemplo de cliente jogador"""
    client = GameClient()
    
    if await client.connect():
        await client.register_as_player("Aragorn")
        
        # Enviar mensagem
        await client.send_chat_message("Olá, estou pronto!")
        
        # Rolar dado
        await client.roll_dice("1d20", 15)
        
        # Receber mensagens
        await client.receive_messages()


if __name__ == "__main__":
    # Executar cliente GM ou jogador
    asyncio.run(example_gm_client())
    # asyncio.run(example_player_client())
