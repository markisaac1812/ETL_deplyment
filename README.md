## Things learnt
Remove ports from docker-compose in etl service cause it is not a server

pip freeze > requirements.txt -> to get all dep and copy it in req.txt file

DATABASE_URL_EXAMPLE="postgres://username:password@service_name:5432/database_name"

when docker compose up -d -> it craetes the container + volumes + network + IMAGE BUILT BY DOCKERIFLE AND GIVE IT A RANDOM NAME (project name + servic name)