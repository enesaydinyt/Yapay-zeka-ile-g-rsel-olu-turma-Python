import openai
from googletrans import Translator
import requests
from PIL import Image
from io import BytesIO
import tkinter as tk
from tkinter import PhotoImage ,simpledialog, messagebox

openai.api_key = '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'
translator = Translator()

def draw():
  try:
    user_input = entry.get()
    example = translator.translate(user_input, dest="en")
    print("İstenen çizim : ",user_input, "\nİngizilcesi : ",example.text)
    response = openai.Image.create(
      prompt=example.text,
      n=1,
      size="1024x1024"
    )
    label = tk.Label(root, text=("İstenen çizim : ",user_input, " İngizilcesi : ",example.text))
    label.pack()
    image_url = response['data'][0]['url']
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.save('outimg.png')
    photo = PhotoImage(file="outimg.png")
    label = tk.Label(root, image=photo)

    label.image = photo
    label.pack()


    root.mainloop()

  except Exception as e:
    print("Bir hata oluştu:", e)
    messagebox.showwarning("Uyarı",("Bir hata oluştu:", e))
root = tk.Tk()
root.title("Resim çizim örneği")
root.attributes("-fullscreen", True)
label = tk.Label(root, text="Yapay zeka ile görsel tasarlama")
label.pack()
entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Çiz", command=draw , width=10, height=1)
button.pack()
button = tk.Button(root, text="Çıkış", command=root.quit, width=10, height=1)
button.pack()

root.mainloop()
