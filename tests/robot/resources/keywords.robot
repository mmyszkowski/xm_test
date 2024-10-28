*** Settings ***
Library           RequestsLibrary
Library           Collections


*** Variables ***
${BASE_URL}      http://127.0.0.1:8000/orders


*** Keywords ***
Create New Order And Return ID
    ${response}=    POST    ${BASE_URL}
    Should Be Equal As Numbers    ${response.status_code}    200
    ${order_id}=    Get From Dictionary    ${response.json()}    orderId
    Log    ${order_id}
    RETURN    ${order_id}

Get Order IDs From Response
    [Arguments]    ${response}
    ${ids}=    Create List
    FOR    ${order}    IN    @{response}
        Append To List    ${ids}    ${order['id']}
    END
    RETURN    ${ids}

Create Multiple Orders And Return IDs
    [Arguments]    ${count}
    ${ids}=    Create List
    FOR    ${index}    IN RANGE    ${count}
        ${order_id}=    Create New Order And Return ID
        Append To List    ${ids}    ${order_id}
    END
    RETURN    ${ids}

Should Contain Values
    [Arguments]    ${actual}    ${expected}
    FOR    ${value}    IN    @{expected}
        Should Contain    ${actual}    ${value}
    END