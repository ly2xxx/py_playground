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