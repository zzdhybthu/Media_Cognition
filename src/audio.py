import whisper
import pyaudio
import numpy as np
import time
from zhipuai import ZhipuAI

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
    result = model.transcribe(audio_array, language = 'English', fp16=False)
    return result.get("text", "")


def save_to_file(text, filename="prompt.txt"):
    """将识别结果保存到文件"""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text + "\n")

def read_from_file(filename="prompt.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        text =  file.read()
    return text

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
                        # buffer = []
                        # is_awake = False
                        # silence_start_time = None
                        # print("Listening for wake word...")
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

def zhipu_ai(api_key, text, obj_list, colour_list):
        obj = ', '.join(obj_list)
        colour = ', '.join(colour_list)
        text = read_from_file()

        client = ZhipuAI(api_key=api_key)
        response = client.chat.completions.create(
            model="glm-4-0520",  # Fill in the model code you need to call
            messages=[
                {
                    "role": "user",
                    # "content": ("你是一个文本处理器 你需要截取一个任务语句中的物品和箱子颜色,物品只可能是[" + obj + "], 颜色只可能是[" + colour + "]. " +
                    #             "语句是语音输入的所以有可能不准确 请你在语句中识别出物品或者与物品拼音接近的词语 和 颜色或者与颜色拼音接近的词语 并输出物品和颜色, 我只需要物品和颜色，若语句不正确或没有物品或颜色请 返回“1”仅此而已。语句是“" + text + "”")
                    "content": f"This is a object list: {obj}\
                                \
                                This is a colour list: {colour}\
                                \
                                This is the task statement: {text}\
                                \
                                You are a text processor. You need to extract the object and box color from a task statement. The object and colour can only be in the object list or colour list \
                                'Since the statement is voice-input, it may not be accurate or according to their own understanding. \
                                Please identify words that are similar to the object or it's related to the object as 'object', for example 'time' is related to 'clock', 'bone' is related to 'dog', 'fish' is related to 'cat'\
                                Then, output the object and color. I only need the object and color, return by this format object, colour. If the statement is incorrect or does not contain an object or color, please return '1' and that's all. "
                }
            ],
        )
        # print(response.choices[0].message.content)
        return response.choices[0].message.content

if __name__ == "__main__":
    objlist = [
        'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
        'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
        'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
        'hair drier', 'toothbrush'
    ]
    # objlist = [
    #     '人', '自行车', '汽车', '摩托车', '飞机', '公共汽车', '火车', '卡车', '船', '交通灯',
    #     '消防栓', '停车标志', '停车计时器', '长椅', '鸟', '猫', '狗', '马', '羊', '牛',
    #     '大象', '熊', '斑马', '长颈鹿', '背包', '雨伞', '手提包', '领带', '行李箱', '飞盘',
    #     '滑雪板', '滑雪板', '运动球', '风筝', '棒球棒', '棒球手套', '滑板', '冲浪板',
    #     '网球拍', '瓶子', '葡萄酒杯', '杯子', '叉子', '刀', '勺子', '碗', '香蕉', '苹果',
    #     '三明治', '橙子', '西兰花', '胡萝卜', '热狗', '披萨', '甜甜圈', '蛋糕', '椅子', '沙发',
    #     '盆栽', '床', '餐桌', '马桶', '电视', '笔记本电脑', '鼠标', '遥控器', '键盘', '手机',
    #     '微波炉', '烤箱', '烤面包机', '水槽', '冰箱', '书', '时钟', '花瓶', '剪刀', '泰迪熊',
    #     '吹风机', '牙刷'
    # ]

    colourlist = ["red", "blue", "grey", "green"]
    # colourlist = ["红色", "蓝色", "灰色", "绿色"]
    apikey = "74dbc34c4cb2979f107458a4e5453010.OXXsSq9DwsvbNs5B"
    listen_and_recognize()
    data = read_from_file()
    print(zhipu_ai(apikey, data, objlist, colourlist))
