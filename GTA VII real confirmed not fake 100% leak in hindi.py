import tkinter as tk
from tkinter import filedialog, messagebox
import random
import subprocess
import os
from PIL import Image, ImageTk
import ctypes
import win32api
import win32gui
import win32con

class GameLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Game Launcher")

        self.game_list = []
        self.current_index = 0
        self.nes_emulator = None

        self.load_games()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.add_button = tk.Button(self.frame, text="Add Game", command=self.add_game)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.import_steam_button = tk.Button(self.frame, text="Import Steam Games", command=self.import_steam_games)
        self.import_steam_button.pack(side=tk.LEFT, padx=10)

        self.random_button = tk.Button(self.frame, text="Play Random Game", command=self.play_random_game)
        self.random_button.pack(side=tk.LEFT, padx=10)

        self.play_current_button = tk.Button(self.frame, text="Play Current Game", command=self.play_current_game)
        self.play_current_button.pack(side=tk.LEFT, padx=10)

        self.quit_button = tk.Button(self.frame, text="Quit", command=self.root.quit)
        self.quit_button.pack(side=tk.LEFT, padx=10)

        self.display_frame = tk.Frame(self.root)
        self.display_frame.pack(pady=20)

        self.icon_label = tk.Label(self.display_frame)
        self.icon_label.pack()

        self.name_label = tk.Label(self.display_frame, text="", font=("Arial", 16))
        self.name_label.pack()

        self.navigation_frame = tk.Frame(self.root)
        self.navigation_frame.pack()

        self.prev_button = tk.Button(self.navigation_frame, text="<<", command=self.prev_game)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.navigation_frame, text=">>", command=self.next_game)
        self.next_button.pack(side=tk.LEFT, padx=10)

        self.update_display()

    def load_games(self):
        if os.path.exists("SavedGames.txt"):
            with open("SavedGames.txt", "r") as file:
                self.game_list = [line.strip() for line in file.readlines()]
                self.nes_emulator = next((game for game in self.game_list if game.endswith(".exe")), None)

    def save_games(self):
        with open("SavedGames.txt", "w") as file:
            for game in self.game_list:
                file.write(game + "\n")

    def add_game(self):
        file_path = filedialog.askopenfilename(
            title="Select Game Executable or NES File", 
            filetypes=[("Executable Files", "*.exe"), ("NES Files", "*.nes;*.nez;*.unf;*.unif")]
        )
        if file_path:
            if file_path.endswith(".exe") and self.nes_emulator is None:
                self.nes_emulator = file_path
                messagebox.showinfo("NES Emulator", "NES Emulator added successfully.")
            self.game_list.append(file_path)
            self.save_games()
            self.update_display()
            print(f"Added: {file_path}")

    def play_random_game(self):
        if not self.game_list:
            print("No games added.")
            return

        game_to_play = random.choice(self.game_list)
        print(f"Playing: {game_to_play}")
        
        if game_to_play.endswith((".nes", ".nez", ".unf", ".unif")):
            self.launch_nes_game(game_to_play)
        else:
            subprocess.Popen(game_to_play)

    def play_current_game(self):
        if not self.game_list:
            print("No games added.")
            return

        game_to_play = self.game_list[self.current_index]
        print(f"Playing: {game_to_play}")
        
        if game_to_play.endswith((".nes", ".nez", ".unf", ".unif")):
            self.launch_nes_game(game_to_play)
        else:
            subprocess.Popen(game_to_play)

    def launch_nes_game(self, game_to_play):
        if self.nes_emulator is None:
            messagebox.showwarning("NES Emulator Required", "Please add an NES emulator.")
            self.add_game()
            if self.nes_emulator is None:
                print("NES emulator not added.")
                return
        subprocess.Popen([self.nes_emulator, game_to_play])

    def update_display(self):
        if not self.game_list:
            self.icon_label.config(image='')
            self.name_label.config(text="No games added.")
            return

        game_path = self.game_list[self.current_index]
        game_name = os.path.basename(game_path)
        self.name_label.config(text=game_name)

        icon_image = self.get_icon(game_path)
        if icon_image:
            self.icon_label.config(image=icon_image)
            self.icon_label.image = icon_image
        else:
            self.icon_label.config(image='')

    def get_icon(self, path):
        try:
            large, small = win32gui.ExtractIconEx(path, 0, 1, 1)
            hicon = large[0] if large else small[0]

            if hicon:
                hdc = win32gui.CreateCompatibleDC(0)
                hbm = win32gui.CreateCompatibleBitmap(win32gui.GetDC(0), 32, 32)
                h_old = win32gui.SelectObject(hdc, hbm)
                win32gui.DrawIconEx(hdc, 0, 0, hicon, 32, 32, 0, 0, win32con.DI_NORMAL)
                win32gui.SelectObject(hdc, h_old)
                win32gui.DeleteDC(hdc)

                bmpinfo = win32gui.GetObject(hbm)
                bmpstr = win32gui.GetBitmapBits(hbm, True)

                image = Image.frombuffer('RGBA', (bmpinfo.bmWidth, bmpinfo.bmHeight), bmpstr, 'raw', 'BGRA', 0, 1)
                image = image.resize((64, 64), Image.ANTIALIAS)
                return ImageTk.PhotoImage(image)
            else:
                return None
        except Exception as e:
            print(f"Error extracting icon: {e}")
            return None

    def prev_game(self):
        if not self.game_list:
            return
        self.current_index = (self.current_index - 1) % len(self.game_list)
        self.update_display()

    def next_game(self):
        if not self.game_list:
            return
        self.current_index = (self.current_index + 1) % len(self.game_list)
        self.update_display()

    def import_steam_games(self):
        steam_dir = "C:\\Program Files (x86)\\Steam\\steamapps\\common"
        if not os.path.exists(steam_dir):
            messagebox.showerror("Error", "Steam directory not found.")
            return
        
        for root, dirs, files in os.walk(steam_dir):
            for file in files:
                if file.endswith(".exe"):
                    exe_path = os.path.join(root, file)
                    self.game_list.append(exe_path)
                    print(f"Imported: {exe_path}")
        
        self.save_games()
        self.update_display()
        messagebox.showinfo("Success", "Steam games imported successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncher(root)
    root.mainloop()
