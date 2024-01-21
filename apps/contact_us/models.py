from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from openpyxl.chart.title import Title
from django.utils.translation import gettext_lazy as _

from apps.common.model import BaseModel


class AboutUs(BaseModel):
    cover = models.ImageField(_("Cover"), upload_to="about_us", null=True, blank=True)
    title = models.CharField(_(Title), max_length=100, null=True, blank=True)
    description = RichTextUploadingField(_("Description"), null=True, blank=True)

    class Meta:
        verbose_name = _("AboutUs")
        verbose_name_plural = _("AboutUs")

    def __str__(self):
        return self.title


class Phone(BaseModel):
    phone = models.CharField(_("Phone"), max_length=13)

    class Meta:
        verbose_name = _("Phone")
        verbose_name_plural = _("Phones")


class SocialMedia(BaseModel):
    name = models.CharField(_("Name"), max_length=255)
    url = models.URLField(_("URL"), max_length=255)
    icon = models.ImageField(_("Icon"), upload_to="social_media", null=True, blank=True)

    class Meta:
        verbose_name = _("Social")
        verbose_name_plural = _("Socials")

    def __str__(self):
        return self.name

class ContactUs(BaseModel):
    phone = models.ManyToManyField(Phone, verbose_name=_("Phone"), blank=True)
    email = models.EmailField(_("Email"), max_length=255, null=True, blank=True)
    longitude = models.FloatField(_("Longitude"), null=True, blank=True)
    latitude = models.FloatField(_("Latitude"), null=True, blank=True)
    address = models.CharField(_("Address"), max_length=255)
    social_media = models.ManyToManyField(SocialMedia, verbose_name=_("Social Media"), blank=True)

    class Meta:
        verbose_name = _("Contact Us")
        verbose_name_plural = _("Contact Us")

    def __str__(self):
        return self.address


class EmployeeContact(BaseModel):
    name = models.CharField(_("Name"), max_length=255)
    image = models.ImageField(_("Image"), upload_to="employee_contact", null=True, blank=True)
    phone = models.CharField(_("Phone"), max_length=255)
    email = models.EmailField(_("Email"), max_length=255, null=True, blank=True)
    telegram_username = models.CharField(_("Telegram Username"), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("Employee Contact")
        verbose_name_plural = _("Employee Contacts")

    def __str__(self):
        return self.name


class ContactForm(BaseModel):
    name = models.CharField(_("Name"), max_length=255)
    email = models.EmailField(_("Email"), max_length=255, null=True, blank=True)
    phone = models.CharField(_("Phone"), max_length=255)
    question = models.TextField(_("Question"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Contact Form")
        verbose_name_plural = _("Contact Forms")
