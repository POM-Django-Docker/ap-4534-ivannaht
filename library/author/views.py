from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from author.models import Author
from .forms import AuthorForm
from rest_framework import viewsets, permissions
from .serializers import AuthorSerializer


def authors_list_view(request):
    """
    Show a list of all authors. Only accessible to librarians (role == 1).
    """
    if not request.user.is_authenticated:
        from django.contrib import messages

        messages.error(request, "You must be logged in to view users.")
        return redirect("authentication:login")

    if getattr(request.user, "role", 0) != 1:
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden("You do not have permission to view this page.")

    authors = Author.objects.all().order_by("id")
    context = {"authors": authors}
    return render(request, "author/authors_list.html", context)


def author_detail_view(request, author_id):
    """
    Show details for a single author. Only accessible to librarians (role == 1).
    """
    if not request.user.is_authenticated:
        from django.contrib import messages

        messages.error(request, "You must be logged in to view author details.")
        return redirect("authentication:login")

    if getattr(request.user, "role", 0) != 1:
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden("You do not have permission to view this page.")

    try:
        a = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        from django.http import Http404

        raise Http404("Author not found")

    context = {"author_obj": a}
    if getattr(a, "role", 0) == 0:
        b = a.books.all()
        context.update({"author": a, "books": b})
    return render(request, "author/author_detail.html", context)


def add_author_view(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("author:authors_list")
    else:
        form = AuthorForm()

    return render(request, "author/add_author.html", {
        "form": form,
    })


def edit_author_view(request, author_id):
    author = get_object_or_404(Author, id=author_id)

    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect("author:authors_list")
    else:
        form = AuthorForm(instance=author)

    return render(request, "author/edit_author.html", {"form": form, "author": author})


def delete_author_view(request, author_id):
    author = get_object_or_404(Author, id=author_id)

    if request.user.role != 1:
        messages.error(request, "You do not have permission to delete authors.")
        return redirect("author:authors_list")

    if author.books.exists():
        messages.error(request, "Cannot delete an author that is linked to books.")
        return redirect("author:authors_list")

    author.delete()
    messages.success(request, "Author was removed successfully!")
    return redirect('author:authors_list')


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authors to be viewed or edited.
    """
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
