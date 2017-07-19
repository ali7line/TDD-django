from django.shortcuts import render, redirect

from .models import Item


def homepage(request):
    if request.method == "POST":
        Item.objects.create(text=request.POST['item_text'])
        return redirect('root')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
