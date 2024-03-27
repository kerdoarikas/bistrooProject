from django.urls import path
from . import views

app_name = "bistrooapp_admin"

urlpatterns = [
    path("", views.menuu_list, name="menuu_list"),
    path("category/", views.CategoryListView.as_view(), name="category"),
    path("category_create/", views.CategoryCreateView.as_view(), name="category_create"),
    path("category_delete/<int:pk>", views.CategoryDeleteView.as_view(), name="category_delete"),
    path("category_update/<int:pk>", views.CategoryUpdateView.as_view(), name="category_update"),
    path("menuu_list/", views.menuu_list, name="menuu_list"),
    path("add_subline/<str:category>/", views.add_subline, name="add_subline"),
    path("add_theme/", views.add_theme, name="add_theme"),
    path("update_theme/<int:theme_id>", views.update_theme, name="update_theme"),
    path("delete_theme/<int:theme_id>", views.delete_theme, name="delete_theme"),
    path("delete_author/<int:theme_id>", views.delete_author, name="delete_author"),
    path("update_subline/<int:line_id>", views.update_subline, name="update_subline"),
    path("delete_subline/<int:line_id>", views.delete_subline, name="delete_subline"),

    path("today/", views.mytoday, name="today"),
    path("move_back/", views.move_back, name="move_back"),
    path("move_forward/", views.move_forward, name="move_forward"),

    path("duplicate_message/", views.dublicate_message, name="duplicate_message"),
    path("duplicate_menu/", views.duplicate_menu, name="duplicate_menu"),

    path("menuu_search/", views.menuu_search, name="menuu_search"),
    path("menuu_search_list/", views.menuu_search_list, name="menuu_search_list"),

    path("ajax/hide_row/", views.hide_row, name="hide_row"),

    path("logout/", views.logout_view, name="logout"),

    path("change_menuu_date/<int:line_id>", views.changeMenuuDate, name="change_menuu_date")
]
