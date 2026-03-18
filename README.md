# Auto-Problem-Decrypt
解决雨课堂题目字形加密的问题，个人兴趣成果，以AI生成为主，主要问题还是太慢了。。。

## 问题描述

在使用雨课堂刷题时，会发现他的题干是加密的，如果要复制很不方便（不过可以一键直接调用AI刷题），这里主要解决复制的问题

## 使用方法
使用Python提供解密服务，油猴脚本在线检测待解密的数据。

1. 安装依赖
   ```
   pip install flask requests fontTools beautifulsoup4
   ```
2. 运行Python服务
   ```
   python server.py
   ```
   或者直接运行`gui.exe`（应当提前配置好python运行环境）
   `exe`文件生成代码：
   ```
   pyinstaller -F -w -i server.ico gui.py
   ```
4. 安装油猴脚本  
   a. 直接导入js  
   b. 从网站下载：[Greasy Fork](https://greasyfork.org/zh-CN/scripts/570108-%E9%9B%A8%E8%AF%BE%E5%A0%82%E8%87%AA%E5%8A%A8%E8%A7%A3%E5%AF%86%E5%AD%97%E5%BD%A2)

## 参考&解密代码
[yuketangHelperBUU](https://github.com/MuWinds/yuketangHelperBUU)

## 代码生成工具
Gemini 3.1 Pro
