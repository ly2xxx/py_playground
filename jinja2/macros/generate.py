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

with open("output/README_WITH_MACROS.md", "w", encoding="utf-8") as f:
    f.write(output)