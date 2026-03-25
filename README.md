# GlyphLoom
A modular spell weaving engine for fantasy magic systems, pre-bundled with 
the DnD SRD spells.

GlyphLoom is a fully modular Python package and command-line interface for 
generating, shaping, and visualizing spells as runes using parametric geometry,
structured metadata, and expressive configuration. It is a solo designed package
with clean abstractions, discoverable APIs, TODO(strong documentation), and a 
CLI that behaves as you expect a modern tool to.

This project draws inspiration from - and explicitly credits - the 
Gorilla of Destiny's Spell Writing Guide (https://www.drivethrurpg.com/en/product/429711/the-spell-writing-guide?src=hottest_filtered&affiliate_id=3673211),
whose creative framework helped shape the foundation for GlyphLoom's spell-construction
philosophy. GlyphLoom opens the door to the system with a programmable 
geometry engine, a declarative spell schema, and a robust CLI for rapid generation.


## Features
GlyphLoom attempts to KISS:
- Core geometry engine
Parametric curves, leylines, founts, and shaping functions implemented as canonical, reusable primitives.
- Spell metadata schema
A structured, validated representation of spell attributes (school, level, damage type, range, duration, etc.).
- Rendering pipeline
Deterministic, reproducible visualizations using Matplotlib with optional live previews.
- CLI orchestration
A Typer‑powered interface that exposes the full system without leaking internal implementation details.


### Command Line Interface
GlyphLooms aims to produce a CLI that mirrors the ergonomics of uv, cargo, and 
git.

#### Highlights
- Positional and Flagged Arguments for flexibility
- Live figure rendering with interactibility
- Help text for discovery of command structure
- Input validation and TODO(descriptive error messages)
- Support for Fifth Edition Dungeons and Dragons including Homebrew

#### Example

```bash
glyphloom 5e draw "Fireball"
```

The CLI is intended to be expressive without too much whelm.


## Installation
```bash
pip install glyphloom
```

Or from source:

```bash
git clone https://github.com/ResoluteVinculum/GlyphLoom
cd GlyphLoom
pip install .
```