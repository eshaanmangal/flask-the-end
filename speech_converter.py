import speech_recognition as sr


audio_file = "normal.wav"
# audio_file = "files/harshit_slow.wav"
# audio_file = "very_slow.wav"


def speech_to_text(filename):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
    try:
        print("Audio text: " + text)
        f = open(filename, "w")
        f.write(text)
        f.close
        return True
    except:
        return False
