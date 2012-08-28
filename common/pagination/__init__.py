def paginate(request):
    try:
        page = int(request.REQUEST.get('page', '1'))
    except ValueError:
        page = 1
    return {"page": page}
