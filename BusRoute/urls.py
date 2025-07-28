from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path("",views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path('add/',views.bus_route_form_view,name='add_bus_route'),
    path('bus/<int:bus_route_id>/', views.bus_route_detail_view,name="bus_route_detail"),
    path('update_route/',views.update_route,name="update-route"),
    path('bus/<int:bus_route_id>/delete/',views.delete_bus_route,name="delete_bus_route"),
    path('report-missing-items/', views.report_and_view_missing_items, name="report_and_view_missing_items"),
    path('edit-missing-item/<int:pk>/', views.edit_missing_item, name='edit_missing_item'),
    path('delete-missing-item/<int:pk>/', views.delete_missing_item, name='delete_missing_item'),
    path('update-missing-item-status/<int:pk>/', views.update_missing_item_status, name='update_missing_item_status'),
    path('driver/<int:pk>/', views.driver_profile, name='driver_profile'),
    path('all-routes/',views.all_routes,name="all_routes"),
    path('all-missing-complaints/',views.all_missing_complaints,name="all_missing_complaints"),
    path('drivers/',views.all_drivers,name="drivers"),
    path('bus-tracker',views.bus_tracker_view,name="bus_tracker_view"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

