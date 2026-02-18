import os
import requests
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class AtlasAgent:
    def __init__(self):
        # إعداد Groq للشات (Llama 3.3)
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.groq_model = "llama-3.3-70b-versatile"
        self.history = [{"role": "system", "content": "انت أطلس، مساعد مغربي ذكي كيهضر بالدارجة."}]

    def chat(self, user_input, image_url=None):
        # --- حالة Vision (Gemini v1beta Direct API) ---
        if image_url:
            try:
                img_res = requests.get(image_url, timeout=20)
                img_base64 = base64.b64encode(img_res.content).decode('utf-8')
                api_key = os.getenv("GEMINI_API_KEY")
                
                # ليستة ديال الموديلات المحتملة بالترتيب
                models_to_try = [
                    "gemini-1.5-flash",
                    "gemini-1.5-flash-8b",
                    "gemini-1.5-pro",
                    "gemini-2.0-flash-exp" # الموديل الجديد ديال 2026
                ]
                
                last_error = ""
                for model_name in models_to_try:
                    # تجربة v1beta أولاً ثم v1
                    for version in ["v1beta", "v1"]:
                        url = f"https://generativelanguage.googleapis.com/{version}/models/{model_name}:generateContent?key={api_key}"
                        payload = {
                            "contents": [{
                                "parts": [
                                    {"text": f"حلل الصورة بالدارجة المغربية: {user_input}"},
                                    {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                                ]
                            }]
                        }
                        
                        response = requests.post(url, json=payload, timeout=20)
                        res_json = response.json()
                        
                        if response.status_code == 200:
                            return res_json['candidates'][0]['content']['parts'][0]['text']
                        else:
                            last_error = res_json.get('error', {}).get('message', 'Unknown')
                            continue # جرب الموديل أو النسخة اللي بعدها
                
                return f"❌ كاع الموديلات عطاو 404. آخر خطأ: {last_error}"
                
            except Exception as e:
                return f"⚠️ Vision Error: {str(e)}"

        # --- حالة Chat (Groq) ---
        else:
            try:
                self.history.append({"role": "user", "content": user_input})
                completion = self.groq_client.chat.completions.create(
                    model=self.groq_model,
                    messages=self.history
                )
                ans = completion.choices[0].message.content
                self.history.append({"role": "assistant", "content": ans})
                return ans
            except Exception as e:
                return f"⚠️ Groq Error: {str(e)}"