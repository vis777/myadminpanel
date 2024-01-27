from django.urls import path
from myapp import views
from myapp.views import AuthorListAPIView, BookListAPIView

urlpatterns = [
    path('indexpage/', views.indexpage, name="indexpage"),
    path('admin_login/', views.admin_login, name="admin_login"),
    path('adminlogin/', views.adminlogin, name="adminlogin"),
    path('admin_logout/', views.admin_logout, name="admin_logout"),
    path('authorpage/', views.authorpage, name="authorpage"),
    path('saveauthor/', views.saveauthor, name="saveauthor"),
    path('bookpage/', views.bookpage, name="bookpage"),
    path('savebook/', views.savebook, name="savebook"),

    path('author_display/', views.author_display, name='author_display'),
    path('deleteauthor/<int:dataid>/', views.deleteauthor, name='deleteauthor'),

    path('book_display/', views.book_display, name='book_display'),
    path('editbook/<int:dataid>/', views.editbook, name='editbook'),
    path('updatebook/<int:dataid>/', views.updatebook, name='updatebook'),
    path('deletebook/<int:dataid>/', views.deletebook, name='deletebook'),
    path('authors/', AuthorListAPIView.as_view(), name='api_author_list'),
    path('books/', BookListAPIView.as_view(), name='api_book_list'),
]