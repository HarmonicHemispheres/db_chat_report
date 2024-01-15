# Install

### Prereqs
- have python 3.7+ installed
- (optional) use a python environment manager (pyenv\conda)
- have python's `poetry` package installed - https://python-poetry.org/docs/

### 1. clone the repo: 
```
> git clone https://github.com/GoInterject/ids-python-api.git
```

### 2. Install Package with Poetry
```
> poetry install
```

### 3. Test Install
```
> idsdata version
0.1.0
```



<br>
<br>
<br>


# Setup

### 1. Create a new config
```
> idsdata create-config
```

### 2. Moddify config or add variables for your project (ie tokens, keys, feature flags, etc..)
```python
# domain where api runs
host = "127.0.0.1"

# port where api runs
port = 7777
reload = True
```


### 3. Run the data api
```
> idsdata run
```

