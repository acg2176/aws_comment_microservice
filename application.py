# Import functions and objects the microservice needs.
# - Flask is the top-level application. You implement the application by adding methods to it.
# - Response enables creating well-formed HTTP/REST responses.
# - requests enables accessing the elements of an incoming HTTP/REST request.
#
import json

# Setup and use the simple, common Python logging framework. Send log messages to the console.
# The application should get the log level out of the context. We will change later.
#

import os
import sys
import ast
import platform
import socket
import boto3
import dynamo_db as db

from flask import Flask, Response
from flask import request

cwd = os.getcwd()
sys.path.append(cwd)

print("*** PYTHONPATH = " + str(sys.path) + "***")

import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Create the application server main class instance and call it 'application'
# Specific the path that identifies the static content and where it is.
application = Flask(__name__,
                    static_url_path='/static',
                static_folder='WebSite/static')

#Table
# TABLE = 'comments'

dynamodb = boto3.resource('dynamodb',
                          # aws_access_key_id=aws_access_key_id,
                          # aws_secret_access_key=aws_secret_access_key,
                          region_name='us-west-2')

other_client = boto3.client("dynamodb")


# 1. Extract the input information from the requests object.
# 2. Log the information
# 3. Return extracted information.
#
def log_and_extract_input(method, path_params=None):

    path = request.path
    args = dict(request.args)
    data = None
    headers = dict(request.headers)
    method = request.method

    try:
        if request.data is not None:
            data = request.json
        else:
            data = None
    except Exception as e:
        # This would fail the request in a more real solution.
        data = "You sent something but I could not get JSON out of it."

    log_message = str(datetime.now()) + ": Method " + method

    inputs =  {
        "path": path,
        "method": method,
        "path_params": path_params,
        "query_params": args,
        "headers": headers,
        "body": data
        }

    log_message += " received: \n" + json.dumps(inputs, indent=2)
    logger.debug(log_message)

    return inputs


def log_response(method, status, data, txt):

    msg = {
        "method": method,
        "status": status,
        "txt": txt,
        "data": data
    }

    logger.debug(str(datetime.now()) + ": \n" + json.dumps(msg, indent=2, default=str))


welcome = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
  <!--
    Copyright 2012 Amazon.com, Inc. or its affiliates. All Rights Reserved.

    Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

        http://aws.Amazon/apache2.0/

    or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
  -->
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>Welcome</title>
  <style>
  body {
    color: #ffffff;
    background-color: #E0E0E0;
    font-family: Arial, sans-serif;
    font-size:14px;
    -moz-transition-property: text-shadow;
    -moz-transition-duration: 4s;
    -webkit-transition-property: text-shadow;
    -webkit-transition-duration: 4s;
    text-shadow: none;
  }
  body.blurry {
    -moz-transition-property: text-shadow;
    -moz-transition-duration: 4s;
    -webkit-transition-property: text-shadow;
    -webkit-transition-duration: 4s;
    text-shadow: #fff 0px 0px 25px;
  }
  a {
    color: #0188cc;
  }
  .textColumn, .linksColumn {
    padding: 2em;
  }
  .textColumn {
    position: absolute;
    top: 0px;
    right: 50%;
    bottom: 0px;
    left: 0px;

    text-align: right;
    padding-top: 11em;
    background-color: #1BA86D;
    background-image: -moz-radial-gradient(left top, circle, #6AF9BD 0%, #00B386 60%);
    background-image: -webkit-gradient(radial, 0 0, 1, 0 0, 500, from(#6AF9BD), to(#00B386));
  }
  .textColumn p {
    width: 75%;
    float:right;
  }
  .linksColumn {
    position: absolute;
    top:0px;
    right: 0px;
    bottom: 0px;
    left: 50%;

    background-color: #E0E0E0;
  }

  h1 {
    font-size: 500%;
    font-weight: normal;
    margin-bottom: 0em;
  }
  h2 {
    font-size: 200%;
    font-weight: normal;
    margin-bottom: 0em;
  }
  ul {
    padding-left: 1em;
    margin: 0px;
  }
  li {
    margin: 1em 0em;
  }
  </style>
</head>
<body id="sample">
  <div class="textColumn">
    <h1>Congratulations</h1>
    <p>My second, modified AWS Elastic Beanstalk Python Application is now running on your own dedicated environment in the AWS Cloud</p>
    <h1>Getting uploaded to Elastic Beanstalk!</h1>
  </div>

  <div class="linksColumn"> 
    <h2>What's Next?</h2>
    <ul>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/">AWS Elastic Beanstalk overview</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/index.html?concepts.html">AWS Elastic Beanstalk concepts</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Python_django.html">Deploy a Django Application to AWS Elastic Beanstalk</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Python_flask.html">Deploy a Flask Application to AWS Elastic Beanstalk</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Python_custom_container.html">Customizing and Configuring a Python Container</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/using-features.loggingS3.title.html">Working with Logs</a></li>

    </ul>
  </div>
</body>
</html>
"""
@application.route("/")
def index():

    rsp = Response(welcome, status=200, content_type="text/html")
    return rsp


# This function performs a basic health check. We will flesh this out.
@application.route("/api/health", methods=["GET"])
def health_check():

    pf = platform.system()

    rsp_data = { "status": "healthy", "time": str(datetime.now()),
                 "platform": pf,
                 "release": platform.release()
                 }

    if pf == "Darwin":
        rsp_data["note"]= "For some reason, macOS is called 'Darwin'"


    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    rsp_data["hostname"] = hostname
    rsp_data["IPAddr"] = IPAddr

    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="application/json")
    return rsp

################comment service##################################
@application.route("/comments", methods=["GET"])
def comment_by_user_or_tag():
    user_id = request.args.get('user_id')
    tag = request.args.get('tag')
    res = db.find_by_user_or_tag(user_id, tag)
    if res is None:
        rsp = Response(json.dumps("Record with user {user_id} not found.".format(user_id=user_id)), status=404,
                       content_type="application/json")
    else:
        rsp = Response(json.dumps(res), status=201, content_type="application/json")
    return rsp


@application.route("/comments/<comment_id>", methods=["GET"])
def get_comment(comment_id):
    res = db.get_item("comments", {
        "comment_id": comment_id
    })
    if res is None:
        rsp = Response(json.dumps("Record with id {comment_id} not found.".format(comment_id=comment_id)), status=404,
                       content_type="application/json")
    else:
        rsp = Response(json.dumps(res), status=201, content_type="application/json")
    return rsp

@application.route("/comments/<comment_id>", methods=["PATCH"])
def update_comment(comment_id):
    old_comment = db.get_item("comments", {"comment_id": comment_id})
    old_version_id = old_comment["version_id"]
    new_comment = ast.literal_eval(request.data.decode("UTF-8"))
    res = db.write_comment_if_not_changed(new_comment, old_comment)
    if res is None:
        rsp = Response(json.dumps("Record with id {comment_id} not found.".format(comment_id=comment_id)), status=404,
                       content_type="application/json")
    else:
        rsp = Response(json.dumps(res), status=204, content_type="text/plain")
    return rsp

@application.route("/comments/<comment_id>/responses", methods=["GET"])
def get_responses(comment_id):
    res = db.get_item("comments", {
        "comment_id": comment_id
    })["responses"]
    if res is None:
        rsp = Response(json.dumps("Record with id {comment_id} not found.".format(comment_id=comment_id)), status=404,
                       content_type="application/json")
    else:
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp
#fix this with args
@application.route("/comments/<comment_id>/responses", methods=["POST"])
def add_new_response(comment_id):
    args = ast.literal_eval(request.data.decode("UTF-8"))
    user_id = args.get("user_id")
    response_text = args.get("response_text")
    res = db.add_response("comments",
                          comment_id,
                          user_id,
                          response_text)
    if res is None:
        rsp = Response(json.dumps("Record with id {comment_id} not found.".format(comment_id=comment_id)), status=404,
                       content_type="application/json")
    else:
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp



# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.

    application.run(port=8000)