# Development Configuration

This directory contains development configuration files.

## Files

- `config.py` - Main development configuration
- `config.ini` - Alternative configuration format
- `.env` - Environment variables for development

## Usage

```python
from configs.temp.config import *
```

## Environment Variables

Make sure to set up your `.env` file with the following variables:

```
DATABASE_URL=sqlite:///dev.db
SECRET_KEY=your-secret-key
DEBUG=True
```
