"""Reuse the working native LOS window shell with a new tic-tac-toe game."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
source = (root / 'src/BlockOut-shell.TEXT').read_text().replace('\r', '\n')
source = source.replace('program BlockOut;', 'program Amoba;')
start = source.index('   boLeft =')
end = source.index('   nextClkPoll :')
source = source[:start] + '''   ttLeft = 24;
   ttTop = 40;
   ttCellW = 60;
   ttCellH = 44;
type BOVideoPtr = ^integer;
var
   ttBoard, ttShown : array[1..9] of integer;
   ttTurn, ttResult, ttMoves, ttSelected : integer;
   ttComputer, ttReady, ttPainted : boolean;
''' + source[end:]
start = source.index('procedure BlockInit;')
end = source.index('procedure doUpdateEvent')
source = source[:start] + '''function TTWinner : integer;
var row, col, a : integer;
begin
   TTWinner := 0;
   for row := 0 to 2 do begin
      a := row*3+1;
      if (ttBoard[a] <> 0) and (ttBoard[a] = ttBoard[a+1]) and
         (ttBoard[a] = ttBoard[a+2]) then TTWinner := ttBoard[a]
   end;
   for col := 1 to 3 do
      if (ttBoard[col] <> 0) and (ttBoard[col] = ttBoard[col+3]) and
         (ttBoard[col] = ttBoard[col+6]) then TTWinner := ttBoard[col];
   if (ttBoard[1] <> 0) and (ttBoard[1] = ttBoard[5]) and
      (ttBoard[1] = ttBoard[9]) then TTWinner := ttBoard[1];
   if (ttBoard[3] <> 0) and (ttBoard[3] = ttBoard[5]) and
      (ttBoard[3] = ttBoard[7]) then TTWinner := ttBoard[3]
end;
function TTScore(player : integer) : integer;
var win, i, score, best, empty : integer;
begin
   win := TTWinner;
   if win <> 0 then begin
      if win = player then TTScore := 1 else TTScore := -1;
      exit(TTScore)
   end;
   best := -2;
   empty := 0;
   for i := 1 to 9 do
      if ttBoard[i] = 0 then begin
         empty := empty+1;
         ttBoard[i] := player;
         score := -TTScore(3-player);
         ttBoard[i] := 0;
         if score > best then best := score;
         if best = 1 then begin
            TTScore := best;
            exit(TTScore)
         end
      end;
   if empty = 0 then TTScore := 0 else TTScore := best
end;
procedure TTNewGame;
var i : integer;
begin
   for i := 1 to 9 do ttBoard[i] := 0;
   ttTurn := 1;
   ttResult := 0;
   ttMoves := 0;
   ttSelected := 5;
   ttPainted := false;
   ttReady := true
end;
procedure TTDraw;
var i, row, col, x, y : integer;
    box : Rect;
    number : Str255;
begin
   if myWindow = nil then exit(TTDraw);
   SetPort(myWindow);
   ClipRect(myWindow^.portRect);
   if not ttPainted then EraseRect(myWindow^.portRect);
   MoveTo(24, 18); DrawString('AMOBA - KOR ES X');
   PenSize(2, 2);
   if not ttPainted then for i := 1 to 2 do begin
      MoveTo(ttLeft+i*ttCellW, ttTop);
      LineTo(ttLeft+i*ttCellW, ttTop+3*ttCellH);
      MoveTo(ttLeft, ttTop+i*ttCellH);
      LineTo(ttLeft+3*ttCellW, ttTop+i*ttCellH)
   end;
   for i := 1 to 9 do begin
      row := (i-1) div 3;
      col := (i-1) mod 3;
      x := ttLeft+col*ttCellW;
      y := ttTop+row*ttCellH;
      if (not ttPainted) or (ttBoard[i] <> ttShown[i]) then begin
      PenSize(1, 1);
      SetRect(box, x+3, y+3, x+ttCellW-2, y+ttCellH-2);
      EraseRect(box);
      PenSize(2, 2);
      if ttBoard[i] = 1 then begin
         SetRect(box, x+12, y+9, x+48, y+35);
         FrameOval(box)
      end
      else if ttBoard[i] = 2 then begin
         MoveTo(x+12, y+9); LineTo(x+48, y+35);
         MoveTo(x+48, y+9); LineTo(x+12, y+35)
      end
      else begin
         NumToStr(i, number);
         MoveTo(x+26, y+29); DrawString(number)
      end
      end;
      ttShown[i] := ttBoard[i]
   end;
   PenSize(1, 1);
   MoveTo(230, 52);
   if ttComputer then DrawString('MOD: EMBER A GEP ELLEN')
   else DrawString('MOD: KET JATEKOS');
   MoveTo(230, 77); DrawString('A KOR MINDIG KEZD.');
   SetRect(box, 228, 85, 498, 110);
   EraseRect(box);
   MoveTo(230, 100);
   case ttResult of
      1: DrawString('A KOR NYERT!');
      2: DrawString('AZ X NYERT!');
      3: DrawString('DONTETLEN!');
      otherwise
         if ttTurn = 1 then DrawString('A KOR KOVETKEZIK.')
         else if ttComputer then DrawString('A GEP KOVETKEZIK.')
         else DrawString('AZ X KOVETKEZIK.')
   end;
   MoveTo(230, 137); DrawString('G: GEP ELLEN');
   MoveTo(230, 155); DrawString('K: KET JATEKOS');
   MoveTo(230, 181); DrawString('N / SZOKOZ: UJ JATEK');
   MoveTo(24, 212); DrawString('KATTINTS EGY URES MEZORE, VAGY NYOMD MEG AZ 1-9 GOMBOT.');
   MoveTo(24, 234); DrawString('HAROM AZONOS JEL EGY SORBAN, OSZLOPBAN VAGY ATLOBAN NYER.');
   ttPainted := true
end;
procedure TTPlace(cell : integer);
begin
   if (cell < 1) or (cell > 9) or (ttResult <> 0) then exit(TTPlace);
   if ttBoard[cell] <> 0 then exit(TTPlace);
   ttBoard[cell] := ttTurn;
   ttMoves := ttMoves+1;
   ttResult := TTWinner;
   if (ttResult = 0) and (ttMoves = 9) then ttResult := 3;
   if ttResult = 0 then ttTurn := 3-ttTurn
end;
procedure TTComputerMove;
var i, cell, score, best, chosen : integer;
begin
   if (not ttComputer) or (ttTurn <> 2) or (ttResult <> 0) then
      exit(TTComputerMove);
   best := -2;
   chosen := 0;
   for i := 1 to 9 do begin
      case i of
         1: cell := 5;
         2: cell := 1;
         3: cell := 3;
         4: cell := 7;
         5: cell := 9;
         6: cell := 2;
         7: cell := 4;
         8: cell := 6;
         9: cell := 8
      end;
      if ttBoard[cell] = 0 then begin
         ttBoard[cell] := 2;
         score := -TTScore(1);
         ttBoard[cell] := 0;
         if score > best then begin best := score; chosen := cell end;
         if best = 1 then begin TTPlace(chosen); exit(TTComputerMove) end
      end
   end;
   if chosen <> 0 then TTPlace(chosen)
end;
procedure TTClick;
var pt : Point;
    cell : integer;
begin
   if (ttResult <> 0) or (ttComputer and (ttTurn = 2)) then exit(TTClick);
   SetPort(myWindow);
   GetMouse(pt);
   if (pt.h < ttLeft) or (pt.h >= ttLeft+3*ttCellW) or
      (pt.v < ttTop) or (pt.v >= ttTop+3*ttCellH) then exit(TTClick);
   cell := ((pt.v-ttTop) div ttCellH)*3+(pt.h-ttLeft) div ttCellW+1;
   TTPlace(cell);
   TTDraw
end;
''' + source[end:]
source = source.replace('   BlockDraw;', '   TTDraw;')
source = source.replace('   TTDraw;\n   if normal then EndUpdate(window)',
                        '   ttPainted := false;\n   TTDraw;\n   if normal then EndUpdate(window)')
start = source.index('function ClockReady')
end = source.index('procedure InitNewDoc')
source = source[:start] + source[end:]
source = source.replace('BlockInit;', '''if not ttReady then begin
ttComputer := true;
TTNewGame
end;''')
start = source.index('procedure DoCopyBoard;')
end = source.index('procedure ProcessTheEvent;')
source = source[:start] + '''procedure MenuCommand(menu, item : integer);
var err : integer;
begin
   if menu = mFile then
      case item of
         miAsideAll: DoFilingCmd(cmdClosAll);
         miAside: DoFilingCmd(cmdClose);
         miPutAway: begin
            TellFiler(err, docClosd, docPutBack, myWindow);
            myWindow := nil
         end
      end
end;
''' + source[end:]
source = source.replace('BlockDraw;', 'TTClick;', 1) if False else source
source = source.replace('else if theEvent.who = myWindow then\nBlockDraw;',
                        'else if theEvent.who = myWindow then\nTTClick;')
start = source.index("case theEvent.ascii of")
end = source.index('folderActivate :', start)
source = source[:start] + '''case theEvent.ascii of
'1'..'9': begin
   if (not ttComputer) or (ttTurn = 1) then
      TTPlace(ord(theEvent.ascii)-ord('0'));
   TTDraw
end;
'g', 'G': begin ttComputer := true; TTNewGame; TTDraw end;
'k', 'K': begin ttComputer := false; TTNewGame; TTDraw end;
'n', 'N', ' ': begin TTNewGame; TTDraw end
end;
''' + source[end:]
source = source.replace('BlockTick;', '''if (myWindow <> nil) and ttComputer and
   (ttTurn = 2) and (ttResult = 0) then begin
   TTComputerMove;
   TTDraw
end;''')
source = source.replace('initing := true;', 'initing := true;\nttReady := false;')
source = source.replace('FolderSize(myWindow, 500, 300, false);',
                        'FolderSize(myWindow, 500, 260, false);\nttPainted := false;')
source = source.replace('BlockDraw', 'TTDraw')
# The verified policy covers every human path for this deterministic computer.
# A table lookup avoids recursive search pauses on the Lisa's 5 MHz 68000.
start = source.index('function TTScore(')
end = source.index('procedure TTNewGame;', start)
source = source[:start] + source[end:]
start = source.index('procedure TTComputerMove;')
end = source.index('procedure TTClick;', start)
policy = (root/'src/AI.TEXT').read_text()
source = source[:start] + policy + '''procedure TTComputerMove;
var i, cell : integer;
begin
   if (not ttComputer) or (ttTurn <> 2) or (ttResult <> 0) then
      exit(TTComputerMove);
   cell := TTChoose;
   if cell = 0 then
      for i := 1 to 9 do
         if (cell = 0) and (ttBoard[i] = 0) then cell := i;
   if cell <> 0 then TTPlace(cell)
end;
''' + source[end:]
assert 'BlockInit' not in source and 'BlockMove' not in source and 'BlockTick' not in source
# Lisa Pascal V3.26 distinguishes only the first eight identifier characters.
# ttComputer (the mode flag) must not collide with TTComputerMove.
source = source.replace('TTComputerMove', 'TTBot')
(root / 'src/M.TEXT').write_bytes(source.replace('\n', '\r').encode('ascii'))
print('Wrote TicTacToe/M.TEXT:', len(source), 'bytes')
