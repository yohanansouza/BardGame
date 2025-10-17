"""
Servidor WebSocket para comunicação local/LAN
"""
import asyncio
import websockets
import json
from typing import Set, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GameServer:
    """Servidor de jogo com WebSocket"""
    
    def __init__(self, host: str = 'localhost', port: int = 5000):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.gm_client = None
        self.world_data: Dict = {}
        self.running = False
    
    async def register_client(self, websocket):
        """Registra novo cliente"""
        self.clients.add(websocket)
        logger.info(f"Cliente conectado. Total: {len(self.clients)}")
        
        # Enviar dados do mundo para novo cliente
        if self.world_data:
            await websocket.send(json.dumps({
                'type': 'world_data',
                'data': self.world_data
            }))
    
    async def unregister_client(self, websocket):
        """Remove cliente"""
        self.clients.remove(websocket)
        if websocket == self.gm_client:
            self.gm_client = None
            logger.info("GM desconectado")
        logger.info(f"Cliente desconectado. Total: {len(self.clients)}")
    
    async def broadcast(self, message: str, exclude=None):
        """Envia mensagem para todos os clientes"""
        if self.clients:
            tasks = []
            for client in self.clients:
                if client != exclude:
                    tasks.append(client.send(message))
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def handle_message(self, websocket, message: str):
        """Processa mensagem recebida"""
        try:
            data = json.loads(message)
            msg_type = data.get('type')
            
            if msg_type == 'register_gm':
                # Registrar como GM
                self.gm_client = websocket
                logger.info("GM registrado")
                await websocket.send(json.dumps({
                    'type': 'registration_success',
                    'role': 'gm'
                }))
            
            elif msg_type == 'register_player':
                # Registrar como jogador
                player_name = data.get('name', 'Unknown')
                logger.info(f"Jogador registrado: {player_name}")
                await websocket.send(json.dumps({
                    'type': 'registration_success',
                    'role': 'player',
                    'name': player_name
                }))
            
            elif msg_type == 'update_world':
                # GM atualiza dados do mundo
                if websocket == self.gm_client:
                    self.world_data = data.get('world_data', {})
                    logger.info("Dados do mundo atualizados")
                    # Broadcast para todos os jogadores
                    await self.broadcast(json.dumps({
                        'type': 'world_updated',
                        'data': self.world_data
                    }), exclude=websocket)
            
            elif msg_type == 'chat_message':
                # Mensagem de chat
                sender = data.get('sender', 'Unknown')
                msg = data.get('message', '')
                logger.info(f"Chat - {sender}: {msg}")
                await self.broadcast(json.dumps({
                    'type': 'chat_message',
                    'sender': sender,
                    'message': msg,
                    'timestamp': data.get('timestamp')
                }))
            
            elif msg_type == 'dice_roll':
                # Rolagem de dados
                sender = data.get('sender')
                result = data.get('result')
                dice = data.get('dice')
                logger.info(f"Dado rolado por {sender}: {dice} = {result}")
                await self.broadcast(json.dumps({
                    'type': 'dice_roll',
                    'sender': sender,
                    'dice': dice,
                    'result': result
                }))
            
            elif msg_type == 'character_update':
                # Atualização de personagem
                await self.broadcast(json.dumps(data), exclude=websocket)
            
            elif msg_type == 'ping':
                # Responder ping
                await websocket.send(json.dumps({'type': 'pong'}))
            
            else:
                logger.warning(f"Tipo de mensagem desconhecido: {msg_type}")
        
        except json.JSONDecodeError:
            logger.error("Erro ao decodificar JSON")
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
    
    async def client_handler(self, websocket, path):
        """Handler para cada cliente conectado"""
        await self.register_client(websocket)
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            logger.info("Conexão fechada pelo cliente")
        finally:
            await self.unregister_client(websocket)
    
    async def start(self):
        """Inicia o servidor"""
        self.running = True
        logger.info(f"Iniciando servidor em {self.host}:{self.port}")
        
        async with websockets.serve(self.client_handler, self.host, self.port):
            logger.info("Servidor iniciado! Aguardando conexões...")
            await asyncio.Future()  # Roda para sempre
    
    def run(self):
        """Executa o servidor"""
        asyncio.run(self.start())


if __name__ == "__main__":
    server = GameServer()
    server.run()
