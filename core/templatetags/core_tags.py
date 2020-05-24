from django import template
from django.db.models import Count, Sum

register =template.Library()
from ..models import Donation, Institution

@register.simple_tag
def get_total_bags_num():
    return Donation.objects.all().aggregate(total_bags=Sum('quantity'))['total_bags']

@register.simple_tag
def get_total_organizations():
    return Institution.objects.all().count()

# @register.simple_tag
# def show_fundations():
#     return Institution.objects.filter(type='Fundacja')
#
# @register.simple_tag
# def show_ngos():
#     return Institution.objects.filter(type='NGOs').order_by('-id')
#
# @register.simple_tag
# def show_local_raise():
#     return Institution.objects.filter(type='Zbiórka').order_by('-id')

