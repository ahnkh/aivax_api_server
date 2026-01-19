
import sys
import os

import datetime
from datetime import date, timedelta
import time

import traceback

import json

from fastapi import FastAPI, APIRouter, Request, Response, HTTPException, Header, Cookie, Depends

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

from libsql.connector.db_connector import DBConnector
from libsql.connector.mariadb_connector import MariaDBConnector
from libsql.connector.sqlite_connector import SQLiteConnector

from libsql.query_helper.query_helper import QueryHelper

from libhttprequest.local_define.http_request_define import HttpRequestDefine
from libhttprequest.http_request_interface import HttpRequestInterface

from libhttp.restapi.api_response_handler import ApiResponseHandler

from libnetwork.network_util import NetworkUtil

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
CONFIG_BASE_PATH = "./local_resource/config/base-config.json"
TRACE_LOG_PATH = "./trace-log"
TRACE_PREFIX = "api_server"

from mainapp.global_resource.module_function import http_request
from mainapp.global_resource.module_function import UTF8Text
from mainapp.global_resource.module_function import sqlprintf