import openai
from googletrans import Translator
import requests
from PIL import Image, ImageTk

from io import BytesIO
import tkinter as tk
from tkinter import PhotoImage ,simpledialog, messagebox

openai.api_key = '#########################' # api key
translator = Translator()
photo_label = None
text_label = None
def draw():
  global photo_label, text_label
  try:
    user_input = entry.get()
    example = translator.translate(user_input, dest="en")
    print("İstenen çizim : ",user_input, "\nİngizilcesi : ",example.text)
    response = openai.Image.create(
      prompt=example.text,
      n=1,
      size="1024x1024"
    )
    # Eğer metin etiketi önceden oluşturulmuşsa, sadece metni güncelle
    if text_label is not None:
      text_label.configure(text="İstenen çizim: " + user_input + "\nİngilizcesi: " + example.text )
    else:
      text_label = tk.Label(root, text="İstenen çizim: " + user_input + "\nİngilizcesi: " + example.text)
      text_label.pack()

    image_url = response['data'][0]['url']
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.save('outimg.png')
    photo = ImageTk.PhotoImage(img)
    if photo_label is not None:
      photo_label.configure(image=photo)
    else:
      photo_label = tk.Label(root, image=photo)
      photo_label.pack()
    photo_label.image = photo


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

button = tk.Button(root, text="Çiz", command=draw, width=10, height=1)
button.pack()
button = tk.Button(root, text="Çıkış", command=root.destroy, width=10, height=1)
button.pack()

root.mainloop()
