# from django.conf.urls import url
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path('^$', views.index, name="credits.index"),
    path('statement/', views.statement, name='credits.statement'),
    path('contact/', views.contact, name='credits.contact'),
    path('pending_redeem/', views.pending_redeem, name="credits.pending_redeem"),
    path('verify_sms/', views.verify_sms, name="credits.verify_sms"),
    re_path(r'^redeem_cancel/$', views.redeem_cancel, name='credits.redeem_cancel'),
    path('paypal_confirm/', views.paypal_confirm, name='credits.paypal_confirm'),
    path('pending_transactions/', views.pending_transactions, name="credits.pending_transactions"),
    path('pending_transactions_paypal/', views.pending_transactions_paypal, name='credits.pending_transactions_paypal'),
    re_path(r'^transaction_cancel/$', views.transaction_cancel, name='credits.transaction_cancel'),
    path('confirm/', views.confirm, name="credits.confirm"),

]
