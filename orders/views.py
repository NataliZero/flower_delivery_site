from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product, Order, OrderItem
from .forms import OrderForm

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
            return HttpResponse("Заказ успешно оформлен!")
    else:
        # При GET-запросе ожидаем параметр product_id в URL (например, ?product_id=1)
        product_id = request.GET.get('product_id')
        if not product_id:
            return HttpResponse("Нет выбранного товара.")
        form = OrderForm(initial={'product_id': product_id})
    return render(request, 'orders/order_form.html', {'form': form})
