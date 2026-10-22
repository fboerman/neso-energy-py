from .nesoraw import NesoRawClient
from importlib.util import find_spec

__all__ = ["NesoRawClient"]
if find_spec("pandas") is not None:
    __all__.append("NesoClient")


def __getattr__(name):
    if name == "NesoClient":
        try:
            from .neso import NesoClient
        except ModuleNotFoundError as exc:
            if exc.name != "pandas":
                raise
            raise ImportError(
                "NesoClient requires pandas. Install it with "
                "`pip install neso-energy-py[pandas]`."
            ) from exc
        return NesoClient
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
