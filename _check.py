import os
root = r'c:\Users\陈烨\Desktop\互联网创新\demo1'
files = sorted([f for f in os.listdir(root) if f.endswith('.html')])
print('=== HTML files ===')
for f in files:
    print(f)
print()
print('=== agent-fab in each file ===')
for f in files:
    with open(os.path.join(root, f), 'r', encoding='utf-8') as fp:
        c = fp.read()
    has = 'agent-fab' in c
    has_id = 'openCozeAgentBtn' in c
    has_drawer = 'cozeDrawer' in c
    body_pos = c.rfind('</body>')
    if body_pos > 0:
        line_no = c[:body_pos].count('\n') + 1
    else:
        line_no = -1
    print(f'{f}: agent-fab={has}, openCozeAgentBtn={has_id}, cozeDrawer={has_drawer}, </body> at line {line_no}')
