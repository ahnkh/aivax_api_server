
import sys
import os

import datetime
from datetime import date, timedelta
import time

import traceback

import json

from fastapi import Request
from fastapi import Response, HTTPException
from fastapi import Header, Cookie, Depends

from fastapi.responses import JSONResponse

import pydantic

from typing import Any, Dict, List, Optional

import requests
import urllib3
urllib3.disable_warnings()

from libutil.logger import *

from libglobal.global_const import *

from libconv.py_conv import *

from libjson.json_helper import JsonHelper
from libutil.file_io_helper import FileIOHelper

from libutil.string_buffer_bulk_writer import StringBufferBulkWriter

from libutil.schedule_util import ScheduleUtil

from libsql.connector.db_connector import DBConnector
from libsql.connector.mariadb_connector import MariaDBConnector
from libsql.connector.sqlite_connector import SQLiteConnector

from libsql.query_helper.query_helper import QueryHelper

from libhttprequest.local_define.http_request_define import HttpRequestDefine
from libhttprequest.http_request_interface import HttpRequestInterface

from libhttp.restapi.api_response_handler import ApiResponseHandler

from libnetwork.network_util import NetworkUtil

from libmail.smtp_mail_sender import SMTPMailSender
from libmail.mail_style_text_convertor import MailStyleTextConvertor

from liboffice.office_document_reader import OfficeDocumentReader

from common_modules.const_define.kshell_global_define import KShellGlobalDefine
from common_modules.const_define.kshell_parameter_define import KShellParameterDefine

from common_modules.const_define.factory_instance_define import FactoryInstanceDefine, InstanceModulePathDefine
from common_modules.const_define.db_sql_define import DBSQLDefine, DBQueryObject

from common_modules.const_define.json_local_config_define import JsonLocalConfigDefine
from common_modules.const_define.web_api_define import WebApiDefine
from common_modules.const_define.error_define import ErrorDefine

ERR_OK = 1
ERR_FAIL = -1 
CONFIG_OPT_ENABLE = 1
CONFIG_OPT_DISABLE = 0

KSHELL_APP_ROOT = "./"
CONFIG_BASE_PATH = "./local_resource/config/wins-config.json"
TRACE_LOG_PATH = "./trace-log"
TRACE_PREFIX = "aivax"

from common_modules.module_function import *
