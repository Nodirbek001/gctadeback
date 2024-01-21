
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.bot.utils import bot_send_message
from apps.product.choices import CartStatusChoices
from apps.product.models import Order


@receiver(post_save, sender=Order)
def send_order_created_message(sender, instance, created, **kwargs):
    if created:
        total_price = instance.cart.total_price
        formatted_price = f"{total_price:,.0f}".replace(",", " ").replace(".00", "") + "so'm"
        message = f"""
        Status: {instance.get_status_display()}
        ID zakaz: {instance.pk}
        Name: {instance.name}
        Telefone: {instance.phone}
        Date: {timezone.now().strftime("%d.%m.%Y %H:%M")}"""

        message += f"""
        Summa: {formatted_price}
        """
        message += f"""
        http://localhost:8000/admin/product/order/{instance.id}/change"""
        instance.cart.status = CartStatusChoices.INACTIVE
        instance.cart.save()
        bot_send_message(instance.pk, message)
