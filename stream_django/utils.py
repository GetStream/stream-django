def get_class_from_string(path, default=None):
    """
    Return the class specified by the string.

    IE: django.contrib.auth.models.User
    Will return the user class or cause an ImportError
    """
    try:
        from importlib import import_module
    except ImportError:
        from django.utils.importlib import import_module
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    mod = import_module(module)
    try:
        return getattr(mod, attr)
    except AttributeError:
        if default:
            return default
        else:
            raise ImportError(
                'Cannot import name {} (from {})'.format(attr, mod))
