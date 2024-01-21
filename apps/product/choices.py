from django.db import models
from django.utils.translation import gettext_lazy as _

class OrderStatusChoices(models.TextChoices):
    IN_MODERATION = 'in_moderation', _('На модерации')
    SOLD = 'sold', _('Продано')
    CANCELLED = 'cancelled', _('Отменено')
class CartStatusChoices(models.TextChoices):
    ACTIVE = "active", _("Активный")
    INACTIVE = "inactive", _("Неактивный")
