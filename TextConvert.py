"""
@copyright Copyright (c) 2014 Wanderson Bragança

"""
import sublime
import sublime_plugin
import os
import sys
import re
import imp
from unicodedata import normalize

st_version = 2
if sublime.version() == '' or int(sublime.version()) > 3000:
    st_version = 3

reloader_name = 'textconvert.reloader'
# ST3 loads each package as a module, so it needs an extra prefix
if st_version == 3:
    reloader_name = 'TextConvert.' + reloader_name
    from imp import reload

if reloader_name in sys.modules:
    reload(sys.modules[reloader_name])

try:
    # Python 3
    from .textconvert import bases
    from .textconvert import slugify

except (ValueError):
    # Python 2
    from textconvert import bases
    from textconvert import slugify


"""
    Replaces all characters of space with "-" characters.
"""
class SlugCommand(bases.PerRegionTextConvert):

    def per_region(self, val):
        val = slugify.slug(val)
        return val

"""
    Replaces all " " or "_" characters with "-" characters.
"""
class HyphenizeCommand(bases.PerRegionTextConvert):
    def per_region(self, val):
        val = "-".join(val.split(" "))
        val = "-".join(val.split("_"))
        val = re.compile('-{2,}').sub('-', val).strip('-')
        return val


"""
    Replaces all " " or "-" characters with "_" characters.
"""
class UnderscoreCommand(bases.PerRegionTextConvert):
    def per_region(self, val):
        val = "_".join(val.split(" "))
        val = "_".join(val.split("-"))
        val = re.compile('_{2,}').sub('_', val).strip('_')
        return val
