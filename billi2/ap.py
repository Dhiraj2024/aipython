import os
import whisper
from openai import OpenAI

# Nvidia API Key
NVIDIA_API_KEY = "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"

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

def extract_text_from_audio(audio_path):
    print("🎧 MP3 से ऑडियो सुना जा रहा है... (19 मिनट के ऑडियो में 2-3 मिनट लग सकते हैं, कृपया रुकें)")
    try:
        # Whisper का 'base' मॉडल लोड कर रहे हैं (यह हल्का और तेज़ है)
        model = whisper.load_model("base")
        
        # ऑडियो को ट्रांसक्राइब करना
        result = model.transcribe(audio_path)
        extracted_text = result["text"]
        
        print("\n✅ ऑडियो से टेक्स्ट सफलता पूर्वक निकाल लिया गया है!")
        return extracted_text
    except Exception as e:
        raise Exception(f"ऑडियो पढ़ने में एरर: {e}")

def generate_hindi_script(audio_text):
    print("🤖 AI से हिंदी वॉइसओवर स्क्रिप्ट जनरेट की जा रही है...\n")
    
    prompt = f"""
यह एक चीनी वीडियो की ट्रांसक्रिप्ट (ऑडियो का टेक्स्ट) है। आपको इसे एक बेहतरीन, सस्पेंस भरी और सरल हिंदी वॉइसओवर स्क्रिप्ट में बदलना है।

⚠️ सबसे महत्वपूर्ण नियम (CORE RULES):
1. यह टेक्स्ट 19 मिनट के ऑडियो से निकाला गया है। आपको इस पूरी कहानी को एक अच्छे फ्लो (Flow) में हिंदी में बताना है।
2. अपनी तरफ से कोई भी एक्स्ट्रा कहानी या फालतू ज्ञान न जोड़ें। जो टेक्स्ट में हुआ है, बस वही बताएं।
3. टोन एक सस्पेंसफुल नैरेटर (Storyteller) वाला होना चाहिए।
4. आम बोलचाल वाली हिंदी का इस्तेमाल करें (जैसे 'तभी', 'अचानक', 'हैरानी की बात तो यह थी')।

Audio Transcript (Text):
{audio_text}
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
        
        choices = completion.choices
        if isinstance(choices, list) and len(choices) > 0:
            first_choice = choices[0]
            if hasattr(first_choice, 'message'):
                full_script = first_choice.message.content
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
    # 🔴 यहाँ अपनी MP3 फाइल का नाम या पाथ (Path) डालें
    AUDIO_FILE_PATH = "chinese_audio.mp3"  
    
    try:
        # 1. MP3 से टेक्स्ट निकालें
        audio_transcript = extract_text_from_audio(AUDIO_FILE_PATH)
        
        # 2. टेक्स्ट से हिंदी स्क्रिप्ट बनाएं
        hindi_script = generate_hindi_script(audio_transcript)
        
        # 3. फाइल में सेव करें
        output_file = "final_hindi_script.txt"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(hindi_script)
            
        print(f"\n\n✅ काम पूरा हुआ! स्क्रिप्ट '{output_file}' में सेव हो चुकी है।")
        
    except Exception as e:
        print(f"\n❌ एरर आया: {e}")