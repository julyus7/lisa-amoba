# Building the native Lisa program

The game was compiled with **Lisa Pascal V3.26**, under **Lisa Workshop 3.0**,
and linked with the **M68000 Object Code Linker 3.0**. Python generates or
packages files; it does not compile the Pascal program.

## Requirements

- Real Apple Lisa 2 (2/5 or 2/10), or LisaEm, with your own compatible ROM, Lisa Office System 3
  and Lisa Workshop 3 environment.
- Workshop's LOS interface objects and runtime libraries, including the units
  named in the `uses` clauses and `IOSPASLIB.OBJ`, `SYS1LIB.OBJ`, `PRLIB.OBJ`.
- Python 3.10+ for the host packaging tools. They use only the standard library.

The ROM, operating system, SDK libraries and prepared developer hard disks
are not distributed in this repository.

## Transfer and compile

All five Pascal files in `src/` are required. They keep classic Mac CR line
endings. Transfer them as Lisa TEXT files, not as raw binary files. One method
is the serial receiver and `tools/lisa_serial_transfer.py` from the upstream
[LOS Minesweeper repository](https://github.com/alexthecat123/los_minesweeper).
Its README explains setting up and running the receiver in Workshop. A typical
host command, using that upstream checkout, is:

```sh
python /path/to/los_minesweeper/tools/lisa_serial_transfer.py COM3 /path/to/this/repository/src/
```

Use the actual serial port for your setup. Work in a disposable Workshop disk
copy; make the source folder the current working prefix and ensure the LOS
interface objects can be resolved. The upstream compilation environment is
another starting point; this repository does not supply that environment.

In Workshop, compile in this dependency order: **G, J, D, I, M**.
For each file, press `P`, enter its source name, accept the default listing
and corresponding `.OBJ` output. A prepared environment may already contain
the four supporting objects, but rebuilding all five avoids stale objects.

Delete any old `B.OBJ` using File Manager. Then press `L` and supply these
linker inputs, one per prompt:

```text
M.OBJ
G.OBJ
J.OBJ
D.OBJ
I.OBJ
IOSPASLIB.OBJ
SYS1LIB.OBJ
PRLIB.OBJ
```

End the input list with Return, accept the default listing, and enter `B.OBJ`
as output. The linker must report **0 Errors detected** and an executable
program file. This is the library list used for the tested releases.

The `src/A.TEXT` alert source documents the game's phrase resources. If these
resources need changing, compile them with Workshop's Alert tool and install
the resulting PHRASE as well. The packaging command below retains the tested
release's PHRASE and native icons; it replaces only the executable.

## Package a newly linked executable

Shut down LisaEm cleanly before reading its Workshop disk. The public packager
reads a closed DC42 Workshop disk containing `B.OBJ` and uses the released
game floppy as its filesystem template:

```sh
python tools/package.py /path/to/linked-workshop.dc42 Amoba-new.dc42
python tools/inspect_image.py Amoba-new.dc42
```

`--object-name` and `--template` override the input executable name and template.
The executable must fit the existing floppy allocation; the script fails if
it would require additional sectors. It keeps the game's registered tool ID,
volume identity, phrase, data segment and three native icons. It preserves all
native sector tags and recalculates the two DC42 container checksums.

The new portable packager is a publication helper; the original releases were
assembled by earlier local scripts and validated in LisaEm. No fresh native
compilation was performed for this GitHub publication. Test the resulting
application in LOS after any source change, including duplication to a hard
disk, keyboard input, repainting and coexistence with other tools.

## Original development and validation

Development ran locally on Windows, initially through a Cygwin LisaEm build
and later through LisaEm inside a local Alpine Linux virtual machine with an
Xvfb display. The guest compiler and linker were the actual Lisa tools.
See `VALIDATION.md` for the recorded tests and release hashes.

A previous packager incorrectly treated byte 11 of each 12-byte Sony floppy
tag as an XOR checksum. That byte is part of the compressed backward page
pointer. The published 2026-10-06 images preserve all 800 native donor tags.
Both uppercase `{Tnnn}` and lowercase `{tnnn}` icon filenames are required
for successful LOS duplication.
