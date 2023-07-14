import requests
import re
import sys
#web_all_name = "https://build.tarsier-infra.com/public/build/home:revy:deepin-riscv-stage2/stage2/riscv64"
#web_all_name = "https://build.tarsier-infra.com/public/build/openEuler:Mainline/standard_riscv64_llvm/riscv64"
web_all_name = "https://build.tarsier-infra.com/public/build/openEuler:Mainline/standard_x86_64_gcc/x86_64"
#web_all_name = "https://build.tarsier-infra.com/package/live_build_log/openEuler:23.03/WasmEngine/23.03/riscv64"
r = requests.get(web_all_name)

lines = r.text.splitlines()

faild_num = 0
file = open("output.html", "w")
for i, line in enumerate(lines):
    #print(i)
    if i == 0:
        continue
    str_line = str(line)
    start_str = '  <entry name="'
    end_str = '" />'
    result = str_line[str_line.find(
        start_str)+len(start_str):str_line.rfind(end_str)]
    NAME = result
    NAME = NAME.replace('"/', '')

    #get name-- above

    #test
    #NAME = "icmake"
    #test over
    #web_log = "https://build.tarsier-infra.com/public/build/home:revy:deepin-riscv-stage2/stage2/riscv64/{0}/_log".format(
    #    NAME)
    #web_log = "https://build.tarsier-infra.com/package/live_build_log/openEuler:23.03/WasmEngine/23.03/riscv64".format(
    #    NAME)
    #此处需要是log的源码部分
    #web_log = "https://build.tarsier-infra.com/public/build/openEuler:Mainline/standard_riscv64_llvm/riscv64/{0}/_log".format(
    #    NAME)

    web_log = "https://build.tarsier-infra.com/public/build/openEuler:Mainline/standard_x86_64_gcc/x86_64/{0}/_log".format(
        NAME)
    #获取源码并且设定超时时间为4秒，去除一些building的包
    try:
        r = requests.get(web_log, timeout=4)
    except requests.exceptions.RequestException as e:
        continue
    lines = r.text.splitlines()

    #test
    # print(NAME)
    # print(faild_num)

    move404_succeedd = str(lines)
    if "logfile</details>" in move404_succeedd:
        # print("move 404")
        continue

    if "dpkg-genchanges: info: not including original source code in upload" in move404_succeedd:
        # print("move success2")
        continue

    if "dpkg-genchanges: info: including full source code in upload" in move404_succeedd:
        # print("move success3")
        continue
    else:
        # 定义要判断的行数
        ROW_NUM = 4

        for a, line in enumerate(lines):

            line = str(line)
            #print(line)
            #匹配逻辑
            #pattern = re.compile(r'(.*)/*?error:.*')
            #pattern = re.compile(r'^.*\|.*$')
            pattern = re.compile(r'^.*~~~.*$')
            matches = pattern.match(line)
            #if NAME in line:

            if matches:
                # if 'dpkg-buildpackage' in str(line):
                #     break

                # 计算要判断的行的范围,防止出现数组越界的bug
                start_row = max(0, a - ROW_NUM)
                end_row = min(len(lines), a + ROW_NUM)
                # 获取要判断的行
                rows = str(lines[start_row:end_row])
                # 判断是否出现了"error:"字符串
                if "error:" in rows:
                    #将输出输入到html文件中，注意此处是w模式，如果文件不存在会创建文件，存在会覆盖
                    print('<br>', file=file)
                    print('<br>', file=file)
                    print(NAME, file=file)
                    print('<br>', file=file)
                    print('<br>'.join(lines[a-12:a+4]), file=file)
                    print('\n', file=file)
                    #https://github.com/deepin-community/{NAME}
                    print('<br>', file=file)
                    print('<br>', file=file)
                    print(
                        f'<a href="https://gitee.com/src-openeuler/{NAME}">{NAME} ---gitee </a>', file=file)
                    print('<br>', file=file)
                    #print(f'<a href="https://build.tarsier-infra.com/public/build/home:revy:deepin-riscv-stage2/stage2/riscv64/{NAME}/_log">{NAME} --log </a>', file=file)
                    print( f'<a href="https://build.tarsier-infra.com/public/build/openEuler:Mainline/standard_x86_64_gcc/x86_64/{NAME}/_log">{NAME} --log </a>', file=file)
                    print('<br>', file=file)
                    print('<br>', file=file)
                    print('<br>', file=file)
                    print('<br>', file=file)
                    if a ==  (len(lines)-1):
                        print('<br>', file=file)
                        print('<br>', file=file)
                        print('<br>', file=file)
                        print('<br>', file=file)
                        print('\n', file=file)
                        print('<br>', file=file)
                        print('编译错误包总共有：', file=file)
                        print('<br>', file=file)
                        print(faild_num, file=file)
                        print('<br>', file=file)
                        print('\n', file=file)
                        print('<br>', file=file)


                    faild_num = faild_num+1
                    #判断faild数目是否正确

                break
        #test 单独测试某一个包需要在此加break，不然无限循环
        #break;

file.close()

