import os
from dotenv import load_dotenv
from groq import Groq

# 1. تحميل المتغيرات البيئية
load_dotenv()

class AtlasAgent:
    def __init__(self):
        # 2. إعداد الاتصال بـ Groq
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-70b-versatile"
        
        # 3. الذاكرة الأساسية (System Prompt)
        self.history = [
            {"role": "system", "content": "انت خبير ذكاء اصطناعي مغربي سميتك أطلس. جاوب بالدارجة المغربية بذكاء."}
        ]

    def chat(self, user_input):
        # 4. إضافة سؤال المستخدم للتاريخ
        self.history.append({"role": "user", "content": user_input})

        try:
            # 5. طلب الجواب مع تفعيل خاصية الـ Streaming
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                stream=True
            )
            
            print("Atlas: ", end="", flush=True)
            full_response = ""
            
            # 6. حلقة استقبال الكلمات (Chunks)
            for chunk in response:
                # التأكد أن "الطرف" المحصل عليه فيه نص
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True) # طبع الكلمة فوراً
                    full_response += content # تجميع الجواب الكامل
            
            print("\n") # سطر جديد في الأخير
            
            # 7. حفظ الجواب الكامل في الذاكرة
            self.history.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            print(f"\nError: {str(e)}")

# 8. حلقة التشغيل الرئيسية
if __name__ == "__main__":
    bot = AtlasAgent()
    print("--- Atlas AI (Streaming Mode) ---")
    while True:
        text = input("You: ")
        if text.lower() in ["exit", "quit"]:
            break
        bot.chat(text)