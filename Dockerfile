FROM python:3.9-slim
WORKDIR /xm_test
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /xm_test
EXPOSE 8000
ENTRYPOINT ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]
#ENTRYPOINT ["python", "ws_client/ws_client.py"]
#ENTRYPOINT ["python", "tests/run_tests.py"]