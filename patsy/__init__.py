# This file is part of Patsy
# Copyright (C) 2011-2013 Nathaniel Smith <njs@pobox.com>
# See file COPYING for license information.

"""patsy is a Python package for describing statistical models and building
design matrices. It is closely inspired by the 'formula' mini-language used in
R and S."""

import sys

__version__ = "0.2.0"

# Do this first, to make it easy to check for warnings while testing:
import os
if os.environ.get("PATSY_FORCE_NO_WARNINGS"):
    import warnings
    warnings.filterwarnings("error", module="^patsy")
    del warnings
del os

import patsy.origin

class PatsyError(Exception):
    """This is the main error type raised by Patsy functions.

    In addition to the usual Python exception features, you can pass a second
    argument to this function specifying the origin of the error; this is
    included in any error message, and used to help the user locate errors
    arising from malformed formulas. This second argument should be an
    :class:`Origin` object, or else an arbitrary object with a ``.origin``
    attribute. (If it is neither of these things, then it will simply be
    ignored.)

    For ordinary display to the user with default formatting, use
    ``str(exc)``. If you want to do something cleverer, you can use the
    ``.message`` and ``.origin`` attributes directly. (The latter may be
    None.)
    """
    def __init__(self, message, origin=None):
        Exception.__init__(self, message)
        self.message = message
        self.origin = None
        self.set_origin(origin)
        
    def __str__(self):
        if self.origin is None:
            return self.message
        else:
            return ("%s\n%s"
                    % (self.message, self.origin.caretize(indent=4)))

    def set_origin(self, origin):
        # This is useful to modify an exception to add origin information as
        # it "passes by", without losing traceback information. (In Python 3
        # we could use the built-in exception wrapping stuff, but it will be
        # some time before we can count on that...)
        if self.origin is None:
            if hasattr(origin, "origin"):
                origin = origin.origin
            if not isinstance(origin, patsy.origin.Origin):
                origin = None
            self.origin = origin

__all__ = ["PatsyError"]

# We make a richer API available for explicit use. To see what exactly is
# exported, check each module's __all__.
def _reexport(modname):
    __import__(modname)
    mod = sys.modules[modname]
    for var in mod.__all__:
        __all__.append(var)
        globals()[var] = getattr(mod, var)
    
for child in ["highlevel", "build", "constraint", "contrasts",
              "desc", "design_info", "eval", "origin", "state",
              "user_util", "missing", "splines"]:
    _reexport("patsy." + child)
# XX FIXME: we aren't exporting any of the explicit parsing interface
# yet. Need to figure out how to do that.
