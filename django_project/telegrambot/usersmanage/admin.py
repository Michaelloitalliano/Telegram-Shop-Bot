from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import *
from .forms import *


@admin.register(User)
class UserModel(admin.ModelAdmin):
    search_fields = ('user_id', 'username')
    list_display = ('user_id', 'username', 'balance', 'count_buy', 'agreement', 'referral')
    form = UserForm

    def has_add_permission(self, request):
        return False


@admin.register(Category)
class CategoryModel(admin.ModelAdmin):
    form = CategoryForm


@admin.register(SubCategory)
class SubCategoryModel(admin.ModelAdmin):
    form = SubCategoryForm
    list_display = ('name', 'id', 'text_mode', 'parse_type', 'only_all')


@admin.register(Product)
class ProductModel(admin.ModelAdmin):
    list_display = ('name', 'cost', 'subcategory', 'no_change', 'id')
    form = ProductForm
    list_filter = ('subcategory',)


@admin.register(BotSettings)
class BotSettingsModel(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AllBuyProduct)
class AllBuyProductModel(admin.ModelAdmin):
    search_fields = ('user__user_id', 'user__username')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    list_display = ('user', 'product', 'count', 'sum', 'date')


@admin.register(LogLink)
class LogLinkModel(admin.ModelAdmin):
    search_fields = ('link',)
    list_display = ('product', 'reg', 'link')
    list_filter = ['reg','product']


@admin.register(Qiwi)
class QiwiAdmin(admin.ModelAdmin):
    list_filter = ("info",)
    ordering = ('info',)
    list_display = ('info','active')


@admin.register(PaySystem)
class PaySystemAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    list_display = ('name','active')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # list_filter = ("amount",)
    ordering = ('-date',)
    list_display = ('from_user','amount','date','pay_id')
    search_fields = ('from_user__user_id', 'from_user__username')

@admin.register(LogFileID)
class LogFileIDAdmin(admin.ModelAdmin):
    search_fields = ('user__user_id', 'user__username', 'log_name')
    ordering = ('-date',)
    list_filter = ('product',)
    list_display = ('user', 'product', 'log_name', 'date')

@admin.register(CvvHistory)
class CvvHistoryAdmin(admin.ModelAdmin):
    ordering = ('-date',)
    list_display = ('card', 'date')