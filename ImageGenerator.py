import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import io
import threading
from datetime import datetime
import requests
import os

# ==========================
# POLLINATIONS API (FREE & WORKING)
# ==========================
class PollinationsClient:
    def __init__(self):
        # Pollinations FREE API - No key needed!
        self.base_url = "https://image.pollinations.ai/prompt"
    
    def generate_image(self, prompt, width=1024, height=1024):
        """Generate image using for free"""
        
        # Format prompt for URL
        encoded_prompt = requests.utils.quote(prompt)
        url = f"{self.base_url}/{encoded_prompt}?width={width}&height={height}&nologo=true"
        
        print(f"📤 Generating from: {url[:100]}...")
        print(f"📝 Prompt: {prompt[:50]}...")
        
        response = requests.get(url, timeout=60)
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        else:
            raise Exception(f"API Error {response.status_code}")

# ==========================
# MAIN APPLICATION
# ==========================
class ImageGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.client = PollinationsClient()
        self.current_image = None
        self.is_generating = False
        self.setup_ui()
        self.insert_message("✅ Pollinations API Connected! (FREE)", "success")
        
    def setup_ui(self):
        self.root.title("🎨 Generate Your Imagination")
        self.root.geometry("1200x700")
        self.root.configure(bg="#0a0a0f")
        
        self.COLORS = {
            "bg": "#0a0a0f",
            "sidebar": "#14141f",
            "card": "#1c1c2a",
            "accent": "#8b5cf6",
            "accent_hover": "#a78bfa",
            "accent_secondary": "#06b6d4",
            "text": "#ffffff",
            "text_secondary": "#a1a1aa",
            "success": "#10b981",
            "error": "#ef4444",
            "warning": "#f59e0b"
        }
        
        self.setup_sidebar()
        self.setup_main_content()
        
    def setup_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg=self.COLORS["sidebar"], width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        logo_frame = tk.Frame(self.sidebar, bg=self.COLORS["sidebar"])
        logo_frame.pack(fill="x", pady=(30, 20))
        
        tk.Label(logo_frame, text="🎨", font=("Arial", 48), 
                bg=self.COLORS["sidebar"], fg=self.COLORS["accent"]).pack()
        tk.Label(logo_frame, text="You Can Download it", font=("Helvetica", 18, "bold"),
                bg=self.COLORS["sidebar"], fg=self.COLORS["text"]).pack()
        tk.Label(logo_frame, text="Free Image Generator", font=("Helvetica", 10),
                bg=self.COLORS["sidebar"], fg=self.COLORS["accent_secondary"]).pack()
        
        info_frame = tk.Frame(self.sidebar, bg=self.COLORS["card"])
        info_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Label(info_frame, text="🆓 100% FREE", font=("Helvetica", 10, "bold"),
                bg=self.COLORS["card"], fg=self.COLORS["success"]).pack(anchor="w", pady=(10, 5))
        tk.Label(info_frame, text="Simple Image Generator", font=("Helvetica", 9),
                bg=self.COLORS["card"], fg=self.COLORS["text_secondary"]).pack(anchor="w")
        tk.Label(info_frame, text="Fast & Reliable", font=("Helvetica", 8),
                bg=self.COLORS["card"], fg=self.COLORS["accent"]).pack(anchor="w", pady=(0, 10))
        
        stats_frame = tk.Frame(self.sidebar, bg=self.COLORS["card"])
        stats_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Label(stats_frame, text="📊 Statistics", font=("Helvetica", 11, "bold"),
                bg=self.COLORS["card"], fg=self.COLORS["text"]).pack(anchor="w", pady=(10, 5))
        
        self.images_count = tk.Label(stats_frame, text="Generated: 0", font=("Helvetica", 10),
                                    bg=self.COLORS["card"], fg=self.COLORS["text_secondary"])
        self.images_count.pack(anchor="w", pady=2)
        
        settings_frame = tk.Frame(self.sidebar, bg=self.COLORS["card"])
        settings_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Label(settings_frame, text="⚙️ Settings", font=("Helvetica", 11, "bold"),
                bg=self.COLORS["card"], fg=self.COLORS["text"]).pack(anchor="w", pady=(10, 5))
        
        tk.Label(settings_frame, text="Width:", font=("Helvetica", 9),
                bg=self.COLORS["card"], fg=self.COLORS["text_secondary"]).pack(anchor="w")
        self.width_var = tk.IntVar(value=1024)
        width_menu = ttk.Combobox(settings_frame, textvariable=self.width_var,
                                  values=[512, 768, 1024, 1280],
                                  state="readonly")
        width_menu.pack(fill="x", pady=(5, 10))
        
        tk.Label(settings_frame, text="Height:", font=("Helvetica", 9),
                bg=self.COLORS["card"], fg=self.COLORS["text_secondary"]).pack(anchor="w")
        self.height_var = tk.IntVar(value=1024)
        height_menu = ttk.Combobox(settings_frame, textvariable=self.height_var,
                                   values=[512, 768, 1024, 1280],
                                   state="readonly")
        height_menu.pack(fill="x", pady=(5, 10))
        
        api_frame = tk.Frame(self.sidebar, bg=self.COLORS["card"])
        api_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Label(api_frame, text="🔑 API Status", font=("Helvetica", 10, "bold"),
                bg=self.COLORS["card"], fg=self.COLORS["text"]).pack(anchor="w", pady=(10, 5))
        
        self.api_status = tk.Label(api_frame, text="● Connected (FREE)", font=("Helvetica", 9),
                                   bg=self.COLORS["card"], fg=self.COLORS["success"])
        self.api_status.pack(anchor="w", pady=(0, 10))
        
    def setup_main_content(self):
        main_content = tk.Frame(self.root, bg=self.COLORS["bg"])
        main_content.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        header_frame = tk.Frame(main_content, bg=self.COLORS["bg"])
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_frame, text="🎨 Free AI Image Generator", font=("Helvetica", 28, "bold"),
                bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(anchor="w")
        tk.Label(header_frame, text="Powered by Pollinations AI · 100% FREE · No Credits Needed!", font=("Helvetica", 11),
                bg=self.COLORS["bg"], fg=self.COLORS["accent_secondary"]).pack(anchor="w")
        
        content_container = tk.Frame(main_content, bg=self.COLORS["bg"])
        content_container.pack(fill="both", expand=True)
        
        self.setup_chat_area(content_container)
        self.setup_image_area(content_container)
        self.setup_input_area(main_content)
        
    def setup_chat_area(self, parent):
        chat_frame = tk.Frame(parent, bg=self.COLORS["card"])
        chat_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        chat_header = tk.Frame(chat_frame, bg=self.COLORS["card"])
        chat_header.pack(fill="x", padx=15, pady=(15, 0))
        
        tk.Label(chat_header, text="💬 Conversation", font=("Helvetica", 14, "bold"),
                bg=self.COLORS["card"], fg=self.COLORS["text"]).pack(side="left")
        
        clear_btn = tk.Button(chat_header, text="Clear Chat", command=self.clear_chat,
                             font=("Helvetica", 9), bg=self.COLORS["error"], fg="white",
                             relief="flat", cursor="hand2", padx=10, pady=3)
        clear_btn.pack(side="right")
        
        self.chat_box = tk.Text(chat_frame, bg=self.COLORS["card"], fg=self.COLORS["text"],
                                font=("Helvetica", 10), wrap="word", bd=0)
        self.chat_box.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.chat_box.tag_config("user", foreground=self.COLORS["accent_secondary"], 
                                 font=("Helvetica", 9, "bold"))
        self.chat_box.tag_config("system", foreground=self.COLORS["text_secondary"])
        self.chat_box.tag_config("success", foreground=self.COLORS["success"])
        self.chat_box.tag_config("error", foreground=self.COLORS["error"])
        
        scrollbar = ttk.Scrollbar(chat_frame, command=self.chat_box.yview)
        scrollbar.pack(side="right", fill="y", pady=10)
        self.chat_box.config(yscrollcommand=scrollbar.set)
        
    def setup_image_area(self, parent):
        image_frame = tk.Frame(parent, bg=self.COLORS["card"], width=550)
        image_frame.pack(side="right", fill="both", expand=True)
        image_frame.pack_propagate(False)
        
        image_header = tk.Frame(image_frame, bg=self.COLORS["card"])
        image_header.pack(fill="x", padx=15, pady=(15, 0))
        
        tk.Label(image_header, text="🖼️ Generated Artwork", font=("Helvetica", 14, "bold"),
                bg=self.COLORS["card"], fg=self.COLORS["text"]).pack(side="left")
        
        save_btn = tk.Button(image_header, text="Save Image", command=self.save_image,
                            font=("Helvetica", 9), bg=self.COLORS["success"], fg="white",
                            relief="flat", cursor="hand2", padx=10, pady=3)
        save_btn.pack(side="right")
        
        image_container = tk.Frame(image_frame, bg=self.COLORS["card"])
        image_container.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.image_label = tk.Label(image_container, bg=self.COLORS["card"],
                                    text="🎨 Your image will appear here!\n\nDescribe something and click Generate",
                                    font=("Helvetica", 12), fg=self.COLORS["text_secondary"])
        self.image_label.pack(fill="both", expand=True)
        
    def setup_input_area(self, parent):
        input_container = tk.Frame(parent, bg=self.COLORS["bg"])
        input_container.pack(fill="x", pady=(20, 0))
        
        input_bg = tk.Frame(input_container, bg=self.COLORS["card"])
        input_bg.pack(fill="x", pady=10)
        
        tk.Label(input_bg, text="✏️ Describe your image:", font=("Helvetica", 10, "bold"),
                bg=self.COLORS["card"], fg=self.COLORS["text"]).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.prompt_entry = tk.Entry(input_bg, font=("Helvetica", 12), bg=self.COLORS["bg"],
                                     fg=self.COLORS["text"], insertbackground=self.COLORS["accent"],
                                     relief="flat", bd=0)
        self.prompt_entry.pack(fill="x", padx=20, pady=(0, 10))
        self.prompt_entry.bind("<Return>", lambda event: self.generate_image())
        
        examples_frame = tk.Frame(input_bg, bg=self.COLORS["card"])
        examples_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        examples = [
            "a beautiful sunset over mountains",
            "a futuristic city with neon lights",
            "a cute cat wearing a wizard hat",
            "a spaceship flying through space"
        ]
        
        for ex in examples:
            btn = tk.Button(examples_frame, text=ex[:25] + "...", command=lambda e=ex: self.set_prompt(e),
                           font=("Helvetica", 8), bg=self.COLORS["bg"], fg=self.COLORS["text_secondary"],
                           relief="flat", cursor="hand2")
            btn.pack(side="left", padx=3)
        
        button_frame = tk.Frame(input_bg, bg=self.COLORS["card"])
        button_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.progress_bar = ttk.Progressbar(button_frame, mode="indeterminate", length=200)
        
        self.generate_btn = tk.Button(button_frame, text="🎨 Generate Image (FREE)", command=self.generate_image,
                                      font=("Helvetica", 12, "bold"), bg=self.COLORS["accent"],
                                      fg="white", relief="flat", cursor="hand2",
                                      padx=25, pady=10)
        self.generate_btn.pack()
        
        self.generate_btn.bind("<Enter>", lambda e: self.generate_btn.config(bg=self.COLORS["accent_hover"]))
        self.generate_btn.bind("<Leave>", lambda e: self.generate_btn.config(bg=self.COLORS["accent"]))
        
    def set_prompt(self, prompt):
        self.prompt_entry.delete(0, tk.END)
        self.prompt_entry.insert(0, prompt)
        
    def generate_image(self):
        if self.is_generating:
            self.insert_message("⚠️ Already generating... Please wait!", "warning")
            return
            
        prompt = self.prompt_entry.get().strip()
        
        if not prompt:
            self.insert_message("⚠️ Please enter a prompt", "error")
            return
        
        self.is_generating = True
        self.insert_message(f"📝 {prompt}", "user")
        self.insert_message("🎨 Generating image...", "system")
        
        self.generate_btn.config(state="disabled", text="⏳ Generating...")
        self.progress_bar.pack(side="right", padx=(10, 0))
        self.progress_bar.start()
        
        def generate_thread():
            try:
                img = self.client.generate_image(
                    prompt, 
                    width=self.width_var.get(),
                    height=self.height_var.get()
                )
                self.root.after(0, self.display_image, img)
                
            except Exception as e:
                self.root.after(0, self.handle_error, str(e))
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def display_image(self, img):
        try:
            display_size = 500
            img.thumbnail((display_size, display_size), Image.Resampling.LANCZOS)
            
            self.current_image = img
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk
            
            current_count = int(self.images_count.cget("text").split(": ")[1])
            self.images_count.config(text=f"Generated: {current_count + 1}")
            
            self.insert_message("✅ Image generated successfully! (FREE)", "success")
            
        except Exception as e:
            self.handle_error(f"Failed to display: {str(e)}")
        finally:
            self.cleanup_generation()
    
    def handle_error(self, error_msg):
        self.insert_message(f"❌ Error: {error_msg}", "error")
        self.cleanup_generation()
    
    def cleanup_generation(self):
        self.is_generating = False
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.generate_btn.config(state="normal", text="🎨 Generate Image (FREE)")
    
    def insert_message(self, text, msg_type="system"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if msg_type == "warning":
            self.chat_box.insert(tk.END, f"[{timestamp}] ⚠️ ", "system")
            self.chat_box.insert(tk.END, f"{text}\n\n", "system")
        else:
            tag = msg_type if msg_type in ["user", "success", "error"] else "system"
            self.chat_box.insert(tk.END, f"[{timestamp}] ", tag)
            self.chat_box.insert(tk.END, f"{text}\n\n", tag)
        
        self.chat_box.see(tk.END)
    
    def clear_chat(self):
        self.chat_box.delete(1.0, tk.END)
        self.insert_message("Chat cleared! Ready for free image generation.", "system")
    
    def save_image(self):
        if self.current_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if file_path:
                self.current_image.save(file_path)
                self.insert_message(f"💾 Image saved to {os.path.basename(file_path)}", "success")
        else:
            self.insert_message("⚠️ No image to save. Generate an image first.", "error")

# ==========================
# RUN APPLICATION
# ==========================
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageGeneratorApp(root)
    
    app.insert_message("🎨 Welcome to Pollinations AI Image Generator!", "success")
    app.insert_message("✨ This API is 100% FREE and working!", "system")
    app.insert_message("💡 Try: 'a beautiful sunset over mountains'", "system")
    app.insert_message("⚡ Just type your prompt and click Generate!", "system")
    
    root.mainloop()