# 深度学习数据集共享平台

基于 Django 5.0 开发的深度学习数据集共享平台,为研究人员提供数据集的分享与获取服务。

## 技术栈

- 后端框架: Django 5.0
- 数据库: MySQL 5.7+
- 前端框架: Bootstrap 5
- 开发语言: Python 3.8+

## 快速开始

### 环境准备

1. 安装 Python 3.8+
2. 安装 MySQL 5.7+
3. 创建虚拟环境(推荐)

### 安装步骤

1. 克隆项目

```bash
git clone [项目地址]
cd DatasetsShareWeb
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 配置数据库

```sql
CREATE DATABASE datasetsharing CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

4. 修改配置

- 复制 `database.cnf.example` 为 `database.cnf`
- 修改数据库配置信息
- 修改 `settings.py` 中的邮箱配置

5. 数据库迁移

```bash
python manage.py migrate
```

6. 运行服务

```bash
python manage.py runserver
```

## 主要功能

### 用户系统

- [x] 邮箱注册
- [x] 账号登录
- [x] 记住登录状态

### 数据集管理

- [ ] 数据集上传
- [ ] 数据集下载
- [ ] 数据集分类
- [ ] 数据集搜索

### 用户面板

- [ ] 个人信息管理
- [ ] 已上传数据集管理
- [ ] 下载记录查看

## 项目结构

```
DatasetsShareWeb/
├── DatasetsShareWeb/    # 项目配置
├── qwjAuth/            # 用户认证
├── sharingPlatform/    # 核心功能
└── templates/         # 模板文件
```

## 开发计划

- [ ] 完善数据集管理功能
- [ ] 添加数据集评论功能
- [ ] 实现数据集评分系统
- [ ] 添加管理员后台
- [ ] 优化用户界面

## 贡献

欢迎提交 Issue 和 Pull Request

## 许可证

MIT License
