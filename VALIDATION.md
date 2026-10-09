# Recorded validation

## Hardware target and test scope

The program is a native Motorola 68000 application for Apple Lisa 2 hardware
(Lisa 2/5 and Lisa 2/10) running Lisa Office System 3. The released tagged
DC42 image can be written to a native Lisa floppy for use on those machines.
The checks below were performed in LisaEm. No physical Lisa 2 hardware test
is recorded in this release; emulator results are not a physical-hardware
test result.


These are results from the local development sessions in September–October
2026. This publication reused the already tested final files; it did not run
a new native compile or new emulator session.

- Independent rules model: all 5,478 reachable boards, all eight winning
  lines and rejection of occupied, out-of-range and finished-game moves.
- The policy embedded in the actual Pascal source was checked against the
  independent optimal model; all 285 decisions were covered.
- Native LOS: human O at square 9 produced computer X at square 5; two-player
  mode, winning, drawn and restarted games were exercised during development.
- Occupied-square input: 100 rapid key presses, 300 sampled board frames,
  zero changes to the stable O1/X5 board.
- Native LOS duplication, hard-disk launch and coexistence with Minesweeper
  (201) and BlockOut (240) succeeded. October 6 retested the corrected floppy
  installation into the shared games disk and O9/X5 play after cold boot.

The existing host checks can be repeated with:

```sh
python tests/test_rules_model.py
python tests/test_source_policy.py
```

Regenerate the policy and main source with `tools/generate_ai_policy.py` then
`tools/generate_source.py`. `src/BlockOut-shell.TEXT` is the exact application
shell input used by the generator; it is not the Amőba program to compile.
Host model checks do not replace running the compiled game in LOS.

## Final release identity

- Floppy: `Amoba.dc42`, 419,284 bytes, 800 tagged sectors.
- LOS tool number: **241**; volume UID suffix: **D601**.
- Executable: **9728 bytes**, SHA-256 `00d7e65025d703adf3808c455b0646958775e7432ef03871df1054e4fdf2f3a1`.
- Floppy SHA-256: `cce3d2afc2f01397459a0cb3cb4684e2ac0a023bc937ce528dc4f8395796cdab`.
- The original 800 native donor tags were retained unchanged; both DC42
  container checksums were recalculated. The three native icon resources
  (`ICON`, `ICON.BACKUP`, lowercase-prefix `icon2`) are identical.

Selected original measurement logs are in `validation/`. You can inspect
the published floppy with `python tools/inspect_image.py`.
