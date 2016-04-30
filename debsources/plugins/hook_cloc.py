# Copyright (C) 2016  The Debsources developers <info@sources.debian.net>.
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

import logging
import os
import subprocess

from debsources import db_storage

from debsources.models import Cloccounts, File


conf = None

CLOC_FLAGS = ['--by-file-by-lang',
              '-csv',
              '--skip-uniqueness',
              '--quiet']

CLOC_START = "language,filename,blank,comment,code,"
CLOC_END = "files,language,blank,comment,code,"

MY_NAME = 'cloc'
MY_EXT = '.' + MY_NAME


def cloc_path(pkgdir):
    return pkgdir + MY_EXT


def parse_cloc(path):
    with open(path) as cloc:
        for line in cloc:
            if CLOC_START in line:
                break
        for line in cloc:
            if CLOC_END in line:
                break
            yield line.split(',')


def add_package(session, pkg, pkgdir, file_table):
    global conf
    logging.debug('add-package %s' % pkg)

    clocfile = cloc_path(pkgdir)
    clocfile_tmp = clocfile + '.new'

    if 'hooks.fs' in conf['backends']:
        if not os.path.exists(clocfile):  # extract tags only if needed
            cmd = ['cloc'] + CLOC_FLAGS + ['--out', clocfile_tmp, pkgdir]
            # ASSUMPTION: will be run under pkgdir as CWD, which is needed to
            # get relative paths right. The assumption is enforced by the
            # updater
            try:
                subprocess.check_call(cmd)
            except subprocess.CalledProcessError as e:
                logging.error("Cloc on %s %s failed with error: %s" %
                              (pkg['package'], pkg['version'], e.output))
                return
            os.rename(clocfile_tmp, clocfile)

    if 'hooks.db' in conf['backends']:
        db_package = db_storage.lookup_package(session, pkg['package'],
                                               pkg['version'])
        if not (session.query(Cloccounts)
                .filter_by(package_id=db_package.id)).first():
            # ASSUMPTION: if *a* ctag of this package has already been added to
            # the db in the past, then *all* of them have, as additions are
            # part of the same transaction
            for cloc in parse_cloc(clocfile):
                if file_table:
                    try:
                        file_id = file_table[cloc[1].replace(pkgdir + '/', "")]
                    except KeyError:
                        continue
                else:
                    file_ = (session.query(File)
                             .filter_by(package_id=db_package.id,
                                        path=cloc[1].replace(pkgdir + '/', ""))
                             .first())
                    if not file_:
                        continue
                    file_id = file_.id
                params = {'package_id': db_package.id,
                          'code_count': cloc[4],
                          'blank_count': cloc[3],
                          'comment_count': cloc[2],
                          'language': cloc[0],
                          'file_id': file_id}
                insert = Cloccounts(**params)
                session.add(insert)


def rm_package(session, pkg, pkgdir, file_table):
    global conf
    logging.debug('rm-package %s' % pkg)

    if 'hooks.fs' in conf['backends']:
        clocfile = cloc_path(pkgdir)
        if os.path.exists(clocfile):
            os.unlink(clocfile)

    if 'hooks.db' in conf['backends']:
        db_package = db_storage.lookup_package(session, pkg['package'],
                                               pkg['version'])
        session.query(Cloccounts) \
               .filter_by(package_id=db_package.id) \
               .delete()


def init_plugin(debsources):
    global conf
    conf = debsources['config']
    debsources['subscribe']('add-package', add_package, title=MY_NAME)
    debsources['subscribe']('rm-package', rm_package, title=MY_NAME)
    debsources['declare_ext'](MY_EXT, MY_NAME)
