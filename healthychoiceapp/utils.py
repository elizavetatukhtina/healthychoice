from django.utils.text import slugify

def unique_slug_generator(model_istance, title, slug_field):
    slug = slugify(title)
    model_class = model_istance.__class__

    while model_class.__default_manager.filter(slug=slug).exists():
        object_pk = model_class.__default_manager.latest('pk')
        object_pk = object_pk.pk + 1

        slug = f'{slug}-{object_pk}'

    return slug
