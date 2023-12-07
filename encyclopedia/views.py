from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from random import choice
from django import forms
from markdown2 import Markdown

from . import util


class TitleForm(forms.Form):
     title = forms.CharField(label= "Title", required=True, widget=forms.TextInput(attrs={"autofocus": "on", "autocomplete" : "off"}))


class ContentForm(forms.Form):
     content = forms.CharField(label= "", required=True, widget=forms.Textarea(attrs= {"autocomplete": "off"}))




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
        markdowner = Markdown()
        content = util.get_entry(title)
        if content is not None:
            content = markdowner.convert(content)
            return render(request, "encyclopedia/entry.html", {
                "title" : title,
                "content" : content,
            })
        else:
             return render(request, "encyclopedia/entry.html", {
                "title" : "Not found",
                "content" : f"<h1>We are not able to find <u style=\"color: red;\">{ title }</u></h1>",
             })

def results(request):
    searched_item = request.GET.get("q")
    print(searched_item)
    result = util.get_entry(searched_item)
    if result is not None:
        return HttpResponseRedirect(f"/wiki/{searched_item}")
    else:
         result_list = []
         all_entries = util.list_entries()
         for entry in all_entries:
              if entry.find(searched_item) != -1:
                   result_list.append(entry)
         return render(request, "encyclopedia/results.html",{
              "results" : result_list
         })

def new(request):
     return render(request, "encyclopedia/new.html", {
          "title_input" : TitleForm(),
          "content_input" : ContentForm(),
     })

def add(request):
    title_form = TitleForm(request.POST)
    content_form = ContentForm(request.POST)
    #server side validation
    if title_form.is_valid() and content_form.is_valid():
        title = request.POST.get("title")
        all_entries = util.list_entries()
        if title in all_entries:
            return render(request, "encyclopedia/exists.html",{
                "title" : title,
            })
        else:
            content = request.POST.get("content")
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")
    else:
         return HttpResponseRedirect("/new")

def edit(request, title):
          content = util.get_entry(title)
          form = ContentForm(initial={'content':content})
          return render(request, "encyclopedia/edit.html", {
          "content_input" : form,
          "title" : title,
     })

def change(request):
    title = request.POST.get("title")
    form = ContentForm(request.POST)
    #sever side validation
    if form.is_valid():
        content = request.POST.get("content")
        util.save_entry(title, content)
        return HttpResponseRedirect(f'/wiki/{title}')
    else:
         return HttpResponseRedirect(f"/wiki/{title}")

def random(request):
    page = choice(util.list_entries())
    return HttpResponseRedirect(f'/wiki/{page}')
