from run import app 

# Tests if server runs 
def test_home_route():
    client = app.test_client() # Simulates browser request
    response = client.get("/") # Checks access

    assert response.status_code == 200 # Shows if successful 

# Tests Rendering 
def test_homepage():
    client = app.test_client()
    response = client.get("/")

    assert b"Budget App" in response.data