"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    #path('urlpattern',view function to be called if pattern matched,)
    #view is file name and index() is a func in that file
    path('', views.index, name='index'),
    path('books/',views.BookListView.as_view(),name='books'),
    path('book/<int:pk>',views.BookDetailView.as_view(),name ='book-detail'),
    path('authors/',views.AuthorListView.as_view(),name='au'),
    path('author/<int:pk>',views.AuthorDetailView.as_view(),name ='author-detail'),
    path('mybooks/',views.LoanedBooksByUserListView.as_view(),name='my-borrowed'),
    path('borrowedbooks/',views.LibrariansListView.as_view(),name='all-borrowed'),
    path('book/<uuid:pk>/renew/',views.renew_book_librarian, name='renew-book-librarian'),
    #    uuid=bookinstnce
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
]
