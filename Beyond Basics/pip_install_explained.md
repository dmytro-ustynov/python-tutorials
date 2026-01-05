# How pip install Works - Under the Hood

## What is pip?

`pip` stands for "Pip Installs Packages" (recursive acronym). It's Python's package installer that downloads and installs packages from the Python Package Index (PyPI) and other sources.

## The Journey of `pip install requests`

Let's trace what happens when you run this simple command:

```bash
pip install requests
```

### Step 1: Resolving the Package Name

1. **pip checks command-line arguments**: Package name is `requests`
2. **Checks if it's already installed**: Looks in `site-packages`
3. **Determines where to look**: Default is PyPI (https://pypi.org)

### Step 2: Querying PyPI

pip makes an HTTPS request to PyPI's API:

```
GET https://pypi.org/pypi/requests/json
```

PyPI responds with JSON metadata:
```json
{
  "info": {
    "name": "requests",
    "version": "2.31.0",
    "summary": "Python HTTP for Humans.",
    "requires_python": ">=3.7"
  },
  "releases": {
    "2.31.0": [
      {
        "filename": "requests-2.31.0-py3-none-any.whl",
        "url": "https://files.pythonhosted.org/packages/.../requests-2.31.0-py3-none-any.whl",
        "requires_dist": [
          "charset-normalizer (<4,>=2)",
          "idna (<4,>=2.5)",
          "urllib3 (<3,>=1.21.1)",
          "certifi (>=2017.4.17)"
        ]
      }
    ]
  }
}
```

### Step 3: Dependency Resolution

pip sees that `requests` requires:
- `charset-normalizer (<4,>=2)`
- `idna (<4,>=2.5)`
- `urllib3 (<3,>=1.21.1)`
- `certifi (>=2017.4.17)`

For each dependency, pip:
1. Checks if it's already installed with compatible version
2. If not, queries PyPI for that package
3. Recursively resolves its dependencies
4. Builds a dependency tree

**Example dependency tree:**
```
requests==2.31.0
├── charset-normalizer==3.2.0
├── idna==3.4
├── urllib3==2.0.4
└── certifi==2023.7.22
```

### Step 4: Downloading Packages

pip downloads packages in one of two formats:

#### Wheel Files (.whl) - Preferred
```
requests-2.31.0-py3-none-any.whl
```

Filename breakdown:
- `requests`: Package name
- `2.31.0`: Version
- `py3`: Python 3 compatible
- `none`: No ABI (Application Binary Interface) requirement
- `any`: Works on any platform

Wheels are **pre-built** - just unzip and copy!

#### Source Distributions (.tar.gz) - Fallback
```
requests-2.31.0.tar.gz
```

Contains source code that must be built before installation.

pip prefers wheels because they're faster (no build step needed).

### Step 5: Installing Packages

For wheel files:
```bash
# pip essentially does:
1. Unzip the .whl file
2. Copy files to site-packages/
3. Create metadata in site-packages/requests-2.31.0.dist-info/
4. Update scripts in bin/ (if package has command-line tools)
```

Directory structure after installation:
```
site-packages/
├── requests/
│   ├── __init__.py
│   ├── api.py
│   ├── models.py
│   └── ...
└── requests-2.31.0.dist-info/
    ├── METADATA
    ├── WHEEL
    ├── RECORD
    └── top_level.txt
```

### Step 6: Creating Entry Points

If the package has console scripts (e.g., `pip` itself), pip creates executable scripts:

```python
# In site-packages/../bin/pip (simplified)
#!/path/to/python
import sys
from pip._internal.cli.main import main

if __name__ == '__main__':
    sys.exit(main())
```

## How `pip install -r requirements.txt` Works

### The requirements.txt Format

```txt
# Basic package
requests

# Specific version
flask==2.3.0

# Version range
django>=4.0,<5.0

# From Git repository
git+https://github.com/user/repo.git@main

# From local directory
./my-local-package

# With extras
celery[redis,auth]

# From specific index
--index-url https://my-private-pypi.com/simple/
my-private-package

# Comments are allowed
numpy>=1.20  # Required for data processing
```

### Processing Requirements File

When you run:
```bash
pip install -r requirements.txt
```

pip does this:

1. **Reads the file line by line**
2. **Parses each requirement** (version specifiers, URLs, etc.)
3. **Builds a list of all packages to install**
4. **Resolves dependencies for ALL packages together**
5. **Checks for conflicts** (e.g., package A needs X<2.0, package B needs X>=2.0)
6. **Downloads and installs in correct order** (dependencies first)

### Dependency Resolution Example

requirements.txt:
```txt
flask==2.3.0
requests==2.31.0
```

pip resolves:
```
flask==2.3.0
├── Werkzeug>=2.3.0
├── Jinja2>=3.0
├── click>=8.0
├── itsdangerous>=2.0
└── (no specific requests requirement)

requests==2.31.0
├── charset-normalizer
├── idna
├── urllib3
└── certifi
```

Installation order (dependencies first):
1. charset-normalizer, idna, urllib3, certifi
2. requests
3. Werkzeug, Jinja2, click, itsdangerous
4. flask

## Package Structure - What Gets Installed

### A Simple Package

```
my-package/
├── setup.py or pyproject.toml    # Package metadata
├── my_package/                     # Actual Python code
│   ├── __init__.py
│   ├── module1.py
│   └── module2.py
├── tests/
└── README.md
```

### setup.py Example

```python
from setuptools import setup, find_packages

setup(
    name='my-package',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
        'click>=8.0',
    ],
    entry_points={
        'console_scripts': [
            'my-command=my_package.cli:main',
        ],
    },
    python_requires='>=3.8',
)
```

### Modern: pyproject.toml (PEP 518)

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "1.0.0"
dependencies = [
    "requests>=2.25.0",
    "click>=8.0",
]
requires-python = ">=3.8"

[project.scripts]
my-command = "my_package.cli:main"
```

## Where Packages Come From

### 1. PyPI (Python Package Index)

Default source: https://pypi.org

```bash
pip install requests  # Downloads from PyPI
```

### 2. Alternative Indexes

```bash
# Use different index
pip install --index-url https://test.pypi.org/simple/ my-package

# Add extra index (search both)
pip install --extra-index-url https://my-company-pypi.com/simple/ private-pkg
```

### 3. Git Repositories

```bash
# Install from GitHub
pip install git+https://github.com/psf/requests.git

# Specific branch/tag
pip install git+https://github.com/psf/requests.git@v2.31.0

# With subdirectory
pip install git+https://github.com/user/repo.git#subdirectory=packages/mypackage
```

### 4. Local Files

```bash
# From wheel file
pip install ./downloads/requests-2.31.0-py3-none-any.whl

# From source directory (development mode)
pip install -e ./my-package  # Editable install
```

## Advanced: Dependency Resolution Algorithm

### The Problem: Constraint Satisfaction

Given:
- Package A requires X>=1.0,<2.0
- Package B requires X>=1.5,<3.0
- Package C requires Y==2.0
- Package X version 1.8 requires Y>=1.5,<2.5

pip must find versions that satisfy ALL constraints.

### Resolution Strategy (Simplified)

1. **Build constraint set**:
   - Collect all version requirements for each package

2. **Find compatible versions**:
   - For each package, find versions that satisfy all constraints

3. **Backtracking**:
   - If no valid version found, backtrack and try different combinations

4. **Install order**:
   - Topological sort of dependency graph

### Real Example

```bash
pip install 'flask==2.0.0' 'jinja2==3.1.0'
```

Problem:
- flask==2.0.0 requires jinja2>=2.11.0,<4.0
- But you asked for jinja2==3.1.0 (compatible!)

Result: Installs both successfully.

But:
```bash
pip install 'flask==2.0.0' 'jinja2==4.0.0'
```

Problem:
- flask==2.0.0 requires jinja2<4.0
- You asked for jinja2==4.0.0 (incompatible!)

Result: Error!
```
ERROR: Cannot install flask==2.0.0 and jinja2==4.0.0 because these package
versions have conflicting dependencies.
```

## How Packages Are Distributed

### Creating a Wheel

```bash
# In your package directory
python -m build

# Creates:
# dist/my_package-1.0.0-py3-none-any.whl
# dist/my_package-1.0.0.tar.gz
```

Inside the wheel (it's just a ZIP file):
```bash
unzip -l my_package-1.0.0-py3-none-any.whl

my_package/__init__.py
my_package/module1.py
my_package-1.0.0.dist-info/METADATA
my_package-1.0.0.dist-info/WHEEL
my_package-1.0.0.dist-info/RECORD
```

### Uploading to PyPI

```bash
# Install twine
pip install twine

# Upload
twine upload dist/*

# Now anyone can:
pip install my-package
```

## pip Internals: Key Concepts

### site-packages Directory

Where packages live:
```bash
python -c "import site; print(site.getsitepackages())"
# /usr/local/lib/python3.11/site-packages
```

### dist-info Metadata

Each installed package has metadata:
```
site-packages/requests-2.31.0.dist-info/
├── METADATA          # Package info, dependencies
├── WHEEL             # Wheel format version
├── RECORD            # All installed files (for uninstall)
├── INSTALLER         # Who installed it (pip)
└── top_level.txt     # Top-level import names
```

METADATA example:
```
Metadata-Version: 2.1
Name: requests
Version: 2.31.0
Summary: Python HTTP for Humans.
Home-page: https://requests.readthedocs.io
Author: Kenneth Reitz
Requires-Python: >=3.7
Requires-Dist: charset-normalizer (<4,>=2)
Requires-Dist: idna (<4,>=2.5)
Requires-Dist: urllib3 (<3,>=1.21.1)
Requires-Dist: certifi (>=2017.4.17)
```

### How pip Knows What to Uninstall

RECORD file lists every installed file:
```
requests/__init__.py,sha256=...,12345
requests/api.py,sha256=...,67890
requests/models.py,sha256=...,11111
...
```

```bash
pip uninstall requests
# Removes all files listed in RECORD
```

## Practical Examples

### Example 1: Freezing Dependencies

```bash
# Install packages for your project
pip install flask sqlalchemy redis

# Save exact versions
pip freeze > requirements.txt
```

requirements.txt:
```txt
blinker==1.6.2
click==8.1.6
Flask==2.3.3
greenlet==2.0.2
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.3
redis==4.6.0
SQLAlchemy==2.0.19
Werkzeug==2.3.6
```

Notice: All dependencies (not just top-level) with exact versions!

### Example 2: Upgrading Packages

```bash
# Upgrade single package
pip install --upgrade requests

# Upgrade all packages from requirements.txt
pip install --upgrade -r requirements.txt

# See what would be upgraded
pip list --outdated
```

### Example 3: Development Dependencies

requirements-dev.txt:
```txt
# Include production requirements
-r requirements.txt

# Add development tools
pytest>=7.0
black>=23.0
flake8>=6.0
mypy>=1.0
```

Install:
```bash
pip install -r requirements-dev.txt
```

### Example 4: Editable Install

For developing your own package:
```bash
# Clone your package
git clone https://github.com/you/my-package.git
cd my-package

# Install in editable mode
pip install -e .

# Now changes to source code are immediately reflected
# No need to reinstall after each edit!
```

This creates a .egg-link file in site-packages pointing to your source directory.

### Example 5: Installing from Private Git

requirements.txt:
```txt
# Public package
requests==2.31.0

# Private company package from Git
git+https://github.com/company/private-lib.git@v1.2.3

# With SSH (for authentication)
git+ssh://git@github.com/company/secret-lib.git@main
```

## Common Issues and Solutions

### Issue 1: Dependency Conflicts

```bash
pip install packageA packageB
# ERROR: Cannot install packageA and packageB because these package
# versions have conflicting dependencies.
```

**Solutions:**
1. Find compatible versions manually
2. Use pip's new resolver (default in pip 20.3+):
   ```bash
   pip install --use-feature=2020-resolver packageA packageB
   ```
3. Use dependency management tools like Poetry or Pipenv

### Issue 2: SSL Certificate Errors

```bash
pip install requests
# ERROR: Could not fetch URL... SSL: CERTIFICATE_VERIFY_FAILED
```

**Solutions:**
```bash
# Temporary fix (not recommended for production)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org requests

# Better: Fix system certificates
# On Mac:
/Applications/Python\ 3.11/Install\ Certificates.command
```

### Issue 3: Permission Denied

```bash
pip install requests
# ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Solutions:**
```bash
# Use virtual environment (recommended!)
python -m venv venv
source venv/bin/activate
pip install requests

# Or user install (not ideal)
pip install --user requests
```

### Issue 4: Package Not Found

```bash
pip install non-existent-package
# ERROR: Could not find a version that satisfies the requirement
```

**Troubleshooting:**
1. Check spelling on PyPI.org
2. Package might be Python 2 only
3. Check if package was removed from PyPI
4. Verify you're using correct index URL

## Best Practices

### 1. Pin Your Dependencies

Bad:
```txt
flask
requests
```

Good:
```txt
flask==2.3.3
requests==2.31.0
```

Better (with hashes for security):
```txt
flask==2.3.3 \
    --hash=sha256:77fd4e1249d8c9923de34907236b747ced06e5467ecac1a419ed39e1f3d929b3
```

Generate with:
```bash
pip freeze --all > requirements.txt
# Or with hashes:
pip-compile --generate-hashes requirements.in
```

### 2. Separate Production and Development Dependencies

```
requirements/
├── base.txt          # Shared dependencies
├── production.txt    # -r base.txt + production-only
└── development.txt   # -r base.txt + dev tools
```

### 3. Use pip-tools for Dependency Management

```bash
pip install pip-tools
```

requirements.in (high-level dependencies):
```txt
flask
requests
```

Generate locked requirements:
```bash
pip-compile requirements.in
# Creates requirements.txt with all sub-dependencies pinned
```

### 4. Regularly Update Dependencies

```bash
# Check for updates
pip list --outdated

# Update requirements.txt
pip-compile --upgrade requirements.in

# Test with new versions
pip install -r requirements.txt
pytest
```

### 5. Use Constraints for Cross-Project Consistency

constraints.txt:
```txt
# Versions approved for all company projects
requests==2.31.0
django>=4.0,<5.0
```

Install:
```bash
pip install -c constraints.txt -r requirements.txt
```

## Conclusion

When you run `pip install -r requirements.txt`, pip:

1. Parses requirements.txt
2. Queries PyPI for each package
3. Resolves all dependencies recursively
4. Checks for version conflicts
5. Downloads wheel files (or source if no wheel available)
6. Installs packages in correct order
7. Creates metadata in site-packages
8. Updates PATH with any console scripts

Understanding this process helps you:
- Debug installation issues
- Manage dependencies effectively
- Create your own packages
- Optimize build and deployment pipelines

**Remember**: Dependencies are code that runs in your application. Treat them with the same care as your own code!