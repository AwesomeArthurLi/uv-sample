# README

## UV

这是UV使用案例和pyproject.toml的配置

### 创建项目

```bash
    uv init --package sample

    # 库开发
    uv init --lab sample
```

### 依赖

[dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/)

#### Importing dependencies

```bash
    uv add click
    # or
    uv add -r requirements.txt
```

#### Removing dependency

```bash
    uv remove click
```

#### Changing dependencies

```bash
    uv add "click >= 8.10.1"
    # or
    uv add "jax; sys_platform == 'linux'"
```

#### optional dependencies

```bash
    uv add httpx --optional network

    # [project.optional-dependencies]
    # network=[
    #     httpx
    # ]

    # uv add "sample[network]"
```

#### development dependencies

```bash
    uv add --dev pytest
    # or
    uv add --group dev pytest

    # other group can be created by --group option
    uv add --group lint ruff
```

#### default groups

执行uv run 或者uv sync时，默认是包括了dev的依赖组里面的所有依赖。不过这个默认配置选项可以通过tool.uv.default-groups来配置。

```toml
    [tool.uv]
    default-groups = ["dev", "foo"]
```

### 运行命令

在pyproject.toml中[project.scripts]可以定义命令。这些命令的运行需要一个隔离环境，否则会存在相同的命令存在。
运行命令，可以通过`pipx run`或者使用 `uv run`

例如

```toml
# pyproject.toml
[project.scripts]
hello = "sample.cli:hello"
```

```python
# src/sample/cli.py
import click
@click.command()
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(name):
    click.echo(f"Hello {name}!")
```

```bash
    uv build
    uv run hello --name world
    # hello world

    # or 
    uv run ./src/sample/cli.py hello --name world

    # or
    pipx install .
    pipx run hello --name world
```

#### 运行pytest测试案例

```bash
uv run pytest
```

### Locking and syncing

类似packages.json.lock文件

#### 创建一个lockfile

默认会创建

```bash
    uv lock
```

#### 转换成requirements.txt

```bash
    uv export --format requirements-txt
```

这个好像有点问题

```bash
(base) ➜  sample git:(master) ✗ uv export --format requirements-txt > requirements.txt
Resolved 23 packages in 1ms
(base) ➜  sample git:(master) ✗ pip install -r requirements.txt   
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Obtaining file:///Users/arthur/workspace/python/sample (from -r requirements.txt (line 3))
ERROR: The editable requirement file:///Users/arthur/workspace/python/sample (from -r requirements.txt (line 3)) cannot be installed when requiring hashes, because there is no single file to hash.
```

### 创建distribution

```bash
    uv build
```

### 运行工具

```bash
    uv tool run ruff check .

    # or
    uvx ruff check .
```

## pyproject.toml

### dynamic

dynamic 是只动态配置项，可以多个。如果配置为dynamic需要对一个的build插件支持。

```toml
dynamic=["version"]
```

#### version根据git tag来

##### setuptools-scm

```toml
[build-system]
build-backend = "setuptools.build_meta"
requires = ["setuptools>=61", "setuptools-scm[toml]>=6.2.3", "wheel"]
#....

[tool.setuptools_scm]
version_file = "src/pytestlab/_version.py"
```

##### hatch-vcs

```toml
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"


[tool.hatch.version]
source = "vcs"

[tool.hatch.build.hooks.vcs]
version-file = "src/sample/version.py"
```
