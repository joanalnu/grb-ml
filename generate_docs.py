import os
import re
import yaml
import importlib
import pkgutil
import inspect
import subprocess
from pathlib import Path

# Target directory matching your Astro/Starlight structure
DOCS_DIR = Path("docs/src/content/docs/reference")
CONFIG_FILE = "pydoc-markdown.yml"
# Optional: Set your repository URL for "[source]" links like NumPy/Pandas
REPO_URL = os.environ.get("REPO_URL", "")  # e.g., "https://github.com/org/repo/blob/main"


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
        for _, name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            modules.append(name)
    return modules


def get_first_sentence(obj):
    """Extract a clean one-line summary for module index tables."""
    doc = inspect.getdoc(obj)
    if not doc:
        return "No description available."
    first_line = doc.strip().split("\n\n")[0].replace("\n", " ").strip()
    return first_line


def get_source_link(obj):
    """Generate a direct GitHub/GitLab link to the object's source code."""
    if not REPO_URL:
        return ""
    try:
        file_path = inspect.getsourcefile(obj)
        lines, start_line = inspect.getsourcelines(obj)
        rel_path = Path(file_path).resolve().relative_to(Path.cwd().resolve())
        end_line = start_line + len(lines) - 1
        return f"[[source]]({REPO_URL}/{rel_path.as_posix()}#L{start_line}-L{end_line})"
    except Exception:
        return ""


def extract_members(module_name):
    """Yields (name, type, full_path, obj) for public classes and functions defined in a module."""
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        return

    for name, obj in inspect.getmembers(module):
        if inspect.ismodule(obj) or getattr(obj, "__module__", None) != module_name:
            continue
        if name.startswith("_"):
            continue

        if inspect.isclass(obj):
            yield name, "class", f"{module_name}:{name}", obj
        elif inspect.isfunction(obj):
            yield name, "function", f"{module_name}:{name}", obj


def format_docstring_fallback(docstring):
    """Convert NumPy-style docstring sections into clean Markdown headers and lists."""
    if not docstring:
        return "_No documentation provided._"

    sections = [
        "Parameters", "Returns", "Yields", "Raises",
        "See Also", "Notes", "References", "Examples", "Attributes"
    ]
    pattern = r"^(" + "|".join(sections) + r")\n-+\n"
    formatted = re.sub(pattern, r"### \1\n", docstring, flags=re.MULTILINE)
    return formatted


def build_class_methods_summary(cls_obj):
    """Generate a Pandas-style summary table of public methods and properties for a class."""
    methods = []
    properties = []

    for name, member in inspect.getmembers(cls_obj):
        if name.startswith("_") and name != "__init__":
            continue
        if inspect.isfunction(member) or inspect.ismethod(member):
            summary = get_first_sentence(member)
            methods.append((name, summary))
        elif isinstance(member, property):
            summary = get_first_sentence(member.fget)
            properties.append((name, summary))

    md_sections = []
    if properties:
        md_sections.append("### Attributes / Properties\n\n| Property | Description |\n| :--- | :--- |")
        for name, summary in properties:
            md_sections.append(f"| `{name}` | {summary} |")
        md_sections.append("")

    if methods:
        md_sections.append("### Methods Summary\n\n| Method | Description |\n| :--- | :--- |")
        for name, summary in methods:
            md_sections.append(f"| `{name}` | {summary} |")
        md_sections.append("")

    return "\n".join(md_sections)


def generate_page(base_config, module_name, obj_name, obj_type, obj, module_dir):
    """Generates an individual, richly styled markdown page for a specific object."""
    out_file = module_dir / f"{obj_name}.md"
    full_qual_name = f"{module_name}.{obj_name}"

    # Merge base config settings with object-specific filter
    base_renderer = base_config.get("renderer", {"type": "markdown"}).copy()
    base_renderer.update({
        "render_module_header": False,
        "descriptive_class_title": False,
        "signature_code_block": True,
        "signature_with_def": True,
    })

    temp_config = {
        "loaders": [{
            "type": "python",
            "search_path": ["."],
            "modules": [module_name]
        }],
        "processors": [
            {
                "type": "filter",
                "expression": f"name == '{obj_name}' or default()",
                "documented_only": False
            },
            {"type": "smart"},
            {"type": "crossref"}
        ],
        "renderer": base_renderer
    }

    temp_file = f"temp_pydoc_{os.getpid()}.yml"
    with open(temp_file, "w") as f:
        yaml.dump(temp_config, f)

    try:
        result = subprocess.run(
            ["pydoc-markdown", "--config", temp_file],
            capture_output=True, text=True, check=True
        )
        content = result.stdout.strip()
    except subprocess.CalledProcessError:
        content = ""
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    # Fallback or enhancement if pydoc-markdown output is empty
    if not content:
        docstring = format_docstring_fallback(inspect.getdoc(obj))
        try:
            sig = str(inspect.signature(obj))
        except (ValueError, TypeError):
            sig = "()"
        prefix = "class" if obj_type == "class" else "def"
        content = f"```python\n{prefix} {full_qual_name}{sig}\n```\n\n{docstring}"

    # Build header metadata (Module path + Source link + Type badge)
    source_link = get_source_link(obj)
    badge_type = "Class" if obj_type == "class" else "Function"
    header_bar = f"**Module:** `{module_name}` | **Type:** `{badge_type}`"
    if source_link:
        header_bar += f" | {source_link}"

    # For classes, inject a Pandas-style summary table before the detailed method docs
    summary_tables = build_class_methods_summary(obj) if obj_type == "class" else ""

    frontmatter = (
        f"---\n"
        f"title: {obj_name}\n"
        f"description: API Reference for {full_qual_name}\n"
        f"---\n\n"
    )

    final_markdown = f"{frontmatter}{header_bar}\n\n{summary_tables}\n\n{content}\n"

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(final_markdown)
    print(f"  Created: {out_file}")


def generate_module_index(module_name, members, module_dir):
    """Generates a Pandas/NumPy-style module overview page with summary tables."""
    if not members:
        return

    module = importlib.import_module(module_name)
    mod_doc = inspect.getdoc(module) or f"API reference for `{module_name}`."

    classes = [m for m in members if m[1] == "class"]
    functions = [m for m in members if m[1] == "function"]

    lines = [
        "---",
        f"title: {module_name}",
        f"description: Overview of {module_name}",
        "sidebar:",
        "  order: 0",
        "---",
        "",
        mod_doc,
        ""
    ]

    if classes:
        lines.extend([
            "## Classes",
            "",
            "| Class | Description |",
            "| :--- | :--- |"
        ])
        for name, _, _, obj in classes:
            summary = get_first_sentence(obj)
            lines.append(f"| [`{name}`](./{name}/) | {summary} |")
        lines.append("")

    if functions:
        lines.extend([
            "## Functions",
            "",
            "| Function | Description |",
            "| :--- | :--- |"
        ])
        for name, _, _, obj in functions:
            summary = get_first_sentence(obj)
            lines.append(f"| [`{name}`](./{name}/) | {summary} |")
        lines.append("")

    index_file = module_dir / "index.md"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Created Module Index: {index_file}")


def main():
    config = load_config()
    packages = config.get("packages", ["my_package", "grb_ml"])
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    for pkg in packages:
        pkg_name = pkg.replace("-", "_")
        print(f"\nScanning package: {pkg_name}...")

        for module_name in get_package_modules(pkg_name):
            members = list(extract_members(module_name))
            if not members:
                continue

            # Organize into nested directories matching module hierarchy
            rel_module_path = Path(*module_name.split("."))
            module_dir = DOCS_DIR / rel_module_path
            module_dir.mkdir(parents=True, exist_ok=True)

            generate_module_index(module_name, members, module_dir)

            for obj_name, obj_type, _, obj in members:
                generate_page(config, module_name, obj_name, obj_type, obj, module_dir)


if __name__ == "__main__":
    main()
