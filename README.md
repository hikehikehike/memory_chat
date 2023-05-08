# AI Assiatant with memory

## Installation

Python3 must be already installed


```shell
git clone https://github.com/hikehikehike/memory_chat
cd memory_chat
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
#### Rename file ".env.sample" to ".env"
#### In file ".env" add your [OPENAI_API_KEY](https://platform.openai.com/account/api-keys)
```shell
uvicorn main:app --reload
```
Go to the link http://127.0.0.1:8000/
