# utils.py
import pkgutil
import importlib
from dataclasses import is_dataclass

def gather_config_names(pkg):
    """
    Scan every sub-module of `pkg` and collect all top-level dataclass instance names.
    Returns a list of lists of names, e.g.:
      [['default','light','medium','heavy'],
       ['default','small','medium','large'],
       ['cube_scale','abc_scale','aec_scale']]
    """
    all_name_lists = []
    for _, mod_name, _ in pkgutil.iter_modules(pkg.__path__):
        module = importlib.import_module(f"{pkg.__name__}.{mod_name}")
        names = sorted(
            name
            for name, val in vars(module).items()
            if is_dataclass(val) and not isinstance(val, type)
        )
        if names:
            all_name_lists.append(names)
    return all_name_lists
