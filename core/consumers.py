import os
import base64
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class MyJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    AUDIO_DIR = 'audio_files'

    # This handler is called when client initially opens a connection and is about to finish the Websocket handshake.
    async def connect(self, content=None, **kwargs):
        print("Websocket Connected...", content, kwargs)
        print("Scope...", self.scope)
        await self.accept()  

    # This handler is called when data received from client with decoded JSON content.
    async def receive_json(self, content, **kwargs):
        print("Message Received from Client...", content, kwargs)

        # Example of expected content structure need to send back to the client:
        # data= {
        #     "event" : "media",
        #     "stream_sid" : "<stream sid>",
        #     "media" : {
        #         "payload" : "<>"
        #     }
        # }

        if "media" in content:
            print("Media content received, processing...")

            self.save_audio_chunk_to_file(content["media"]["payload"], content.get("stream_sid", ""))

            data = {
                "event": "media",
                "stream_sid": content.get("stream_sid", ""),
                "media": {
                    "payload": '6P8IAAgACAAIAAgA6P=',
                },
            }

            print("Data to send...", data)

            await self.send_json(data)

    # Helper function to save the base64-encoded audio chunk into a file
    def save_audio_chunk_to_file(self, base64_audio_data, stream_sid):
        try:
            print("Saving audio chunk to file...", base64_audio_data)

            # Decode the base64 string into bytes
            audio_data = base64.b64decode(base64_audio_data)

            # Create the audio directory if it does not exist
            if not os.path.exists(self.AUDIO_DIR):
                os.makedirs(self.AUDIO_DIR)

            # Define the file name based on stream_sid (or any other unique identifier)
            file_name = f"{stream_sid}_audio.wav"
            file_path = os.path.join(self.AUDIO_DIR, file_name)

            # Write the decoded audio data to the file
            with open(file_path, "ab") as audio_file:
                audio_file.write(audio_data)

            print(f"Audio saved to {file_path}")
            return file_path

        except Exception as e:
            print(f"Error saving audio to file: {e}")
            return None

    # This handler is called when either connection to the client is lost, either from the client closing the connection, or loss of the socket.
    async def disconnect(self, close_code):
        print("Websocket Disconnected...", close_code)
