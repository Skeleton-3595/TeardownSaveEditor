# MADE BY SKELETON3595
import os
import shutil
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
import customtkinter as ctk
import logging
import webbrowser

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# --- DESIGN CONFIGURATION ---
THEME = {
    "bg_main": "#141414",       
    "bg_sidebar": "#2b2b2b",    
    "accent": "#FDB813",
    "accent_hover": "#e0a100",  
    "text": "#ffffff",
    "text_gray": "#aaaaaa",
    "danger": "#cf352e",        
    "danger_hover": "#ad2b25",
    "success": "#4caf50",
    "sidebar_width": 280
}

# --- DEFAULT VALUES ---
TOOL_DEFAULTS = {
    "sledge":       {"enabled": 1},
    "spraycan":     {"enabled": 1},
    "extinguisher": {"enabled": 1},
    "blowtorch":    {"enabled": 1, "ammo": 60},
    "shotgun":      {"enabled": 1, "ammo": 96, "range": 60, "damage": 5},
    "plank":        {"enabled": 1, "ammo": 64, "width": 5, "length": 64},
    "pipebomb":     {"enabled": 1, "ammo": 36, "damage": 4},
    "gun":          {"enabled": 1, "ammo": 36, "range": 100, "damage": 3},
    "bomb":         {"enabled": 1, "ammo": 36, "damage": 6},
    "wire":         {"enabled": 1, "ammo": 24, "stretch": 5},
    "rocket":       {"enabled": 1, "damage": 5, "ammo": 24},
    "leafblower":   {"enabled": 1, "power": 50},
    "booster":      {"enabled": 1, "ammo": 24, "power": 400, "time": 8},
    "turbo":        {"enabled": 1, "ammo": 24, "power": 400},
    "explosive":    {"enabled": 1, "damage": 8, "ammo": 16},
    "rifle":        {"enabled": 1, "ammo": 18},
    "steroid":      {"enabled": 1, "ammo": 4, "time": 6}
}

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class TeardownSaveHandler:
    def __init__(self):
        self.tree = None
        self.root = None
        self.filepath = None
        self.version = "Unknown"

    def find_default_path(self):
        local_app_data = os.getenv('LOCALAPPDATA')
        if local_app_data:
            possible_path = os.path.join(local_app_data, "Teardown", "savegame.xml")
            if os.path.exists(possible_path):
                logging.info(f"Found default save file: {possible_path}")
                return possible_path
        logging.info("Default save file not found.")
        return None

    def _sanitize_xml(self, content):
        content = re.sub(r'<(\d)', r'<_\1', content)
        content = re.sub(r'</(\d)', r'</_\1', content)
        return content

    def _desanitize_xml(self, content):
        content = re.sub(r'<_(\d)', r'<\1', content)
        content = re.sub(r'</_(\d)', r'</\1', content)
        return content

    def load_file(self, path):
        logging.info(f"Attempting to load file: {path}")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw_content = f.read()
            
            clean_content = self._sanitize_xml(raw_content)
            
            self.root = ET.fromstring(clean_content)
            self.tree = ET.ElementTree(self.root)
            self.filepath = path
            
            if 'version' in self.root.attrib:
                self.version = self.root.attrib['version']
            else:
                self.version = "Unknown"
            
            logging.info(f"File loaded successfully. Registry Version: {self.version}")
            return True
        except Exception as e:
            logging.error(f"Failed to load file: {e}")
            messagebox.showerror("Load Error", f"Failed to parse XML.\nError: {e}")
            return False

    def save_file(self, new_version=None):
        if not self.filepath or not self.root:
            return False, "No file loaded"
        
        try:
            logging.info("Starting save process...")
            if new_version:
                logging.info(f"Updating version to: {new_version}")
                self.root.set('version', new_version)

            backup_path = self.filepath + ".bak"
            shutil.copy2(self.filepath, backup_path)
            logging.info(f"Backup created at: {backup_path}")
            
            rough_string = ET.tostring(self.root, encoding='unicode')
            final_string = self._desanitize_xml(rough_string)
            
            with open(self.filepath, "w", encoding="utf-8") as f:
                f.write(final_string)
            
            logging.info(f"File saved successfully to: {self.filepath}")
            return True, backup_path
        except Exception as e:
            logging.error(f"Save failed: {e}")
            return False, str(e)

    def get_node_dict(self, parent_tag):
        if self.root is None: return {}
        savegame = self.root.find('savegame')
        if savegame is None: return {}
        
        section = savegame.find(parent_tag)
        if section is None: return {}

        data = {}
        for child in section:
            val = child.get('value')
            tag_name = child.tag
            if tag_name.startswith('_') and tag_name[1:].isdigit():
                tag_name = tag_name[1:]
            data[tag_name] = val
        return data

    def get_tools_data(self):
        if self.root is None: return {}
        savegame = self.root.find('savegame')
        if savegame is None: return {}
        tools_section = savegame.find('tool')
        if tools_section is None: return {}

        tools = {}
        for tool in tools_section:
            attributes = {}
            for param in tool:
                attributes[param.tag] = param.get('value')
            tools[tool.tag] = attributes
        return tools

    def update_value(self, section_tag, item_tag, attr_name, new_value):
        if self.root is None: return
        
        search_item_tag = item_tag
        if item_tag.isdigit():
            search_item_tag = "_" + item_tag

        savegame = self.root.find('savegame')
        section = savegame.find(section_tag)
        if section is None: return

        item = section.find(search_item_tag)
        
        if item is not None:
            if attr_name == "self": 
                logging.info(f"UPDATE {section_tag}: {item_tag} -> {new_value}")
                item.set('value', str(new_value))
            else:
                param = item.find(attr_name)
                if param is not None:
                    logging.info(f"UPDATE TOOL {item_tag}: {attr_name} -> {new_value}")
                    param.set('value', str(new_value))

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.handler = TeardownSaveHandler()
        
        self.title("Teardown Save Editor [BETA]")
        self.geometry("1200x800")
        self.configure(fg_color=THEME["bg_main"])
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()
        
        self.after(200, self.initial_load)

    def open_creator_site(self):
        webbrowser.open("https://skeleton3595.fun/")

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=THEME["sidebar_width"], corner_radius=0, fg_color=THEME["bg_sidebar"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False) 
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="TEARDOWN\nSAVE EDITOR", 
                                     font=("Impact", 32), text_color=THEME["accent"])
        self.logo_label.pack(pady=(40, 20), padx=20)
        
        self.credits_btn = ctk.CTkButton(self.sidebar, 
                                         text="Created by: Skeleton3595", 
                                         command=self.open_creator_site,
                                         fg_color="transparent",
                                         hover_color=THEME["bg_main"],
                                         text_color=THEME["text_gray"],
                                         font=("Arial", 12))
        self.credits_btn.pack(pady=(0, 30))

        self.nav_buttons = []
        self.create_nav_btn("📂  FILE & INFO", self.show_home)
        self.create_nav_btn("🔫  TOOLS & WEAPONS", self.show_tools)
        self.create_nav_btn("💎  VALUABLES", self.show_valuables)
        self.create_nav_btn("👤  CHARACTERS", self.show_chars)
        self.create_nav_btn("🏆  REWARDS", self.show_rewards)
        
        self.status_label = ctk.CTkLabel(self.sidebar, text="Waiting...", text_color=THEME["text_gray"], wraplength=THEME["sidebar_width"]-20)
        self.status_label.pack(side="bottom", pady=20, padx=10)

    def create_nav_btn(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, command=command,
                            corner_radius=0, height=50, fg_color="transparent", 
                            text_color=THEME["text"], anchor="w", font=("Arial", 12, "bold"),
                            hover_color=THEME["bg_main"])
        btn.pack(fill="x", padx=0, pady=2)
        self.nav_buttons.append(btn)

    def create_main_area(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

    def clear_main_area(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def check_loaded(self):
        if self.handler.root is None:
            self.clear_main_area()
            ctk.CTkLabel(self.main_frame, text="⚠ NO FILE LOADED", font=("Impact", 40), text_color=THEME["danger"]).pack(pady=50)
            ctk.CTkLabel(self.main_frame, text="Please go to 'FILE & INFO' and load savegame.xml", font=("Arial", 16)).pack()
            return False
        return True

    # --- PAGES ---

    def show_home(self):
        self.clear_main_area()
        logging.info("Switched to Home Tab")
        
        title = ctk.CTkLabel(self.main_frame, text="FILE SETTINGS", font=("Impact", 30), text_color=THEME["accent"])
        title.pack(anchor="w", pady=(0, 30))

        path_group = ctk.CTkFrame(self.main_frame, fg_color=THEME["bg_sidebar"], corner_radius=0)
        path_group.pack(fill="x", pady=10)
        
        ctk.CTkLabel(path_group, text="File Path:", font=("Arial", 12, "bold"), text_color=THEME["text_gray"]).pack(anchor="w", padx=15, pady=(10,0))
        
        input_frame = ctk.CTkFrame(path_group, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=10)

        self.path_entry = ctk.CTkEntry(input_frame, corner_radius=0, height=40, font=("Consolas", 12))
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        if self.handler.filepath:
            self.path_entry.insert(0, self.handler.filepath)

        ctk.CTkButton(input_frame, text="BROWSE", command=self.browse_file, width=100, height=40,
                      corner_radius=0, fg_color=THEME["accent"], text_color="black", hover_color=THEME["accent_hover"]).pack(side="right")

        ver_group = ctk.CTkFrame(self.main_frame, fg_color=THEME["bg_sidebar"], corner_radius=0)
        ver_group.pack(fill="x", pady=10)

        ctk.CTkLabel(ver_group, text="Registry Version:", font=("Arial", 12, "bold"), text_color=THEME["text_gray"]).pack(anchor="w", padx=15, pady=(10,0))
        
        ver_input_frame = ctk.CTkFrame(ver_group, fg_color="transparent")
        ver_input_frame.pack(fill="x", padx=10, pady=10)
        
        self.ver_entry = ctk.CTkEntry(ver_input_frame, width=150, height=40, corner_radius=0, font=("Consolas", 14))
        self.ver_entry.pack(side="left")
        if self.handler.version:
            self.ver_entry.insert(0, self.handler.version)
            
        ctk.CTkLabel(ver_input_frame, text="* Only change this if you know what you are doing", text_color=THEME["text_gray"]).pack(side="left", padx=20)

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", pady=20)

        ctk.CTkButton(btn_frame, text="💾 SAVE CHANGES", command=self.save_all, 
                      height=60, corner_radius=0, font=("Impact", 20),
                      fg_color=THEME["accent"], text_color="black", hover_color=THEME["accent_hover"]).pack(fill="x")

    def show_tools(self):
        if not self.check_loaded(): return
        self.clear_main_area()
        logging.info("Switched to Tools Tab")
        
        head = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        head.pack(fill="x", pady=(0,20))
        ctk.CTkLabel(head, text="TOOLS & WEAPONS", font=("Impact", 30), text_color=THEME["accent"]).pack(side="left")

        ctk.CTkButton(head, text="RESET ALL TO DEFAULTS", command=self.reset_all_tools,
                      fg_color=THEME["danger"], hover_color=THEME["danger_hover"], 
                      text_color="white", corner_radius=0, font=("Arial", 12, "bold")).pack(side="right")

        scroll = ctk.CTkScrollableFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        tools_data = self.handler.get_tools_data()
        
        for tool_name, params in tools_data.items():
            card = ctk.CTkFrame(scroll, fg_color=THEME["bg_sidebar"], corner_radius=0)
            card.pack(fill="x", pady=5, padx=5)
            
            top = ctk.CTkFrame(card, fg_color="#333", corner_radius=0, height=40)
            top.pack(fill="x")
            
            ctk.CTkLabel(top, text=tool_name, font=("Consolas", 14, "bold"), text_color="white").pack(side="left", padx=10)
            
            if tool_name in TOOL_DEFAULTS:
                ctk.CTkButton(top, text="RESET DEFAULT", width=100, height=24, corner_radius=0,
                              fg_color="#555", hover_color="#666", font=("Arial", 10),
                              command=lambda t=tool_name: self.reset_tool_to_default(t)).pack(side="right", padx=10, pady=5)

            if 'enabled' in params:
                is_on = int(params['enabled']) == 1
                sw = ctk.CTkSwitch(top, text="ENABLED", progress_color=THEME["accent"], corner_radius=0, text_color="white", font=("Arial", 10, "bold"))
                if is_on: sw.select()
                sw.configure(command=lambda t=tool_name, v=sw: self.handler.update_value('tool', t, 'enabled', v.get()))
                sw.pack(side="right", padx=10, pady=5)

            sliders_frame = ctk.CTkFrame(card, fg_color="transparent")
            sliders_frame.pack(fill="x", padx=10, pady=10)
            
            grid_row = 0
            for key in ['ammo', 'damage', 'range', 'power', 'time', 'stretch', 'length', 'width']:
                if key in params:
                    val = int(params[key])
                    max_val = 2000 if key == 'ammo' else (500 if key in ['damage', 'range', 'power'] else 100)
                    
                    lbl_text = f"{key}: {val}"
                    lbl = ctk.CTkLabel(sliders_frame, text=lbl_text, width=120, anchor="w", font=("Consolas", 12))
                    lbl.grid(row=grid_row, column=0, padx=5, pady=2)
                    
                    slider = ctk.CTkSlider(sliders_frame, from_=0, to=max_val, number_of_steps=max_val, 
                                           progress_color=THEME["accent"], button_color="white", button_hover_color=THEME["accent"])
                    slider.set(val)
                    slider.grid(row=grid_row, column=1, sticky="ew", padx=10, pady=2)
                    
                    slider.configure(command=lambda v, t=tool_name, k=key, l=lbl: self.on_slider_change(t, k, v, l))
                    grid_row += 1
            
            sliders_frame.grid_columnconfigure(1, weight=1)

    def show_valuables(self):
        if not self.check_loaded(): return
        self.clear_main_area()
        logging.info("Switched to Valuables Tab")
        
        head = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        head.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(head, text="VALUABLES", font=("Impact", 30), text_color=THEME["accent"]).pack(side="left")
        
        ctk.CTkButton(head, text="UNLOCK ALL", command=lambda: self.batch_unlock('valuable', self.show_valuables),
                      fg_color=THEME["accent"], text_color="black", corner_radius=0, font=("Arial", 12, "bold")).pack(side="right")

        scroll = ctk.CTkScrollableFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        vals = self.handler.get_node_dict('valuable')
        
        cols = 3
        frame_grid = ctk.CTkFrame(scroll, fg_color="transparent")
        frame_grid.pack(fill="both")

        for i, (item, val) in enumerate(vals.items()):
            is_checked = int(val) == 1
            cb = ctk.CTkCheckBox(frame_grid, text=item, corner_radius=0, font=("Consolas", 12),
                                 fg_color=THEME["accent"], hover_color=THEME["accent_hover"], checkmark_color="black")
            if is_checked: cb.select()
            cb.configure(command=lambda x=item, c=cb: self.handler.update_value('valuable', x, 'self', c.get()))
            cb.grid(row=i//cols, column=i%cols, sticky="w", padx=10, pady=5)

    def show_chars(self):
        if not self.check_loaded(): return
        self.clear_main_area()
        logging.info("Switched to Characters Tab")
        
        head = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        head.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(head, text="CHARACTERS", font=("Impact", 30), text_color=THEME["accent"]).pack(side="left")
        
        ctk.CTkButton(head, text="UNLOCK ALL", command=lambda: self.batch_unlock('characters', self.show_chars),
                      fg_color=THEME["accent"], text_color="black", corner_radius=0, font=("Arial", 12, "bold")).pack(side="right")

        scroll = ctk.CTkScrollableFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        chars = self.handler.get_node_dict('characters')
        for item, val in chars.items():
            row = ctk.CTkFrame(scroll, fg_color=THEME["bg_sidebar"], corner_radius=0)
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=item, font=("Consolas", 14)).pack(side="left", padx=15, pady=10)
            
            sw = ctk.CTkSwitch(row, text="Unlocked", progress_color=THEME["accent"], corner_radius=0)
            if int(val) == 1: sw.select()
            sw.configure(command=lambda x=item, s=sw: self.handler.update_value('characters', x, 'self', s.get()))
            sw.pack(side="right", padx=15)

    def show_rewards(self):
        if not self.check_loaded(): return
        self.clear_main_area()
        logging.info("Switched to Rewards Tab")
        
        head = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        head.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(head, text="REWARDS", font=("Impact", 30), text_color=THEME["accent"]).pack(side="left")
        
        ctk.CTkButton(head, text="UNLOCK ALL", command=lambda: self.batch_unlock('reward', self.show_rewards),
                      fg_color=THEME["accent"], text_color="black", corner_radius=0, font=("Arial", 12, "bold")).pack(side="right")

        scroll = ctk.CTkScrollableFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        rewards = self.handler.get_node_dict('reward')
        
        cols = 4
        frame_grid = ctk.CTkFrame(scroll, fg_color="transparent")
        frame_grid.pack(fill="both")

        for i, (item, val) in enumerate(rewards.items()):
            is_checked = int(val) == 1
            cb = ctk.CTkCheckBox(frame_grid, text=f"Rank {item}", corner_radius=0, 
                                 fg_color=THEME["accent"], hover_color=THEME["accent_hover"], checkmark_color="black")
            if is_checked: cb.select()
            cb.configure(command=lambda x=item, c=cb: self.handler.update_value('reward', x, 'self', c.get()))
            cb.grid(row=i//cols, column=i%cols, sticky="w", padx=10, pady=5)


    # --- LOGIC ---

    def initial_load(self):
        path = self.handler.find_default_path()
        if path:
            self.status_label.configure(text=f"Auto: {os.path.basename(path)}")
            if self.handler.load_file(path):
                self.show_home()
            else:
                self.status_label.configure(text="Load Error")
        else:
            self.status_label.configure(text="File not found automatically")
            self.show_home()

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")])
        if filename:
            if self.handler.load_file(filename):
                self.path_entry.delete(0, 'end')
                self.path_entry.insert(0, filename)
                self.ver_entry.delete(0, 'end')
                self.ver_entry.insert(0, self.handler.version)
                self.status_label.configure(text=f"Loaded: {os.path.basename(filename)}")
                messagebox.showinfo("Success", "Savegame loaded successfully!")
            else:
                self.status_label.configure(text="Load Error")

    def on_slider_change(self, tool, key, value, label):
        val = int(value)
        label.configure(text=f"{key}: {val}")
        self.handler.update_value('tool', tool, key, val)

    def reset_tool_to_default(self, tool_name):
        logging.info(f"Resetting {tool_name} to defaults")
        if tool_name in TOOL_DEFAULTS:
            defaults = TOOL_DEFAULTS[tool_name]
            for key, val in defaults.items():
                self.handler.update_value('tool', tool_name, key, val)
            self.show_tools()
        else:
            messagebox.showwarning("Unknown Tool", f"No default values known for '{tool_name}'")

    def reset_all_tools(self):
        if not messagebox.askyesno("Confirm Reset", "Are you sure you want to reset ALL tools to default values?"):
            return

        logging.warning("RESETTING ALL TOOLS TO DEFAULTS")
        for tool_name, defaults in TOOL_DEFAULTS.items():
            for key, val in defaults.items():
                self.handler.update_value('tool', tool_name, key, val)
        
        self.show_tools()
        messagebox.showinfo("Reset Complete", "All tools have been reset to defaults.")

    def batch_unlock(self, section, refresh_method):
        logging.info(f"Batch unlock triggered for: {section}")
        items = self.handler.get_node_dict(section)
        for item in items:
            self.handler.update_value(section, item, 'self', 1)
        refresh_method()
        messagebox.showinfo("Done", f"All items in {section} unlocked.")

    def save_all(self):
        if not self.handler.root:
            messagebox.showwarning("Warning", "No file loaded.")
            return

        new_ver = self.ver_entry.get()
        success, info = self.handler.save_file(new_ver)
        
        if success:
            messagebox.showinfo("Saved", f"Changes saved successfully!\nBackup: {info}")
        else:
            messagebox.showerror("Save Error", info)

def print_socials():
    print("\n" + "="*70)
    print("   TEARDOWN SAVE EDITOR")
    print("   Created by: Skeleton3595")
    print("   ----------------------------------------")
    print("   🌐 Website:  https://skeleton3595.fun")
    print("   ✈️  Telegram: https://t.me/skeleton3595")
    print("   🤖 Discord:  https://discordapp.com/users/911562356109242378")
    print("   🐙 GitHub:   https://github.com/Skeleton-3595")
    print("   📺 YouTube:  https://www.youtube.com/@Skeleton3595")
    print("="*70 + "\n")

def print_gameversion_warning():
    print("="*120)
    print("GAME VERSION | The program only works with version 2.0.0 or later. If you have an older version, update the game.")
    print("="*120 + "\n")

if __name__ == "__main__":
    print_socials()
    print_gameversion_warning()
    app = App()

    app.mainloop()
