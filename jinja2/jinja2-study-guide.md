# Jinja2 Study Guide - Markdown Templating

**Tonight's Focus:** Options 1 & 2 from morning discussion  
**Time:** 1-2 hours hands-on practice  
**Goal:** Generate flexible Markdown files with Jinja2

---

## 📦 Setup (5 minutes)

### Install Jinja2
```bash
pip install jinja2
```

### Create Project Structure
```
jinja2-practice/
├── templates/           # Option 2: File-based templates
│   ├── readme.md
│   ├── changelog.md
│   └── api-doc.md
├── output/             # Generated files
├── data.json           # Sample data
└── generate.py         # Main script
```

---

## 🎯 Option 1: Inline Templates (30 minutes)

### 1.1 Basic String Template

**Concept:** Define template as Python string, render with variables.

```python
from jinja2 import Template

# Simple variable substitution
template = Template("Hello {{ name }}!")
output = template.render(name="Yang")
print(output)  # Hello Yang!
```

**Practice Exercise 1:** Create a simple README
```python
from jinja2 import Template

template = Template("""
# {{ project_name }}

## Description
{{ description }}

## Author
- **Name:** {{ author }}
- **Email:** {{ email }}
- **Date:** {{ date }}

## License
{{ license }}
""")

output = template.render(
    project_name="QR Greeting",
    description="A beautiful QR code greeting card generator",
    author="Yang Li",
    email="your.email@example.com",
    date="2026-02-10",
    license="MIT"
)

print(output)
# Save to file
with open("README.md", "w") as f:
    f.write(output)
```

### 1.2 Lists and Loops

**Concept:** Use `{% for %}` to iterate over lists.

```python
from jinja2 import Template

template = Template("""
# Features

{% for feature in features %}
- **{{ feature.name }}**: {{ feature.description }}
{% endfor %}
""")

output = template.render(
    features=[
        {"name": "QR Generation", "description": "Create beautiful QR codes"},
        {"name": "Customization", "description": "Multiple themes and colors"},
        {"name": "Mobile-First", "description": "Optimized for mobile viewing"}
    ]
)

print(output)
```

**Output:**
```markdown
# Features

- **QR Generation**: Create beautiful QR codes
- **Customization**: Multiple themes and colors
- **Mobile-First**: Optimized for mobile viewing
```

### 1.3 Conditionals

**Concept:** Use `{% if %}` for conditional content.

```python
from jinja2 import Template

template = Template("""
# {{ project_name }}

{% if status == "beta" %}
⚠️ **This project is in beta. Use with caution.**
{% elif status == "stable" %}
✅ **Production ready!**
{% else %}
🚧 **Under development**
{% endif %}

## Installation

{% if has_pypi %}
```bash
pip install {{ package_name }}
```
{% else %}
Clone from GitHub and install locally.
{% endif %}
""")

output = template.render(
    project_name="QR Greeting",
    status="beta",
    has_pypi=False,
    package_name="qr-greeting"
)

print(output)
```

### 1.4 Filters

**Concept:** Transform variables with `|filter`.

```python
from jinja2 import Template

template = Template("""
# {{ title | upper }}

Created: {{ date | default("Unknown") }}
Author: {{ author | title }}
Description: {{ description | truncate(50) }}

## Tags
{{ tags | join(", ") }}
""")

output = template.render(
    title="hello world",
    date="2026-02-10",
    author="yang li",
    description="This is a very long description that will be truncated to 50 characters",
    tags=["python", "jinja2", "markdown", "template"]
)

print(output)
```

**Common Filters:**
- `upper`, `lower`, `title` - case conversion
- `default(value)` - fallback for undefined
- `truncate(length)` - limit length
- `join(separator)` - join lists
- `length` - get length
- `replace(old, new)` - string replacement

### 1.5 Practical Exercise: API Documentation Generator

**Task:** Create a template that generates API endpoint documentation.

```python
from jinja2 import Template

api_template = Template("""
# API Documentation - {{ service_name }}

Base URL: `{{ base_url }}`

## Endpoints

{% for endpoint in endpoints %}
### {{ endpoint.method | upper }} {{ endpoint.path }}

**Description:** {{ endpoint.description }}

{% if endpoint.auth_required %}
🔒 **Authentication required**
{% endif %}

**Parameters:**
{% if endpoint.params %}
| Name | Type | Required | Description |
|------|------|----------|-------------|
{% for param in endpoint.params %}
| `{{ param.name }}` | {{ param.type }} | {{ "Yes" if param.required else "No" }} | {{ param.description }} |
{% endfor %}
{% else %}
No parameters required.
{% endif %}

**Example Request:**
```bash
curl -X {{ endpoint.method | upper }} {{ base_url }}{{ endpoint.path }} \\
{% if endpoint.auth_required %}
  -H "Authorization: Bearer YOUR_TOKEN" \\
{% endif %}
{% if endpoint.example_body %}
  -d '{{ endpoint.example_body }}'
{% endif %}
```

**Example Response:**
```json
{{ endpoint.example_response }}
```

---

{% endfor %}

## Error Codes

{% for error in error_codes %}
- **{{ error.code }}**: {{ error.description }}
{% endfor %}
""")

output = api_template.render(
    service_name="QR Greeting API",
    base_url="https://api.qr-greeting.com/v1",
    endpoints=[
        {
            "method": "post",
            "path": "/qr/generate",
            "description": "Generate a new QR code",
            "auth_required": True,
            "params": [
                {"name": "url", "type": "string", "required": True, "description": "Target URL"},
                {"name": "theme", "type": "string", "required": False, "description": "Theme name (fireworks, stars, etc.)"}
            ],
            "example_body": '{"url": "https://example.com", "theme": "fireworks"}',
            "example_response": '{"qr_id": "abc123", "image_url": "https://cdn.qr-greeting.com/abc123.png"}'
        },
        {
            "method": "get",
            "path": "/qr/:id",
            "description": "Retrieve QR code details",
            "auth_required": False,
            "params": [],
            "example_body": None,
            "example_response": '{"id": "abc123", "url": "https://example.com", "created_at": "2026-02-10T18:00:00Z"}'
        }
    ],
    error_codes=[
        {"code": 400, "description": "Bad Request - Invalid parameters"},
        {"code": 401, "description": "Unauthorized - Missing or invalid token"},
        {"code": 404, "description": "Not Found - QR code doesn't exist"}
    ]
)

with open("API_DOCS.md", "w") as f:
    f.write(output)

print("✅ API documentation generated!")
```

---

## 🗂️ Option 2: File-Based Templates (45 minutes)

### 2.1 Setup Environment

**Concept:** Load templates from files instead of strings.

**Create `templates/readme.md`:**
```markdown
# {{ project_name }}

{{ description }}

## Installation

```bash
{{ install_command }}
```

## Features

{% for feature in features %}
- {{ feature }}
{% endfor %}

## Usage

{{ usage_example }}

## Contributing

Pull requests welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

{{ license }}
```

**Python script (`generate.py`):**
```python
from jinja2 import Environment, FileSystemLoader

# Setup environment
env = Environment(loader=FileSystemLoader('templates/'))

# Load template
template = env.get_template('readme.md')

# Render
output = template.render(
    project_name="QR Greeting",
    description="Create beautiful QR code greeting cards.",
    install_command="pip install qr-greeting",
    features=[
        "Multiple themes (fireworks, stars, confetti)",
        "Mobile-optimized landing pages",
        "Marketing funnel QR codes"
    ],
    usage_example="python -m qr_greeting generate --url https://example.com",
    license="MIT License"
)

# Save
with open("output/README.md", "w") as f:
    f.write(output)

print("✅ README.md generated!")
```

### 2.2 Template Inheritance

**Concept:** Create base templates and extend them (DRY principle).

**Create `templates/base.md`:**
```markdown
# {{ title }}

---

{% block content %}
Default content goes here
{% endblock %}

---

*Generated with ❤️ by {{ author }}*
```

**Create `templates/changelog.md`:**
```markdown
{% extends "base.md" %}

{% block content %}
## Changelog

{% for version in versions %}
### [{{ version.number }}] - {{ version.date }}

{% if version.added %}
**Added:**
{% for item in version.added %}
- {{ item }}
{% endfor %}
{% endif %}

{% if version.fixed %}
**Fixed:**
{% for item in version.fixed %}
- {{ item }}
{% endfor %}
{% endif %}

{% if version.changed %}
**Changed:**
{% for item in version.changed %}
- {{ item }}
{% endfor %}
{% endif %}

{% endfor %}
{% endblock %}
```

**Generate:**
```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates/'))
template = env.get_template('changelog.md')

output = template.render(
    title="QR Greeting - Changelog",
    author="Yang Li",
    versions=[
        {
            "number": "1.2.0",
            "date": "2026-02-10",
            "added": [
                "Marketing funnel QR feature",
                "Pottery-themed landing page design"
            ],
            "fixed": [
                "CSS not applying in iframe",
                "Scan tab intercepting view tab"
            ]
        },
        {
            "number": "1.1.0",
            "date": "2026-02-05",
            "added": [
                "NetPull integration",
                "Batch QR generation"
            ],
            "changed": [
                "Updated color palette"
            ]
        }
    ]
)

with open("output/CHANGELOG.md", "w") as f:
    f.write(output)

print("✅ CHANGELOG.md generated!")
```

### 2.3 Macros (Reusable Components)

**Concept:** Define reusable template snippets.

**Create `templates/macros.md`:**
```markdown
{% macro badge(label, color="blue") -%}
![{{ label }}](https://img.shields.io/badge/{{ label | replace(" ", "%20") }}-{{ color }})
{%- endmacro %}

{% macro code_block(language, code) -%}
```{{ language }}
{{ code }}
```
{%- endmacro %}

{% macro feature_card(title, description, icon="✨") -%}
### {{ icon }} {{ title }}

{{ description }}
{%- endmacro %}
```

**Use macros in `templates/readme_with_macros.md`:**
```markdown
{% import 'macros.md' as m %}

# {{ project_name }}

{{ m.badge("Python", "blue") }} {{ m.badge("License-MIT", "green") }} {{ m.badge("Status-Beta", "yellow") }}

## Description

{{ description }}

## Features

{% for feature in features %}
{{ m.feature_card(feature.title, feature.description, feature.icon) }}
{% endfor %}

## Installation

{{ m.code_block("bash", "pip install " + package_name) }}

## Quick Start

{{ m.code_block("python", usage_code) }}
```

**Generate:**
```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates/'))
template = env.get_template('readme_with_macros.md')

output = template.render(
    project_name="QR Greeting",
    package_name="qr-greeting",
    description="Beautiful QR code greeting cards",
    features=[
        {"title": "Themes", "description": "Multiple design themes", "icon": "🎨"},
        {"title": "Mobile First", "description": "Optimized for phones", "icon": "📱"},
        {"title": "Tracking", "description": "Analytics built-in", "icon": "📊"}
    ],
    usage_code="""from qr_greeting import generate

qr = generate(
    url="https://example.com",
    theme="fireworks"
)
qr.save("output.png")"""
)

with open("output/README_WITH_MACROS.md", "w") as f:
    f.write(output)
```

### 2.4 Multiple Templates, One Script

**Concept:** Generate multiple documents from different templates.

```python
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def generate_all_docs(project_data):
    """Generate all project documentation"""
    env = Environment(loader=FileSystemLoader('templates/'))
    
    # Common data for all templates
    common_data = {
        "generated_date": datetime.now().strftime("%Y-%m-%d"),
        "author": project_data["author"]
    }
    
    # Generate README
    readme_template = env.get_template('readme.md')
    readme_output = readme_template.render(**project_data, **common_data)
    with open("output/README.md", "w") as f:
        f.write(readme_output)
    print("✅ README.md generated")
    
    # Generate CHANGELOG
    changelog_template = env.get_template('changelog.md')
    changelog_output = changelog_template.render(
        title=f"{project_data['project_name']} - Changelog",
        versions=project_data["versions"],
        **common_data
    )
    with open("output/CHANGELOG.md", "w") as f:
        f.write(changelog_output)
    print("✅ CHANGELOG.md generated")
    
    # Generate API docs
    api_template = env.get_template('api.md')
    api_output = api_template.render(
        service_name=project_data["project_name"],
        endpoints=project_data["api_endpoints"],
        **common_data
    )
    with open("output/API.md", "w") as f:
        f.write(api_output)
    print("✅ API.md generated")

# Usage
project_data = {
    "author": "Yang Li",
    "project_name": "QR Greeting",
    "description": "Beautiful QR greeting cards",
    "install_command": "pip install qr-greeting",
    "features": ["Themes", "Mobile-first", "Tracking"],
    "usage_example": "python -m qr_greeting",
    "license": "MIT",
    "versions": [
        # ... version data
    ],
    "api_endpoints": [
        # ... endpoint data
    ]
}

generate_all_docs(project_data)
```

---

## 🎓 Practice Exercises (30 minutes)

### Exercise 1: Personal Project README Generator

**Goal:** Create a template for your GitHub projects.

**Requirements:**
1. Project name, description, badges
2. Features list with icons
3. Installation instructions
4. Usage examples with code blocks
5. Contribution guidelines
6. License section

**Bonus:** Add conditional sections (e.g., only show "Demo" if demo_url exists)

### Exercise 2: Changelog Generator from Git Commits

**Goal:** Generate CHANGELOG.md from structured data.

**Requirements:**
1. Group by version number
2. Categorize changes (Added/Fixed/Changed/Removed)
3. Include dates
4. Support "Unreleased" section

### Exercise 3: Multi-Language Documentation

**Goal:** Generate same doc in multiple languages.

**Requirements:**
1. Create templates for EN, DE, ZH
2. Load translations from JSON/dict
3. Generate all versions with one command

---

## 💡 Best Practices

### 1. Whitespace Control

**Problem:** Extra blank lines in output.

**Solution:** Use `-` in tags to trim whitespace.

```python
# Without whitespace control
template = Template("""
{% for item in items %}
- {{ item }}
{% endfor %}
""")
# Output has extra blank lines

# With whitespace control
template = Template("""
{%- for item in items %}
- {{ item }}
{% endfor -%}
""")
# Output is compact
```

### 2. Escaping

**Problem:** Special characters in Jinja syntax.

**Solution:** Use `{% raw %}` blocks.

```markdown
## Jinja2 Syntax

{% raw %}
To use variables: {{ variable_name }}
To loop: {% for item in items %}
{% endraw %}
```

### 3. Custom Filters

**Create your own filters:**

```python
from jinja2 import Environment, FileSystemLoader

def slugify(text):
    """Convert text to URL-friendly slug"""
    return text.lower().replace(" ", "-")

def markdown_link(text, url):
    """Create markdown link"""
    return f"[{text}]({url})"

env = Environment(loader=FileSystemLoader('templates/'))
env.filters['slugify'] = slugify
env.filters['md_link'] = markdown_link

# Use in template:
# {{ "Hello World" | slugify }}  → hello-world
# {{ "Click here" | md_link("https://example.com") }}  → [Click here](https://example.com)
```

### 4. Separate Data from Templates

**Good practice:** Store data in JSON/YAML files.

**`data/project.json`:**
```json
{
  "project_name": "QR Greeting",
  "description": "...",
  "features": [...]
}
```

**`generate.py`:**
```python
import json
from jinja2 import Environment, FileSystemLoader

# Load data
with open("data/project.json") as f:
    data = json.load(f)

# Generate
env = Environment(loader=FileSystemLoader('templates/'))
template = env.get_template('readme.md')
output = template.render(**data)
```

---

## 🚀 Tonight's Goal Checklist

- [ ] Install Jinja2
- [ ] Create project folder structure
- [ ] **Option 1:** Create 3 inline templates (basic, with loops, with conditionals)
- [ ] **Option 2:** Create 3 file-based templates (README, CHANGELOG, API)
- [ ] Try template inheritance (base + child)
- [ ] Create one macro and use it
- [ ] Complete at least 1 practice exercise
- [ ] Generate documentation for one of your actual projects

---

## 📚 Quick Reference Card

### Variable Substitution
```
{{ variable }}
{{ dict.key }}
{{ list[0] }}
```

### Control Flow
```
{% if condition %}...{% elif condition %}...{% else %}...{% endif %}
{% for item in list %}...{% endfor %}
{% for key, value in dict.items %}...{% endfor %}
```

### Filters
```
{{ text | upper }}
{{ text | default("N/A") }}
{{ list | join(", ") }}
{{ text | truncate(50) }}
```

### Whitespace Control
```
{%- for item in items -%}
  {{ item }}
{%- endfor -%}
```

### Comments
```
{# This is a comment #}
```

### Template Inheritance
```
{% extends "base.md" %}
{% block content %}...{% endblock %}
```

### Macros
```
{% macro name(param1, param2) %}...{% endmacro %}
{{ name("value1", "value2") }}
```

---

## 🔗 Resources

**Official Docs:** https://jinja.palletsprojects.com/  
**Template Designer Docs:** https://jinja.palletsprojects.com/templates/  
**Filters List:** https://jinja.palletsprojects.com/templates/#builtin-filters

---

**Good luck tonight! 🎉**

Let me know if you hit any issues or want to discuss your implementation tomorrow!
