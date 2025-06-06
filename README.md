---
<div align="center">

# 开播爆米

_自动送礼物_

<img alt="Python Version" src="https://img.shields.io/pypi/pyversions/WeiboBot" /></a>
<img alt="Python Implementation" src="https://img.shields.io/pypi/implementation/WeiboBot" /></a>
<a href="http://github.com/MerlinCN/AutoBliveGift/src/branch/master/LICENSE"><img alt="License" src="https://img.shields.io/github/license/MerlinCN/WeiboBot"></a>

</div>

## 目录 📚

1. [前提条件](#前提条件)
2. [安装步骤](#安装步骤)
3. [运行程序](#运行程序)
4. [常见问题](#常见问题)
5. [贡献](#贡献)
6. [许可证](#许可证)

## 前提条件

在开始之前，请确保您的系统中已安装以下软件：

- Python 3.6 及以上版本
- pip（Python 包管理器）

如果还没有安装，请访问 [Python 官方网站](https://www.python.org/) 进行安装。

## 安装步骤

1. **克隆仓库**

    ```bash
    git clone http://github.com/MerlinCN/AutoBliveGift.git
    ```

2. **进入项目目录**

    ```bash
    cd AutoBliveGift
    ```

3. **安装依赖**

    ```bash
    pip install uv 
    uv sync
    uv venv
    ```

## 运行程序 

### 方式一：源码启动

在安装完依赖后，您可以运行主程序：

```bash
uv run src/main.py
```

程序应当会启动并在终端中输出结果。

### 方式二：Docker Compose 启动

1. **确保已安装 Docker 和 Docker Compose**

    如果尚未安装，请参考 [Docker 官方文档](https://docs.docker.com/get-docker/) 进行安装。

2. **使用 Docker Compose 启动**

    ```bash
    docker compose up -d
    ```

    这将以后台模式启动服务。如果需要查看日志，可以使用：

    ```bash
    docker compose logs -f
    ```

3. **停止服务**

    ```bash
    docker compose down
    ```

## 常见问题

- **无法安装依赖**

    请确保您的 Python 和 pip 版本是最新的。尝试更新 pip：

    ```bash
    pip install --upgrade pip
    ```

- **程序运行报错**

    请确保您已经激活了虚拟环境，并且所有依赖都已正确安装。如果问题仍然存在，请提交 issue。

## 贡献

欢迎各种形式的贡献！您可以：

- 提交 bug 报告或功能请求
- 提交 pull request 改进代码


## 许可证

本项目采用 AGPLv3.0 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

---
