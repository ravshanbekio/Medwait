from django.db.models import Q
from .models import SicknessList

def searchSickness(request):

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    get_sickness = SicknessList.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(about_sickness__icontains=search_query)
    )

    return search_query, get_sickness
