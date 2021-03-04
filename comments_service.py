import json
import dynamo_db as db
# import application as app

# def t1(comment_id):
#     res = db.get_item("comments", {
#         "comment_id": comment_id
#     })
#     print("Result= \n", json.dumps(res, indent=4))
#
# t1("03d0e62d-d2df-430d-bbb0-55f7eb039b6d")

# queries the table, 	GET -- Returns comments matching a query string. Your query string must support
# querying by email and/or tag.
# A comment matches if its tag list contains the requested tag.

# def t3(tag): # query by tag
#     res = db.find_by_tag(tag)
#     print("Result= \n", json.dumps(res, indent=4))
#
# t3("happy")

# def t4(email, tag):
#     res = db.find_by_email_or_tag(email, tag)
#     print("Result= \n", json.dumps(res, indent = 4))
#     return json.dumps(res, indent = 4)
#
# t4("dmalfoy@gmail.com", "happy")

def t5():
    # table_name, comment_id, commenter_email, response
    res = db.add_response("comments",
                          "d05b3120-8428-4905-a26e-d357ad318cfe",
                          "ssnape@gmail.com",
                          "Yessir")
    print("Result= \n", json.dumps(res, indent = 4))

t5()
# import copy

# def t6():
#     comment_id = "03d0e62d-d2df-430d-bbb0-55f7eb039b6d"
#     old_comment = db.get_item("comments", {"comment_id": comment_id})
#     old_version_id = old_comment["version_id"]
    new_comment = {
  "comment_id": "03d0e62d-d2df-430d-bbb0-55f7eb039b6d",
  "comment_text": "Hi!",
  "email": "dmalfoy@gmail.com",
  "datetime": "2020-05-11 10:06:57",
  "tags": [
    "happy",
    "excited"
    ],
  "version_id": "15155336-f80d-4fe4-80cd-c4ffa7b014a0",
  "responses": [
    {
        "response_text": "I disagree.",
        "datetime": "2020-12-04 04:00:19",
        "version_id": "14e95b13-ec4f-44e9-be19-8944313ecc7b",
        "response_id": "3d0c4005-7bdd-4ed5-ac73-15d3ec7b0515",
        "email": "hpotter@gmail.com"
    }
  ]
}
#     res = db.write_comment_if_not_changed(new_comment, old_comment)
#     print("Result= \n", json.dumps(res, indent = 4))
# t6()



# table = db.Table("comments")
# import uuid
# db.put_item("comments",
#     item={
#   "comment_id": str(uuid.uuid4()),
#   "comment_text": "This is amazing!",
#   "email": "dmalfoy@gmail.com",
#   "datetime": "2020-03-07 12:40:37",
#   "tags": [
#     "happy",
#     "excited"
#     ],
#   "version_id": str(uuid.uuid4()),
#   "responses": [
#     {
#       "response_id": str(uuid.uuid4()),
#       "response_text": "I disagree.",
#       "email": "hpotter@gmail.com",
#       "datetime": "2020-12-04 04:00:19",
#       "version_id": str(uuid.uuid4())
#     }]
# }
#
#
# )

# def t7():
#     res = db.find_by_template("comments",
#                               {"email": "dmalfoy@gmail.com",
#                                      "tags": "happy"})
#     print("Result= \n", json.dumps(res, indent = 4))
#     return json.dumps(res, indent = 4)


# def t8():
#     res = db.find_by_email_or_tag({"email": "dmalfoy@gmail.com",
#                                      "tags": "happy"})
#     print("Result= \n", json.dumps(res, indent = 4))
#     return json.dumps(res, indent = 4)



# test for post request add response:
    {

    "commenter_email": "hagrid@gmail.com",
    "response": "Gee whiz"
}



# {
#   "comment_id": "03d0e62d-d2df-430d-bbb0-55f7eb039b6d",
#   "comment_text": "Great Job!",
#   "datetime": "2020-05-11 10:06:57",
#   "responses": [
#     {
#       "datetime": "2020-12-04 04:00:19",
#       "response_id": "3d0c4005-7bdd-4ed5-ac73-15d3ec7b0515",
#       "response_text": "I disagree.",
#       "user_id": "2",
#       "version_id": "14e95b13-ec4f-44e9-be19-8944313ecc7b"
#     },
#     {
#       "datetime": "2020-12-09 04:29:14",
#       "response": null,
#       "response_id": "c53fab91-a9be-4302-95ba-f0c8dff9b583",
#       "user_id": "3",
#       "version_id": "ddbcda5f-d71c-4ca8-858d-a1f96393fb3b"
#     },
#     {
#       "datetime": "2020-12-09 04:31:53",
#       "response": null,
#       "response_id": "273d08c2-1675-494d-bf6c-dec510dcb9db",
#       "user_id": "4",
#       "version_id": "99a04004-a3b7-4e2a-ab06-c369dab8143c"
#     }
#   ],
#   "tags": [
#     "happy",
#     "excited"
#   ],
#   "user_id": "1",
#   "version_id": "b02c3d4e-4cda-4354-a64b-8936244b5a60"
# }