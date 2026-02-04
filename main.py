import os
import sys
# تأكد أنك أنسطاليتي python-dotenv و groq
from dotenv import load_dotenv
from groq import Groq

# تحميل السوارت من ملف .env
load_dotenv()

class AtlasAgent:
    def __init__(self):
        # 1. التأكد من وجود الـ API Key
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY missing in .env file!")
            
        self.client = Groq(api_key=api_key)
        
        # 2. جلب الموديل من .env (درت ليك llama-3.1-8b-instant كاحتياط حيت مستقر)
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        
        # 3. الذاكرة (System Prompt)
        self.history = [
            {"role": "system", "content": "انت خبير ذكاء اصطناعي مغربي سميتك أطلس. جاوب بالدارجة المغربية بذكاء واحترافية."}
        ]

    def chat(self, user_input):
        """هاد الدالة كتاخد السؤال وترجع الجواب"""
        # إضافة سؤال المستخدم للذاكرة
        self.history.append({"role": "user", "content": user_input})

        try:
            # طلب الجواب من Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                stream=True
            )
            
            # طباعة الجواب في الـ Terminal (للمراقبة)
            print("Atlas: ", end="", flush=True)
            full_response = ""
            
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                if content:
                    print(content, end="", flush=True)
                    full_response += content
            
            print("\n") # سطر جديد بعد نهاية الجواب
            
            # حفظ جواب البوت في الذاكرة
            self.history.append({"role": "assistant", "content": full_response})
            
            # ركز هنا: ضروري نرجعو النص باش Telegram يقدر يخدم بيه
            return full_response
            
        except Exception as e:
            error_msg = f"Error calling Groq API: {str(e)}"
            print(f"\n⚠️ {error_msg}")
            return error_msg

# حلقة التشغيل (كتخدم غير إلا شعلتي هاد الملف نيشان)
if __name__ == "__main__":
    try:
        bot = AtlasAgent()
        print(f"--- Atlas AI Online ({bot.model}) ---")
        print("Type 'exit' to quit.")
        
        while True:
            text = input("You: ")
            if text.lower() in ["exit", "quit"]:
                print("Bye! 👋")
                break
            # هنا ما غنحتاجوش نديرو print حيت الدالة chat ديجا كتدير print للـ chunks
            bot.chat(text)
            
    except KeyboardInterrupt:
        print("\nStopped by user. Bye!")
        sys.exit()