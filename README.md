# MeituanCustomLintDemo
美团自定义Lint示例

## 代码使用说明

本库主要分为aar、plugin、python脚本三部分

- aar提供了集成自定义lint规则的aar(包括基本的编码规范以及公司要求的安全规范），团队可以集成后结合本身的lint配置进行使用。详见aar文件夹中的README。


- plugin提供集成自定义lint aar、lintOptions、lint.xml的插件（配置使用统一标准)，方便工程内一键部署使用，不用担心lint规则配置麻烦的问题。详见plugin文件夹中的README。


- check_custom_lint.py：集成plugin，同时针对遇到的retrolambda ast问题进行了自动处理，并运行lint查找代码问题，查找完成执行git reset，减少对后续检查的影响。可真正实现一键运行效果，方便CI部署。

  ```
  ./check_custom_lint.py -s aar/app
  ```

  ​

## 使用场景

一般配合CI使用，如Jenkins等。

本地使用场景有两个缺点：

- lint检查耗时
- 本地检查容易被忽略或者修改，无法保证质量。

## 声明 

本仓库仅提供美团自定义Lint的框架，具体lint检查实现仅提供了两个示例，并不是可直接部署使用的工具。开发者可根据公司代码规范自行增加定制开发。

##  License

```
Copyright 2016 GavinCT

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

