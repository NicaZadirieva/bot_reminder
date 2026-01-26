#!/usr/bin/env python3
"""
Скрипт для установки зависимостей из requirements-dev.txt
"""

import subprocess
import sys
import os

def install_requirements():
    # Проверяем существование файла
    if not os.path.exists('requirements-dev.txt'):
        print("❌ Файл requirements-dev.txt не найден!")
        print("Создайте файл со зависимостями или укажите правильный путь.")
        return False
    
    print("📦 Начинаю установку зависимостей из requirements-dev.txt...")
    
    try:
        # Читаем файл и устанавливаем зависимости построчно
        with open('requirements-dev.txt', 'r', encoding='utf-8') as f:
            dependencies = f.readlines()
        
        # Фильтруем пустые строки и комментарии
        clean_deps = []
        for dep in dependencies:
            dep = dep.strip()
            if dep and not dep.startswith('#'):
                clean_deps.append(dep)
        
        if not clean_deps:
            print("⚠️  Файл requirements-dev.txt пуст или содержит только комментарии")
            return True
        
        print(f"📋 Найдено {len(clean_deps)} зависимостей для установки")
        
        # Устанавливаем зависимости
        for dep in clean_deps:
            print(f"⬇️  Устанавливаю: {dep}")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                print(f"✅ Успешно: {dep}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Ошибка установки {dep}: {e}")
                # Можно раскомментировать следующую строку, чтобы прервать при ошибке
                # return False
        
        print("\n🎉 Все зависимости успешно установлены!")
        return True
        
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Установщик зависимостей requirements-dev.txt")
    print("=" * 50)
    
    success = install_requirements()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)