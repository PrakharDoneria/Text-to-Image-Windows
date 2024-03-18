import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser

def generate_image(prompt, api_key):
    url = "https://text-to-image-stable-ai.p.rapidapi.com/prompt"
    payload = {"prompt": prompt}
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "text-to-image-stable-ai.p.rapidapi.com"
    }
    response = requests.post(url, data=payload, headers=headers)
    return response.json()

def load_image(image_url):
    response = requests.get(image_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    return ImageTk.PhotoImage(img)

def open_link():
    webbrowser.open_new("https://rapidapi.com/yashdoneria/api/text-to-image-stable-ai/")

def clear_entry(event):
    event.widget.delete(0, tk.END)

def create_gui():
    window = tk.Tk()
    window.title("Text to Image App")

    custom_font = ("Arial", 12)

    # Custom colors
    background_color = "#FFFFFF"
    text_color = "#333333"
    input_bg_color = "#E0E0E0"
    button_bg_color = "#2196F3"
    link_color = "#4CAF50"

    window.config(bg=background_color)

    style = ttk.Style()
    style.theme_use('clam')

    style.configure('TButton', background=button_bg_color, foreground=text_color, font=custom_font)
    style.map('TButton', background=[('active', '#1976D2')])

    label_prompt = tk.Label(window, text="Enter prompt:", font=custom_font, bg=background_color, fg=text_color)
    label_prompt.pack()

    entry_prompt = tk.Entry(window, font=custom_font, bg=input_bg_color, fg=text_color)
    entry_prompt.pack()
    entry_prompt.insert(0, "Enter keyword")
    entry_prompt.bind("<FocusIn>", clear_entry)

    label_api_key = tk.Label(window, text="Enter RapidAPI Key:", font=custom_font, bg=background_color, fg=text_color)
    label_api_key.pack()

    entry_api_key = tk.Entry(window, font=custom_font, bg=input_bg_color, fg=text_color)
    entry_api_key.pack()

    image_label = tk.Label(window)
    image_label.pack()

    image_url_label = tk.Label(window, font=custom_font, bg=background_color, fg=text_color)
    image_url_label.pack()

    def generate_image_action():
        prompt = entry_prompt.get()
        api_key = entry_api_key.get()
        if prompt and api_key:
            response = generate_image(prompt, api_key)
            if "image_url" in response:
                image_url = response["image_url"]
                image = load_image(image_url)
                image_label.config(image=image)
                image_label.image = image
                image_url_label.config(text=f"Image URL: {image_url}")
            elif "error" in response:
                messagebox.showerror("Error", response["error"])
            else:
                messagebox.showerror("Error", "Unknown error occurred.")
        else:
            messagebox.showerror("Error", "Please enter prompt and API key.")

    button_generate = ttk.Button(window, text="Generate Image", command=generate_image_action)
    button_generate.pack(pady=10)

    link_label = tk.Label(window, text="Subscribe to API", fg=link_color, cursor="hand2", font=custom_font, bg=background_color)
    link_label.pack(pady=5)
    link_label.bind("<Button-1>", lambda e: open_link())

    window.mainloop()

if __name__ == "__main__":
    create_gui()
