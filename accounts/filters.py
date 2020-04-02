import django_filters
from .models import *
from django_filters import DateFilter, CharFilter

class OrderFilter(django_filters.FilterSet):  # models name and Filter.
    start_date = DateFilter(field_name="date_created", lookup_expr='gte') # greater then equal
    end_date = DateFilter(field_name="date_created", lookup_expr='lte')
    note = CharFilter(field_name="note", lookup_expr='icontains') # icontains means ignore case sensative

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created'] # i don't want these in Search form
