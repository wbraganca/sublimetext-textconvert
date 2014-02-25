"""
@copyright Copyright (c) 2014 Wanderson Bragança

"""

import sublime
import sublime_plugin
import re

"""
    Common functions used by various classes
"""
def string_as_integer(string):
    reg = re.compile("-?[0-9]+")
    match = reg.match(string)
    if match is not None:
        return int(string[match.start():match.end()])
    else:
        return None


def num_to_hex(num):
    return hex(num)[2:]


class PerRegionTextConvert(sublime_plugin.TextCommand):
    def pre(self):
        pass

    def post(self):
        pass

    def per_region(self, region_text):
        return region_text

    def run(self, edit):
        self.pre()
        view = self.view
        regions = view.sel()

        for region in regions:
            val = view.substr(region)
            view.replace(edit, region, self.per_region(val))

        self.post()


class PerLineTextConvert(PerRegionTextConvert):
    def pre(self):
        self.linebreak = "\n"

    def per_line(self, line):
        return line

    def per_region(self, region):
        lines = region.split(self.linebreak)
        return self.linebreak.join(map(self.per_line, lines))


class PerWordTextConvert(PerRegionTextConvert):
    def pre(self):
        self.word_regex = re.compile("(\\s+)")

    def per_word(self, word):
        return word

    def per_region(self, region):
        word_result = ""

        words = self.word_regex.split(region)

        for word in words:

            if self.word_regex.match(word):
                word_result += word
                continue

            word_result += self.per_word(word)

        return word_result


class PerIntegerTextConvert(PerWordTextConvert):
    def per_int(self, intval):
        pass

    def per_word(self, word):
        val = string_as_integer(word)

        if val is not None:
            return self.per_int(val)

        return word
