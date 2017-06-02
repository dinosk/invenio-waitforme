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

"""Command Line Interface."""

from __future__ import absolute_import, print_function

import click

from .utils import elasticsearch, postgres, rabbitmq, redis


@click.group('wait-for')
def wait_for():
    """Invenio-Waitforme related commands."""


@wait_for.command('elasticsearch')
@click.argument('uri', default=['http://localhost:9200/'])
@click.argument('timeout', default=5)
@click.argument('status', default='green')
def elasticsearch_cmd(timeout, uri, status):
    """Check elasticsearch status."""
    elasticsearch(timeout, uri, status)
    click.secho('Elasticsearch is %s.' % status, fg='green')


@wait_for.command('redis')
@click.argument('timeout', default=5)
@click.argument('uri', default='redis://127.0.0.1:6379')
def redis_cmd(timeout, uri):
    """Check redis server status."""
    redis(timeout, uri)
    click.secho('redis-server is up.', fg='green')


@wait_for.command('rabbitmq')
@click.argument('timeout', default=5)
@click.argument('uri', default='localhost')
def rabbitmq_cmd(timeout, uri):
    """Check rabbitmq server status."""
    rabbitmq(timeout, uri)
    click.secho('rabbitmq-server is up.', fg='green')


@wait_for.command('postgres')
@click.argument('timeout', default=5)
@click.argument('host', default='localhost')
@click.argument('dbname', default='invenio')
@click.argument('dbpass', default='')
@click.argument('user', default='postgres')
def postgres_cmd(timeout, host, dbname, dbpass, user):
    """Check elasticsearch status."""
    postgres(timeout, host, dbname, dbpass, user)
    click.secho('Postgres is up.', fg='green')
