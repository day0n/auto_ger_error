import requests
import re
web_all_name = "https://build.tarsier-infra.com/public/build/home:revy:deepin-riscv-stage2/stage2/riscv64"

r = requests.get(web_all_name)

lines = r.text.splitlines()

faild_num = 0
for i,line in enumerate(lines):
    #print(i)
    if i == 0:
        continue
    str_line = str(line)
    start_str = '  <entry name="'
    end_str = '" />'
    result = str_line[str_line.find(start_str)+len(start_str):str_line.rfind(end_str)]
    
    NAME = result
    #get name-- above

    #test
    #NAME = "icmake"
    #test over
    web_log = "https://build.tarsier-infra.com/public/build/home:revy:deepin-riscv-stage2/stage2/riscv64/{0}/_log".format(
        NAME)
    #获取源码并且设定超时时间为4秒，去除一些building的包
    try:
        r = requests.get(web_log,timeout = 4)
    except requests.exceptions.RequestException as e:
        continue
    lines = r.text.splitlines()

    #test
    # print(NAME)
    # print(faild_num)

    move404_succeedd  = str(lines)
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
        for a,line in enumerate(lines):
            line = str(line)
            #print(line)
            pattern = re.compile(r'(.*)/*?error:.*')
            matches = pattern.match(line)
            if NAME in line:

                if matches:
                    if 'dpkg-buildpackage' in str(line):
                        break

                    print(NAME)
                    print('\n'.join(lines[a-12:a+4]))
                    print('\n')
                    
                        #判断faild数目是否正确
                    faild_num = faild_num+1
                    break
                
print('\n')
print(faild_num)
print('\n')
