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

"""Module tests."""

from __future__ import absolute_import, print_function

import pytest
from invenio_waitforme.utils import elasticsearch as wait_for_elasticsearch
from invenio_waitforme.utils import redis as wait_for_redis
from invenio_waitforme.utils import rabbitmq as wait_for_rabbitmq
import testing.elasticsearch
from subprocess import Popen
import time
from invenio_waitforme.utils import time_limit, TimeoutException
from pika.exceptions import ConnectionClosed
from mock import Mock, patch


@patch('psycopg2.connect')
def test_wait_for_postgres(mock_connection):
    mock_connection.return_value = True
    with time_limit(3):
        wait_for_rabbitmq()

    mock_connection.return_value = ConnectionClosed()
    with pytest.raises(TimeoutException):
        with time_limit(3):
            wait_for_rabbitmq()


def test_wait_for_rabbitmq():
    mock_connection = Mock()
    mock_connection.return_value = True
    with time_limit(3):
        with patch('pika.BlockingConnection', new=mock_connection):
            wait_for_rabbitmq()

    mock_connection.return_value = ConnectionClosed()
    with pytest.raises(TimeoutException):
        with time_limit(3):
            with patch('pika.BlockingConnection', new=mock_connection):
                wait_for_rabbitmq()

    mock_connection.return_value = False
    with pytest.raises(TimeoutException):
        with time_limit(3):
            with patch('pika.BlockingConnection', new=mock_connection):
                wait_for_rabbitmq()


def test_wait_for_elasticsearch(app):
    with testing.elasticsearch.Elasticsearch() as elasticsearch:
        with time_limit(3):
            wait_for_elasticsearch(elasticsearch.dsn()['hosts'], 'green')

    with pytest.raises(TimeoutException):
        with time_limit(3):
            wait_for_elasticsearch()


def test_wait_for_redis(app):
    Popen(['redis-server'])
    wait_for_redis()
    time.sleep(3)
    Popen(['redis-cli', 'shutdown'])
    time.sleep(3)
    with pytest.raises(TimeoutException):
        with time_limit(3):
            wait_for_redis()
