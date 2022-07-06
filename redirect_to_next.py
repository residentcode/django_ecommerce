
def redirect_to_next(request):
    next = request.GET.get('next')
    if next:
        return next
    referer = request.META.get('HTTP_REFERER')
    if 'next' in referer:
        referer_url = referer.split('=')[1]
        return referer_url
    return request.path