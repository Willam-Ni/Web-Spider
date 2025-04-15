import requests
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os

# 关闭系统代理
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()

        current = data['current_condition'][0]
        result = f"📍 当前城市：{city}\n"
        result += f"🌤 当前天气：{current['weatherDesc'][0]['value']}\n"
        result += f"🌡 当前温度：{current['temp_C']}°C\n"
        result += f"💧 湿度：{current['humidity']}%\n"
        result += f"🍃 风速：{current['windspeedKmph']} km/h\n\n"

        result += "📅 未来 3 天预报：\n"
        for i in range(3):
            day = data['weather'][i]
            date = day['date']
            avg_temp = day['avgtempC']
            weather = day['hourly'][4]['weatherDesc'][0]['value']  # 中午12点天气
            result += f"{date} | 平均温度：{avg_temp}°C | 天气：{weather}\n"
        return result

    except Exception as e:
        return f"❌ 获取天气失败：{e}"

def query_weather():
    city = entry.get()
    if not city:
        ttk.messagebox.showwarning("提示", "请输入城市名称")
        return
    result = get_weather(city)
    output.delete(1.0, "end")
    output.insert("end", result)

# 创建美化窗口
app = ttk.Window(title="🌦 天气查询器", themename="flatly", size=(500, 400))

# 输入框
label = ttk.Label(app, text="请输入城市名称（如 Beijing、Shanghai）：", font=("微软雅黑", 12))
label.pack(pady=10)

entry = ttk.Entry(app, width=30, font=("微软雅黑", 11))
entry.pack()

btn = ttk.Button(app, text="查询天气", bootstyle=PRIMARY, command=query_weather)
btn.pack(pady=10)

# 输出框
output = ttk.Text(app, height=12, width=60, font=("Consolas", 10))
output.pack(padx=10, pady=10)

app.mainloop()
