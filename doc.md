## 数据库

**sqlite3**

基于文件，容易维护，容易迁移，轻量化

## 后端框架

**django, django rest framework**

基于python，可以完全跨平台，兼容wsgi接口，可对接多种Web server

一些废话： django设计理念(DRY don't repeat yourself)，减少代码冗余量，低耦合，高服用性balabala

## 网络服务架构

**REST**

分离client与server, 符合HTTP标准，完全独立于开发平台和语言，
易于理解，具备良好可读性与可扩展性

可自动生成接口文档，代码样例，交互测试

## orm 框架 (Object-relational mapping)

**django bulit in orm**

实现python数据模型层到数据库层的映射，完全封装sql和数据库相关操作， 
减少开发周期和成本，便于维护，更新，复用

充分利用自动化工具，不需要写一行sql语句，
完全封装数据库操作，不用改代码就能切换成别的数据库

## smtplib

自动发邮件

## django signal

**django“信号机制”**

自动新建token当新用户被创建，（类似数据库trigger）
```python
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```
自动发送邮件当用户被分配合同审核
```python
@receiver(post_save, sender=Review)
def review_send_email(sender, instance=None, created=False, **kwargs):
    if created:
        instance.user.email_user(
            'You are assigned to a new reivew.',
            'Contract #%s needs your review.' % instance.contract.id,
            settings.EMAIL_HOST_USER
        )
```