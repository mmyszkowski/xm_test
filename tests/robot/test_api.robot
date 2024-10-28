*** Settings ***
Documentation  Testsuite for API
Resource    resources/keywords.robot


*** Test Cases ***
Create Order
    [Documentation]    Test creating a new order
    ${response}=    POST    ${BASE_URL}
    Should Be Equal As Numbers    ${response.status_code}    200
    Log    ${response.json()}
    ${order_id}=    Get From Dictionary    ${response.json()}    orderId
    ${status}=    Get From Dictionary    ${response.json()}    status
    Should Be Equal    ${status}    EXECUTED

Get Single Order
    [Documentation]    Test retrieving a single order
    ${response}=    POST    ${BASE_URL}
    ${order_id}=    Get From Dictionary    ${response.json()}    orderId
    ${single_response}=    GET    ${BASE_URL}/${order_id}
    Should Be Equal As Numbers    ${single_response.status_code}    200
    Should Contain    ${single_response.json()}    id
    Should Contain    ${single_response.json()}    status

Get All Orders
    [Documentation]    Test retrieving all orders
    ${order_ids}=    Create Multiple Orders And Return IDs    3
    ${response}=    GET    ${BASE_URL}
    Should Be Equal As Numbers    ${response.status_code}    200
    Log    ${response.json()}
    ${response_ids}=    Get Order IDs From Response    ${response.json()}
    Should Contain Values    ${response_ids}    ${order_ids}

Cancel Order
    [Documentation]    Test cancelling an order
    ${response}=    POST    ${BASE_URL}
    ${order_id}=    Get From Dictionary    ${response.json()}    orderId
    ${cancel_response}=    DELETE    ${BASE_URL}/${order_id}
    Should Be Equal As Numbers    ${cancel_response.status_code}    204
