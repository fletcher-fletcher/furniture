import os
import requests
from urllib.parse import urlparse
import time

# Папки для сохранения
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_IMAGES_DIR = os.path.join(BASE_DIR, 'app', 'static', 'images')
PRODUCTS_DIR = os.path.join(STATIC_IMAGES_DIR, 'products')
CATEGORIES_DIR = os.path.join(STATIC_IMAGES_DIR, 'categories')

# Создаем папки если их нет
os.makedirs(PRODUCTS_DIR, exist_ok=True)
os.makedirs(CATEGORIES_DIR, exist_ok=True)

# Изображения товаров (реальные URL с Unsplash)
product_images = {
    'divan_komfort.jpg': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800',  # Диван
    'divan_uglovoy.jpg': 'https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=800',  # Угловой диван
    'kreslo_relaks.jpg': 'https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?w=800',  # Кресло
    'stolik_modern.jpg': 'https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?w=800',  # Журнальный столик
    'shkaf_grand.jpg': 'https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800',  # Шкаф-стенка
    'krovat_sonata.jpg': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800',  # Кровать
    'krovat_klassika.jpg': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800',  # Кровать классика
    'komod_praktik.jpg': 'https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800',  # Комод
    'tumba_noch.jpg': 'https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=400',  # Тумба
    'kuhnya_uyut.jpg': 'https://images.unsplash.com/photo-1556911220-bda9f9f7597e?w=800',  # Кухонный гарнитур
    'stol_semeynyy.jpg': 'https://images.unsplash.com/photo-1577140917170-285929fb55b7?w=800',  # Обеденный стол
    'stul_komfort.jpg': 'https://images.unsplash.com/photo-1592078615290-033ee584e267?w=400',  # Стул
    'shkaf_vizit.jpg': 'https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800',  # Шкаф для прихожей
    'tumba_obuv.jpg': 'https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=400',  # Тумба для обуви
    'krovat_kapitoshka.jpg': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800',  # Детская кровать
    'stol_uchenik.jpg': 'https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?w=800',  # Письменный стол
    'kreslo_direktor.jpg': 'https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?w=800',  # Офисное кресло
    'stol_biznes.jpg': 'https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?w=800',  # Письменный стол бизнес
    'stellazh_ofisnyy.jpg': 'https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800',  # Стеллаж
}

# Изображения категорий
category_images = {
    'gostinaya.jpg': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600',  # Гостиная
    'spalnya.jpg': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=600',  # Спальня
    'kuhnya.jpg': 'https://images.unsplash.com/photo-1556911220-bda9f9f7597e?w=600',  # Кухня
    'prihozhaya.jpg': 'https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=600',  # Прихожая
    'detskaya.jpg': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=600',  # Детская
    'ofis.jpg': 'https://images.unsplash.com/photo-1497215842964-222b430dc094?w=600',  # Офис
}

def download_image(url, filepath):
    """Скачивает изображение по URL и сохраняет в filepath"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"  Ошибка при скачивании {filepath}: {e}")
        return False

def create_placeholder_image(filepath, text):
    """Создает заглушку если не удалось скачать реальное изображение"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Создаем серое изображение
        img = Image.new('RGB', (800, 600), color='#CCCCCC')
        draw = ImageDraw.Draw(img)
        
        # Добавляем текст
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        # Центрируем текст
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((800 - text_width) // 2, (600 - text_height) // 2)
        
        draw.text(position, text, fill='#666666', font=font)
        img.save(filepath)
        return True
    except Exception as e:
        print(f"  Не удалось создать заглушку: {e}")
        return False

def main():
    print("Начинаем скачивание изображений...")
    print("=" * 50)
    
    # Скачиваем изображения товаров
    print("\n📦 Скачивание изображений товаров:")
    for filename, url in product_images.items():
        filepath = os.path.join(PRODUCTS_DIR, filename)
        print(f"  Скачиваю {filename}...", end=" ")
        
        if download_image(url, filepath):
            print("✓")
        else:
            print("✗ (создаю заглушку)")
            create_placeholder_image(filepath, filename.replace('.jpg', ''))
        
        time.sleep(0.5)  # Небольшая задержка чтобы не перегружать сервер
    
    # Скачиваем изображения категорий
    print("\n📁 Скачивание изображений категорий:")
    for filename, url in category_images.items():
        filepath = os.path.join(CATEGORIES_DIR, filename)
        print(f"  Скачиваю {filename}...", end=" ")
        
        if download_image(url, filepath):
            print("✓")
        else:
            print("✗ (создаю заглушку)")
            create_placeholder_image(filepath, filename.replace('.jpg', ''))
        
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("✅ Готово!")
    print(f"Изображения товаров сохранены в: {PRODUCTS_DIR}")
    print(f"Изображения категорий сохранены в: {CATEGORIES_DIR}")
    
    # Создаем файл README с информацией
    readme_path = os.path.join(STATIC_IMAGES_DIR, 'README.txt')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("Папка с изображениями магазина мебели\n")
        f.write("=" * 40 + "\n")
        f.write("products/ - изображения товаров\n")
        f.write("categories/ - изображения категорий\n")
        f.write("\nИзображения загружены с Unsplash.com\n")
    
    print(f"Создан файл: {readme_path}")

if __name__ == '__main__':
    main()