##  Overview

<p align="center">
    <img src="diagram.png">
</p>


## Components & Miscs

### LLM
- [2 bit GGUF-based quantized model](https://huggingface.co/TheBloke/phi-2-GGUF) __(phi-2)__ from this incredible user [(@TheBlock)](https://huggingface.co/TheBloke) on the HuggingFace model hub.


### Serving
-  Prebuilt server from __llama.cpp__.


### Chatbot service
- __FastAPI__ for creating RESTful API endpoint.


### Tools
- __Postman__ for interactive API testing environment.
- __tmux__ for conventional terminal screen splitting.
- __git-lfs__ for pushing the above quantized Phi-2 model to Github server.

## How to run?
1. Firstly, activate your virtual environment. In my case is:
```
source superbench-venv/bin/activate
```
and do not forget installing the required packages from the `requirements.txt` as below:
```
pip install -r requirements.txt
```

2. You need to download the model from HuggingFace hub using `huggingface-cli` tool:
```
huggingface-cli download TheBloke/phi-2-GGUF phi-2.Q2_K.gguf --local-dir llm/models --local-dir-use-symlinks False
```

3. Then, start the _FastAPI-based_ chatbot service with this command:
```
uvicorn server/server:chatbot_app
```

4. Finally, kick off the prebuilt _llama.cpp_ server
```
./llm/ext_lib/llama.cpp/server -ngl 32 -c 256 -m llm/models/phi-2.Q2_K.gguf
```

__Voila!__, now just testing the API with your favorite tool.


## Quick Demo
<video src="https://github.com/hosjiu1702/superbench-assessment-demo/raw/master/demo/demo.mp4"></video>
