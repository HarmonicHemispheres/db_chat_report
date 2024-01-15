![alt](./ai_report.png)

# DuckDB AI Manager Report 
an interject report for creating and interacting with a database using natural language

<br>

# Setup

### Add OpenAI API Key to Env Var
```
(windows)
> Set-Item -Path Env:OPENAI_API_KEY -Value ($Env:OPENAI_API_KEY + "sk-???????????????????????????????")
```

### Install Package
NOTE: you may need to use your own package manager if default python is not >=3.11
```
> cd ids-python-api

> poetry install
```

### Start Data API
```
python data_api.py
```