
import asyncio
import os
from edge_tts import Communicate

# ==============================
# 🎬 YOUR MANUAL SCRIPT (UNCHANGED)
# ==============================
script = [
    {
        "voice": "hi-IN-MadhurNeural",
        "text": "ha mummy mai school se ghar wapas aa gaya hun ",
        "rate": "+10%",
        "pitch": "+15Hz"
    },
     {
        "voice": "hi-IN-MadhurNeural",
        "text": "abhi park men chair lekar relax karunga okey. ",
        "rate": "+5%",
        "pitch": "+15Hz"
    },
     {
        "voice": "hi-IN-MadhurNeural",
        "text": " hey girls kya bata sakti ho mera jacket se paise ka note kaha gira ,",
        "rate": "+30%",
        "pitch": "+25Hz"
    },
      {
        "voice": "hi-IN-SwaraNeural",
        "text": " nai pata, ok bhai ",
        "rate": "+20%",
        "pitch": "-1Hz"
    },
            {
        "voice": "hi-IN-SwaraNeural",
        "text": "abe saale yaha kya ho raha hi , ye chair ko kisne bite kiya? are ye ladka kitna funny hai jisne chair ko pura bite  kar dala ye pagla gaya hi doston",
        "rate": "+20%",
        "pitch": "+19Hz"
    }
]
AUDIO_OUTPUT = "conversation.mp3"


# ==============================
# 🚀 AUDIO GENERATOR (ONLY PLAYBACK)
# ==============================
async def generate_audio():
    final_audio_data = b""

    print("🚀 Audio generate ho raha hai...")

    for i, line in enumerate(script):
        print(f"Line {i+1}...")

        communicate = Communicate(
            text=line["text"],
            voice=line["voice"],
            rate=line["rate"],
            pitch=line["pitch"],
        )

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                final_audio_data += chunk["data"]

        # 👉 Cinematic pause (important)
        final_audio_data += b"\x00" * 20000

    # Save MP3
    with open(AUDIO_OUTPUT, "wb") as f:
        f.write(final_audio_data)

    print("🎉 Done!")
    print(f"🎵 Audio: {os.path.abspath(AUDIO_OUTPUT)}")


# ==============================
# ▶ RUN
# ==============================
if __name__ == "__main__":
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(generate_audio())