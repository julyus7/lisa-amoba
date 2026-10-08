"""Replace the executable in this game's released floppy, without reallocating."""
import argparse
from pathlib import Path
from lisa_image import LisaImage

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('workshop', type=Path, help='closed DC42 Workshop disk containing B.OBJ')
p.add_argument('output', type=Path, help='new floppy; must differ from the template')
p.add_argument('--object-name', default='B.OBJ')
p.add_argument('--template', type=Path,
               default=Path(__file__).resolve().parent.parent/'dist'/'Amoba.dc42')
a = p.parse_args()
if a.output.resolve() in (a.template.resolve(), a.workshop.resolve()):
    p.error('Use a separate output file; never overwrite an input image')
source = LisaImage(a.workshop)
dest = LisaImage(a.template)
dest.verify_checksums()
if set(dest.tools()) != {241}:
    p.error('Wrong game template / LOS tool identity')
tags_before = bytes(dest.b[84+dest.ds:])
code = source.read(a.object_name)
if not code:
    p.error('Empty executable')
dest.replace(dest.tools()[241], code)
if bytes(dest.b[84+dest.ds:]) != tags_before:
    raise ValueError('Native page tags must remain unchanged')
dest.save(a.output)
print('Wrote', a.output, 'with', len(code), 'executable bytes')
