from django.db.models import Q

def searchFilter(queryset, request):
    searchSrc = request.query_params.get('search', None)
    if (searchSrc is None):
        return queryset
    # maybe add unaccent
    queryset = queryset.filter(Q(description__icontains=searchSrc)
                              |Q(name__icontains=searchSrc))
    return queryset