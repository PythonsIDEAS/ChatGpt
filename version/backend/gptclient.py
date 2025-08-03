from flask import jsonify
import requests

class GPTClient:
    def __init__(self):
        self.history = []
        self.base_url = "https://js.puter.com/v2/"
    
    def add_message(self, role, content):
        """Add a message to the conversation history."""
        self.history.append({"role": role, "content": content})
    
    def get_response(self, user_message):
        """Get response from Puter.js API."""
        self.add_message("user", user_message)
        assistant_response = ""
        
        try:
            # Create HTML file with Puter.js integration
            html_content = f"""
            <script src="{self.base_url}"></script>
            <script>
                puter.ai.chat("{user_message}", {{ model: "gpt-4.1-nano" }})
                    .then(response => {{                        
                        document.getElementById('response').textContent = response;
                    }});
            </script>
            <div id="response"></div>
            """
            
            # Send request to Puter.js
            response = requests.post(
                f"{self.base_url}chat",
                json={
                    "message": user_message,
                    "model": "gpt-4.1-nano"
                }
            )
            
            if response.status_code == 200:
                assistant_response = response.json().get('response', '')
                self.add_message("assistant", assistant_response)
            else:
                assistant_response = f"Error: {response.status_code}"
                
        except Exception as e:
            print(f"Error occurred: {e}")
            return str(e)
        
        return assistant_response

# Example usage
if __name__ == "__main__":
    gpt_client = GPTClient()
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = gpt_client.get_response(user_input)
        print("\nAssistant:", response)