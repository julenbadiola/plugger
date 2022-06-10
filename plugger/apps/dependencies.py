DEPENDENCIES = {
    "mongodb": {
        "show": False,
        "configuration": {
            "system": [
                {
                    "key": "MONGODB_USERNAME",
                    "value": "user"
                },
                {
                    "key": "MONGODB_PASSWORD",
                    "value": "userpass"
                },
                {
                    "key": "MONGODB_DATABASE",
                    "value": "data"
                },
                {
                    "key": "MONGODB_ROOT_USER",
                    "value": "root"
                },
                {
                    "key": "MONGODB_ROOT_PASSWORD",
                    "value": "rootpassword"
                },
            ],
        },
        "outputs": [
            {
                "key": "MONGODB_USERNAME",
                "value": "user"
            },
            {
                "key": "MONGODB_PASSWORD",
                "value": "userpass"
            },
            {
                "key": "MONGODB_DATABASE",
                "value": "data"
            },
            {
                "key": "MONGODB_ROOT_USER",
                "value": "root"
            },
            {
                "key": "MONGODB_ROOT_PASSWORD",
                "value": "rootpassword"
            },
            {
                "key": "MONGODB_HOST",
                "value": "mongodb"
            },
            {
                "key": "MONGODB_PORT",
                "value": "27017"
            },
            {
                "key": "MONGO_NETWORK",
                "value": "db-network"
            },
        ],
        "image": "bitnami/mongodb:latest",
        "network": "##PUBLIC_NETWORK##",
    },
    "core": {
        "show": False,
        "configuration": {
            "routing": {
                "traefik": {
                    "inner_port": 3000,
                    "prefix": "/",
                }
            },
            "system": [
                {
                    "key": "NODE_ENV",
                    "value": "development"
                },
                {
                    "key": "PORT",
                    "value": "3000"
                },
            ],
        },
        "outputs": [
        ],
        "image": "julenbadiola/core:master",
        "network": "##PUBLIC_NETWORK##",
    }
}
