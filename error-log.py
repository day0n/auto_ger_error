import requests

NAME = input("Please enter your name: ")

web_log = "https://build.tarsier-infra.com/public/build/home:revy:deepin-riscv-stage2/stage2/riscv64/{0}/_log".format(NAME)

r = requests.get(web_log)

lines = r.text.splitlines()

for i, line in enumerate(lines):
    if 'error:'in line.lower():
        if '.' in line.lower():
            #print('\n'.join(lines[i-3:i+3]))
            
            print(i)
        
