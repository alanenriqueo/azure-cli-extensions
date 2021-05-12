# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------
import argparse
from knack.util import CLIError
from knack.prompting import prompt, prompt_y_n


def validate_source_resource(cmd, namespace):
    from azure.mgmt.core.tools import resource_id, is_valid_resource_id
    from azure.cli.core.commands.client_factory import get_subscription_id
    if namespace.webapp:
        namespace.source_provider = 'Microsoft.Web'
        namespace.source_resource_type = 'sites'
        namespace.source_resource_name = namespace.webapp
        del namespace.webapp
        return
    webapp = cmd.cli_ctx.local_context.get('cupertino', 'web_name')
    if webapp:
        if prompt_y_n('Found webapp:' + webapp + ' in local context, do you want to use it as source resource?'):
            namespace.source_provider = 'Microsoft.Web'
            namespace.source_resource_type = 'sites'
            namespace.source_resource_name = webapp
            del namespace.webapp
        else:
            raise Exception('Source resource is required.')


def validate_target_resource(cmd, namespace):
    from azure.mgmt.core.tools import resource_id
    from azure.cli.core.commands.client_factory import get_subscription_id
    resource_group = namespace.resource_group_name
    if namespace.target_resource_group_name:
        resource_group = namespace.target_resource_group_name
    if namespace.postgres:
        namespace.target_id = resource_id(
            subscription=get_subscription_id(cmd.cli_ctx),
            resource_group=resource_group,
            namespace='Microsoft.DBforPostgreSQL',
            type='servers',
            name=namespace.postgres,
        )
        if not namespace.database:
            raise Exception('--database is required.')
        namespace.target_id = namespace.target_id + '/databases/' + namespace.database
        if not namespace.linker_name:
            namespace.linker_name = 'Connection_' + namespace.postgres
        del namespace.postgres
        del namespace.database
        del namespace.target_resource_group_name
        return
    postgres = cmd.cli_ctx.local_context.get('cupertino', 'postgres_server_name')
    database = cmd.cli_ctx.local_context.get('cupertino', 'postgres_database_name')
    if postgres and database:
        if prompt_y_n('Found postgres:' + postgres + ' in local context, do you want to use it as target resource?'):
            namespace.target_id = resource_id(
                subscription=get_subscription_id(cmd.cli_ctx),
                resource_group=resource_group,
                namespace='Microsoft.DBforPostgreSQL',
                type='servers',
                name=postgres,
            )
            namespace.target_id = namespace.target_id + '/databases/' + database
            if not namespace.linker_name:
                namespace.linker_name = 'Connection_' + namespace.postgres
            del namespace.postgres
            del namespace.database
            del namespace.target_resource_group_name
        else:
            raise Exception('Target resource is required.')