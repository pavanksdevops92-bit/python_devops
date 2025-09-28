from fastapi import FastAPI, HTTPException
import uvicorn
app = FastAPI(title="Calculator API")

@app.get("/")
def welcome():
    return {"Welcome to the calculator App"}

@app.get("/add")
def add(a: float, b: float):
    return {"result": a + b}


@app.get("/substract")
def subtract(a: float, b: float):
    return {"result": a - b}


@app.get("/multiply")
def multiply(a: float, b: float):
    return {"result": a * b}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)