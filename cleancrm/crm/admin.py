from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Leads, AccountDatas, Lead_comments

@admin.register(Leads)  # Декратерем говорим для какой модели данный класс
class LeadsAdmin(admin.ModelAdmin):
    fields = ('name', 'phone', 'request_date', 'address', 'product', 'status', 'operator', 'quantity', 'price', 'sold_date', 'regwarded', 'call_count', 'lead_calldate')
    list_display = ('id', 'name', 'phone', 'request_date', 'product', 'status')
    list_display_links = ('id', 'name', 'phone', 'request_date', 'product', 'status')
    list_filter = ('status',)
    #
    # # Метод для отправки фото с тегом в Админку
    # def get_photo(self, obj):
    #     if obj.photo:
    #         try:
    #             return mark_safe(f'<img src="{obj.photo.url}" width="40px">')
    #         except:
    #             return '-'
    #     else:
    #         return '-'

admin.site.register(Lead_comments)

@admin.register(AccountDatas)  # Декратерем говорим для какой модели данный класс
class AccountDatasAdmin(admin.ModelAdmin):
    fields = ('owner', 'role', 'gender', 'phone', 'avatar', 'last_online', 'datas')
    list_display = ('id', 'role', 'owner', 'gender', 'phone', 'last_online', 'get_avatar')
    list_display_links = ('id', 'role', 'owner', 'gender', 'phone', 'last_online', 'get_avatar')
    list_filter = ('gender', 'role')

    def get_avatar(self, obj):
        if obj.avatar:
            try:
                return mark_safe(f'<img src="{obj.avatar.url}" width="40px">')
            except:
                return '-'
        else:
            return '-'