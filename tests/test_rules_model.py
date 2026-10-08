"""Exhaustive independent model checks; these do not replace LOS execution tests."""
from functools import lru_cache

LINES=((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
ORDER=(4,0,2,6,8,1,3,5,7)
def winner(b):
    found=0
    for row in range(3):
        a=row*3
        if b[a] and b[a]==b[a+1]==b[a+2]: found=b[a]
    for col in range(3):
        if b[col] and b[col]==b[col+3]==b[col+6]: found=b[col]
    if b[0] and b[0]==b[4]==b[8]: found=b[0]
    if b[2] and b[2]==b[4]==b[6]: found=b[2]
    return found
def place(b,turn,cell):
    if not 0<=cell<9 or b[cell] or winner(b) or all(b): return b,turn
    out=list(b);out[cell]=turn;out=tuple(out)
    return out,turn if winner(out) or all(out) else 3-turn
@lru_cache(None)
def score(b,player):
    w=winner(b)
    if w: return 1 if w==player else -1
    best=-2
    for i in range(9):
        if not b[i]:
            out=list(b);out[i]=player
            best=max(best,-score(tuple(out),3-player))
            if best==1: return best
    return 0 if best==-2 else best
def computer(b):
    best=-2;chosen=None
    for cell in ORDER:
        if not b[cell]:
            out=list(b);out[cell]=2
            value=-score(tuple(out),1)
            if value>best: best=value;chosen=cell
            if best==1: break
    return chosen

seen=set()
def visit(b,turn):
    if b in seen: return
    seen.add(b)
    expected=next((b[a] for a,c,d in LINES if b[a] and b[a]==b[c]==b[d]),0)
    assert winner(b)==expected
    assert b.count(1) in (b.count(2),b.count(2)+1)
    for cell in (-1,9): assert place(b,turn,cell)==(b,turn)
    if winner(b) or all(b):
        for cell in range(9): assert place(b,turn,cell)==(b,turn)
        return
    for cell in range(9):
        out,nxt=place(b,turn,cell)
        if b[cell]: assert (out,nxt)==(b,turn)
        else: visit(out,nxt)
visit((0,)*9,1)
assert len(seen)==5478
ai_games=0
def against_ai(b):
    global ai_games
    assert winner(b)!=1,'The computer allowed a human win'
    if winner(b) or all(b): ai_games+=1;return
    assert b.count(1)==b.count(2)
    for cell in range(9):
        if b[cell]: continue
        out,turn=place(b,1,cell)
        if winner(out) or all(out):
            assert winner(out)!=1
            ai_games+=1;continue
        chosen=computer(out)
        assert chosen is not None and not out[chosen]
        nxt,_=place(out,2,chosen)
        against_ai(nxt)
against_ai((0,)*9)
print('PASS: 5478 reachable boards, 8 winning lines, occupied/out-of-range/finished moves rejected.')
print(f'PASS: {ai_games} complete human-vs-computer paths; circle starts and optimal X never loses.')
print('Scope: host-side rules model only; compiled Lisa application still requires LOS tests.')
