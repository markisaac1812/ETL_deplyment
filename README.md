## Things learnt
Remove ports from docker-compose in etl service cause it is not a server

pip freeze > requirements.txt -> to get all dep and copy it in req.txt file

DATABASE_URL_EXAMPLE="postgres://username:password@service_name:5432/database_name"

when docker compose up -d -> it craetes the container + volumes + network + IMAGE BUILT BY DOCKERIFLE AND GIVE IT A RANDOM NAME (project name + servic name)

build: . is equal to build:
                        context: .
                        dockerfile: Dockerfile

----------------------------------------------------------------------- 
 ### Deployment phase                       

 ##### ways of deployment
            1.       EC2
            (SSH into server,Clone repo ,install docker and docker compose, docker compose up -d) 



        2.         ECR---------------------
                    /\                    |
                   /  \                   |
                  /    \                  |
                 /      \                 |
                ECR+EC2  ECR+ECS     ECR+ECS+fargate     
-------------------------------------------------------

#### 1 ECR+EC2 (ECR only store custom images (images you built yourself not Base IMages form docker hub)) (e.g if your docker compose have 9 serivces coming from 3 Base images and 1 custom images -> ECR will store only custom image which is 1 image only)
                    Docker Hub
                  ┌─────────────┐
                  │ postgres:16 │
                  └──────┬──────┘
                         │
                         ▼
                 postgres container

                  ┌──────────────┐
                  │ redis:7.2    │
                  └──────┬────────┘
                         │
                         ▼
                  redis container


                 Your Dockerfile
FROM apache/airflow:3.2.2
COPY requirements.txt .
RUN pip install -r requirements.txt

                         │
                         ▼
               Your custom Airflow image
                         │
        ┌────────────────┼─────────────────┐
        ▼                ▼                 ▼
 airlfow-apiserver  airflow-scheduler  airflow-worker
        ▼                ▼                 ▼
 airflow-triggerer  airflow-dag-processor  airflow-init                        


### So actually we have only 4 images 
3 base images -> redis , -> postgres metadata , -> postgres for user

1 custom image to build all airflow containers


-----------------------------------------
Airflow services

airflow-apiserver

airflow-scheduler

airflow-worker

airflow-triggerer

airflow-dag-processor

airflow-init

All of them inherit:

x-airflow-common:
  build: .

and your Dockerfile is:

FROM apache/airflow:3.2.2

COPY requirements.txt .

RUN pip install -r requirements.txt

Offical airflow image + my req.txt -> my custom image


