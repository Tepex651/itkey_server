#### Requirements
python3.9.5 or later<br>
Docker version 20.10.8 or later<br>
docker-compose version 1.29.2 or later<br>

#### Create virtual environment for running
*If `virtualenv` is not installed, run `pip install virtualenv`*

Navigate to the main project directory and run: <br>
Unix: `python virtualenv env` <br>

#### Use the virtual environment
Unix: 
`source env/bin/activate`

#### Install requirements.txt for client from main project directory (itkey_server/requirements.txt)

`pip install -r requirements.txt`

#### Start services using docker-compose

`cd itkey_server/server`<br>
`sudo docker-compose up --build`

#### After that run client.py from main project directory (itkey_server)

`python client.py`

### If you want to change settings
1.  first change your docker-compose.yml file for services
2.  expose current changes in the config.yaml file for client
