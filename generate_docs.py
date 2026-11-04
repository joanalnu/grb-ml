import os
import yaml
import importlib
import pkgutil
import inspect
import subprocess
from pathlib import Path

# Target directory matching your Astro structure
DOCS_DIR = Path("docs/src/content/docs/reference")
CONFIG_FILE = "pydoc-markdown.yml"

def load_config():
    """Load the base pydoc-markdown configuration if it exists."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return yaml.safe_load(f) or {}
    return {}

def get_package_modules(package_name):
    """Recursively discover all modules within a package."""
    try:
        package = importlib.import_module(package_name)
    except ImportError as e:
        print(f"Skipping {package_name}: {e}")
        return []
    
    modules = [package.__name__]
    if hasattr(package, "__path__"):
        for _, name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            modules.append(name)
    return modules

def extract_members(module_name):
    """Yields (name, type, full_path) for all classes and functions defined in a module."""
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        return

    for name, obj in inspect.getmembers(module):
        # Ignore imported objects; only document objects originally defined in this module
        if inspect.ismodule(obj) or getattr(obj, "__module__", None) != module_name:
            continue
        
        # Exclude private/dunder methods from getting their own pages
        if name.startswith("_"):
            continue

        if inspect.isclass(obj):
            yield name, "class", f"{module_name}:{name}"
        elif inspect.isfunction(obj):
            yield name, "function", f"{module_name}:{name}"

def generate_page(obj_path, obj_name, obj_type):
    """Generates an individual markdown page for a specific object."""
    out_file = DOCS_DIR / f"{obj_name}.md"
    module_name, member_name = obj_path.split(":")
    
    # Generate a temporary pydoc-markdown YAML config to filter extraction to this specific object
    temp_config = {
        "loaders": [{"type": "python", "modules": [module_name]}],
        "processors": [{"type": "filter", "expression": f"name == '{obj_name}'"}],
        "renderer": {"type": "markdown"}
    }
    
    with open("temp_pydoc.yml", "w") as f:
        yaml.dump(temp_config, f)
        
    try:
        # Run pydoc-markdown to parse and format the docstring
        result = subprocess.run(
            ["pydoc-markdown", "--config", "temp_pydoc.yml"],
            capture_output=True, text=True, check=True
        )
        content = result.stdout.strip()
    except subprocess.CalledProcessError:
        # Fallback to direct docstring extraction if pydoc-markdown filter fails
        module = importlib.import_module(module_name)
        member = getattr(module, member_name)
        docstring = inspect.getdoc(member) or "No documentation provided."
        signature = str(inspect.signature(member)) if obj_type == "function" else ""
        content = f"```python\n{member_name}{signature}\n```\n\n{docstring}"
    finally:
        if os.path.exists("temp_pydoc.yml"):
            os.remove("temp_pydoc.yml")

    if not content:
        return

    # Prepend Astro/Starlight Frontmatter
    frontmatter = f"---\ntitle: {obj_name}\ndescription: API Reference for {module_name}.{obj_name} ({obj_type})\n---\n\n"
    
    with open(out_file, "w") as f:
        f.write(frontmatter + content)
    print(f"Created: {out_file}")

def main():
    config = load_config()
    # Default to your repo's package directories if no config specifies them
    packages = config.get("packages", ["my_package", "grb_ml"])
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    for pkg in packages:
        # Normalize package names (handles grb-ml -> grb_ml import conversion)
        pkg_name = pkg.replace("-", "_")
        print(f"\nScanning package: {pkg_name}...")
        
        for module_name in get_package_modules(pkg_name):
            for obj_name, obj_type, obj_path in extract_members(module_name):
                generate_page(obj_path, obj_name, obj_type)

if __name__ == "__main__":
    main()
