from pyngrok import ngrok
import time

# ВАШ ТОКЕН - нужно получить бесплатно на ngrok.com
# Зарегистрируйтесь на https://ngrok.com (через Google или email)
# В панели управления возьмите ваш auth token
AUTH_TOKEN = "ваш_токен_сюда"

# Устанавливаем токен
ngrok.set_auth_token(AUTH_TOKEN)

# Создаем туннель
public_url = ngrok.connect(5001)
print(f"\n✅ Туннель создан: {public_url}")
print("Нажмите Ctrl+C для остановки\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    ngrok.kill()
    print("\nТуннель закрыт")