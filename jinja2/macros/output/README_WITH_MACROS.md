

# QR Greeting

![Python](https://img.shields.io/badge/Python-blue) ![License-MIT](https://img.shields.io/badge/License-MIT-green) ![Status-Beta](https://img.shields.io/badge/Status-Beta-yellow)

## Description

Beautiful QR code greeting cards

## Features


🎨 Themes
Multiple design themes

📱 Mobile First
Optimized for phones

📊 Tracking
Analytics built-in


## Installation

```bash
pip install qr-greeting

## Quick Start

```python
from qr_greeting import generate

qr = generate(
    url="https://example.com",
    theme="fireworks"
)
qr.save("output.png")