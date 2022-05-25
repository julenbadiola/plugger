
## CATALOGUE
labels = {
    "traefik.enable": "true",
    "com.docker.compose.project": "tfm",
}
env = [
    "PROTOCOL=http://",
    "SERVER_NAME=localhost",
    "PORT=80",
    "MONGODB_DATABASE=data",
    "MONGODB_URL=mongodb://user:userpass@mongodb:27017/data?retryWrites=true&w=majority",
    "MODE=development",
]

PLUGINS_LIST = [
    {
        "card": {
            "icon": "https://upload.wikimedia.org/wikipedia/commons/d/da/Google_Drive_logo.png",
            "name_to_show": "Google drive resource editor",
            "description": "Google Drive is a file storage and synchronization service developed by Google. Launched on April 24, 2012, Google Drive allows users to store files in the cloud, synchronize files across devices, and share files. Google Drive encompasses Google Docs, Google Sheets, and Google Slides, which are a part of the Google Docs Editors office suite that permits collaborative editing of documents, spreadsheets, presentations, drawings, forms, and more. Files created and edited through the Google Docs suite are saved in Google Drive. This software INTERLIKER allows users of the collaborative environment to create new documents, spreadsheets and presentations which can be co-edited and shared by co-production team participants",
            "snapshots_links": ["https://www.filo.news/export/sites/claro/img/2022/02/21/aisummary.gif_344325628.gif"],
            "preconditions": []
        },
        "info": {
            "name": "Google Drive",
            "url": "/googledrive/assets",
            "text": "Create a new Google Drive resource"
        },
        "configuration": {
            "environment": [
                {
                    "key": "GOOGLE_PROJECT_ID",
                    "default": "interlink-deusto",
                    "mandatory": True
                },
                {
                    "key": "GOOGLE_PRIVATE_KEY_ID",
                    "default": "85c9fdaa12b700e47e172de5095188742ff79139",
                    "mandatory": True
                },
                {
                    "key": "GOOGLE_PRIVATE_KEY",
                    "default": "-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDNhvhUuk8M73h+\\nX73Q5E/k4vDzizI+Yz5BnUyCfrdsbHmITah3dH4IIy5jIHHhFLIWThUCH9g2Z547\\nctA/VvygihdM9eRe5v+JH+D3kB7rz3s5kvl5aR0Hfl5HvS22pUtnED6sC/kE2Y+q\\nW+oSSZHu+ahk/6If6+XQYbLroUyVMtSUy+x8zSNtw2yc6DTkcnMpiA1M04ZG7qFf\\nfaLOH+jV8fi21DnNohxnL9MGC0chINKlTbzDtIF8m8vkk4BVeLKCGyXNQtLAPt0p\\nAcI7SFloXdqtIERY5B3+0XdZalhuvlo8HPqMC1QZtOmmiEh1668/Hpk2Qmi8dyck\\nNEXNs2YtAgMBAAECggEAEpgrtvStKrkusFZGpNPHI6jhjlMxXkIZ05Ng5OyEeUd+\\nHlYSUA5myaMvMvIwQ2IdM5XoYisR42gwAWZjj1t2GysrLQARI4HoLBaJgrRUC9cX\\naa/RqMmZAgDNlFV6AYyGXCJ03RlvM+BgFlRfAr0LujB1qv+SwisUPWxdZOKQvG21\\ndoUJT4QITQYzw8we/p7a8TM8sRc5hAsgiPF6BB1l457uLAkyk8rEp6KlOKvHK8xF\\nqvtmHGnMTUJ/aoroff9y/wXThiq6dm2q7cU+T6x6d+3AouZaVolesBnr3QZpsaGv\\npDSINUnm1GqUmPvmdTyaepeqRdHp4Rp3GK5azfvuyQKBgQD5M1P0cF2zzx3lMxI1\\nyku7hhhFs/tsvsKVi3+j+eBiQHiKEzKpNpJcpRwrWZSNmDM/eP5ySbpjsxIBrFUx\\nWCqE6x8HF8d7X3h2hjJYZeYD6EoInyn0r7dxHIX09OI6kLJw48g6pbUBP8DOFpgI\\nryhYzp+mnVuVaKI3kgmfx9KU6QKBgQDTIpVIJe/3qgX122osiMNmSDWSlandWtpX\\n7CB+oB36W+K5q1q65FpTo6sGT+fc50I+e83jm4SKF1mDBWaUSmi4fMusuaMqVsNt\\njryg4ByRCzDoS1ZFFmk6/5A8ZXKz7EGs1sDHdpfyGjEzZz7SHWSA57g3IPDE11za\\n+ETFPvqMpQKBgQCU0eRXXCt5UD1IPWGoofDsQj6Ikd2aqalG6ZIGeRlZU6souiJN\\nD3wEu83AzbR7guNICpfZ5NHc7HnaafJOj5qE2m0jLT5CHVexYJ78T4430yczUuoZ\\naD6i3Cfbi8r2sqb95+oRrBgWcN5RtQiCVyg/MNYDCIJDDcOicCIzO4A00QKBgQCh\\nb2nxVoCbP7d6+x+9mXy+civ0Ptc410TnwTY/W7JQQX2kNa8UA5JFLXmRQ/unXnO6\\nTvNoOvsmkx/wHGsIq7RSi6k4EmD9+IVI+cCkyXdON95XX3NBNBeV8t6YL4F6rQSy\\nYSnZ2YXoqbpA8YqJIcw8+/BQxrER8RGgpAABSVxNuQKBgAuKb5DGBcvBjZDjbj4p\\nGu/RxR6jx7yeQjit8p73hk2NgJMG7D17LArTNRyoegexQB4txb6G9ATaAa9pfWWP\\nQNpW3qlqTDtxS21n4VCE7jl/bdRFmWNGvkV5ZmlgQdDJ0Zm0QNEoNIv+iJbSwlOJ\\nNiYyoevLNlTe4I/K1Rpl94XN\\n-----END PRIVATE KEY-----\\n",
                    "mandatory": True
                },
                {
                    "key": "GOOGLE_CLIENT_EMAIL",
                    "default": "tfm-238@interlink-deusto.iam.gserviceaccount.com",
                    "mandatory": True
                },
                {
                    "key": "GOOGLE_CLIENT_ID",
                    "default": "115455968021672182104",
                    "mandatory": True
                },
            ]
        },
        "name": "googledrive",
        "image": "interlinkproject/interlinker-googledrive:master",
        "labels": {
            **labels,
            "traefik.http.routers.tfm-googledrive.rule": "Host(`localhost`) && PathPrefix(`/googledrive`)",
            "traefik.http.services.tfm-googledrive.loadbalancer.server.port": "80",
            "traefik.http.middlewares.googledrive-stripprefix.stripprefix.prefixes": "/googledrive",
            "traefik.http.routers.tfm-googledrive.middlewares": "googledrive-stripprefix",
        },
        "env": env + ["BASE_PATH=/googledrive", "COLLECTION_NAME=googledrive_assets", "BACKEND_CORS_ORIGINS=[\"http://localhost\"]"],
    },
    {
        "card": {
            "icon": "https://surveyjs.io/Content/Images/logo_1200x630.jpg",
            "name_to_show": "Survey editor",
            "description": "Survey designer and publishing INTERLINKER which allows to create on demand new forms to gather information or help in decision making in co-production processess. It is based on open source tool SurveyJs (https://github.com/surveyjs)",
            "snapshots_links": [
                "https://miro.medium.com/max/521/1*J_auLSp-flPAU44iGA8ejA.png"
            ],
            "preconditions": []
        },
        "configuration": {
            "environment": [

            ]
        },
        "name": "surveyeditor",
        "image": "interlinkproject/interlinker-surveyeditor:master",
        "labels": {
            **labels,
            "name": "Survey editor",
            "url": "/surveyeditor/assets",
            "traefik.http.middlewares.surveyeditor-stripprefix.stripprefix.prefixes": "/surveyeditor",
            "traefik.http.routers.tfm-surveyeditor.middlewares": "surveyeditor-stripprefix",
            "traefik.http.routers.tfm-surveyeditor.rule": "Host(`localhost`) && PathPrefix(`/surveyeditor`)",
            "traefik.http.services.tfm-surveyeditor.loadbalancer.server.port": "80"
        },
        "env": env + ["BASE_PATH=/surveyeditor", "COLLECTION_NAME=surveyeditor_assets"],
    },
]
