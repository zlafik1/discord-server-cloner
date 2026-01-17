import sys
import os

if sys.platform == "win32":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)
    except:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from colorama import Fore, Style, init
import urllib.request
import urllib.error
import json
import ssl
import time
import base64
import aiohttp
import asyncio
import re
from typing import Optional, Dict, List, Any, Tuple
import traceback

init(autoreset=True)

BLUE = Fore.BLUE
CYAN = Fore.CYAN
WHITE = Fore.WHITE

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def разделитель(ширина=65):
    return BLUE + "─" * ширина

def заголовок(текст):
    print(f"\n{BLUE}┌{'─' * 63}┐")
    print(f"{BLUE}│ {CYAN}{текст:^61} {BLUE}│")
    print(f"{BLUE}└{'─' * 63}┘")

def подзаголовок(текст):
    print(f"\n{BLUE}├{'─' * 63}┤")
    print(f"{BLUE}│ {CYAN}{текст:^61} {BLUE}│")
    print(f"{BLUE}├{'─' * 63}┤")

def информация(текст):
    print(f"{CYAN}│ {WHITE}{текст}")

def успех(текст):
    print(f"{CYAN}│ {BLUE}[+] {WHITE}{текст}")

def предупреждение(текст):
    print(f"{CYAN}│ {BLUE}[!] {WHITE}{текст}")

def ошибка(текст):
    print(f"{CYAN}│ {BLUE}[-] {WHITE}{текст}")

def ввод_подсказка(текст):
    print(f"{CYAN}│ {BLUE}[?] {WHITE}{текст}")
    print(f"{CYAN}│ {BLUE}  -> {WHITE}", end="")
    return input()

def ввод_поле(текст):
    print(f"{CYAN}│ {BLUE}[>] {WHITE}{текст}:")
    print(f"{CYAN}│ {BLUE}  -> {WHITE}", end="")
    return input()

def печать_баннера():
    clear_screen()
    print(f"{BLUE}╔{'═' * 63}╗")
    print(f"{BLUE}║ {CYAN}{'DISCORD SERVER CLONER V3.3':^61} {BLUE}║")
    print(f"{BLUE}║ {CYAN}{'BLUE EDITION':^61} {BLUE}║")
    print(f"{BLUE}╠{'═' * 63}╣")
    print(f"{BLUE}║ {WHITE}Автор: {CYAN}zlafik{'':^47} {BLUE}║")
    print(f"{BLUE}║ {WHITE}Discord: {CYAN}zlafik{'':^46} {BLUE}║")
    print(f"{BLUE}║ {WHITE}Telegram: {CYAN}@qtiq0{'':^46} {BLUE}║")
    print(f"{BLUE}║ {WHITE}Канал: {CYAN}@biozlafik{'':^46} {BLUE}║")
    print(f"{BLUE}╠{'─' * 63}╣")
    print(f"{BLUE}║ {CYAN}Возможности программы:{'':^38} {BLUE}║")
    print(f"{BLUE}║ {WHITE}• Полное клонирование структуры сервера{'':^22} {BLUE}║")
    print(f"{BLUE}║ {WHITE}• Сохранение ролей, каналов и категорий{'':^23} {BLUE}║")
    print(f"{BLUE}║ {WHITE}• Чистый улучшенный интерфейс{'':^32} {BLUE}║")
    print(f"{BLUE}║ {WHITE}• Удобные подсказки и уведомления{'':^29} {BLUE}║")
    print(f"{BLUE}╚{'═' * 63}╝")

def печать_соглашения():
    clear_screen()
    print(f"{BLUE}╔{'═' * 63}╗")
    print(f"{BLUE}║ {CYAN}{'ПОЛЬЗОВАТЕЛЬСКОЕ СОГЛАШЕНИЕ':^61} {BLUE}║")
    print(f"{BLUE}╠{'─' * 63}╣")
    print(f"{BLUE}║ {CYAN}ВНИМАТЕЛЬНО ПРОЧИТАЙТЕ ПЕРЕД ИСПОЛЬЗОВАНИЕМ:{'':^20} {BLUE}║")
    print(f"{BLUE}║ {WHITE}1. Вы несете ответственность за использование программы{'':^8} {BLUE}║")
    print(f"{BLUE}║ {WHITE}2. Разработчик не несет ответственности за последствия{'':^7} {BLUE}║")
    print(f"{BLUE}║ {WHITE}3. Использование осуществляется на свой риск{'':^20} {BLUE}║")
    print(f"{BLUE}║ {WHITE}4. Запрещено использовать во вред другим пользователям{'':^3} {BLUE}║")
    print(f"{BLUE}╠{'─' * 63}╣")
    print(f"{BLUE}║ {CYAN}Принимая соглашение, вы подтверждаете понимание рисков{'':^3} {BLUE}║")
    print(f"{BLUE}╚{'═' * 63}╝")

def подтвердить_соглашение():
    печать_соглашения()
    подтверждение = ввод_подсказка("Для подтверждения введите: 'Подтвердить'")
    return подтверждение.strip().lower() == "подтвердить"

class SafeSSLContext:
    def __init__(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
    def get_context(self):
        return self.ctx

class DiscordValidator:
    @staticmethod
    def validate_token(token: str) -> bool:
        if not token or not isinstance(token, str):
            return False
        token = token.strip()
        if len(token) < 50:
            return False
        patterns = [
            r'^[A-Za-z0-9\.\-_]{59}\.[A-Za-z0-9\.\-_]{6}\.[A-Za-z0-9\.\-_]{27}$',
            r'^[A-Za-z0-9\.\-_]{24}\.[A-Za-z0-9\.\-_]{6}\.[A-Za-z0-9\.\-_]{27}$',
            r'^mfa\.[A-Za-z0-9\.\-_]{84}$',
            r'^[A-Za-z0-9\.\-_]{70,}$'
        ]
        for pattern in patterns:
            if re.match(pattern, token):
                return True
        return False

    @staticmethod
    def validate_snowflake(snowflake: str) -> bool:
        if not snowflake or not isinstance(snowflake, str):
            return False
        snowflake = snowflake.strip()
        if not snowflake.isdigit():
            return False
        if len(snowflake) < 17 or len(snowflake) > 20:
            return False
        try:
            snowflake_int = int(snowflake)
            return snowflake_int > 10000000000000000
        except:
            return False

    @staticmethod
    def clean_channel_name(name: str) -> str:
        if not name or not isinstance(name, str):
            return "канал"
        cleaned = ''.join(char for char in name if char.isprintable() or char in ' ')
        cleaned = ' '.join(cleaned.split())
        if len(cleaned) > 100:
            cleaned = cleaned[:97] + "..."
        cleaned = cleaned.replace('```', '`\u200b`\u200b`')
        if not cleaned or cleaned.isspace():
            return "канал"
        return cleaned

    @staticmethod
    def clean_role_name(name: str) -> str:
        if not name or not isinstance(name, str):
            return "Новая роль"
        cleaned = DiscordValidator.clean_channel_name(name)
        if cleaned == "канал":
            return "Новая роль"
        return cleaned

    @staticmethod
    def sanitize_permissions(perms: Any) -> str:
        try:
            if isinstance(perms, str):
                perms_int = int(perms)
            elif isinstance(perms, int):
                perms_int = perms
            else:
                perms_int = 0
            if perms_int == 0:
                perms_int = 1024
            max_perms = 0x7FFFFFFFFFFFFFFF
            perms_int = perms_int & max_perms
            return str(perms_int)
        except:
            return "1024"

class RequestManager:
    def __init__(self, headers: Dict[str, str]):
        self.headers = headers.copy()
        self.ssl_context = SafeSSLContext()
        self.max_retries = 3
        self.base_delay = 1.5
        self.timeout = 30
        self.headers.setdefault('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        self.headers.setdefault('Accept', 'application/json')
        self.headers.setdefault('Accept-Language', 'en-US,en;q=0.9')
        self.headers.setdefault('Connection', 'keep-alive')

    def _handle_rate_limit(self, headers: Dict) -> float:
        retry_after = headers.get('Retry-After')
        if retry_after:
            try:
                return float(retry_after) + 0.5
            except:
                pass
        reset_after = headers.get('X-RateLimit-Reset-After')
        if reset_after:
            try:
                return float(reset_after) + 0.5
            except:
                pass
        return 2.0

    def _prepare_data(self, data: Any) -> Optional[bytes]:
        if data is None:
            return None
        if isinstance(data, dict) or isinstance(data, list):
            try:
                json_str = json.dumps(data, ensure_ascii=False)
                return json_str.encode('utf-8')
            except Exception as e:
                ошибка(f"Ошибка сериализации JSON: {e}")
                return None
        if isinstance(data, str):
            return data.encode('utf-8')
        if isinstance(data, bytes):
            return data
        try:
            return str(data).encode('utf-8')
        except:
            ошибка(f"Не удалось подготовить данные типа {type(data)}")
            return None

    def request(self, method: str, url: str, data: Any = None) -> Tuple[Optional[Any], Optional[Any]]:
        headers = self.headers.copy()
        if data is not None:
            headers['Content-Type'] = 'application/json'
        for attempt in range(self.max_retries):
            try:
                encoded_data = self._prepare_data(data)
                req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method.upper())
                with urllib.request.urlopen(req, context=self.ssl_context.get_context(), timeout=self.timeout) as response:
                    status = response.status
                    response_data = response.read()
                    if response_data:
                        try:
                            decoded = response_data.decode('utf-8', errors='ignore')
                            if decoded.strip():
                                json_data = json.loads(decoded)
                            else:
                                json_data = None
                        except json.JSONDecodeError:
                            json_data = response_data.decode('utf-8', errors='ignore')
                    else:
                        json_data = None
                    if status == 429:
                        delay = self._handle_rate_limit(response.headers)
                        предупреждение(f"Rate limit. Ждем {delay:.1f} сек...")
                        time.sleep(delay)
                        continue
                    return response, json_data
            except urllib.error.HTTPError as e:
                status = e.code
                if status == 429:
                    delay = self._handle_rate_limit(e.headers)
                    предупреждение(f"Rate limit (HTTPError). Ждем {delay:.1f} сек...")
                    time.sleep(delay)
                    continue
                elif status == 401:
                    ошибка("HTTP 401: Неверный токен")
                    return None, {"error": "Unauthorized"}
                elif status == 403:
                    ошибка("HTTP 403: Нет прав доступа")
                    return None, {"error": "Forbidden"}
                elif status == 404:
                    ошибка(f"HTTP 404: Не найдено - {url}")
                    return None, {"error": "Not Found"}
                else:
                    ошибка(f"HTTP {status}: {e.reason}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.base_delay)
                        continue
                return e, None
            except urllib.error.URLError as e:
                ошибка(f"Ошибка подключения: {e.reason}")
                time.sleep(3)
                if attempt < self.max_retries - 1:
                    continue
            except ssl.SSLError as e:
                ошибка(f"SSL ошибка: {e}")
                time.sleep(2)
                if attempt < self.max_retries - 1:
                    continue
            except Exception as e:
                ошибка(f"Неожиданная ошибка: {type(e).__name__}: {e}")
                time.sleep(2)
                if attempt < self.max_retries - 1:
                    continue
        ошибка(f"Не удалось после {self.max_retries} попыток: {method} {url}")
        return None, None

    def get(self, url: str) -> Tuple[Optional[Any], Optional[Any]]:
        return self.request('GET', url)

    def post(self, url: str, data: Any = None) -> Tuple[Optional[Any], Optional[Any]]:
        return self.request('POST', url, data)

    def delete(self, url: str) -> Tuple[Optional[Any], Optional[Any]]:
        return self.request('DELETE', url)

    def patch(self, url: str, data: Any = None) -> Tuple[Optional[Any], Optional[Any]]:
        return self.request('PATCH', url, data)

class AdvancedCloner:
    def __init__(self, token: str):
        if not DiscordValidator.validate_token(token):
            raise ValueError("Неверный формат токена Discord")
        self.token = token
        self.validator = DiscordValidator()
        self.headers = {
            'Authorization': token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        }
        self.request_manager = RequestManager(self.headers)
        self.channel_delay = 1.2
        self.role_delay = 1.5
        self.bulk_delay = 2.0
        self.cache = {}

    def _check_response(self, response, operation: str = "") -> bool:
        if response is None:
            ошибка(f"Нет ответа для операции: {operation}")
            return False
        if hasattr(response, 'status'):
            status = response.status
            if 200 <= status < 300:
                return True
            else:
                ошибка(f"Статус {status} для операции: {operation}")
                return False
        return False

    def get_server_info(self, server_id: str) -> Optional[Dict]:
        if not self.validator.validate_snowflake(server_id):
            ошибка(f"Неверный ID сервера: {server_id}")
            return None
        cache_key = f"server_{server_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        url = f'https://discord.com/api/v9/guilds/{server_id}'
        response, data = self.request_manager.get(url)
        if response and hasattr(response, 'status') and response.status == 200:
            if isinstance(data, dict):
                self.cache[cache_key] = data
                return data
            else:
                ошибка(f"Неверные данные ответа для сервера {server_id}")
        return None

    def get_servers(self) -> List[Dict]:
        url = 'https://discord.com/api/v9/users/@me/guilds'
        response, data = self.request_manager.get(url)
        if response and hasattr(response, 'status'):
            if response.status == 200:
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'message' in data:
                    ошибка(f"Ошибка Discord API: {data.get('message')}")
                else:
                    ошибка(f"Неверный формат ответа от Discord API")
            else:
                ошибка(f"HTTP {response.status} при получении серверов")
        return []

    def get_channels(self, server_id: str) -> List[Dict]:
        if not self.validator.validate_snowflake(server_id):
            ошибка(f"Неверный ID сервера: {server_id}")
            return []
        cache_key = f"channels_{server_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        url = f'https://discord.com/api/v9/guilds/{server_id}/channels'
        response, data = self.request_manager.get(url)
        if self._check_response(response, "get_channels"):
            if isinstance(data, list):
                self.cache[cache_key] = data
                return data
        return []

    def get_roles(self, server_id: str) -> List[Dict]:
        if not self.validator.validate_snowflake(server_id):
            ошибка(f"Неверный ID сервера: {server_id}")
            return []
        cache_key = f"roles_{server_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        url = f'https://discord.com/api/v9/guilds/{server_id}/roles'
        response, data = self.request_manager.get(url)
        if self._check_response(response, "get_roles"):
            if isinstance(data, list):
                self.cache[cache_key] = data
                return data
        return []

    def get_server_icon(self, server_id: str) -> Optional[str]:
        try:
            server_info = self.get_server_info(server_id)
            if not server_info or not server_info.get('icon'):
                return None
            icon_hash = server_info['icon']
            for size in [256, 128, 64]:
                try:
                    icon_url = f"https://cdn.discordapp.com/icons/{server_id}/{icon_hash}.png?size={size}"
                    req = urllib.request.Request(icon_url, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    })
                    with urllib.request.urlopen(req, timeout=30) as response:
                        if response.status == 200:
                            icon_data = response.read()
                            return base64.b64encode(icon_data).decode('utf-8')
                except Exception:
                    continue
            return None
        except Exception as e:
            предупреждение(f"Ошибка загрузки иконки сервера: {e}")
            return None

    def delete_channel(self, channel_id: str) -> bool:
        if not self.validator.validate_snowflake(channel_id):
            ошибка(f"Неверный ID канала: {channel_id}")
            return False
        url = f'https://discord.com/api/v9/channels/{channel_id}'
        response, _ = self.request_manager.delete(url)
        if self._check_response(response, "delete_channel"):
            time.sleep(self.channel_delay * 0.5)
            return True
        return False

    def create_channel(self, server_id: str, channel_data: Dict) -> Tuple[bool, Optional[Dict]]:
        if not self.validator.validate_snowflake(server_id):
            ошибка(f"Неверный ID сервера: {server_id}")
            return False, None
        sanitized_data = self._sanitize_channel_data(channel_data)
        if not sanitized_data:
            return False, None
        url = f'https://discord.com/api/v9/guilds/{server_id}/channels'
        response, data = self.request_manager.post(url, sanitized_data)
        if self._check_response(response, "create_channel"):
            time.sleep(self.channel_delay)
            return True, data if isinstance(data, dict) else None
        return False, None

    def _sanitize_channel_data(self, channel_data: Dict) -> Optional[Dict]:
        if not isinstance(channel_data, dict):
            return None
        sanitized = channel_data.copy()
        if 'name' not in sanitized:
            sanitized['name'] = "канал"
        if 'type' not in sanitized:
            sanitized['type'] = 0
        sanitized['name'] = self.validator.clean_channel_name(sanitized['name'])
        valid_types = [0, 2, 4, 5, 13, 15]
        if sanitized['type'] not in valid_types:
            предупреждение(f"Неверный тип канала {sanitized['type']}, используем 0 (текстовый)")
            sanitized['type'] = 0
        if 'parent_id' in sanitized:
            parent_id = sanitized['parent_id']
            if parent_id and not self.validator.validate_snowflake(str(parent_id)):
                предупреждение(f"Неверный parent_id: {parent_id}, удаляем")
                del sanitized['parent_id']
        if 'position' in sanitized:
            try:
                sanitized['position'] = int(sanitized['position'])
            except:
                sanitized['position'] = 0
        return sanitized

    def create_role(self, server_id: str, role_data: Dict) -> Tuple[bool, Optional[Dict]]:
        if not self.validator.validate_snowflake(server_id):
            ошибка(f"Неверный ID сервера: {server_id}")
            return False, None
        sanitized_data = self._sanitize_role_data(role_data)
        if not sanitized_data:
            return False, None
        url = f'https://discord.com/api/v9/guilds/{server_id}/roles'
        response, data = self.request_manager.post(url, sanitized_data)
        if self._check_response(response, "create_role"):
            time.sleep(self.role_delay)
            return True, data if isinstance(data, dict) else None
        return False, None

    def _sanitize_role_data(self, role_data: Dict) -> Optional[Dict]:
        if not isinstance(role_data, dict):
            return None
        sanitized = role_data.copy()
        if 'name' not in sanitized:
            sanitized['name'] = "Новая роль"
        sanitized['name'] = self.validator.clean_role_name(sanitized['name'])
        if 'color' not in sanitized:
            sanitized['color'] = 0
        try:
            color = int(sanitized['color'])
            sanitized['color'] = max(0, min(0xFFFFFF, color))
        except:
            sanitized['color'] = 0
        sanitized['permissions'] = self.validator.sanitize_permissions(
            sanitized.get('permissions', '0')
        )
        for field in ['hoist', 'mentionable']:
            if field in sanitized:
                sanitized[field] = bool(sanitized[field])
            else:
                sanitized[field] = False
        return sanitized

    def update_role_positions(self, server_id: str, position_data: List[Dict]) -> bool:
        if not self.validator.validate_snowflake(server_id):
            ошибка(f"Неверный ID сервера: {server_id}")
            return False
        if not isinstance(position_data, list) or not position_data:
            предупреждение("Нет данных о позициях")
            return True
        validated = []
        for item in position_data:
            if not isinstance(item, dict):
                continue
            if 'id' not in item or 'position' not in item:
                continue
            if not self.validator.validate_snowflake(str(item['id'])):
                предупреждение(f"Неверный ID роли в данных позиций: {item['id']}")
                continue
            try:
                position = int(item['position'])
                if position < 0:
                    предупреждение(f"Неверная позиция: {position}")
                    continue
            except:
                предупреждение(f"Неверное значение позиции: {item['position']}")
                continue
            validated.append({
                'id': str(item['id']),
                'position': position
            })
        if not validated:
            предупреждение("Нет валидных данных о позициях после проверки")
            return True
        url = f'https://discord.com/api/v9/guilds/{server_id}/roles'
        response, _ = self.request_manager.patch(url, validated)
        if self._check_response(response, "update_role_positions"):
            time.sleep(self.bulk_delay)
            return True
        return False

    def update_server_info(self, server_id: str, server_data: Dict) -> bool:
        if not self.validator.validate_snowflake(server_id):
            ошибка(f"Неверный ID сервера: {server_id}")
            return False
        url = f'https://discord.com/api/v9/guilds/{server_id}'
        response, _ = self.request_manager.patch(url, server_data)
        return self._check_response(response, "update_server_info")

    def delete_role(self, server_id: str, role_id: str) -> bool:
        if not self.validator.validate_snowflake(server_id):
            ошибка(f"Неверный ID сервера: {server_id}")
            return False
        if not self.validator.validate_snowflake(role_id):
            ошибка(f"Неверный ID роли: {role_id}")
            return False
        url = f'https://discord.com/api/v9/guilds/{server_id}/roles/{role_id}'
        response, _ = self.request_manager.delete(url)
        if self._check_response(response, "delete_role"):
            time.sleep(self.role_delay * 0.5)
            return True
        return False

    def clone_server(self, source_id: str, target_id: str) -> bool:
        try:
            clear_screen()
            заголовок("ЗАПУСК КЛОНИРОВАНИЯ")
            print(f"{BLUE}│")
            информация("Получаем информацию о серверах...")
            source_info = self.get_server_info(source_id)
            if not source_info:
                ошибка("Не удалось получить информацию об исходном сервере")
                return False
            target_info = self.get_server_info(target_id)
            if not target_info:
                ошибка("Не удалось получить информацию о целевом сервере")
                return False
            source_name = source_info.get('name', 'Неизвестный сервер')
            target_name = target_info.get('name', 'Неизвестный сервер')
            успех(f"Исходный сервер: {source_name}")
            успех(f"Целевой сервер: {target_name}")
            print(f"{BLUE}│")
            информация("Копируем название сервера...")
            name_data = {'name': source_name}
            if self.update_server_info(target_id, name_data):
                успех(f"Название скопировано: {source_name}")
            else:
                предупреждение("Не удалось скопировать название")
            print(f"{BLUE}│")
            информация("Копируем иконку сервера...")
            icon_b64 = self.get_server_icon(source_id)
            if icon_b64:
                try:
                    icon_data = {'icon': f"data:image/png;base64,{icon_b64}"}
                    if self.update_server_info(target_id, icon_data):
                        успех("Иконка сервера скопирована")
                    else:
                        предупреждение("Не удалось скопировать иконку")
                except Exception as e:
                    предупреждение(f"Ошибка при обработке иконки: {e}")
            else:
                информация("У сервера нет иконки или не удалось ее загрузить")
            print(f"{BLUE}│")
            информация("Анализируем структуры серверов...")
            source_channels = self.get_channels(source_id)
            target_channels = self.get_channels(target_id)
            source_roles = self.get_roles(source_id)
            target_roles = self.get_roles(target_id)
            успех(f"Исходный сервер: {len(source_channels)} каналов, {len(source_roles)} ролей")
            предупреждение(f"Целевой сервер: {len(target_channels)} каналов, {len(target_roles)} ролей")
            print(f"{BLUE}│")
            if not self._clean_target_server(target_id, target_channels, target_roles):
                ошибка("Не удалось очистить целевой сервер")
                return False
            if not self._clone_roles(source_roles, target_id):
                ошибка("Не удалось клонировать роли")
                return False
            if not self._clone_channels(source_channels, target_id):
                ошибка("Не удалось клонировать каналы")
                return False
            clear_screen()
            заголовок("КЛОНИРОВАНИЕ ЗАВЕРШЕНО")
            print(f"{BLUE}│")
            успех(f"Сервер '{source_name}' успешно клонирован в '{target_name}'")
            успех("Все структуры созданы в правильном порядке")
            print(f"{BLUE}│")
            успех("Перезайдите на сервер, чтобы увидеть все изменения")
            print(f"\n{BLUE}└{'─' * 63}┘")
            return True
        except Exception as e:
            ошибка(f"Критическая ошибка при клонировании: {e}")
            return False

    def _clean_target_server(self, target_id: str, channels: List[Dict], roles: List[Dict]) -> bool:
        подзаголовок("ОЧИСТКА ЦЕЛЕВОГО СЕРВЕРА")
        print(f"{BLUE}│")
        if channels:
            информация(f"Удаляем {len(channels)} каналов...")
            deleted = 0
            for channel in channels:
                if self.delete_channel(channel['id']):
                    deleted += 1
                    if deleted % 10 == 0:
                        информация(f"Удалено {deleted}/{len(channels)} каналов...")
                else:
                    ошибка(f"Не удалось удалить канал: {channel.get('name', 'Неизвестно')}")
            успех(f"Удалено каналов: {deleted}/{len(channels)}")
        time.sleep(self.bulk_delay)
        print(f"{BLUE}│")
        if roles:
            информация(f"Удаляем {len(roles)} ролей...")
            deleted = 0
            sorted_roles = sorted(roles, key=lambda x: x.get('position', 0))
            for role in sorted_roles:
                if role.get('name') == '@everyone' or role.get('managed', False):
                    continue
                if self.delete_role(target_id, role['id']):
                    deleted += 1
                    if deleted % 5 == 0:
                        информация(f"Удалено {deleted} ролей...")
                else:
                    ошибка(f"Не удалось удалить роль: {role.get('name', 'Неизвестно')}")
            успех(f"Удалено ролей: {deleted}")
        time.sleep(self.bulk_delay * 2)
        print(f"\n{BLUE}└{'─' * 63}┘")
        return True

    def _clone_roles(self, source_roles: List[Dict], target_id: str) -> bool:
        заголовок("КЛОНИРОВАНИЕ РОЛЕЙ")
        print(f"{BLUE}│")
        roles_to_create = []
        for role in source_roles:
            if role.get('name') == '@everyone' or role.get('managed', False):
                continue
            roles_to_create.append(role)
        if not roles_to_create:
            информация("Нет ролей для клонирования")
            print(f"\n{BLUE}└{'─' * 63}┘")
            return True
        успех(f"Будет создано {len(roles_to_create)} ролей")
        print(f"{BLUE}│")
        sorted_roles = sorted(roles_to_create, key=lambda x: x.get('position', 0), reverse=True)
        role_mapping = {}
        created = 0
        информация("Создаем роли...")
        for i, role in enumerate(sorted_roles, 1):
            role_name = role.get('name', f'Роль {i}')
            role_data = {
                'name': role_name,
                'color': role.get('color', 0),
                'hoist': role.get('hoist', False),
                'mentionable': role.get('mentionable', False),
                'permissions': role.get('permissions', '0')
            }
            success_create, response_data = self.create_role(target_id, role_data)
            if success_create and isinstance(response_data, dict):
                new_role_id = response_data.get('id')
                if new_role_id:
                    role_mapping[role['id']] = new_role_id
                    created += 1
                    успех(f"Создана роль: {role_name} ({i}/{len(sorted_roles)})")
                else:
                    ошибка(f"Не удалось получить ID созданной роли: {role_name}")
            else:
                ошибка(f"Ошибка создания роли: {role_name}")
            if i % 5 == 0 or i == len(sorted_roles):
                информация(f"Прогресс: {i}/{len(sorted_roles)} ролей")
        print(f"{BLUE}│")
        if role_mapping:
            информация("Обновляем порядок ролей...")
            position_updates = []
            for source_role in sorted_roles:
                source_id = source_role['id']
                if source_id in role_mapping:
                    position_updates.append({
                        'id': role_mapping[source_id],
                        'position': source_role.get('position', 0)
                    })
            if position_updates:
                self.update_role_positions(target_id, position_updates)
        успех(f"Создано ролей: {created}/{len(sorted_roles)}")
        print(f"\n{BLUE}└{'─' * 63}┘")
        return created > 0

    def _clone_channels(self, source_channels: List[Dict], target_id: str) -> bool:
        заголовок("КЛОНИРОВАНИЕ КАНАЛОВ")
        print(f"{BLUE}│")
        if not source_channels:
            информация("Нет каналов для клонирования")
            print(f"\n{BLUE}└{'─' * 63}┘")
            return True
        categories = [ch for ch in source_channels if ch.get('type') == 4]
        channels = [ch for ch in source_channels if ch.get('type') != 4]
        успех(f"Будет создано: {len(categories)} категорий и {len(channels)} каналов")
        print(f"{BLUE}│")
        category_map = {}
        if categories:
            информация("Создаем категории...")
            sorted_categories = sorted(categories, key=lambda x: x.get('position', 0))
            for i, category in enumerate(sorted_categories, 1):
                category_name = category.get('name', f'Категория {i}')
                category_data = {
                    'name': category_name,
                    'type': 4,
                    'position': category.get('position', 0)
                }
                success_create, response_data = self.create_channel(target_id, category_data)
                if success_create and isinstance(response_data, dict):
                    new_id = response_data.get('id')
                    if new_id:
                        category_map[category['id']] = new_id
                        успех(f"Создана категория: {category_name} ({i}/{len(sorted_categories)})")
                    else:
                        ошибка(f"Не удалось получить ID категории: {category_name}")
                else:
                    ошибка(f"Ошибка создания категории: {category_name}")
                if i % 3 == 0 or i == len(sorted_categories):
                    информация(f"Прогресс категорий: {i}/{len(sorted_categories)}")
        time.sleep(self.bulk_delay)
        print(f"{BLUE}│")
        if channels:
            информация("Создаем каналы...")
            sorted_channels = sorted(channels, key=lambda x: x.get('position', 0))
            created = 0
            for i, channel in enumerate(sorted_channels, 1):
                channel_name = channel.get('name', f'Канал {i}')
                channel_type = channel.get('type', 0)
                valid_types = [0, 2, 5, 13, 15]
                if channel_type not in valid_types:
                    предупреждение(f"Пропускаем тип {channel_type}: {channel_name}")
                    continue
                channel_data = {
                    'name': channel_name,
                    'type': channel_type,
                    'position': channel.get('position', 0)
                }
                parent_id = channel.get('parent_id')
                if parent_id and parent_id in category_map:
                    channel_data['parent_id'] = category_map[parent_id]
                success_create, _ = self.create_channel(target_id, channel_data)
                if success_create:
                    created += 1
                    успех(f"Создан канал: {channel_name} ({i}/{len(sorted_channels)})")
                else:
                    ошибка(f"Ошибка создания канала: {channel_name}")
                if i % 10 == 0 or i == len(sorted_channels):
                    информация(f"Прогресс каналов: {i}/{len(sorted_channels)}")
            успех(f"Создано каналов: {created}/{len(sorted_channels)}")
        print(f"\n{BLUE}└{'─' * 63}┘")
        return True

async def check_servers_async(token: str):
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    async with aiohttp.ClientSession() as session:
        try:
            clear_screen()
            заголовок("ПРОВЕРКА СЕРВЕРОВ")
            print(f"{BLUE}│")
            информация("Проверяем токен...")
            async with session.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=30) as response:
                if response.status == 200:
                    user_data = await response.json()
                    username = user_data.get('username', 'N/A')
                    discriminator = user_data.get('discriminator', '0000')
                    user_id = user_data.get('id', 'N/A')
                    успех("ТОКЕН РАБОЧИЙ!")
                    информация(f"Пользователь: {username}#{discriminator}")
                    информация(f"ID: {user_id}")
                    информация(f"Email: {user_data.get('email', 'Не указан')}")
                    print(f"{BLUE}│")
                    информация("Получаем список серверов...")
                    async with session.get('https://discord.com/api/v9/users/@me/guilds', headers=headers, timeout=30) as guilds_response:
                        if guilds_response.status == 200:
                            guilds = await guilds_response.json()
                            успех(f"Найдено серверов: {len(guilds)}")
                            подзаголовок("СПИСОК СЕРВЕРОВ")
                            for i, guild in enumerate(guilds, 1):
                                guild_id = guild.get('id', 'N/A')
                                guild_name = guild.get('name', 'Неизвестный сервер')
                                permissions = int(guild.get('permissions', 0))
                                is_admin = (permissions & 0x8) != 0
                                is_owner = guild.get('owner', False)
                                admin_badge = " [ADMIN]" if is_admin else ""
                                owner_badge = " [ВЛАДЕЛЕЦ]" if is_owner else ""
                                icon = " [ICON]" if guild.get('icon') else ""
                                print(f"{BLUE}│ {WHITE}{i:3d}. {guild_name}{admin_badge}{owner_badge}{icon}")
                                print(f"{BLUE}│     {CYAN}ID: {WHITE}{guild_id}")
                                if i < len(guilds):
                                    print(f"{BLUE}│     {BLUE}{'─' * 55}")
                            print(f"{BLUE}│")
                            успех("Все сервера успешно загружены!")
                            информация("Скопируйте ID нужного сервера для клонирования")
                        else:
                            ошибка(f"Не удалось получить серверы: {guilds_response.status}")
                else:
                    ошибка(f"Токен невалидный: {response.status}")
        except aiohttp.ClientConnectionError:
            ошибка("Ошибка подключения к Discord")
        except asyncio.TimeoutError:
            ошибка("Таймаут подключения")
        except aiohttp.ClientResponseError as e:
            ошибка(f"Ошибка ответа: {e.status} - {e.message}")
        except Exception as e:
            ошибка(f"Неожиданная ошибка: {type(e).__name__}: {e}")
        print(f"\n{BLUE}└{'─' * 63}┘")

def check_servers(token: str):
    asyncio.run(check_servers_async(token))

def check_server_menu():
    clear_screen()
    печать_баннера()
    подзаголовок("ВЫБОР СПОСОБА ВВОДА ТОКЕНА")
    print(f"{BLUE}│")
    информация("1. Ввести токен вручную")
    информация("2. Использовать токен из файла")
    информация("3. Инструкция по получению токена")
    информация("4. Назад в главное меню")
    print(f"{BLUE}│")
    choice = ввод_подсказка("Выберите вариант (1/2/3/4):").strip()
    if choice == "4":
        return
    token = ""
    if choice == "1":
        предупреждение("Внимание: Токен будет виден при вводе!")
        token = ввод_поле("Введите токен Discord").strip()
    elif choice == "2":
        token_file = "token.txt"
        if os.path.exists(token_file):
            try:
                with open(token_file, "r", encoding="utf-8") as f:
                    token = f.read().strip()
                успех(f"Токен загружен из {token_file}")
            except Exception as e:
                ошибка(f"Ошибка чтения файла: {e}")
                ввод_подсказка("Нажмите Enter для продолжения...")
                check_server_menu()
                return
        else:
            ошибка(f"Файл {token_file} не найден!")
            информация(f"Создайте файл {token_file} с вашим токеном")
            ввод_подсказка("Нажмите Enter для продолжения...")
            check_server_menu()
            return
    elif choice == "3":
        clear_screen()
        заголовок("ИНСТРУКЦИЯ ПО ПОЛУЧЕНИЮ ТОКЕНА")
        print(f"{BLUE}│")
        информация("1. Откройте Discord в браузере")
        информация("2. Нажмите F12 (DevTools)")
        информация("3. Перейдите на вкладку 'Network'")
        информация("4. Обновите страницу (F5)")
        информация("5. Найдите запрос к discord.com")
        информация("6. В разделе 'Headers' найдите 'Authorization'")
        информация("7. Скопируйте токен (начинается с букв)")
        print(f"{BLUE}│")
        предупреждение("ВАЖНО: Никому не передавайте ваш токен!")
        предупреждение("Токен дает полный доступ к вашему аккаунту!")
        print(f"\n{BLUE}└{'─' * 63}┘")
        ввод_подсказка("Нажмите Enter для возврата...")
        check_server_menu()
        return
    else:
        ошибка("Неверный выбор!")
        ввод_подсказка("Нажмите Enter для продолжения...")
        check_server_menu()
        return
    if not token:
        ошибка("Токен не может быть пустым!")
        ввод_подсказка("Нажмите Enter для продолжения...")
        check_server_menu()
        return
    if not DiscordValidator.validate_token(token):
        ошибка("Неверный формат токена!")
        информация("Токен должен быть длинной строкой (50+ символов)")
        ввод_подсказка("Нажмите Enter для продолжения...")
        check_server_menu()
        return
    check_servers(token)
    ввод_подсказка("Нажмите Enter для возврата в меню...")

def main_cloner():
    if not подтвердить_соглашение():
        clear_screen()
        заголовок("ОТМЕНА")
        print(f"{BLUE}│")
        ошибка("Вы не подтвердили пользовательское соглашение!")
        print(f"\n{BLUE}└{'─' * 63}┘")
        ввод_подсказка("Нажмите Enter для выхода...")
        return
    clear_screen()
    печать_баннера()
    подзаголовок("ВВОД ДАННЫХ ДЛЯ КЛОНИРОВАНИЯ")
    print(f"{BLUE}│")
    token = ввод_поле("Токен Discord").strip()
    if not token:
        ошибка("Токен не может быть пустым!")
        ввод_подсказка("Нажмите Enter для продолжения...")
        return
    if not DiscordValidator.validate_token(token):
        ошибка("Неверный формат токена!")
        ввод_подсказка("Нажмите Enter для продолжения...")
        return
    source_id = ввод_поле("ID исходного сервера").strip()
    if not source_id or not DiscordValidator.validate_snowflake(source_id):
        ошибка("Неверный ID исходного сервера!")
        ввод_подсказка("Нажмите Enter для продолжения...")
        return
    target_id = ввод_поле("ID целевого сервера").strip()
    if not target_id or not DiscordValidator.validate_snowflake(target_id):
        ошибка("Неверный ID целевого сервера!")
        ввод_подсказка("Нажмите Enter для продолжения...")
        return
    if source_id == target_id:
        ошибка("Исходный и целевой сервер не могут быть одинаковыми!")
        ввод_подсказка("Нажмите Enter для продолжения...")
        return
    try:
        cloner = AdvancedCloner(token)
    except ValueError as e:
        ошибка(f"Ошибка инициализации: {e}")
        ввод_подсказка("Нажмите Enter для продолжения...")
        return
    except Exception as e:
        ошибка(f"Неожиданная ошибка: {e}")
        ввод_подсказка("Нажмите Enter для продолжения...")
        return
    print(f"{BLUE}│")
    информация("Проверяем доступ к серверам...")
    servers = cloner.get_servers()
    if not servers:
        ошибка("Не удалось получить список серверов!")
        предупреждение("Проверьте токен и подключение к интернету")
        ввод_подсказка("Нажмите Enter для продолжения...")
        return
    source_exists = any(server.get('id') == source_id for server in servers)
    target_exists = any(server.get('id') == target_id for server in servers)
    if not source_exists:
        ошибка("Исходный сервер не найден в вашем списке!")
        предупреждение("Убедитесь, что вы есть на этом сервере")
        ввод_подсказка("Нажмите Enter для продолжения...")
        return
    if not target_exists:
        ошибка("Целевой сервер не найден в вашем списке!")
        предупреждение("Убедитесь, что вы есть на этом сервере")
        ввод_подсказка("Нажмите Enter для продолжения...")
        return
    успех("Оба сервера найдены и доступны!")
    print(f"{BLUE}│")
    clear_screen()
    заголовок("ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ")
    print(f"{BLUE}│")
    предупреждение("ВСЕ СУЩЕСТВУЮЩИЕ КАНАЛЫ И РОЛИ НА ЦЕЛЕВОМ СЕРВЕРЕ БУДУТ УДАЛЕНЫ!")
    print(f"{BLUE}│")
    информация("Будет скопировано:")
    информация("  • Название сервера")
    информация("  • Иконка сервера")
    информация("  • Все роли (кроме @everyone)")
    информация("  • Все категории и каналы")
    print(f"{BLUE}│")
    информация("НЕ будет скопировано:")
    информация("  • Сообщения в каналах")
    информация("  • Участники сервера")
    информация("  • Вебхуки и интеграции")
    print(f"{BLUE}│")
    ошибка("ОТМЕНИТЬ ЭТО ДЕЙСТВИЕ БУДЕТ НЕВОЗМОЖНО!")
    print(f"\n{BLUE}└{'─' * 63}┘")
    confirm = ввод_подсказка("Вы уверены, что хотите продолжить? (y/N):").strip().lower()
    if confirm not in ['y', 'yes', 'да']:
        clear_screen()
        заголовок("ОТМЕНА")
        print(f"{BLUE}│")
        ошибка("Операция отменена пользователем")
        print(f"\n{BLUE}└{'─' * 63}┘")
        ввод_подсказка("Нажмите Enter для возврата в меню...")
        return
    успех("Начинаем клонирование...")
    start_time = time.time()
    result = cloner.clone_server(source_id, target_id)
    end_time = time.time()
    elapsed = end_time - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    if result:
        clear_screen()
        заголовок("КЛОНИРОВАНИЕ УСПЕШНО ЗАВЕРШЕНО")
        print(f"{BLUE}│")
        успех(f"Время выполнения: {minutes} мин {seconds} сек")
        успех("Все структуры созданы в правильном порядке")
        успех("Перезайдите на сервер, чтобы увидеть все изменения")
    else:
        clear_screen()
        заголовок("КЛОНИРОВАНИЕ НЕ УДАЛОСЬ")
        print(f"{BLUE}│")
        ошибка("Произошла ошибка в процессе клонирования")
        предупреждение("Проверьте логи выше и попробуйте снова")
    print(f"\n{BLUE}└{'─' * 63}┘")
    ввод_подсказка("Нажмите Enter для возврата в меню...")

def main_menu():
    печать_баннера()
    подзаголовок("ГЛАВНОЕ МЕНЮ")
    print(f"{BLUE}│")
    информация("1. Клонирование сервера")
    информация("2. Проверка серверов (получить ID)")
    информация("3. Выход")
    print(f"{BLUE}│")
    choice = ввод_подсказка("Выберите вариант (1/2/3):").strip()
    if choice == "1":
        main_cloner()
        main_menu()
    elif choice == "2":
        check_server_menu()
        main_menu()
    elif choice == "3":
        clear_screen()
        заголовок("ВЫХОД")
        print(f"{BLUE}│")
        успех("До свидания! Спасибо за использование программы!")
        print(f"\n{BLUE}└{'─' * 63}┘")
        time.sleep(1)
        return
    else:
        ошибка("Неверный выбор!")
        ввод_подсказка("Нажмите Enter для продолжения...")
        main_menu()

def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{BLUE}[-] Программа прервана пользователем")
        input(f"{BLUE}[?] Нажмите Enter для выхода...")
    except Exception as e:
        print(f"\n\n{BLUE}[-] Критическая ошибка: {type(e).__name__}: {e}")
        traceback.print_exc()
        input(f"\n{BLUE}[?] Нажмите Enter для выхода...")
    finally:
        clear_screen()
        print(f"{BLUE}╔{'═' * 63}╗")
        print(f"{BLUE}║ {CYAN}{'Discord Server Cloner V3.3 - Blue Edition':^61} {BLUE}║")
        print(f"{BLUE}║ {CYAN}{'Автор: zlafik | Поддержка: @qtiq0':^61} {BLUE}║")
        print(f"{BLUE}╚{'═' * 63}╝")

if __name__ == "__main__":
    main()