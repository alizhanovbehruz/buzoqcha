from django.contrib import admin
from .models import *

# from .models import Head, cat_offline, payment_history, \
#     Payment, sub_cat_offline, doctors, questions, pacient_info, admin_info, laboratory_analice, \
#     mskt_book, recomended_centers, connect_admin, about, detail, another_text, Group_info
#
#

# Register your models here.
#
# class Tabdetail(admin.TabularInline):
#     model = detail
#
#
# class Tababout(admin.TabularInline):
#     model = about
#
#
# class Tabulardoctor(admin.TabularInline):
#     model = cat_offline
#
#
# class Tabularadmin(admin.TabularInline):
#     model = connect_admin
#
#
# class Tabularlab_analice(admin.TabularInline):
#     model = laboratory_analice
#
#
# class TabularMSKT(admin.TabularInline):
#     model = mskt_book
#
#
# class Tabularquestion(admin.TabularInline):
#     model = questions
#
#
# class Tabularrecomended_centers(admin.TabularInline):
#     model = recomended_centers
#
#
# class base(admin.ModelAdmin):
#     inlines = [Tabdetail, Tababout, Tabulardoctor, Tabularadmin, Tabularlab_analice, TabularMSKT, Tabularquestion,
#                Tabularrecomended_centers]
#
#
# admin.site.register((sub_cat_offline,doctors, Payment, questions,
#                      pacient_info, about, cat_offline, Group_info,another_text, admin_info, laboratory_analice, recomended_centers, mskt_book))
#
# admin.site.register(Head, base)


# @admin.register(head, )
# class TagsAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'description': ('name',)}


admin.site.register((Users,Admin_bot,City, Region, Doctor, clinic))
