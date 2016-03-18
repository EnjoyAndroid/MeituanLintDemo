#!/usr/bin/python
# coding=utf-8

import argparse
import codecs
import os
import re

# 脚本功能说明：
# 1. 自动添加plugin repositories & classpath & apply
# 2. 自动判断是否需要使用retrolambda ast并进行添加
# 3. 执行完成后reset改动,保证不影响后续检查

__author__ = 'chentong'


def handle_gradle_buildscript(gradle_path, use_retrolambda_ast):
    gradle_backup_path = os.path.join(os.path.dirname(gradle_path), "build_backup.gradle")
    os.rename(gradle_path, gradle_backup_path)

    buildscript_begin = False
    buildscript_dependencies_begin = False

    plugin_classpath_write = False
    plugin_classpath = "\t\tclasspath 'com.czt.mtlint:plugin:latest.integration'\n"

    retrolambda_ast_write = False
    retrolambda_ast_classpath = "\t\tclasspath 'me.tatarka.retrolambda.projectlombok:lombok.ast:0.2.3.a2'\n"

    exclude_lint_ast_write = False
    exclude_lint_ast = "\tconfigurations.classpath.exclude group: 'com.android.tools.external.lombok'\n"

    no_dynamic_cache_write = False
    no_dynamic_cache_line = "\t\tresolutionStrategy.cacheDynamicVersionsFor 0, 'seconds'\n"
    no_dynamic_cache_all = "\tconfigurations.all {\n\t\tresolutionStrategy.cacheDynamicVersionsFor 0, 'seconds'\n\t}\n"


    with codecs.open(gradle_backup_path, 'r', 'utf-8') as f_old, codecs.open(gradle_path, 'w', 'utf-8') as f_new:
        for line in f_old:

            if line.startswith("buildscript {"):
                buildscript_begin = True

            if buildscript_begin:

                if "dependencies {" in line:
                    # buildscipt中的dependencies
                    buildscript_dependencies_begin = True

                if buildscript_dependencies_begin:
                    if "com.czt.mtlint:plugin:" in line:
                        # 如果应经使用了plugin,强制写入新版本
                        f_new.write(plugin_classpath)
                        plugin_classpath_write = True
                        continue

                    if "me.tatarka.retrolambda.projectlombok:lombok.ast:" in line:
                        # 如果应经使用了retrolambda ast,强制写入新版本
                        f_new.write(retrolambda_ast_classpath)
                        retrolambda_ast_write = True
                        continue

                    if "}" in line:
                        buildscript_dependencies_begin = False
                        if not plugin_classpath_write:
                            # 没有使用plugin classpath
                            f_new.write(plugin_classpath)
                        if (not retrolambda_ast_write) and use_retrolambda_ast:
                            # 没有使用retrolambda ast
                            f_new.write(retrolambda_ast_classpath)

                if "configurations.classpath.exclude group: 'com.android.tools.external.lombok'" in line:
                    exclude_lint_ast_write = True

                if "resolutionStrategy.cacheDynamicVersionsFor" in line:
                    # 强制更新动态版本缓存策略
                    f_new.write(no_dynamic_cache_line)
                    no_dynamic_cache_write = True
                    continue


                if line.startswith("}"):
                    buildscript_begin = False
                    if (not exclude_lint_ast_write) and use_retrolambda_ast:
                        f_new.write(exclude_lint_ast)
                    if not no_dynamic_cache_write:
                        f_new.write(no_dynamic_cache_all)

            f_new.write(line)

    os.remove(gradle_backup_path)


def handle_module_build_gradle(src, use_retrolambda_ast):
    apply_plugin_text = "\napply plugin: 'MTLintPlugin'"
    module_build_gradle = os.path.join(src, "build.gradle")
    # 插入lint插件
    not_apply = True
    if apply_plugin_text in open(module_build_gradle).read():
        not_apply = False
    if not_apply:
        with open(module_build_gradle, "a") as newFile:
            newFile.write(apply_plugin_text)

    # 处理module里的buildscript情况
    handle_gradle_buildscript(module_build_gradle, use_retrolambda_ast)




def custom_lint(src):
    project_build_gradle = os.path.join(os.path.dirname(src), "build.gradle")

    use_retrolambda = False
    plugin_version_int = -1

    for line in open(project_build_gradle):
        if "com.android.tools.build:gradle:" in line:
            classpath_build = line.strip().split(" ")[-1][1:-1]
            plugin_version = classpath_build.split(":")[-1].split("-")[0]  # - 排除1.4.0-beta1 1.3.0-SNAPSHOT这种情况,直接看版本号
            plugin_version_int = int(plugin_version.replace(".", ""))
            if plugin_version_int < 130:
                # 1.3.0以下版本不支持使用插件, 需要自己手动配置
                return
        if "me.tatarka:gradle-retrolambda:" in line:
            use_retrolambda = True

    # 1.5.0以上,使用retrolambda需要使用retrolambda出的ast,否则lint出错
    use_retrolambda_ast = False
    if use_retrolambda and (plugin_version_int >= 150):
        use_retrolambda_ast = True

    handle_gradle_buildscript(project_build_gradle, use_retrolambda_ast)
    handle_module_build_gradle(src, use_retrolambda_ast)

    os.chdir(src)
    code = os.system('../gradlew lintForArchon --stacktrace')

    os.system('git reset --hard')

    # 报错
    if code == 256:
        # 没有文件生成
        project_lint_html = os.path.join(src, "lint-report/lint-report.html")
        if not os.path.exists(project_lint_html):
            exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', help='Module Source Folder, such as aar/app, ==> ./check_custom_lint.py -s aar/app')
    args = parser.parse_args()
    src = os.path.abspath(args.s)

    custom_lint(src)


if __name__ == '__main__':
    main()
