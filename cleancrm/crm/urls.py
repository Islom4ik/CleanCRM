from django.urls import path
from .views import login_page, crm_view, logout_view, post_lead, create_operator_view, view_operators_page, view_operator_page

urlpatterns = [
    path('', login_page, name='login'),
    path('crm/', crm_view, name='crm'),
    path('crm/operators/', view_operators_page, name='operators'),
    path('crm/operators/<int:pk>/', view_operator_page, name='operator'),
    path('logout/', logout_view, name='logout'),
    path('post-lead/', post_lead),
    path('crm/create_operator/', create_operator_view, name='create_operator'),
]