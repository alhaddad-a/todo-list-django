from django.shortcuts import render, redirect , HttpResponse
from django.contrib.auth.decorators import login_required
from .models import ToDoList, Item
from .forms import CreateList


def home(request):
    if request.user.is_authenticated:
        total_items = 0
        completed_items = 0
        for todolist in request.user.todolist.all():
            items = todolist.item_set.all()
            total_items += items.count()
            completed_items += items.filter(complete=True).count()
        return render(request, "home.html", {
            "total_items": total_items,
            "completed_items": completed_items
        })
    return render(request, "home.html")

@login_required(login_url="/login")
def view(request):
    lists = ToDoList.objects.filter(user=request.user)
    return render(request, "view.html", {"lists": lists})

@login_required(login_url="/login")
def create(request):
    if request.method == "POST":
        form = CreateList(request.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n, user=request.user)
            t.save()
            return redirect(f"/{t.id}")
    else:
        form = CreateList()
    return render(request, "create.html", {"form": form})

@login_required(login_url="/login")
def index(request, id):
    ls = ToDoList.objects.get(id=id)
    if ls in request.user.todolist.all():
        if request.method == "POST":
            if request.POST.get("save"):
                for item in ls.item_set.all():
                    if request.POST.get("c"+str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
            elif request.POST.get("newItem"):
                txt = request.POST.get("new")
                if len(txt) > 0:
                    ls.item_set.create(text=txt, complete=False)
            else:
                for item in ls.item_set.all():
                    delete_key = f"delete{item.id}"
                    if delete_key in request.POST:
                        item.delete()
                        return redirect(f"/{id}")
        return render(request, "list.html", {"ls": ls})
    return redirect("/view")
