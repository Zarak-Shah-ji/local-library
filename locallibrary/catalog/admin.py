from django.contrib import admin

# Register your models here.
from .models import Author ,Genre, Book, BookInstance, Language

#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)
admin.site.register(Language)

###################################advanced config############################

class BookInline(admin.TabularInline):
        model = Book
        #extra attribute used to NO spare book instances by default 
        #and just add them with the Add another Book instance link,
        extra = 0

#defining the admin class to change how model is displayed,
#which inherits ModelAdmin class
class AuthorAdmin(admin.ModelAdmin):
    #list_display to add additional fields to the view. 
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    #brackets used to make tuples and to show different fields HORIZONTALLY
    fields = ['first_name','last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
#Now registering this admin class with our associated model i.e author here
admin.site.register(Author,AuthorAdmin)

#############used for inline bookinstance in add book pg########
class BooksInstanceInline(admin.TabularInline):
        model = BookInstance
        extra = 0
#############################################################

#Registering admin class for books using decorator
#!!!!imp to register before class using decorator!!!!!
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','display_genre')
    inlines = [BooksInstanceInline]

#regsitering admin class for book instance
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','id', 'status', 'due_back','borrower')
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {'fields': ('book','imprint', 'id') }),
        ('Availability', {'fields':('status','due_back','borrower') })
    )

    