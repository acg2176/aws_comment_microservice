import os
import sys
import platform
import socket
import ast
import bcrypt
from flask import Flask, Response
from flask import request

cwd = os.getcwd()
sys.path.append(cwd)
print("*** PYHTHONPATH = " + str(sys.path) + "***")

import logging
from datetime import datetime
import address_service
import user_service
import notification
import security

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


@ @-40

, 6 + 39, 16 @ @
static_url_path = '/static',
static_folder = 'WebSite/static')
 # 1. Extract the input information from the requests object.
 # 2. Log the information
@@ -228,164 +240,90 @@
     rsp = Response(rsp_str, status=200, content_type="application/json")
     return rsp