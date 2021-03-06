# Copyright (C) 2015  The Debsources developers <info@sources.debian.net>.
# See the AUTHORS file at the top-level directory of this distribution and at
# https://anonscm.debian.org/gitweb/?p=qa/debsources.git;a=blob;f=AUTHORS;hb=HEAD
#
# This file is part of Debsources. Debsources is free software: you can
# redistribute it and/or modify it under the terms of the GNU Affero General
# Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.  For more information
# see the COPYING file at the top-level directory of this distribution and at
# https://anonscm.debian.org/gitweb/?p=qa/debsources.git;a=blob;f=COPYING;hb=HEAD

from __future__ import absolute_import

import os.path
import unittest

from nose.tools import istest
from nose.plugins.attrib import attr

from debsources.hashutil import sha1sum, sha256sum
from debsources.tests.testdata import TEST_DATA_DIR


def make_path(path):
    return os.path.join(TEST_DATA_DIR, 'sources', path)


@attr('hashutil')
class HashutilTests(unittest.TestCase):
    """ Unit tests for debsources.hashutil """

    @istest
    def assertSha1Sum(self):
        self.assertEqual(
            sha1sum(make_path('main/libc/libcaca/0.99.beta18-1/COPYING')),
            'b57075f60950289e0f32be3145b74b7b17e6e5c5')

    @istest
    def assertSha256Sum(self):
        self.assertEqual(
            sha256sum(make_path('main/libc/libcaca/0.99.beta18-1/COPYING')),
            'd10f0447c835a590ef137d99dd0e3ed29b5e032e7434a87315b30402bf14e7fd')
