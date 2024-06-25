# llm-serving

Model은 해당 checkpoint: beomi/Llama-3-KoEn-8B-Instruct-preview



### Install package
    poetry shell
    poetry install

### Run app
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

### Testing with CLI
    curl -X POST "hsttp://127.0.0.1:8000/post/recommend" -H "Content-Type: application/json" -d '{"question": "밥은 잘 먹고 다니냐"}'
