import os
from openai import OpenAI
import yt_dlp

# Nvidia API Key
NVIDIA_API_KEY = "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"

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

def get_video_metadata(video_url):
    print("🔗 वीडियो की जानकारी (Metadata) निकाली जा रही है...")
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        # 'cookiesfrombrowser': ('chrome',), # अगर Bilibili ब्लॉक करे तो इसके आगे से # हटा दें
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'No Title')
            description = info.get('description', 'No Description')
            return f"Title: {title}\nDescription: {description}"
    except Exception as e:
        raise Exception(f"लिंक पढ़ने में एरर: {e}")

def generate_script_with_deepseek(video_context):
    print("🤖 AI से प्रीमियम वॉइसओवर स्क्रिप्ट जनरेट की जा रही है... (कृपया 5-10 सेकंड इंतज़ार करें)\n")
    
    prompt = f"""
यह एक बेहद जरूरी काम है। आपको नीचे दिए गए 'Video Context' (जिसमें एक चीनी वीडियो का Title और Description है) को एक सीधे, सरल और रहस्यमयी हिंदी स्टोरीटेलिंग या टीज़र स्क्रिप्ट में बदलना है।

⚠️ सबसे महत्वपूर्ण नियम (STRICT CORE RULES):
1. NO HALLUCINATION: अपनी तरफ से कोई भी काल्पनिक घटना, इंसान, कमरे का सीन (जैसे टीवी देखना, खिड़की से झांकना) बिल्कुल न जोड़ें। 
2. आपको वीडियो में क्या हो रहा है यह नहीं पता है, आपको सिर्फ दिए गए Text (Title और Description) को एक वॉइसओवर में बदलना है।
3. जो जानकारी Video Context में नहीं है, उसका जिक्र तक न करें।
4. इस वीडियो का चीनी टाइटल (जैसे: '天黑别出门' जिसका मतलब है 'अंधेरा होने के बाद बाहर मत निकलना') और विवरण का असली भाव समझें और उसे एक सस्पेंस से भरे इंट्रो (Intro) में बदलें।
5. स्क्रिप्ट का टोन एक गंभीर स्टोरीटेलर (Narrator) जैसा होना चाहिए।

🎯 स्क्रिप्ट का ढांचा (Structure):
- शुरुआत एक दमदार हुक (Hook) से करें जो दिए गए टाइटल पर आधारित हो।
- इसके बाद डिस्क्रिप्शन में दी गई जानकारी (अगर कोई है) को रहस्यमयी और सरल हिंदी में बताएं।
- वाक्य छोटे और वॉइसओवर (Voiceover) के लिए उपयुक्त होने चाहिए। किताब वाली भाषा नहीं, आम बोलचाल वाली भाषा (जैसे 'तभी', 'लेकिन', 'हैरानी की बात तो यह है') का इस्तेमाल करें।

❌ इन चीजों से सख्त परहेज करें:
- "यह वीडियो हमें सिखाता है..." या "दोस्तों आज मैं आपको..." जैसे घिसे-पिटे शब्द न लिखें।
- पूरी तरह से मनगढ़ंत कहानी बनाने की कोशिश न करें। अगर Context छोटा है, तो स्क्रिप्ट भी छोटी और क्रिस्प (Crisp) रखें।

Video Context:
{video_context}
"""

    try:
        completion = client.chat.completions.create(
            model="meta/llama-3.3-70b-instruct",  
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,    
            top_p=0.95,
            max_tokens=4096,    
            stream=False 
        )
        
        # 🟢 बुलेटप्रूफ डेटा एक्सट्रैक्शन (अब एरर नहीं आएगा)
        choices = completion.choices
        if isinstance(choices, list) and len(choices) > 0:
            first_choice = choices
            
            # अगर डेटा Object फॉर्मेट में है
            if hasattr(first_choice, 'message'):
                full_script = first_choice.message.content
            # अगर डेटा Dictionary (JSON) फॉर्मेट में है
            elif isinstance(first_choice, dict) and 'message' in first_choice:
                full_script = first_choice['message'].get('content', '')
            else:
                full_script = str(first_choice)
        else:
            full_script = "⚠️ API से कोई जवाब नहीं मिला।"

        print(full_script)
        return full_script
        
    except Exception as e:
        raise Exception(f"API से कनेक्ट करने में एरर: {e}")

if __name__ == "__main__":
    # Bilibili का URL
    BILIBILI_VIDEO_URL = "https://www.bilibili.com/bangumi/play/ep836727/?share_source=copy_web" 
    
    try:
        # 1. मेटाडेटा निकालें
        context = get_video_metadata(BILIBILI_VIDEO_URL)
        
        # 2. AI से स्क्रिप्ट जनरेट करें
        script_output = generate_script_with_deepseek(context)
        
        # 3. फाइल में सेव करें
        output_file = "bilibili_script.txt"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(script_output)
            
        print(f"\n\n✅ काम पूरा हुआ! स्क्रिप्ट '{output_file}' में सेव हो चुकी है।")
        
    except Exception as e:
        print(f"\n❌ एरर आया: {e}")