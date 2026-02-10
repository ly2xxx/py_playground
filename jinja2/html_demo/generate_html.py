from jinja2 import Environment, FileSystemLoader
import os

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

# 1. Setup Jinja2 environment
env = Environment(loader=FileSystemLoader('templates/'))
template = env.get_template('page.html')

# 2. Data to inject
data = {
    "page_title": "Jinja2 HTML Demo",
    "items": [
        {"title": "Feature A", "description": "This is a cool feature that does amazing things."},
        {"title": "Feature B", "description": "Another feature to help you be more productive."},
        {"title": "Feature C", "description": "Final feature in the list, very robust."}
    ],
    "show_promo": True
}

# 3. Render HTML
output = template.render(**data)

# 4. Save to file
path = "output/index.html"
with open(path, "w", encoding="utf-8") as f:
    f.write(output)

print(f"✅ HTML generated at {path}")
print("   Open it in your browser to see the result!")
