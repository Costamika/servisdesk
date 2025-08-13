#!/usr/bin/env python3
"""
Скрипт для автоматического исправления проблем качества кода в Django проекте ServisDesk.

Этот скрипт выполняет следующие действия:
1. Удаляет неиспользуемые импорты
2. Форматирует код с помощью Black
3. Сортирует импорты с помощью isort
4. Удаляет лишние пробелы
5. Проверяет безопасность с помощью Bandit
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Выполняет команду и выводит результат"""
    print(f"\n{'='*60}")
    print(f"Выполняю: {description}")
    print(f"Команда: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.stdout:
            print("Вывод:")
            print(result.stdout)
        
        if result.stderr:
            print("Ошибки:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Успешно выполнено")
        else:
            print(f"❌ Ошибка (код: {result.returncode})")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return False


def install_tools():
    """Устанавливает необходимые инструменты"""
    tools = [
        "autoflake",
        "black",
        "isort",
        "bandit",
        "flake8",
        "pylint",
        "ruff"
    ]
    
    print("Устанавливаю инструменты для анализа кода...")
    for tool in tools:
        run_command(f"pip install {tool}", f"Установка {tool}")


def remove_unused_imports():
    """Удаляет неиспользуемые импорты"""
    directories = ["tickets", "users", "servisdesk"]
    
    for directory in directories:
        if os.path.exists(directory):
            run_command(
                f"autoflake --in-place --remove-all-unused-imports --recursive {directory}/",
                f"Удаление неиспользуемых импортов в {directory}/"
            )


def format_code():
    """Форматирует код с помощью Black"""
    directories = ["tickets", "users", "servisdesk"]
    
    for directory in directories:
        if os.path.exists(directory):
            run_command(
                f"black {directory}/ --line-length=88",
                f"Форматирование кода в {directory}/ с помощью Black"
            )


def sort_imports():
    """Сортирует импорты с помощью isort"""
    directories = ["tickets", "users", "servisdesk"]
    
    for directory in directories:
        if os.path.exists(directory):
            run_command(
                f"isort {directory}/",
                f"Сортировка импортов в {directory}/ с помощью isort"
            )


def remove_trailing_whitespace():
    """Удаляет лишние пробелы в конце строк"""
    directories = ["tickets", "users", "servisdesk"]
    
    for directory in directories:
        if os.path.exists(directory):
            run_command(
                f"find {directory}/ -name '*.py' -exec sed -i 's/[[:space:]]*$//' {{}} \\;",
                f"Удаление лишних пробелов в {directory}/"
            )


def check_security():
    """Проверяет безопасность кода"""
    directories = ["tickets", "users", "servisdesk"]
    
    for directory in directories:
        if os.path.exists(directory):
            run_command(
                f"bandit -r {directory}/ -f json -o {directory}_bandit_report.json",
                f"Проверка безопасности в {directory}/ с помощью Bandit"
            )


def run_linters():
    """Запускает линтеры для проверки качества кода"""
    print("\n" + "="*60)
    print("ПРОВЕРКА КАЧЕСТВА КОДА ПОСЛЕ ИСПРАВЛЕНИЙ")
    print("="*60)
    
    # Flake8
    run_command(
        "flake8 tickets/ users/ servisdesk/ --exclude=venv,__pycache__,migrations,.git,product,logs --max-line-length=88 --count --statistics",
        "Проверка с помощью Flake8"
    )
    
    # Pylint
    run_command(
        "pylint tickets/ users/ servisdesk/ --disable=C0114,C0115,C0116 --output-format=text",
        "Проверка с помощью Pylint"
    )
    
    # Ruff (если установлен)
    run_command(
        "ruff check tickets/ users/ servisdesk/",
        "Проверка с помощью Ruff"
    )


def create_backup():
    """Создает резервную копию перед изменениями"""
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_before_fix_{timestamp}"
    
    print(f"\nСоздаю резервную копию в {backup_dir}/...")
    
    try:
        # Копируем только Python файлы
        for directory in ["tickets", "users", "servisdesk"]:
            if os.path.exists(directory):
                shutil.copytree(directory, f"{backup_dir}/{directory}")
        
        print(f"✅ Резервная копия создана: {backup_dir}/")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания резервной копии: {e}")
        return False


def main():
    """Основная функция"""
    print("🔧 ИСПРАВЛЕНИЕ КАЧЕСТВА КОДА DJANGO ПРОЕКТА SERVISDESK")
    print("="*60)
    
    # Проверяем, что мы в корневой директории проекта
    if not all(os.path.exists(d) for d in ["tickets", "users", "servisdesk"]):
        print("❌ Ошибка: Скрипт должен быть запущен в корневой директории проекта")
        sys.exit(1)
    
    # Создаем резервную копию
    if not create_backup():
        response = input("Продолжить без резервной копии? (y/N): ")
        if response.lower() != 'y':
            print("Отменено.")
            sys.exit(1)
    
    # Устанавливаем инструменты
    install_tools()
    
    # Выполняем исправления
    print("\n" + "="*60)
    print("ВЫПОЛНЕНИЕ ИСПРАВЛЕНИЙ")
    print("="*60)
    
    # 1. Удаляем неиспользуемые импорты
    remove_unused_imports()
    
    # 2. Удаляем лишние пробелы
    remove_trailing_whitespace()
    
    # 3. Сортируем импорты
    sort_imports()
    
    # 4. Форматируем код
    format_code()
    
    # 5. Проверяем безопасность
    check_security()
    
    # 6. Запускаем линтеры для проверки результата
    run_linters()
    
    print("\n" + "="*60)
    print("✅ ИСПРАВЛЕНИЯ ЗАВЕРШЕНЫ")
    print("="*60)
    print("\nРекомендации:")
    print("1. Проверьте результаты работы линтеров выше")
    print("2. Протестируйте функциональность приложения")
    print("3. Если что-то сломалось, используйте резервную копию")
    print("4. Настройте pre-commit hooks для автоматической проверки")
    print("5. Добавьте тесты для улучшения качества кода")


if __name__ == "__main__":
    main()
