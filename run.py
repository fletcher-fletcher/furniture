import os
from app import app, db
from app.models import User, Category, Product, Review


def create_sample_data():
    """Создание демонстрационных данных"""
    with app.app_context():
        # Проверяем, есть ли уже данные
        if Category.query.first():
            print("Данные уже существуют, пропускаем создание.")
            return

        print("Создание демонстрационных данных...")

        # Категории с изображениями
        categories_data = [
            {'name': 'Гостиная', 'slug': 'gostinaya', 'description': 'Мебель для гостиной: диваны, кресла, столы, шкафы', 'image': 'categories/gostinaya.jpg'},
            {'name': 'Спальня', 'slug': 'spalnya', 'description': 'Кровати, матрасы, комоды, тумбы для спальни', 'image': 'categories/spalnya.jpg'},
            {'name': 'Кухня', 'slug': 'kuhnya', 'description': 'Кухонные гарнитуры, столы, стулья', 'image': 'categories/kuhnya.jpg'},
            {'name': 'Прихожая', 'slug': 'prihozhaya', 'description': 'Шкафы для прихожей, вешалки, тумбы для обуви', 'image': 'categories/prihozhaya.jpg'},
            {'name': 'Детская', 'slug': 'detskaya', 'description': 'Мебель для детской комнаты: кровати, столы, шкафы', 'image': 'categories/detskaya.jpg'},
            {'name': 'Офис', 'slug': 'ofis', 'description': 'Офисная мебель: столы, кресла, стеллажи', 'image': 'categories/ofis.jpg'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat = Category(**cat_data)
            db.session.add(cat)
            db.session.flush()
            categories[cat_data['slug']] = cat

        # Товары с изображениями
        products_data = [
            # Гостиная
            {
                'name': 'Диван "Комфорт" прямой',
                'slug': 'divan-komfort-pryamoy',
                'description': 'Удобный прямой диван с раскладным механизмом и вместительным бельевым ящиком. Обивка из велюра приятна на ощупь и легко чистится.',
                'price': 45990, 'old_price': 52990, 'stock': 15,
                'material': 'Велюр, ДСП', 'dimensions': '220x95x90 см', 'color': 'Серый', 'weight': 65,
                'category_slug': 'gostinaya', 'is_featured': True,
                'image': 'products/divan_komfort.jpg'
            },
            {
                'name': 'Диван угловой "Люкс"',
                'slug': 'divan-uglovoy-luks',
                'description': 'Угловой диван с ортопедическим основанием и большим спальным местом. Идеально подходит для ежедневного сна.',
                'price': 72990, 'old_price': 84990, 'stock': 8,
                'material': 'Рогожка, ДВП', 'dimensions': '280x180x90 см', 'color': 'Бежевый', 'weight': 95,
                'category_slug': 'gostinaya', 'is_featured': True,
                'image': 'products/divan_uglovoy.jpg'
            },
            {
                'name': 'Кресло "Релакс"',
                'slug': 'kreslo-relaks',
                'description': 'Мягкое кресло с реклайнером для максимального комфорта. Поворотный механизм 360°.',
                'price': 24990, 'old_price': None, 'stock': 20,
                'material': 'Экокожа', 'dimensions': '85x90x100 см', 'color': 'Коричневый', 'weight': 35,
                'category_slug': 'gostinaya', 'is_featured': False,
                'image': 'products/kreslo_relaks.jpg'
            },
            {
                'name': 'Журнальный столик "Модерн"',
                'slug': 'zhurnalnyy-stolik-modern',
                'description': 'Стильный журнальный столик с закаленным стеклом и хромированными ножками.',
                'price': 8990, 'old_price': 10990, 'stock': 30,
                'material': 'Закаленное стекло, металл', 'dimensions': '100x60x45 см', 'color': 'Прозрачный', 'weight': 18,
                'category_slug': 'gostinaya', 'is_featured': True,
                'image': 'products/stolik_modern.jpg'
            },
            {
                'name': 'Шкаф-стенка "Гранд"',
                'slug': 'shkaf-stenka-grand',
                'description': 'Вместительная стенка для гостиной с множеством отделений для хранения.',
                'price': 38990, 'old_price': 44990, 'stock': 5,
                'material': 'ЛДСП, МДФ', 'dimensions': '300x45x200 см', 'color': 'Венге', 'weight': 120,
                'category_slug': 'gostinaya', 'is_featured': False,
                'image': 'products/shkaf_grand.jpg'
            },
            # Спальня
            {
                'name': 'Кровать "Соната" 160x200',
                'slug': 'krovat-sonata-160x200',
                'description': 'Двуспальная кровать с мягким изголовьем и подъемным механизмом.',
                'price': 32990, 'old_price': 37990, 'stock': 12,
                'material': 'ЛДСП, велюр', 'dimensions': '170x210x110 см', 'color': 'Серый', 'weight': 75,
                'category_slug': 'spalnya', 'is_featured': True,
                'image': 'products/krovat_sonata.jpg'
            },
            {
                'name': 'Кровать "Классика" 180x200',
                'slug': 'krovat-klassika-180x200',
                'description': 'Элегантная кровать из массива дерева с резным изголовьем.',
                'price': 54990, 'old_price': 62990, 'stock': 6,
                'material': 'Массив дуба', 'dimensions': '190x210x120 см', 'color': 'Дуб', 'weight': 90,
                'category_slug': 'spalnya', 'is_featured': True,
                'image': 'products/krovat_klassika.jpg'
            },
            {
                'name': 'Комод "Практик"',
                'slug': 'komod-praktik',
                'description': 'Комод с 5 выдвижными ящиками для хранения белья и аксессуаров.',
                'price': 15990, 'old_price': 18990, 'stock': 18,
                'material': 'ЛДСП', 'dimensions': '100x45x85 см', 'color': 'Белый', 'weight': 45,
                'category_slug': 'spalnya', 'is_featured': False,
                'image': 'products/komod_praktik.jpg'
            },
            {
                'name': 'Тумба прикроватная "Ночь"',
                'slug': 'tumba-prikrovatnaya-noch',
                'description': 'Компактная прикроватная тумба с выдвижным ящиком.',
                'price': 4990, 'old_price': None, 'stock': 40,
                'material': 'ЛДСП', 'dimensions': '45x40x50 см', 'color': 'Белый', 'weight': 12,
                'category_slug': 'spalnya', 'is_featured': False,
                'image': 'products/tumba_noch.jpg'
            },
            # Кухня
            {
                'name': 'Кухонный гарнитур "Уют" 2.0м',
                'slug': 'kuhonnyy-garnitur-uyut-2m',
                'description': 'Компактный кухонный гарнитур с вместительными шкафчиками и столешницей.',
                'price': 28990, 'old_price': 33990, 'stock': 7,
                'material': 'ЛДСП, пластик', 'dimensions': '200x60x210 см', 'color': 'Белый/Дуб', 'weight': 110,
                'category_slug': 'kuhnya', 'is_featured': True,
                'image': 'products/kuhnya_uyut.jpg'
            },
            {
                'name': 'Обеденный стол "Семейный"',
                'slug': 'obedennyy-stol-semeynyy',
                'description': 'Раздвижной обеденный стол для 4-8 человек.',
                'price': 18990, 'old_price': 21990, 'stock': 14,
                'material': 'Массив дерева', 'dimensions': '120-180x80x75 см', 'color': 'Орех', 'weight': 40,
                'category_slug': 'kuhnya', 'is_featured': True,
                'image': 'products/stol_semeynyy.jpg'
            },
            {
                'name': 'Стул "Комфорт"',
                'slug': 'stul-komfort',
                'description': 'Мягкий стул с удобной спинкой.',
                'price': 3990, 'old_price': 4990, 'stock': 50,
                'material': 'Дерево, ткань', 'dimensions': '45x50x90 см', 'color': 'Серый', 'weight': 7,
                'category_slug': 'kuhnya', 'is_featured': False,
                'image': 'products/stul_komfort.jpg'
            },
            # Прихожая
            {
                'name': 'Шкаф для прихожей "Визит"',
                'slug': 'shkaf-dlya-prihozhey-vizit',
                'description': 'Шкаф с отделениями для одежды и обуви, с зеркалом.',
                'price': 19990, 'old_price': 22990, 'stock': 10,
                'material': 'ЛДСП, зеркало', 'dimensions': '120x40x200 см', 'color': 'Венге', 'weight': 65,
                'category_slug': 'prihozhaya', 'is_featured': False,
                'image': 'products/shkaf_vizit.jpg'
            },
            {
                'name': 'Тумба для обуви "Порядок"',
                'slug': 'tumba-dlya-obuvi-poryadok',
                'description': 'Тумба с 4 отделениями для обуви и мягким сиденьем.',
                'price': 7990, 'old_price': 9990, 'stock': 25,
                'material': 'ЛДСП, ткань', 'dimensions': '80x35x50 см', 'color': 'Белый', 'weight': 20,
                'category_slug': 'prihozhaya', 'is_featured': False,
                'image': 'products/tumba_obuv.jpg'
            },
            # Детская
            {
                'name': 'Кровать детская "Капитошка"',
                'slug': 'krovat-detskaya-kapitoshka',
                'description': 'Детская кровать с бортиками и ящиком для игрушек.',
                'price': 17990, 'old_price': 20990, 'stock': 9,
                'material': 'ЛДСП', 'dimensions': '160x80x70 см', 'color': 'Голубой', 'weight': 35,
                'category_slug': 'detskaya', 'is_featured': True,
                'image': 'products/krovat_kapitoshka.jpg'
            },
            {
                'name': 'Письменный стол "Ученик"',
                'slug': 'pismennyy-stol-uchenik',
                'description': 'Письменный стол с полками и выдвижным ящиком.',
                'price': 12990, 'old_price': 14990, 'stock': 16,
                'material': 'ЛДСП', 'dimensions': '120x60x75 см', 'color': 'Белый', 'weight': 30,
                'category_slug': 'detskaya', 'is_featured': False,
                'image': 'products/stol_uchenik.jpg'
            },
            # Офис
            {
                'name': 'Офисное кресло "Директор"',
                'slug': 'ofisnoe-kreslo-direktor',
                'description': 'Эргономичное офисное кресло с поддержкой поясницы.',
                'price': 22990, 'old_price': 26990, 'stock': 11,
                'material': 'Экокожа, металл', 'dimensions': '65x65x110 см', 'color': 'Черный', 'weight': 25,
                'category_slug': 'ofis', 'is_featured': True,
                'image': 'products/kreslo_direktor.jpg'
            },
            {
                'name': 'Стол письменный "Бизнес"',
                'slug': 'stol-pismennyy-biznes',
                'description': 'Просторный письменный стол с тумбой.',
                'price': 19990, 'old_price': 22990, 'stock': 8,
                'material': 'ЛДСП', 'dimensions': '160x80x75 см', 'color': 'Орех', 'weight': 55,
                'category_slug': 'ofis', 'is_featured': False,
                'image': 'products/stol_biznes.jpg'
            },
            {
                'name': 'Стеллаж "Офисный"',
                'slug': 'stellazh-ofisnyy',
                'description': 'Открытый стеллаж с 5 полками.',
                'price': 9990, 'old_price': 11990, 'stock': 22,
                'material': 'ЛДСП', 'dimensions': '90x30x180 см', 'color': 'Белый', 'weight': 30,
                'category_slug': 'ofis', 'is_featured': False,
                'image': 'products/stellazh_ofisnyy.jpg'
            },
        ]

        for prod_data in products_data:
            category_slug = prod_data.pop('category_slug')
            prod_data['category_id'] = categories[category_slug].id
            product = Product(**prod_data)
            db.session.add(product)

        # Тестовые отзывы
        reviews_data = [
            {'product_id': 1, 'user_name': 'Анна', 'rating': 5, 'text': 'Отличный диван! Очень удобный, качество на высоте. Доставили быстро, сборщики молодцы.', 'is_approved': True},
            {'product_id': 1, 'user_name': 'Михаил', 'rating': 4, 'text': 'Хороший диван за свои деньги. Единственный минус — цвет немного отличается от фото.', 'is_approved': True},
            {'product_id': 6, 'user_name': 'Елена', 'rating': 5, 'text': 'Кровать просто супер! Мягкое изголовье, удобный подъемный механизм.', 'is_approved': True},
            {'product_id': 11, 'user_name': 'Сергей', 'rating': 5, 'text': 'Стол раздвижной, очень удобно когда приходят гости. Качество дерева отличное.', 'is_approved': True},
            {'product_id': 15, 'user_name': 'Ольга', 'rating': 4, 'text': 'Купили сыну, ему очень нравится. Ящик для игрушек очень пригодился.', 'is_approved': True},
            {'product_id': 17, 'user_name': 'Алексей', 'rating': 5, 'text': 'Кресло для офиса — лучшее, что я покупал. Спина больше не болит.', 'is_approved': True},
        ]

        for review_data in reviews_data:
            review = Review(**review_data)
            db.session.add(review)

        db.session.commit()
        print("Демонстрационные данные успешно созданы!")
        print(f"  Категорий: {len(categories_data)}")
        print(f"  Товаров: {len(products_data)}")
        print(f"  Отзывов: {len(reviews_data)}")


if __name__ == '__main__':
    create_sample_data()
    app.run(debug=True, host='0.0.0.0', port=5001)