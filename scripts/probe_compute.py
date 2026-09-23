"""Session 4: discover what compute units the CI runner exposes."""
import importlib
import inspect
import sys


def banner(text):
    print(f"\n{'=' * 60}\n{text}\n{'=' * 60}")


def introspect(module_name):
    """Dump a module's public surface, flagging compute-unit-ish names."""
    banner(f"MODULE: {module_name}")
    try:
        mod = importlib.import_module(module_name)
    except Exception as e:
        print(f"IMPORT FAILED: {type(e).__name__}: {e}")
        return None

    print(f"version: {getattr(mod, '__version__', 'unknown')}")
    print(f"file:    {getattr(mod, '__file__', 'unknown')}")

    names = [n for n in dir(mod) if not n.startswith("_")]
    print(f"\npublic names ({len(names)}):")
    for n in sorted(names):
        print(f"  {n}")

    keywords = ("compute", "unit", "device", "backend", "engine",
                "accelerator", "gpu", "cpu", "ane", "neural", "target")
    hits = [n for n in names if any(k in n.lower() for k in keywords)]
    if hits:
        print("\n*** COMPUTE-RELATED NAMES ***")
        for n in hits:
            obj = getattr(mod, n)
            print(f"\n  {n}  ({type(obj).__name__})")
            if inspect.isclass(obj):
                members = [m for m in dir(obj) if not m.startswith("_")]
                print(f"    members: {members}")
            doc = inspect.getdoc(obj)
            if doc:
                print(f"    doc: {doc.splitlines()[0][:100]}")
    return mod


def main():
    print(f"python: {sys.version}")
    for name in ("coreai_core", "coreai_torch", "coreai_opt"):
        introspect(name)

    banner("coremltools compute units (for comparison)")
    try:
        import coremltools as ct
        print(f"coremltools {ct.__version__}")
        print(f"ComputeUnit members: {[m.name for m in ct.ComputeUnit]}")
    except Exception as e:
        print(f"FAILED: {type(e).__name__}: {e}")

    banner("torch backends")
    try:
        import torch
        print(f"torch {torch.__version__}")
        print(f"mps available:  {torch.backends.mps.is_available()}")
        print(f"mps built:      {torch.backends.mps.is_built()}")
    except Exception as e:
        print(f"FAILED: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()