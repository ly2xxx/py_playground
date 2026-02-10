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

with open("output/CHANGELOG.md", "w", encoding="utf-8") as f:
    f.write(output)

print("✅ CHANGELOG.md generated!")