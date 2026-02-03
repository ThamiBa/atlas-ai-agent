import os
import sys
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

class AtlasAgent:
    def __init__(self):
        # تأكد أن المفتاح كاين باش البرنامج ما يتبلوكاش من بعد
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY non trouvée dans le fichier .env")
            
        self.client = Groq(api_key=api_key)
        # خذ الموديل من .env وإذا مالقيتيهش استعمل هاد الافتراضي
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-specdec")
        
        self.history = [
            {"role": "system", "content": "انت خبير ذكاء اصطناعي مغربي سميتك أطلس. جاوب بالدارجة المغربية بذكاء."}
        ]

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                stream=True
            )
            
            print("Atlas: ", end="", flush=True)
            full_response = ""
            
            for chunk in response:
                # طريقة آمنة للحصول على النص
                content = chunk.choices[0].delta.content or ""
                if content:
                    print(content, end="", flush=True)
                    full_response += content
            
            print("\n")
            self.history.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            print(f"\n⚠️ Error calling Groq API: {str(e)}")

if __name__ == "__main__":
    try:
        bot = AtlasAgent()
        print(f"--- Atlas AI Online ({bot.model}) ---")
        while True:
            text = input("You: ")
            if text.lower() in ["exit", "quit"]:
                print("Bye! 👋")
                break
            bot.chat(text)
    except KeyboardInterrupt: # التعامل مع Ctrl+C بجمالية
        print("\nStopped by user. Bye!")
        sys.exit()