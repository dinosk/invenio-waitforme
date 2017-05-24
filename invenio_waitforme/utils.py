# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Utility Functions."""

from __future__ import absolute_import, print_function

import os
import sys
from redis import Redis
from redis.exceptions import ConnectionError
from waiting import wait
from elasticsearch import Elasticsearch
from subprocess import Popen, PIPE, CalledProcessError


class RedirectStdStreams(object):
    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush()
        self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush()
        self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr


def elasticsearch(status):
    es = Elasticsearch(['http://localhost:9200/'], verify_certs=True)

    if status == 'up':
        status = 'green'

    def predicate():
        devnull = open(os.devnull, 'w')
        with RedirectStdStreams(stdout=devnull, stderr=devnull):
            try:
                es.cluster.health()
            except Exception:
                return False
        return True

    wait(predicate)


def redis(status):
    red = Redis()

    def predicate():
        try:
            return red.ping()
        except ConnectionError:
            return False

    wait(predicate)


def rabbitmq(status):

    def predicate():
        try:
            child = Popen(['rabbitmqctl', 'status'],
                          stdout=PIPE)
            streamdata = child.communicate()[0]
            return_code = child.returncode
            # click.secho(streamdata.decode('utf-8'), fg='green')
        except Exception:
            return False
        return return_code == 0

    wait(predicate)


def postgres(status):

    def predicate():
        try:
            child = Popen(['pg_ctl', 'status', '-D',
                           '/Users/dinossimpson/CERN/postgres.db'],
                          stdout=PIPE)
                        import socket                                                                                                                                                              
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect(('localhost', 5432))
                s.close()
            except socket.error, ex:
                print("Connection failed with errno {0}: {1}".format(ex.errno, ex.strerror))
            streamdata = child.communicate()[0]
            return_code = child.returncode
            # click.secho(streamdata.decode('utf-8'), fg='green')
        except CalledProcessError as e:
            return False
        return return_code == 0

    wait(predicate)
