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

from .utils import elasticsearch, postgres, redis, rabbitmq


@click.group('wait-for')
def wait_for():
    """Invenio-Waitforme related commands."""


@wait_for.command('elasticsearch')
@click.argument('status', default='green')
def elasticsearch_cmd(status):
    elasticsearch(status)
    click.secho('Elasticsearch is %s.' % status, fg='green')


@wait_for.command('redis')
@click.argument('status', default='up')
def redis_cmd(status):
    redis(status)
    click.secho('redis-server is %s.' % status, fg='green')


@wait_for.command('rabbitmq')
@click.argument('status', default='up')
def rabbitmq_cmd(status):
    rabbitmq(status)
    click.secho('rabbitmq-server is %s.' % status, fg='green')


@wait_for.command('postgres')
@click.argument('status', default='up')
def postgres_cmd(status):
    postgres(status)
    click.secho('Postgres is %s.' % status, fg='green')
