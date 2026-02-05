from pydantic import BaseModel

class EmailRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    spam: bool

def test_request_schema():
    req = EmailRequest(text="Hello there")
    assert isinstance(req.text, str)

def test_response_schema():
    res = PredictionResponse(spam=True)
    assert isinstance(res.spam, bool)
