from blog.models import Category


def get_categorys(request):
    if request.user.is_authenticated:
        categorys = Category.objects.all().order_by('ordering')
    else:
        categorys = Category.objects.filter(is_publish=True).order_by('ordering')
    return {'categorys': categorys}
