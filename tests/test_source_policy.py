"""Validate the actual policy embedded in M.TEXT against the independent model."""
from pathlib import Path
import re,runpy
root=Path(__file__).resolve().parent
model=runpy.run_path(str(root/'test_rules_model.py'))
source=(root.parent/'src/M.TEXT').read_text()
tables=re.findall(r"table := '([^']*)';",source)
assert len(tables)==10
policy={}
for table in tables:
    assert len(table)%4==0 and len(table)<=255
    for p in range(0,len(table),4):
        a,b,c,move=table[p:p+4]
        key=((ord(a)-48)*32+ord(b)-48)*32+ord(c)-48
        assert key not in policy
        policy[key]=int(move)-1
assert len(policy)==285
seen=set();used=set();terminal=0
def walk(board):
    global terminal
    if board in seen:return
    seen.add(board)
    if model['winner'](board) or all(board):
        assert model['winner'](board)!=1
        terminal+=1
        return
    for cell in range(9):
        if board[cell]:continue
        human,_=model['place'](board,1,cell)
        if model['winner'](human) or all(human):
            assert model['winner'](human)!=1
            continue
        key=sum(v*3**i for i,v in enumerate(human))
        assert key in policy
        move=policy[key];used.add(key)
        assert not human[move] and move==model['computer'](human)
        following,_=model['place'](human,2,move)
        walk(following)
walk((0,)*9)
assert used==set(policy)
assert 'function TTScore' not in source
assert 'procedure TTBot;' in source and 'TTComputerMove' not in source
print('PASS: all 285 actual M.TEXT policy decisions are legal and match the independent optimal model.')
print('PASS: all reachable computer replies are covered; no reachable human victory.')
print('Scope: source policy and host rules model; native LOS runtime tests are separate.')
