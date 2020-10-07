from django.db import models
#importing User to make it available to all models that use it
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
####################genre model##################################
class Genre(models.Model):
    """Model representing a book genre."""
  #field name
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name
################language model########################################
class Language(models.Model):
    """Model representing a language"""
    name =models.CharField(max_length=100,help_text="Enter lang of book")
    

    def __str__(self):
        """String for representing the Model object(in Admin etc)"""
        return self.name

##########################boookkkkkkkk model######################
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language',on_delete=models.SET_NULL,null=True)
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    #for displaying genre in book admin
    def display_genre(self):
        """Create a string for the Genre from the first three values of the genre field (if they exist) """
        return ','.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'   
        #############################book instance model################

import uuid # Required for unique book instances

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    #null when book is available
    #this borrower var stores the user names of users who have borrowed any book instnce
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    #tuple of key-val pair->
    #key actual val stored,val is display val that user can select
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back'] 
        #ordering of due back dates when returnd in query,sorted in chronological order

        #django has some default permissions in admin but
       #here using permission  can define your own permissions to models and grant them to specific users
       #permission = (permission name,permission display value in admin)
        permissions = (("can_mark_returned","book as returned"),)


    def __str__(self):
        """String for representing the Model object."""
        #f is used for formatted string the below whole line after f is formatted
        #as book variable and Book class have a relationship so book used to call variable of
        #book class(####not sure####)
        return f'{self.id} ({self.book.title})'
    
    @property
    def is_overdue(self):
        #due_back anded with date.today to verify it is not empty
        #as empty values are not comparable and django would throw error then
        if self.due_back and date.today() > self.due_back:
            return True
        return False

#####################author class#############################

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
   #optional fields both dob and dod
    date_of_birth = models.DateField(null=True, blank=True)
    #why 'Died' used?
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    #ordering of author names first would compare on first name 
    class Meta:
        ordering = ['first_name','last_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name}, {self.last_name}'





    
