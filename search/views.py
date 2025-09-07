from django.shortcuts import render

def search_test_page(request):
    return render(request, "search_test.html")
