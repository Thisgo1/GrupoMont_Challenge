#!/usr/bin/env python3
"""
Script de automação para executar o projeto GrupoMont Challenge.
Cria venv, instala dependências, migra banco e inicia servidor.
"""

import os
import sys
import subprocess
import platform

# Caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
VENV_DIR = os.path.join(BASE_DIR, 'venv')
REQUIREMENTS = os.path.join(BACKEND_DIR, 'requirements.txt')

# Cores para terminal (opcional)
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

def print_info(msg):
    print(f"{Colors.GREEN}[INFO]{Colors.RESET} {msg}")

def print_warn(msg):
    print(f"{Colors.YELLOW}[WARN]{Colors.RESET} {msg}")

def print_error(msg):
    print(f"{Colors.RED}[ERROR]{Colors.RESET} {msg}")

def is_windows():
    return platform.system() == 'Windows'

def get_venv_python():
    if is_windows():
        return os.path.join(VENV_DIR, 'Scripts', 'python.exe')
    return os.path.join(VENV_DIR, 'bin', 'python')

def run_command(cmd, cwd=None):
    """Executa um comando no shell e exibe saída em tempo real."""
    print_info(f"Executando: {cmd}")
    # Usa shell=True no Windows para respeitar PATH e políticas de execução
    result = subprocess.run(cmd, shell=True, cwd=cwd, text=True)
    if result.returncode != 0:
        print_error(f"Comando falhou com código {result.returncode}")
        sys.exit(result.returncode)
    return result

def create_venv():
    if os.path.exists(VENV_DIR):
        print_info("Ambiente virtual já existe. Pulando criação.")
        return
    print_info("Criando ambiente virtual...")
    run_command(f"python -m venv {VENV_DIR}")

def install_dependencies():
    print_info("Instalando dependências do backend...")
    python = get_venv_python()
    # Usa python -m pip em vez de pip.exe diretamente (resolve "Acesso negado" no Windows)
    run_command(f'"{python}" -m pip install -r "{REQUIREMENTS}"')

def run_migrations():
    print_info("Executando migrações do Django...")
    python = get_venv_python()
    manage = os.path.join(BACKEND_DIR, 'manage.py')
    run_command(f'"{python}" "{manage}" migrate', cwd=BACKEND_DIR)

def load_mock_data():
    print_info("Carregando dados de mock...")
    python = get_venv_python()
    manage = os.path.join(BACKEND_DIR, 'manage.py')
    # Verifica se o comando de importação existe, se não, avisa
    run_command(f'"{python}" "{manage}" import_csv', cwd=BACKEND_DIR)

def start_server():
    print_info("Iniciando servidor Django...")
    python = get_venv_python()
    manage = os.path.join(BACKEND_DIR, 'manage.py')
    run_command(f'"{python}" "{manage}" runserver', cwd=BACKEND_DIR)

def main():
    if not os.path.exists(BACKEND_DIR):
        print_error("Pasta 'backend/' não encontrada. Execute o script na raiz do projeto.")
        sys.exit(1)

    if not os.path.exists(REQUIREMENTS):
        print_warn("Arquivo requirements.txt não encontrado. Pulando instalação de dependências.")
    else:
        create_venv()
        install_dependencies()
        run_migrations()
        # Opcional: carregar dados de mock se existir o comando
        # load_mock_data()

    start_server()

if __name__ == "__main__":
    main()
