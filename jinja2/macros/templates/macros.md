{% macro badge(label, color="blue") -%}
![{{ label }}](https://img.shields.io/badge/{{ label | replace(" ", "%20") }}-{{ color }})
{%- endmacro %}

{% macro code_block(language, code) -%}
```{{ language }}
{{ code }}
{%- endmacro %}

{% macro feature_card(title, description, icon="✨") -%}
{{ icon }} {{ title }}
{{ description }} 
{%- endmacro %}