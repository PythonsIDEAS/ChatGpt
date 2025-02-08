import ssl
import certifi
from functools import partial
from g4f.client import Client  # Ensure that the g4f package is installed correctly
import g4f
# Set SSL configuration
ssl.default_ca_certs = certifi.where()
ssl.create_default_context = partial(
    ssl.create_default_context,
    cafile=certifi.where()
)

class GPTClient:
    def __init__(self):
        # Initialize the GPT-3.5 client
        self.client = Client()
        self.history = []
    
    def add_message(self, role, content):
        """Add a message to the conversation history."""
        self.history.append({"role": role, "content": content})
    
    def get_response(self, user_message):
        self.add_message("user", user_message)
        
        assistant_response = ""  # Initialize the assistant response
        
        try:
            # Create a streaming response
            stream = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Change to the desired model
                messages=self.history,
                web_search=False,
                stream=True,
                #provider=g4f.Provider.OIVSCode
            )
            
            # Process the streamed response
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    # Print the chunk of content as it arrives
                    print(chunk.choices[0].delta.content, end="", flush=True)
                    # Accumulate the assistant's response
                    assistant_response += chunk.choices[0].delta.content
            
            # Save the complete assistant's response to history
            self.add_message("assistant", assistant_response)
            return assistant_response
        
        except Exception as e:
            return str(e)

# Example usage
if __name__ == "__main__":
    gpt_client = GPTClient()
    user_input = "Hello, how are you?"
    response = gpt_client.get_response(user_input)
    print("\nAssistant:", response)