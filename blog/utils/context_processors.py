from blog.models import Category


def get_categorys(self):
    categorys = Category.objects.filter(is_publish=True).order_by('ordering')
    return {'categorys': categorys}
