
from .dependencies import DEPENDENCIES
import os

PROTOCOL = "http://"
DOMAIN = "localhost"
VARIABLES_FOR_SUBSTITUTION = {
    "DOMAIN": DOMAIN,
    "PROTOCOL": PROTOCOL,
    "COMPLETE_PATH": "http://localhost",
    "PUBLIC_NETWORK": os.getenv("NETWORK_NAME")
}

APPLICATIONS = {
    "googledrive": {
        "info": {
            "icon": "https://upload.wikimedia.org/wikipedia/commons/d/da/Google_Drive_logo.png",
            "name": "Google Drive",
            "large_name": "Google drive resource editor",
            "description": "Google Drive is a file storage and synchronization service developed by Google. Launched on April 24, 2012, Google Drive allows users to store files in the cloud, synchronize files across devices, and share files. Google Drive encompasses Google Docs, Google Sheets, and Google Slides, which are a part of the Google Docs Editors office suite that permits collaborative editing of documents, spreadsheets, presentations, drawings, forms, and more. Files created and edited through the Google Docs suite are saved in Google Drive. This software INTERLIKER allows users of the collaborative environment to create new documents, spreadsheets and presentations which can be co-edited and shared by co-production team participants",
            "snapshots": ["https://www.filo.news/export/sites/claro/img/2022/02/21/aisummary.gif_344325628.gif"],
            "preconditions": [],
            "url": "##COMPLETE_PATH##/googledrive/assets",
            "urls": {
                "instantiate": "##COMPLETE_PATH##/googledrive/assets/instantiate",
                "list": "##COMPLETE_PATH##/googledrive/api/v1/assets",
                "get": "##COMPLETE_PATH##/googledrive/assets/{id}",
                "clone": "##COMPLETE_PATH##/googledrive/assets/{id}/clone",
                "download": "##COMPLETE_PATH##/googledrive/assets/{id}/download",
                "view": "##COMPLETE_PATH##/googledrive/assets/{id}/view",
            },
            "action_text": "Create a new Google Drive resource"
        },
        "dependencies": ["mongodb"],
        "network": "##PUBLIC_NETWORK##",
        "configuration": {
            "routing": {
                "traefik": {
                    "inner_port": 80,
                    "prefix": "/googledrive",
                    "strip": True
                }
            },
            "editable": [
                {
                    "key": "GOOGLE_PROJECT_ID",
                    "default": "deep-sun-346308",
                    "mandatory": True
                },
                {
                    "key": "GOOGLE_PRIVATE_KEY_ID",
                    "default": "ada0de332ba04652feaeb05c2808369b2b4c65a8",
                    "mandatory": True
                },
                {
                    "key": "GOOGLE_PRIVATE_KEY",
                    "default":  "-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC0NIUNEPpISOEk\\nEp2RqCXrQkWu5P5d1qKKuTvA68gxaGKi0GuUwnqRN+W6fy2jV0W5kYNjC/XhKOtZ\\nBk42vJgrB9rbw0ZugsTU6En4BtnraZFSh1W40dZ782GjW9UhHtOGt5Lynmm7J5Zr\\nCku9E/lqyComGoKdWYu9YjCXrvCjACiXMoV93FtaTlo+0fq6jdd65bfmgzZYgo4O\\nK0CR1UZVFkWpKYWhhd5Zkk+1jQW7xYhuqCuNfqN5EcrHbVniTEQj+igtkDCPzj/W\\nTbKGjwoTjW6njdApr83Ht6wsmPA8AqcF03Exw6N3UjO6FEWvCFqF91TkJNX0yd0c\\nzQyzv6CrAgMBAAECggEAJiGM29BxXVVKipMD03vklizeSN08s8eEel0qty5NHKNN\\nZ805Tm9+dvcAfd+GXS9M2jDfv9gajavWbO6II03x1v0hAuqFn0G9e52xdTGh8A3V\\nCcUITwTb4TuFOAdpCEqZEMMMbZk2nzsHuZuinh45Yy56uLhYVgpKJuc9iAMk+SBm\\nvpjjz5HE9v8CMnUOQKQtbQWgRrP1VqGnfV4PGLvt17CkW7aiqcMKEX304ks4+YkG\\nf0ChPHGS7NK6RtGzCwGTyo32RuUYQ/dyyycJZ+pGTuxql+MSHbk+gC4nCTcWr85B\\ncpSVZJlk01fJLPl5Q+3lP7GTE7vmWJi8eoEfUHQvAQKBgQDpl++ouGD25UyIzQhi\\nyCcPYmxeUaw/TrhG8H4S59dZTVadSehJT+fCmnpXOx6OvPHOUEa/c0DuzF7fZ/cS\\nqqux9yeYehbGJHOve7ExW4T8M0QO9KmsIvKi+R0b7K4kdmIlVHyr6Q32hFSEXOxf\\nA1v0dcwN6fRJPwlT18LV+oPFAQKBgQDFfZe3qq0M4pa1CNXUNRKXct1Te79mRRgr\\nWd2lmvI4d3P4E+GJ/jNPB2lysN6NNTFpwVsqFi7pgp/wtQRvbfaZr6Dg0Z9eDLsb\\nbHmV6MgN1eYCn/wTGhaKC7kxzv4Prj0aDLet3RR/vDeAs0oakuo/P5s8GTHB4EYw\\nNk5+Nc4JqwKBgQCzzueE+UBybHjoSOMunqEqf3mpdLbhGGhS+uYhCWND83s7odtz\\nK1Xb/2sy4GgaOajsRfDfiAkwiBJzZ6TRMpztZbGN9lS3evGt38m6k5cfRxsZZA2D\\nWndpKdbVWu+FU7ciwxEgh0nfO2ePZ7PvQzeySkajYzZOd35nkosAiVCLAQKBgC/O\\nDwOulOUhlEmOMfSERFPUwi6LLfGbmBYmUrjboPZ6M+BBL78vgUwIB0Zz+etEjQmE\\nfITbic+MhxrFNqWigKcDFHZXR7SEcGZbA7N9/a8br+nCwEn/bqVL4TBlYqp5CuFb\\nYrr7YRLqhKTqwW1dUsaspu8NSjYcC+Fvw+BZNd6xAoGBAL4l5Ul1a96zeiIkPYNY\\nbpvm9m/miU9F78KYHnQdABKigPpB5uFvsQ34Ova7rrf8/+Sc+QAiPc7ilMQaLuLx\\nlonEH0fPrMMUYMFs4KzWxwswdzLCzwQKbsFAbPuclm0ncY3rrpkST/oGe0yyIvBo\\nQeM8gAuTwvHAO0O0n8RennqY\\n-----END PRIVATE KEY-----\\n",
                    "mandatory": True
                },
                {
                    "key": "GOOGLE_CLIENT_EMAIL",
                    "default": "tfm-818@deep-sun-346308.iam.gserviceaccount.com",
                    "mandatory": True
                },
                {
                    "key": "GOOGLE_CLIENT_ID",
                    "default": "111919952112944000615",
                    "mandatory": True
                },
            ],
            "system": [
                {
                    "key": "MONGODB_URL",
                    "value": "mongodb://##MONGODB_USERNAME##:##MONGODB_PASSWORD##@##MONGODB_HOST##:##MONGODB_PORT##/##MONGODB_DATABASE##?retryWrites=true&w=majority"
                },
                {
                    "key": "PORT",
                    "value": "80"
                },
                {
                    "key": "PROTOCOL",
                    "value": "##PROTOCOL##"
                },
                {
                    "key": "SERVER_NAME",
                    "value": "##DOMAIN##"
                },
                {
                    "key": "MONGODB_DATABASE",
                    "value": "data"
                },
                {
                    "key": "MODE",
                    "value": "development"
                },
                {
                    "key": "BASE_PATH",
                    "value": "/googledrive"
                },
                {
                    "key": "COLLECTION_NAME",
                    "value": "googledrive_assets"
                },
                {
                    "key": "BACKEND_CORS_ORIGINS",
                    "value": "[\"##COMPLETE_PATH##\"]"
                },
            ],
        },
        "outputs": [],
        "image": "interlinkproject/interlinker-googledrive:master",
        "labels": {
        },
    },
    "surveyeditor": {
        "info": {
            "icon": "https://surveyjs.io/Content/Images/logo_1200x630.jpg",
            "name": "Survey editor",
            "description": "Survey designer and publishing INTERLINKER which allows to create on demand new forms to gather information or help in decision making in co-production processess. It is based on open source tool SurveyJs (https://github.com/surveyjs)",
            "snapshots": [
                "https://miro.medium.com/max/521/1*J_auLSp-flPAU44iGA8ejA.png"
            ],
            "preconditions": [],
            "urls": {
                "instantiate": "##COMPLETE_PATH##/surveyeditor/assets/instantiate",
                "list": "##COMPLETE_PATH##/surveyeditor/api/v1/assets",
                "get": "##COMPLETE_PATH##/surveyeditor/assets/{id}",
                "clone": "##COMPLETE_PATH##/surveyeditor/assets/{id}/clone",
                "download": "##COMPLETE_PATH##/surveyeditor/assets/{id}/download",
                "view": "##COMPLETE_PATH##/surveyeditor/assets/{id}/view",
            },
            "action_text": "Create a new survey"
        },
        "dependencies": ["mongodb"],
        "configuration": {
            "routing": {
                "traefik": {
                    "inner_port": 80,
                    "prefix": "/surveyeditor",
                    "strip": True
                }
            },
            "environment": [
            ],
            "system": [
                {
                    "key": "MONGODB_URL",
                    "value": "mongodb://##MONGODB_USERNAME##:##MONGODB_PASSWORD##@##MONGODB_HOST##:##MONGODB_PORT##/##MONGODB_DATABASE##?retryWrites=true&w=majority"
                },
                {
                    "key": "PORT",
                    "value": "80"
                },
                {
                    "key": "PROTOCOL",
                    "value": "##PROTOCOL##"
                },
                {
                    "key": "SERVER_NAME",
                    "value": "##DOMAIN##"
                },
                {
                    "key": "MONGODB_DATABASE",
                    "value": "data"
                },
                {
                    "key": "MODE",
                    "value": "development"
                },
                {
                    "key": "BASE_PATH",
                    "value": "/surveyeditor"
                },
                {
                    "key": "COLLECTION_NAME",
                    "value": "surveyeditor_assets"
                },
                {
                    "key": "BACKEND_CORS_ORIGINS",
                    "value": "[\"##COMPLETE_PATH##\"]"
                },
            ],
        },
        "outputs": [],
        "network": "##PUBLIC_NETWORK##",
        "image": "interlinkproject/interlinker-surveyeditor:master",
        "labels": {
        },
    },
}
ALL = {**DEPENDENCIES, **APPLICATIONS}
for k, v in ALL.items():
    outputs = v.get("outputs", [])
    for output in outputs:
        VARIABLES_FOR_SUBSTITUTION[output["key"]] = output["value"]

def substitute(obj):
    obj_type = type(obj)
    if obj_type == str:
        new_str = obj
        for varkey, varvalue in VARIABLES_FOR_SUBSTITUTION.items():
            new_str = new_str.replace(f"##{varkey}##", varvalue)
        return new_str
    elif obj_type == dict:
        new_obj = {}
        for key, value in obj.items():
            new_obj[key] = substitute(value)
        return new_obj
    elif obj_type == list:
        new_list = []
        for value in obj:
            new_list.append(substitute(value))
        return new_list
    else:
        return obj

PLUGINS_LIST = substitute(ALL)