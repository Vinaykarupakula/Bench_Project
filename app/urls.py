from django.urls import path
from app import views

app_name = "app"

urlpatterns = [
    path('', views.index, name="index"),
    path('add_employees/', views.employees, name="home"),
    path('searchposts/',views.searchposts, name='searchposts'),
    path('date_range/',views.filter_by_date, name='filter_by_date'),
    path('download/',views.export_data, name='download'),
    path('download_search/', views.export_data_by_search, name = 'download_search'),
    path('add_employees/update/', views.edit_employees, name = 'update'),
    path('employees/delete/<int:employee_emp_id>', views.delete_employees),
    path('searchposts/update/',views.edit_employees, name = 'searhUpdate'),
    path('date_range/update/',views.edit_employees, name = 'dateUpdate')
    
    
]
