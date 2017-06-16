from mongoengine import fields
from mongoengine import common

from . import djangoflavor


def init_module():
    """
    Create classes with Django-flavor mixins,
    use DjangoField mixin as default
    """
    import sys
    current_module = sys.modules[__name__]
    current_module.__all__ = fields.__all__

    for name in fields.__all__:
        fieldcls = getattr(fields, name)
        mixin = getattr(djangoflavor, name, djangoflavor.DjangoField)
        patched_cls = type(name, (mixin, fieldcls), {})
        setattr(current_module, name, patched_cls)
        common._class_registry_cache[name] = patched_cls

init_module()

def patch_mongoengine_field(field_name):
    """
    patch mongoengine.[field_name] for comparison support
    becouse it's required in django.forms.models.fields_for_model
    importing using mongoengine internal import cache
    """
    field = common._import_class(field_name)
    for k in ["__eq__", "__lt__", "__hash__", "attname"]:
        if not k in field.__dict__:
            setattr(field, k, djangoflavor.DjangoField.__dict__[k])

#for f in ["StringField", "ObjectIdField"]:
#    patch_mongoengine_field(f)
