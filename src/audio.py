

# import whisper
# import pyaudio
# import numpy as np
# import time

# # 初始化 Whisper 模型
# model = whisper.load_model("base")  # 可选择 'tiny', 'small', 'medium', 'large'

# # 唤醒词设置
# WAKE_WORD = "hello"

# # 配置音频输入
# CHUNK = 1024  # 每个数据块的帧数
# FORMAT = pyaudio.paInt16  # 采样格式
# CHANNELS = 1  # 单声道
# RATE = 16000  # 采样率
# SILENCE_THRESHOLD = 500  # 静音阈值（音量）
# SILENCE_DURATION = 3  # 静音检测时长（秒）


# def is_silent(audio_data):
#     """判断音频数据是否静音"""
#     audio_array = np.frombuffer(audio_data, np.int16)
#     return np.abs(audio_array).mean() < SILENCE_THRESHOLD


# def transcribe_audio(audio_data):
#     """使用 Whisper 模型进行语音识别"""
#     audio_array = np.frombuffer(audio_data, np.int16).astype(np.float32) / 32768.0
#     result = model.transcribe(audio_array, fp16=False)
#     return result.get("text", "")


# def listen_and_recognize():
#     """实时监听和识别语音"""
#     audio = pyaudio.PyAudio()
#     stream = audio.open(format=FORMAT, channels=CHANNELS,
#                         rate=RATE, input=True,
#                         frames_per_buffer=CHUNK)

#     print("Listening for wake word...")
#     buffer = []
#     is_awake = False
#     silence_start_time = None
#     start_time = None

#     try:
#         while True:
#             data = stream.read(CHUNK, exception_on_overflow=False)

#             if is_awake:
#                 buffer.append(data)

#                 # 检测静音
#                 if is_silent(data):
#                     if silence_start_time is None:
#                         silence_start_time = time.time()
#                     elif time.time() - silence_start_time >= SILENCE_DURATION:
#                         # 静音超过指定时间，停止识别并输出结果
#                         print("Silent detected, stopping recognition.")
#                         audio_data = b''.join(buffer)
#                         result = transcribe_audio(audio_data)
#                         print("Recognized text:", result.strip())
#                         buffer = []
#                         is_awake = False
#                         silence_start_time = None
#                         print("Listening for wake word...")
#                 else:
#                     silence_start_time = None  # 重置静音计时

#             else:
#                 # 在非激活模式下检查唤醒词
#                 buffer.append(data)
#                 if len(buffer) >= int(RATE / CHUNK * 2):  # 2秒缓冲区
#                     audio_data = b''.join(buffer)
#                     buffer = []
#                     text = transcribe_audio(audio_data).lower()
#                     print("Recognized:", text)

#                     if WAKE_WORD in text:
#                         print("Wake word detected. Starting recognition...")
#                         is_awake = True
#                         buffer = []
#                         silence_start_time = None
#     except KeyboardInterrupt:
#         print("\nExiting...")
#     finally:
#         stream.stop_stream()
#         stream.close()
#         audio.terminate()


# if __name__ == "__main__":
#     listen_and_recognize()


import whisper
import pyaudio
import numpy as np
import time

# 初始化 Whisper 模型
model = whisper.load_model("base")  # 可选择 'tiny', 'small', 'medium', 'large'

# 唤醒词设置
WAKE_WORD = "hello"

# 配置音频输入
CHUNK = 1024  # 每个数据块的帧数
FORMAT = pyaudio.paInt16  # 采样格式
CHANNELS = 1  # 单声道
RATE = 16000  # 采样率
SILENCE_THRESHOLD = 500  # 静音阈值（音量）
SILENCE_DURATION = 3  # 静音检测时长（秒）


def is_silent(audio_data):
    """判断音频数据是否静音"""
    audio_array = np.frombuffer(audio_data, np.int16)
    return np.abs(audio_array).mean() < SILENCE_THRESHOLD


def transcribe_audio(audio_data):
    """使用 Whisper 模型进行语音识别"""
    audio_array = np.frombuffer(audio_data, np.int16).astype(np.float32) / 32768.0
    result = model.transcribe(audio_array, fp16=False)
    return result.get("text", "")


def save_to_file(text, filename="prompt.txt"):
    """将识别结果保存到文件"""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text + "\n")


def listen_and_recognize():
    """实时监听和识别语音"""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Listening for wake word...")
    buffer = []
    is_awake = False
    silence_start_time = None

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)

            if is_awake:
                buffer.append(data)

                # 检测静音
                if is_silent(data):
                    if silence_start_time is None:
                        silence_start_time = time.time()
                    elif time.time() - silence_start_time >= SILENCE_DURATION:
                        # 静音超过指定时间，停止识别并输出结果
                        print("Silent detected, stopping recognition.")
                        audio_data = b''.join(buffer)
                        result = transcribe_audio(audio_data)
                        print("Recognized text:", result.strip())

                        # 写入文件
                        save_to_file(result.strip())
                        print(f"Result saved to 'prompt.txt'.")

                        break

                        buffer = []
                        is_awake = False
                        silence_start_time = None
                        print("Listening for wake word...")
                else:
                    silence_start_time = None  # 重置静音计时

            else:
                # 在非激活模式下检查唤醒词
                buffer.append(data)
                if len(buffer) >= int(RATE / CHUNK * 2):  # 2秒缓冲区
                    audio_data = b''.join(buffer)
                    buffer = []
                    text = transcribe_audio(audio_data).lower()
                    print("Recognized:", text)

                    if WAKE_WORD in text:
                        print("Wake word detected. Starting recognition...")
                        is_awake = True
                        buffer = []
                        silence_start_time = None
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

def SplitPrompt():
    prompt = ""
    with open(r'prompt.txt','r',encoding='utf-8') as test:
        test.seek(0, 0)
        prompt = test.readline()   
    prompt = prompt.split(' ')
    obj = prompt[1]
    box = prompt[3]
    # print(type((obj, box)))
    return (obj, box)


if __name__ == "__main__":
    listen_and_recognize()
