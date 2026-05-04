"""Load legacy script modules without mutating global import paths."""

from __future__ import annotations

import importlib.util
import sys
from functools import lru_cache
from pathlib import Path
from types import ModuleType


@lru_cache(maxsize=8)
def load_script_module(module_name: str, path: str) -> ModuleType:
    """Load a Python script by path under a stable module name."""
    module_path = Path(path)
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load script module from {module_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
