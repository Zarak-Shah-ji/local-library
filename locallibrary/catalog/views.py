from django.shortcuts import render

# Create your views here.

#here we import our models,used to access data in all our views
from catalog.models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    #fetches the number of records using the objects.all()
    ####################refer using models for understanding below used things##################
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_books_word = Book.objects.filter(title__icontains='half').count
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()

    #Number of visits to this view,as counted in the session variable
    #get = Get a session value and setting default if value not present(0)
    #num_visits = session key here(sesssion variable)
    num_visits = request.session.get('num_visits',0)
    # Each time a request is received, 
    # we then increment the value and store it back in the session
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres' : num_genres,
        'num_books_word':num_books_word,
        'num_visits':num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

#The generic view will query the database
#to get all records for the specified model (Book) then render a template
#access the list of books with the template variable named object_list 
#OR book_list (i.e. generically "the_model_name_list").
class BookListView(generic.ListView):
    model = Book
    #to put them in diff pgs
    paginate_by = 2
#for more changes to this class check MDN 6

class BookDetailView(generic.DetailView):
    model =Book
    #paginate is used when more records are there and 
    
class AuthorListView(generic.ListView):
    model =Author
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model =Author

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
def email(request):
    send_mail(
        'thanks',
        'password_reset_email.html',
        'zarak.shahjee1@gmail.com',
        ['jahanzaibmalk321@gmail.com','suzainshafiq97@gmail.com'],
        fail_silently=False,
    )
    return redirect('redirect')


from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    #declare a template_name, rather than using the default, because we may end up having a few different lists of BookInstance records, with different views and templates.
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 1
    
    #In order to restrict our query to just the BookInstance objects for the current user use get_queryset()
    def get_queryset(self):
        # o = code for "on-loan"
        #order by due back so that oldest items are displayed first
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

from django.contrib.auth.mixins import PermissionRequiredMixin


class LibrariansListView(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_librarian_user.html'
    permission_required = 'catalog.can_mark_returned'
    paginate_by = 1

    def get_queryset(self):
        
        #here we filter bookinstances by status having "on loan" not required to filter by user as all loaned books to be shown
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm
#permission to restrict view to librarians only
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    # returns specified object on its pk or raises http404 exception
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    #this would not be true for first req to URL
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        #This process is called "binding" and allows us to validate the form.
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        #here all error msgs generated if form invalid
        #it runs all validation code on all the fields
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write(store) it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    #else would be used for first req to the url
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        #here we create default form passing in an intial value for renewal date
        #proposed renewal date is already written in renewal box as intial value
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        #we'll use  bookinstnce in the template to provide information about the book we're renewing
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)



from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

#defining the associated model below
from catalog.models import Author

class AuthorCreate(PermissionRequiredMixin,CreateView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    fields = '__all__'
    #dictionary of field_name:value
    initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    model = Author
    permission_required = 'catalog.can_mark_returned' 
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

#The AuthorDelete class doesn't need to display any of the fields, so these don't need to be specified. You do however need to specify the success_url, because there is no obvious default value for Django to use. 
class AuthorDelete(PermissionRequiredMixin,DeleteView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    #By default, these views will redirect on success to a page displaying the newly created/edited model item, which in our case will be the author detail view 
    #alternative redirect location by explicitly declaring parameter success_url
    success_url = reverse_lazy('au')
    #reverse_lazy() is a lazily executed version of reverse(), used here because we're providing a URL to a class-based view attribute.


from catalog.models import Book

class BookCreate(PermissionRequiredMixin,CreateView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    fields = '__all__'
    

class BookUpdate(PermissionRequiredMixin,UpdateView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    fields = '__all__'

class BookDelete(PermissionRequiredMixin,DeleteView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('books')
