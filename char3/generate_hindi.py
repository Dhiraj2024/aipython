# import os
# from dotenv import load_dotenv
# from elevenlabs.client import ElevenLabs

# # 1. .env file se API Key load karein
# load_dotenv()
# API_KEY = os.getenv("ELEVENLABS_API_KEY")

# if not API_KEY:
#     raise ValueError("Error: ELEVENLABS_API_KEY nahi mili! .env file check karein.")

# # 2. ElevenLabs Client initialize karein
# client = ElevenLabs(api_key=API_KEY)

# # 3. Hindi Text (Expressions ke liye sabse best hai ki aap pure Hindi script likhein)
# hindi_text = (
#     "अरे भाई! तुम कहाँ रह गए थे? मैं कब से तुम्हारा इंतज़ार कर रहा हूँ। "
#     "चchal bhag yahan se kamine nikal nai  तो आराम से बैठो और बताओ क्या बात है!"
# )

# print("⏳ ElevenLabs AI aapki Hindi audio generate kar raha hai (with emotions)...")

# try:
#     # 4. API Call - text_to_speech.convert
#     # Humne model_id="eleven_v3" rakha hai jo multilingual emotions ke liye best hai
#     audio_generator = client.text_to_speech.convert(
#         text=hindi_text,
#         voice_id="JBFqnCBsd6RMkjVDRZzb",  # George Voice
#         model_id="eleven_v3",
#         output_format="mp3_44100_128"
#     )

#     # 5. Generator se saara raw audio data ek baar me nikalne ke liye
#     audio_data = b"".join(audio_generator)

#     # 6. Audio ko file me save karna
#     output_filename = "hindi_output.mp3"
#     with open(output_filename, "wb") as f:
#         f.write(audio_data)

#     print(f"\n✅ Kamaal ka Hindi audio generate ho gaya hai!")
#     print(f"🎵 File aapke folder me save ho chuki hai: '{output_filename}'")

# except Exception as e:
#     print(f"\n❌ Ek error aayi: {e}")

import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

# 1. API Key Load karein
load_dotenv()
API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not API_KEY:
    raise ValueError("Error: ELEVENLABS_API_KEY nahi mili!")

client = ElevenLabs(api_key=API_KEY)

# 2. AAPKI CUSTOM SCRIPT (Yahan aap manually voice_id aur settings badal sakte hain)
# Tip: stability kam karne se aawaz me expressions/gussa/drama badhta hai.
script = [
    {
        "character_name": "Male Monkey Expert",
        "voice_id": "JBFqnCBsd6RMkjVDRZzb",  # George (Male)
        "text": "हम भी देखते हैं कि क्या होगा अगर कोई बंदर पेड़ पर चढ़कर गाली दे दे!",
        "stability": 0.45,       # Low stability = More expressions/emotions
        "similarity": 0.75
    },
    {
        "character_name": "Female Replying",
        "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Lily (Female - Funny/High Tone)
        "text": "कुछ नहीं होगा! बस तुम्हें पागलों की तरह ट्रीट किया जाएगा।",
        "stability": 0.50,       
        "similarity": 0.80
    }
]

# Saare characters ka audio data isme jama hoga
final_audio_segments = []

print("⏳ Multi-Character conversation generate ho raha hai...\n")

try:
    for index, dialogue in enumerate(script):
        print(f"🎙️ Generating dialogue {index + 1} ({dialogue['character_name']})...")
        
        # ElevenLabs API Call for each character
        audio_generator = client.text_to_speech.convert(
            text=dialogue["text"],
            voice_id=dialogue["voice_id"],
            model_id="eleven_v3",  # Hindi support ke liye best model
            output_format="mp3_44100_128",
            voice_settings={
                "stability": dialogue["stability"],
                "similarity_boost": dialogue["similarity"]
            }
        )
        
        # Raw audio byte chunks ko convert karke segment me add karein
        audio_bytes = b"".join(audio_generator)
        final_audio_segments.append(audio_bytes)

    # 3. Saare generated audios ko ek sath merge (join) karein
    full_conversation_audio = b"".join(final_audio_segments)

    # 4. Final Output File Save Karein
    output_filename = "final_story.mp3"
    with open(output_filename, "wb") as f:
        f.write(full_conversation_audio)

    print(f"\n✅ Kamaal ki conversation taiyar hai!")
    print(f"🎵 File save ho chuki hai: '{output_filename}'")

except Exception as e:
    print(f"\n❌ Ek error aayi: {e}")