from apps.item.models import Category

def m_categories(request):
    categories = Category.objects.all()

    return {'m_categories': categories}