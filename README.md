# Test Task for XM - API with WebSocket
Sample REST API server that exposes a set of endpoints to simulate a trading platform.  
The platform uses WebSocket connections for receiving real-time order status messages. 
Each endpoint has random short delay between 0.1 and 1 second.
After client sends POST/orders request, server sends confirmation and orderId.
After orders are received from the client, the server sends back orderId and orderStatus as a response. 
Order has three statuses: PENDING, EXECUTED, CANCELLED. 
Order is created with PENDING status then after short delay status is changed to EXECUTED.
Order can be cancelled only when the order status is PENDING.
Server is asynchronous.Database is kept in memory.
Project contains automated tests in Pytest and Robot Framework. 
## Setup
- Clone repository https://github.com/mmyszkowski/xm_test.git
- Create virtual environment

`python -m venv myenv`
- Activate virtual environment

on Linux:

`source myenv/bin/activate`

on Windows:

`myenv\Scripts\activate`
- Install packages from requirements.txt

`pip install -r requirements.txt`

## Start client and server
- Start server with command

`uvicorn api.api:app --reload `

- Start client with command

`python ws_client/ws_client.py`

## Tests
- Start unit tests 

`pytest -v`

- Start robot tests 

on Linux

`python tests/robot/run_tests.py`

on Windows

`python.exe .\tests\robot\run_tests.py`

results are saved in /static directory and published on http://localhost:8000/test_results

## Docker
Project contains Dockerfile, that allows to start server, client and tests on separate docker containers.
Before creating docker image you need to:
- uncomment expected last line in accordance with expectations.
- change BASE_URL in /robot/resources/keywords to API docker name e.g. http://api_container:8000/orders
- change URI from 127.0.0.1 to API docker name in /ws_client/ws_client.py
- build server:

`docker build -t xm_test_server .`

- build client:

`docker build -t xm_test_client .`

- build tests:

`docker build -t xm_test_tests .`

- create docker network:

`docker network create xm_test_network`

- run containers:

`docker run --network xm_test_network --name api_container -p 8000:8000 xm_test_server`

`docker run --network xm_test_network --name tests_container xm_test_tests`

`docker run --network xm_test_network --name client_container xm_test_client`

## Technologies and tools
- Python 3.12
- PyTest
- Robot Framework
- FastAPI - https://fastapi.tiangolo.com 