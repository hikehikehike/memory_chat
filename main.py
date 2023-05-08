from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from pathlib import Path

from chatbot import conversation, save_history

app = FastAPI()

conversation_with_summary, vectordb = conversation()

history = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Handle the WebSocket connection by accepting the connection,
    receiving messages from the client, sending responses to the client,
    and storing the conversation history in a global list.
    """
    global history
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        response = conversation_with_summary.predict(input=message)
        history.append(message)

        await websocket.send_text(response)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Delete the Chroma collection and save the conversation history to a file
    when the server is shut down.
    """
    vectordb.delete_collection()
    await save_history(history)


@app.get("/")
async def get():
    """
    Serve the index.html file as a response to GET requests to the root path.
    """
    file_path = Path("templates/index.html")
    return FileResponse(file_path)
