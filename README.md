# Betting
To run the solution:

Docker-compose.yaml

version: "3"
services:
    coupon-database:
        image: postgres
        restart: always
        container_name: coupon-database
        environment:
            POSTGRES_USER: change me
            POSTGRES_PASSWORD: change me
            POSTGRES_DB: 50-lappen
        expose:
            - 5432
        ports: 
            - 5432:5432
        volumes:
            - change me:/var/lib/postgresql/data

    adminer:
        image: adminer
        restart: always
        depends_on:
            - coupon-database
        ports:
            - 8080:8080

    coupon-manager:
        image: diffen/50-lappen-coupon
        #restart: on-failure[:3]
        #restart: always
        depends_on: 
            - coupon-database
        environment:
            - COUPON_DB_USER=change me
            - COUPON_DB_PASSWORD=change me
            - COUPON_DB_NAME=50-lappen
            - COUPON_HOST=coupon-database
            - COUPON_DB_PORT=5432

    coupon-manager-api:
        image: diffen/50-lappen-coupon-api
        #restart: on-failure[:3]
        #restart: always
        container_name: coupon-manager-api
        depends_on: 
            - coupon-manager
        environment:
            - COUPON_DB_USER=change me
            - COUPON_DB_PASSWORD=change me
            - COUPON_DB_NAME=50-lappen
            - COUPON_HOST=coupon-database
            - COUPON_DB_PORT=5432
        ports:
            - 8081:8081

    50-lappen:
        image: diffen/50-lappen
        #restart: on-failure[:3]
        #restart: always
        container_name: 50-lappen
        depends_on: 
            - coupon-database
        ports:
            - 8082:5000