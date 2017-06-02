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
import signal
import sys
from contextlib import contextmanager

import psycopg2
from elasticsearch import Elasticsearch
import pika
from pika.exceptions import ConnectionClosed
from redis import Redis
from redis.exceptions import ConnectionError
from waiting import wait


class TimeoutException(Exception):
    """Timeout exception."""

    pass


@contextmanager
def time_limit(seconds):
    """Context manager throwing timeout exceptions."""
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


class RedirectStdStreams(object):
    """Context manager to redirect stdout and stderr."""

    def __init__(self, stdout=None, stderr=None):
        """Initialize instance."""
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        """Run on entry of redirected output block."""
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush()
        self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        """Run on exit of redirected output block."""
        self._stdout.flush()
        self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr


def elasticsearch(timeout=5, uri=['http://localhost:9200/'], status='green'):
    """Wait for elasticsearch to start."""
    es = Elasticsearch(uri, verify_certs=True)

    def predicate():
        devnull = open(os.devnull, 'w')
        with RedirectStdStreams(stdout=devnull, stderr=devnull):
            try:
                es.cluster.health()
            except Exception:
                return False
        return True

    with time_limit(timeout):
        wait(predicate)


def redis(timeout=5, uri=None):
    """Wait for redis to start."""
    red = Redis(uri)

    def predicate():
        try:
            return red.ping()
        except ConnectionError:
            return False

    with time_limit(timeout):
        wait(predicate)


def rabbitmq(timeout=5, uri='localhost'):
    """Wait for rabbitmq to start."""
    def predicate():
        devnull = open(os.devnull, 'w')

        with RedirectStdStreams(stdout=devnull, stderr=devnull):
            try:
                pika.BlockingConnection(pika.ConnectionParameters(uri))
            except ConnectionClosed as e:
                return False
        return True

    with time_limit(timeout):
        wait(predicate)


def postgres(timeout=5, host='localhost', dbname='invenio', dbpass='',
             user='postgres'):
    """Wait for postgres to start."""
    def predicate():
        try:
            psycopg2.connect("dbname='" + dbname + "' user='" + user + "'"
                             "' host='" + host + "' password='" + dbpass + "'")
        except Exception:
            return False
        return True

    with time_limit(timeout):
        wait(predicate)
