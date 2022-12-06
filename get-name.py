import requests
import re
web_log = "https://build.tarsier-infra.com/public/build/home:revy:deepin-riscv-stage2/stage2/riscv64"

r = requests.get(web_log)

lines = r.text.splitlines()

faild_num = 0
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
    print(NAME)
