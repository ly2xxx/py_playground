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