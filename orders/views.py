import os
import requests
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product, Order, OrderItem
from .forms import OrderForm

def send_order_to_telegram(order):
    """Отправляет информацию о заказе в Telegram-бота."""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")  # Теперь используем CHAT_ID

    if not bot_token:
        print("Ошибка: TELEGRAM_BOT_TOKEN не найден в .env")
        return
    if not chat_id:
        print("Ошибка: TELEGRAM_CHAT_ID не найден в .env")
        return

    # Получаем первый заказанный товар
    order_item = order.orderitem_set.first()
    if not order_item:
        print("Ошибка: заказ не содержит товаров.")
        return

    # Формируем текст сообщения
    message = (
        f"🛒 *Новый заказ!*\n"
        f"📦 *Товар:* {order_item.product.name}\n"
        f"📍 *Адрес:* {order.address}\n"
        f"📞 *Телефон:* {order.phone}\n"
        f"📦 *Количество:* {order_item.quantity}\n"
    )

    # Отправляем сообщение в Telegram
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Ошибка отправки в Telegram: {response.text}")
    except Exception as e:
        print(f"Ошибка соединения с Telegram API: {e}")

def index(request):
    return HttpResponse("Добро пожаловать в магазин цветов!")

def catalog(request):
    products = Product.objects.all()
    return render(request, 'orders/catalog.html', {'products': products})

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            product = get_object_or_404(Product, id=product_id)
            quantity = form.cleaned_data['quantity']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']

            # Создаем заказ (без привязки к пользователю)
            order = Order.objects.create(
                address=address,
                phone=phone
            )

            # Создаем связь заказа с товаром
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

            # Отправляем заказ в Telegram-бота
            send_order_to_telegram(order)

            return HttpResponse("Заказ успешно оформлен и отправлен в Telegram!")
    else:
        # При GET-запросе ожидаем параметр product_id в URL (например, ?product_id=1)
        product_id = request.GET.get('product_id')
        if not product_id:
            return HttpResponse("Нет выбранного товара.")
        form = OrderForm(initial={'product_id': product_id})

    return render(request, 'orders/order_form.html', {'form': form})
