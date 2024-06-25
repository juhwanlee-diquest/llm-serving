# llm-serving

여기서는 Serving만 진행하고자한다.

### Model: beomi/Llama-3-KoEn-8B-Instruct-preview



### run app
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload


### testing with CLI
    curl -X POST "http://127.0.0.1:8000/post/recommend" -H "Content-Type: application/json" -d '{"question": "밥은 잘 먹고 다니냐"}'
