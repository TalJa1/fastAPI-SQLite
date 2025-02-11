def test_get_customer(client):
    response = client.get("/customers/1/")
    assert response.status_code == 200
    assert response.json() == {
        "customer_id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "",
        "phone": "",
    }
