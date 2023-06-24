from catalog.models import Category

def supercategory_list(request):
    supercategories = Category.objects.filter(supercategory=None) # retrieve all supercategories from database
    return {'supercategories': supercategories}
