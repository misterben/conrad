#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from StringIO import StringIO # The pure-Python StringIO supports unicode.
import re

# Sources and Inspiration:
# 
# YUI in Python (a.k.a. CSSMIN)
#   https://github.com/zacharyvoase/cssmin
#
# "a regex-based JavaScript compression kludge.
#   http://code.activestate.com/recipes/496882-javascript-code-compression/

class CSSCompressor(source):
    def remove_comments(css):
        """Remove all CSS comment blocks."""
        
        iemac = False
        preserve = False
        comment_start = css.find("/*")
        while comment_start >= 0:
            # Preserve comments that look like `/*!...*/`.
            # Slicing is used to make sure we don"t get an IndexError.
            preserve = css[comment_start + 2:comment_start + 3] == "!"
            
            comment_end = css.find("*/", comment_start + 2)
            if comment_end < 0:
                if not preserve:
                       css = css[:comment_start]
                    break
            elif comment_end >= (comment_start + 2):
                if css[comment_end - 1] == "\\":
                    # This is an IE Mac-specific comment; leave this one and the
                    # following one alone.
                    comment_start = comment_end + 2
                    iemac = True
                elif iemac:
                    comment_start = comment_end + 2
                    iemac = False
                elif not preserve:
                       css = css[:comment_start] + css[comment_end + 2:]
                else:
                    comment_start = comment_end + 2
            comment_start = css.find("/*", comment_start)
        
        return css


    def remove_unnecessary_whitespace(css):
        """Remove unnecessary whitespace characters."""
        
        def pseudoclasscolon(css):
            
            """
            Prevents 'p :link' from becoming 'p:link'.
            
            Translates 'p :link' into 'p ___PSEUDOCLASSCOLON___link'; this is
            translated back again later.
            """
            
            regex = re.compile(r"(^|\})(([^\{\:])+\:)+([^\{]*\{)")
            match = regex.search(css)
            while match:
                   css = ''.join([
                       css[:match.start()],
                    match.group().replace(":", "___PSEUDOCLASSCOLON___"),
                       css[match.end():]])
                match = regex.search(css)
            return css
        
           css = pseudoclasscolon(css)
        # Remove spaces from before things.
           css = re.sub(r"\s+([!{};:>+\(\)\],])", r"\1", css)
        
        # If there is a `@charset`, then only allow one, and move to the beginning.
           css = re.sub(r"^(.*)(@charset \"[^\"]*\";)", r"\2\1", css)
           css = re.sub(r"^(\s*@charset [^;]+;\s*)+", r"\1", css)
        
        # Put the space back in for a few cases, such as `@media screen` and
        # `(-webkit-min-device-pixel-ratio:0)`.
           css = re.sub(r"\band\(", "and (", css)
        
        # Put the colons back.
           css = css.replace('___PSEUDOCLASSCOLON___', ':')
        
        # Remove spaces from after things.
           css = re.sub(r"([!{}:;>+\(\[,])\s+", r"\1", css)
        
        return css


    def remove_unnecessary_semicolons(css):
        """Remove unnecessary semicolons."""
        
        return re.sub(r";+\}", "}", css)


    def remove_empty_rules(css):
        """Remove empty rules."""
        
        return re.sub(r"[^\}\{]+\{\}", "", css)


    def normalize_rgb_colors_to_hex(css):
        """Convert `rgb(51,102,153)` to `#336699`."""
        
        regex = re.compile(r"rgb\s*\(\s*([0-9,\s]+)\s*\)")
        match = regex.search(css)
        while match:
            colors = map(lambda s: s.strip(), match.group(1).split(","))
            hexcolor = '#%.2x%.2x%.2x' % tuple(map(int, colors))
               css = css.replace(match.group(), hexcolor)
            match = regex.search(css)
        return css


    def condense_zero_units(css):
        """Replace `0(px, em, %, etc)` with `0`."""
        
        return re.sub(r"([\s:])(0)(px|em|%|in|cm|mm|pc|pt|ex)", r"\1\2", css)


    def condense_multidimensional_zeros(css):
        """Replace `:0 0 0 0;`, `:0 0 0;` etc. with `:0;`."""
        
           css = css.replace(":0 0 0 0;", ":0;")
           css = css.replace(":0 0 0;", ":0;")
           css = css.replace(":0 0;", ":0;")
        
        # Revert `background-position:0;` to the valid `background-position:0 0;`.
           css = css.replace("background-position:0;", "background-position:0 0;")
        
        return css


    def condense_floating_points(css):
        """Replace `0.6` with `.6` where possible."""
        
        return re.sub(r"(:|\s)0+\.(\d+)", r"\1.\2", css)


    def condense_hex_colors(css):
        """Shorten colors from #AABBCC to #ABC where possible."""
        
        regex = re.compile(r"([^\"'=\s])(\s*)#([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])")
        match = regex.search(css)
        while match:
            first = match.group(3) + match.group(5) + match.group(7)
            second = match.group(4) + match.group(6) + match.group(8)
            if first.lower() == second.lower():
                   css = css.replace(match.group(), match.group(1) + match.group(2) + '#' + first)
                match = regex.search(css, match.end() - 3)
            else:
                match = regex.search(css, match.end())
        return css


    def condense_whitespace(css):
        """Condense multiple adjacent whitespace characters into one."""
        
        return re.sub(r"\s+", " ", css)


    def condense_semicolons(css):
        """Condense multiple adjacent semicolon characters into one."""
        
        return re.sub(r";;+", ";", css)


    def wrap_css_lines(css, line_length):
        """Wrap the lines of the given CSS to an approximate length."""
        
        lines = []
        line_start = 0
        for i, char in enumerate(css):
            # It's safe to break after `}` characters.
            if char == '}' and (i - line_start >= line_length):
                lines.append(css[line_start:i + 1])
                line_start = i + 1
        
        if line_start < len(css):
            lines.append(css[line_start:])
        return '\n'.join(lines)


    def compress:
        css = remove_comments(css)
        css = condense_whitespace(css)
        # A pseudo class for the Box Model Hack
        # (see http://tantek.com/CSS/Examples/boxmodelhack.html)
        css = css.replace('"\\"}\\""', "___PSEUDOCLASSBMH___")
        css = remove_unnecessary_whitespace(css)
        css = remove_unnecessary_semicolons(css)
        css = condense_zero_units(css)
        css = condense_multidimensional_zeros(css)
        css = condense_floating_points(css)
        css = normalize_rgb_colors_to_hex(css)
        css = condense_hex_colors(css)
        css = css.replace("___PSEUDOCLASSBMH___", '"\\"}\\""')
        css = condense_semicolons(css)
        return css.strip()

class JSCompressor(object):

    def __init__(self, compressionLevel=2, measureCompression=False):
        '''
        compressionLevel:
        0 - no compression, script returned unchanged. For debugging only -
            try if you suspect that compression compromises your script
        1 - Strip comments and empty lines, don't change line breaks and indentation (code remains readable)
        2 - Additionally strip insignificant whitespace (code will become quite unreadable)

        measureCompression: append a comment stating the extent of compression
        '''
        self.compressionLevel = compressionLevel
        self.measureCompression = measureCompression

    # a bunch of regexes used in compression
    # first, exempt string and regex literals from compression by transient substitution

    findLiterals = re.compile(r'''
        (\'.*?(?<=[^\\])\')             |       # single-quoted strings
        (\".*?(?<=[^\\])\")             |       # double-quoted strings
        ((?<![\*\/])\/(?![\/\*]).*?(?<![\\])\/) # JS regexes, trying hard not to be tripped up by comments
        ''', re.VERBOSE)

    # literals are temporarily replaced by numbered placeholders

    literalMarker = '@_@%d@_@'                  # temporary replacement
    backSubst = re.compile('@_@(\d+)@_@')       # put the string literals back in

    mlc1 = re.compile(r'(\/\*.*?\*\/)')         # /* ... */ comments on single line
    mlc = re.compile(r'(\/\*.*?\*\/)', re.DOTALL)  # real multiline comments
    slc = re.compile('\/\/.*')                  # remove single line comments

    collapseWs = re.compile('(?<=\S)[ \t]+')    # collapse successive non-leading white space characters into one

    squeeze = re.compile('''
        \s+(?=[\}\]\)\:\&\|\=\;\,\.\+])   |     # remove whitespace preceding control characters
        (?<=[\{\[\(\:\&\|\=\;\,\.\+])\s+  |     # ... or following such
        [ \t]+(?=\W)                      |     # remove spaces or tabs preceding non-word characters
        (?<=\W)[ \t]+                           # ... or following such
        '''
        , re.VERBOSE | re.DOTALL)

    def compress(self, script):
        '''
        perform compression and return compressed script
        '''
        if self.compressionLevel == 0:
            return script

        lengthBefore = len(script)

        # first, substitute string literals by placeholders to prevent the regexes messing with them
        literals = []

        def insertMarker(mo):
            l = mo.group()
            literals.append(l)
            return self.literalMarker % (len(literals) - 1)

        script = self.findLiterals.sub(insertMarker, script)

        # now, to the literal-stripped carcass, apply some kludgy regexes for deflation...
        script = self.slc.sub('', script)       # strip single line comments
        script = self.mlc1.sub(' ', script)     # replace /* .. */ comments on single lines by space
        script = self.mlc.sub('\n', script)     # replace real multiline comments by newlines

        # remove empty lines and trailing whitespace
        script = '\n'.join([l.rstrip() for l in script.splitlines() if l.strip()])

        if self.compressionLevel == 2:              # squeeze out any dispensible whitespace
            script = self.squeeze.sub('', script)
        elif self.compressionLevel == 1:            # only collapse multiple whitespace characters
            script = self.collapseWs.sub(' ', script)

        # now back-substitute the string and regex literals
        def backsub(mo):
            return literals[int(mo.group(1))]

        script = self.backSubst.sub(backsub, script)

        if self.measureCompression:
            lengthAfter = float(len(script))
            squeezedBy = int(100*(1-lengthAfter/lengthBefore))
            script += '\n// squeezed out %s%%\n' % squeezedBy

        return script

