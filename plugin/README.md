# 集成

仅支持gradle plugin 1.3.0 以上

``` groovy
buildscript {
    repositories {
        jcenter()
    }
    dependencies {
        classpath 'com.czt.mtlint:plugin:latest.integration'
    }
}
```

``` groovy
apply plugin: 'MTLintPlugin'
```

# 功能介绍

- 集成了原生lint和[自定义lint]()的所有检查规则
- 内置lintOptions （所有warning视为error，只输出htmlReport到`${project.projectDir}/lint-report/lint-report.html`)和 lint.xml。集成此插件后，原有配置会被覆盖，没有配置的也会执行插件中的配置
- 根据retrolambda版本判断是否在lint.xml加入try-with-resource警告屏蔽（1.8.0版以上开始支持try-with-resource）

注： plugin新增一个task：lintForArchon，会选择一个variantName（取遍历结果的第一个）。

# lint.xml配置

plugin/src/main/resources/config/lint.xml

retrolambda_lint.xml是针对retrolambda的特殊配置，识别到开发者使用retrolambda之后会将该规则与lint.xml合并。
同样，有其他特殊情况，也可参照此例进行添加。

# 注意

## 项目中使用了retrolambda

如果项目中使用了gradle plugin 1.5 和 retrolambda，请注意配置替换原有的抽象语法树（ast），避免lint因不识别lambda表达式而报错

``` groovy
buildscript {
    repositories {
        jcenter()
    }

    dependencies {
        classpath 'com.android.tools.build:gradle:<version>'
        classpath "me.tatarka:gradle-retrolambda:<version>"
        classpath 'me.tatarka.retrolambda.projectlombok:lombok.ast:0.2.3.a2'
    }

    // Exclude the version that the android plugin depends on.
    configurations.classpath.exclude group: 'com.android.tools.external.lombok'
}
```