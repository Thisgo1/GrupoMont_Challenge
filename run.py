#!/usr/bin/env python3
"""
Script de automação para executar o projeto GrupoMont Challenge.
<<<<<<< HEAD
Cria venv, instala dependências, migra banco, carrega dados mock e inicia servidor.
=======
Cria venv, instala dependências, migra banco e inicia servidor.
>>>>>>> ebe9cb67065704b6a95a87ca70df959bc3f0443a
"""

import os
import sys
import subprocess
import platform
<<<<<<< HEAD
import argparse

=======

# Caminhos
>>>>>>> ebe9cb67065704b6a95a87ca70df959bc3f0443a
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
VENV_DIR = os.path.join(BASE_DIR, 'venv')
REQUIREMENTS = os.path.join(BACKEND_DIR, 'requirements.txt')
<<<<<<< HEAD
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

=======

# Cores para terminal (opcional)
>>>>>>> ebe9cb67065704b6a95a87ca70df959bc3f0443a
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

<<<<<<< HEAD
def run_command(cmd, cwd=None, check=True):
    print_info(f"Executando: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, text=True)
    if check and result.returncode != 0:
=======
def run_command(cmd, cwd=None):
    """Executa um comando no shell e exibe saída em tempo real."""
    print_info(f"Executando: {cmd}")
    # Usa shell=True no Windows para respeitar PATH e políticas de execução
    result = subprocess.run(cmd, shell=True, cwd=cwd, text=True)
    if result.returncode != 0:
>>>>>>> ebe9cb67065704b6a95a87ca70df959bc3f0443a
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
<<<<<<< HEAD
    if not os.path.exists(REQUIREMENTS):
        print_warn("requirements.txt não encontrado. Pulando instalação.")
        return
    print_info("Instalando dependências do backend...")
    python = get_venv_python()
    run_command(f'"{python}" -m pip install --upgrade pip')
    run_command(f'"{python}" -m pip install -r "{REQUIREMENTS}"')

def install_frontend_dependencies():
    if not os.path.exists(FRONTEND_DIR):
        print_warn("Pasta frontend/ não encontrada. Pulando.")
        return
    print_info("Instalando dependências do frontend...")
    run_command("npm install", cwd=FRONTEND_DIR)

=======
    print_info("Instalando dependências do backend...")
    python = get_venv_python()
    # Usa python -m pip em vez de pip.exe diretamente (resolve "Acesso negado" no Windows)
    run_command(f'"{python}" -m pip install -r "{REQUIREMENTS}"')

>>>>>>> ebe9cb67065704b6a95a87ca70df959bc3f0443a
def run_migrations():
    print_info("Executando migrações do Django...")
    python = get_venv_python()
    manage = os.path.join(BACKEND_DIR, 'manage.py')
    run_command(f'"{python}" "{manage}" migrate', cwd=BACKEND_DIR)

def load_mock_data():
<<<<<<< HEAD
    print_info("Carregando dados de mock (isso pode levar alguns segundos)...")
    python = get_venv_python()
    manage = os.path.join(BACKEND_DIR, 'manage.py')
    run_command(f'"{python}" "{manage}" load_mock_data --reset', cwd=BACKEND_DIR)

def start_server(port):
    print_info(f"Iniciando servidor Django na porta {port}...")
    python = get_venv_python()
    manage = os.path.join(BACKEND_DIR, 'manage.py')
    run_command(f'"{python}" "{manage}" runserver 0.0.0.0:{port}', cwd=BACKEND_DIR)

def main():
    parser = argparse.ArgumentParser(description="Gerencia o projeto GrupoMont Challenge.")
    parser.add_argument("--no-mock", action="store_true", help="Pula o carregamento dos dados de mock.")
    parser.add_argument("--port", type=int, default=8000, help="Porta para o servidor Django (padrão: 8000).")
    parser.add_argument("--frontend", action="store_true", help="Instala dependências do frontend também.")
    args = parser.parse_args()

=======
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
>>>>>>> ebe9cb67065704b6a95a87ca70df959bc3f0443a
    if not os.path.exists(BACKEND_DIR):
        print_error("Pasta 'backend/' não encontrada. Execute o script na raiz do projeto.")
        sys.exit(1)

<<<<<<< HEAD
    create_venv()
    install_dependencies()

    if args.frontend:
        install_frontend_dependencies()

    run_migrations()

    if not args.no_mock:
        load_mock_data()
    else:
        print_warn("Pulando carregamento de dados mock (--no-mock).")

    start_server(args.port)
=======
    if not os.path.exists(REQUIREMENTS):
        print_warn("Arquivo requirements.txt não encontrado. Pulando instalação de dependências.")
    else:
        create_venv()
        install_dependencies()
        run_migrations()
        # Opcional: carregar dados de mock se existir o comando
        # load_mock_data()

    start_server()
>>>>>>> ebe9cb67065704b6a95a87ca70df959bc3f0443a

if __name__ == "__main__":
    main()
