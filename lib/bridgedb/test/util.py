# -*- coding: utf-8 -*-
#
# This file is part of BridgeDB, a Tor bridge distribution system.
#
# :authors: Isis Lovecruft 0xA3ADB67A2CDB8B35 <isis@torproject.org>
#           please also see AUTHORS file
# :copyright: (c) 2013, Isis Lovecruft
#             (c) 2007-2013, The Tor Project, Inc.
#             (c) 2007-2013, all entities within the AUTHORS file
# :license: 3-Clause BSD, see LICENSE for licensing information

"""Unittests utilitys the `bridgedb.test` package."""

from __future__ import print_function
from __future__ import unicode_literals

import abc
import doctest
import os

from functools import wraps

from twisted.trial import unittest


def fileCheckDecorator(func):
    """Method decorator for a t.t.unittest.TestCase test_* method.

    .. codeblock:: python

        import shutil
        from twisted.trial import unittest

        pyunit = __import__('unittest')

        class TestTests(unittest.TestCase):
            @fileCheckDecorator
            def doCopyFile(src, dst, description=None):
                shutil.copy(src, dst)
            def test_doCopyFile(self):
                srcfile = self.mktemp()
                dstfile = self.mktemp()
                with open(srcfile, 'wb') as fh:
                    fh.write('testing TestCase method decorator utility')
                    fh.flush()
                self.doCopyFile(srcfile, dstfile, 'asparagus')

        testtest = TestTests()
        testtest.runTest()

    ..

    :type func: callable
    :param func: The ``test_*`` method, from a
                 :api:`twisted.trial.unittest.TestCase` instance, to wrap.
    """
    @wraps(func)
    def wrapper(self, src, dst, description):
        self.assertTrue(os.path.isfile(src),
                        "Couldn't find original %s file: %r"
                        % (str(description), src))
        func(self, src, dst, description)
        self.assertTrue(os.path.isfile(dst),
                        "Couldn't find new %s file: %r. Original: %r"
                        % (str(description), dst, src))
    return wrapper


class TestCaseMixin:
    """Subclasses of me can be used as mix-in classes with ``TestCase``s."""
    __metaclass__ = abc.ABCMeta
TestCaseMixin.register(unittest.TestCase)


if __name__ == "__main__":
    doctest.run_docstring_examples(fileCheckDecorator, None)
