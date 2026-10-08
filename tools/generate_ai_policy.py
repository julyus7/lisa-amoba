"""Precompute the deterministic optimal X policy so a real 68000 responds quickly."""
from pathlib import Path
import runpy
root=Path(__file__).resolve().parent
model=runpy.run_path(str(root.parent/'tests/test_rules_model.py'))
policy={};seen=set()
def walk(board):
    if board in seen: return
    seen.add(board)
    if model['winner'](board) or all(board): return
    for i in range(9):
        if board[i]: continue
        human,_=model['place'](board,1,i)
        if model['winner'](human) or all(human): continue
        cell=model['computer'](human)
        policy[human]=cell
        following,_=model['place'](human,2,cell)
        walk(following)
walk((0,)*9)
records=[]
for board,cell in sorted(policy.items(),key=lambda pair:sum(v*3**i for i,v in enumerate(pair[0]))):
    key=sum(v*3**i for i,v in enumerate(board))
    encoded=''.join(chr(48+((key>>shift)&31)) for shift in (10,5,0))+str(cell+1)
    assert ((ord(encoded[0])-48)*32+ord(encoded[1])-48)*32+ord(encoded[2])-48==key
    assert not board[cell]
    records.append(encoded)
pages=[''.join(records[i:i+31]) for i in range(0,len(records),31)]
lines=['function TTChoose : integer;',
 'var page, i, p, key, mult, skey : integer;',
 '    table : Str255;',
 'begin','   key := 0; mult := 1;',
 '   for i := 1 to 9 do begin',
 '      key := key+ttBoard[i]*mult; mult := mult*3',
 '   end;',f'   for page := 1 to {len(pages)} do begin','      case page of']
for i,page in enumerate(pages,1): lines.append(f"         {i}: table := '{page}';")
lines+=['      end;', '      for i := 1 to length(table) div 4 do begin',
 '         p := (i-1)*4;',
 '         skey := ((ord(table[p+1])-48)*32+',
 '            ord(table[p+2])-48)*32+ord(table[p+3])-48;',
 '         if skey = key then begin',
 "            TTChoose := ord(table[p+4])-ord('0');",
 '            exit(TTChoose)', '         end', '      end', '   end;',
 '   TTChoose := 0', 'end;']
(root.parent/'src/AI.TEXT').write_bytes(('\r'.join(lines)+'\r').encode('ascii'))
print(f'Generated and checked {len(records)} optimal decisions in {len(pages)} short string pages.')
