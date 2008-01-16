# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework
"""
This is based on  rlcompleter module, but
without code that depends on readline.
"""

import __builtin__
import __main__

import keyword, re, sets

reAttribute = re.compile(r"(\w+(\.\w+)*)\.(\w*)")


class Completer:

    def __init__(self, namespace = None):
        if namespace and not isinstance(namespace, dict):
            raise TypeError,'namespace must be a dictionary'
        if namespace is None:
            namespace = __main__.__dict__
        self.namespace = namespace


    def matches(self, text):
        """Return a list of possible completion for 'text'"""
        if "." in text:
            m = self.attr_matches(text)
        else:
            m = self.global_matches(text)
        return m


    def global_matches(self, text):
        """Compute matches when text is a simple name.

        Return a list of all keywords, built-in functions and names currently
        defined in self.namespace that match.

        """
        matches = sets.Set()
        n = len(text)
        for list in [keyword.kwlist, __builtin__.__dict__, self.namespace]:
            for word in list:
                if word[:n] == text and word != "__builtins__":
                    matches.add(word)
        return matches


    def attr_matches(self, text):
        """Compute matches when text contains a dot.

        Assuming the text is of the form NAME.NAME....[NAME], and is
        evaluatable in self.namespace, it will be evaluated and its attributes
        (as revealed by dir()) are used as possible completions.  (For class
        instances, class members are also considered.)

        WARNING: this can still invoke arbitrary C code, if an object
        with a __getattr__ hook is evaluated.
        """
        m = reAttribute.match(text)
        if not m:
            return
        expr, attr = m.group(1, 3)
        object = eval(expr, self.namespace)
        words = dir(object)
        if hasattr(object,'__class__'):
            words.append('__class__')
            words = words + get_class_members(object.__class__)
        matches = sets.Set()
        n = len(attr)
        for word in words:
            if word[:n] == attr and word != "__builtins__":
                matches.add("%s.%s" % (expr, word))
        return matches


def get_class_members(klass):
    ret = dir(klass)
    if hasattr(klass,'__bases__'):
        for base in klass.__bases__:
            ret = ret + get_class_members(base)
    return ret
