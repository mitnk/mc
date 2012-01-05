def forbid_ie67(request):
    flags = {}
    ua = request.META.get("HTTP_USER_AGENT", '').lower()
    if 'msie 6' in ua or 'msie 7' in ua:
        flags["is_ie67"] = True
    return flags
