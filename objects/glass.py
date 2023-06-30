from functools import partial

from objects.box import new_box


new_glass = partial(new_box, mtl="flltgrey", name="glass")
