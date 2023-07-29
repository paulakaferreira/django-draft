from catalog.models import Category

def supercategory_list(request):
    """Pass a list of all supercategories to every page as context"""
    supercategories = Category.objects.filter(supercategory=None) # retrieve all supercategories from database
    return {'supercategories': supercategories}
