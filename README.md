# Zeon Bazar

### zeon bazar is Ecommerce project with features
- advertisement with CRUD
- category and sub category with CRUD
- custom Base Command
- custom middleware for limiting request
- custom user auth with email
- user activation, forgot password, change password
- support docker, nginx

### Installation
- clone git repo 
```
git clone https://github.com/Shairbekov-Bakyt/Zmall
``` 
- run with docker
```
sudo docker-compose up -d  --build
```
- run without docker
```
cd server && make migrate && make run_prod
```
- run webserver
```
cd webserver/webserver && npm install && npm start
```

### Makefile
- run_dev 
  - run server with local settings
- run_prod 
  - run server with prod settings

- migrate
    - make migrations and migrate
- web 
  - run web scraping and base filling

- create
    - create virtualenv
- install
	- install requirements


### Example .env
### [Pusher](https://pusher.com/)

```
SECRET_KEY="" django secret key
EMAIL_HOST_USER="" email for smtp
EMAIL_HOST_PASSWORD="" email app password for smtp
PUSHER_APP_ID="" pusher app id
PUSHER_KEY="" pusher app key
PUSHER_SECRET="" pusher app secret key


POSTGRES_DB="zeon"
POSTGRES_USER="zeon_user"
POSTGRES_PASSWORD="zeon_password"
DB_NAME="zeon"
DB_USER="zeon_user"
DB_PASSWORD="zeon_password"
DB_HOST="db"
```

### Special thanks
- #### [Zharkyn](https://github.com/Zharkyn20)
- #### [Sardor](https://github.com/IsrailovSardor)
- #### [Talgat](https://github.com/slice312)