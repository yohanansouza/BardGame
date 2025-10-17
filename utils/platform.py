"""
utils.platform

Funções utilitárias para detectar a plataforma e informações do ambiente.
"""
import os
import sys
import platform as _platform
import getpass

def detect_platform():
    """Detecta a plataforma e retorna um dict com informações úteis.

    Retorna:
      {
        'platform': 'android'|'ios'|'windows'|'macos'|'linux'|..., 
        'is_mobile': True|False,
        'user': username,
        'node': nodename,
        'machine': machine,
        'python': python_version
      }
    """
    plat = None
    is_mobile = False

    # Tenta detecção via Kivy, se disponível (recomendado quando app roda com Kivy)
    try:
        from kivy.utils import platform as kivy_platform
        plat = kivy_platform
    except Exception:
        plat = None

    # Se Kivy forneceu a plataforma e é mobile
    if plat in ("android", "ios"):
        is_mobile = True
        platform_name = plat
    else:
        # Heurísticas via variáveis de ambiente (Buildozer/Android)
        if any(k in os.environ for k in ("ANDROID_ARGUMENT", "ANDROID_BOOTLOGO", "KIVY_BUILD")):
            platform_name = "android"
            is_mobile = True
        else:
            sp = sys.platform
            if sp.startswith("linux"):
                platform_name = "linux"
            elif sp in ("win32", "cygwin"):
                platform_name = "windows"
            elif sp == "darwin":
                # macOS vs iOS: assumimos macOS a menos que Kivy diga iOS
                platform_name = "macos"
            else:
                platform_name = sp or "unknown"

    info = {
        'platform': platform_name,
        'is_mobile': bool(is_mobile),
        'user': getpass.getuser(),
        'node': _platform.node(),
        'machine': _platform.machine(),
        'python': _platform.python_version(),
    }

    return info


def is_mobile():
    return detect_platform().get('is_mobile', False)
