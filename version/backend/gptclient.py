import ssl
import certifi
from functools import partial
from g4f.client import Client  # Убедитесь, что пакет g4f установлен корректно
import g4f
# Настройка конфигурации SSL
ssl.default_ca_certs = certifi.where()
ssl.create_default_context = partial(
    ssl.create_default_context,
    cafile=certifi.where()
)

class GPTClient:
    def __init__(self):
        # Инициализация клиента GPT-3.5
        self.client = Client()
        self.history = []
    
    def add_message(self, role, content):
        """Добавить сообщение в историю разговора."""
        self.history.append({"role": role, "content": content})
    
    def get_response(self, user_message):
        self.add_message("user", user_message)
        
        assistant_response = ""  # Инициализация ответа ассистента
        
        try:
            # Создание потокового ответа
            stream = self.client.chat.completions.create(
                model="deepseek-chat",  # Измените на нужную модель
                messages=self.history,
                web_search=False,
                stream=True,
                provider=g4f.Provider.Blackbox
            )
            
            # Обработка потокового ответа
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    # Печать части контента по мере поступления
                    print(chunk.choices[0].delta.content, end="", flush=True)
                    # Накопление ответа ассистента
                    assistant_response += chunk.choices[0].delta.content
            
            # Сохранение полного ответа ассистента в историю
            self.add_message("assistant", assistant_response)
            return assistant_response
        
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return str(e)

# Пример использования
if __name__ == "__main__":
    gpt_client = GPTClient()
    
    while True:
        user_input = input("\nВы: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = gpt_client.get_response(user_input)
        print("\nАссистент:", response)