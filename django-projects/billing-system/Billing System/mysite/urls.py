from django.contrib import admin
from django.urls import path
from invoices import views
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from django.views.generic import RedirectView

#path('address/', view_function, name='nickname')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/home/'), name='root'),
    path('home/', views.HomePageView.as_view(), name='home'),
    path('invoices/', views.InvoiceListView.as_view(), name='all-invoices'),
    path('invoice/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoice/new/', views.InvoiceCreateView.as_view(), name='invoice-create'),
    path('invoice/<int:pk>/edit/', views.InvoiceUpdateView.as_view(), name='invoice-update'),
    path('invoice/<int:pk>/delete/', views.InvoiceDeleteView.as_view(), name='invoice-delete'),
    path('invoice//', views.add_invoice, name='add-invoice'),
    path('login/', 
         auth_views.LoginView.as_view(template_name = 'accounts/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', account_views.signup, name='signup'),

]
