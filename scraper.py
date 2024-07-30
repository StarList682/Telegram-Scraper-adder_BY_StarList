import tkinter as tk
from tkinter import messagebox, font
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import PeerFloodError
from telethon.tl.functions.channels import InviteToChannelRequest
import asyncio

user_ids = []

def start_scraping():
    api_id = entry_api_id.get()
    api_hash = entry_api_hash.get()
    phone_number = entry_phone_number.get()
    group_or_channel = entry_group_or_channel.get()
    
    if not (api_id and api_hash and phone_number and group_or_channel):
        messagebox.showerror("Error", "Please fill all fields.")
        return

    try:
        api_id = int(api_id)
    except ValueError:
        messagebox.showerror("Error", "API ID must be an integer.")
        return
    
    client = TelegramClient('session_name', api_id, api_hash)

    async def scrape():
        await client.start(phone_number)
        async for participant in client.iter_participants(group_or_channel):
            user_ids.append(participant.id)
            listbox_users.insert(tk.END, f"{participant.id} - {participant.username}")
        messagebox.showinfo("Success", "Scraping completed.")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape())

def start_adding():
    api_id = entry_api_id.get()
    api_hash = entry_api_hash.get()
    phone_number = entry_phone_number.get()
    target_group_or_channel = entry_target_group_or_channel.get()
    
    if not (api_id and api_hash and phone_number and target_group_or_channel):
        messagebox.showerror("Error", "Please fill all fields.")
        return

    try:
        api_id = int(api_id)
    except ValueError:
        messagebox.showerror("Error", "API ID must be an integer.")
        return
    
    client = TelegramClient('session_name', api_id, api_hash)

    async def add_users():
        await client.start(phone_number)
        for user_id in user_ids:
            try:
                await client(InviteToChannelRequest(target_group_or_channel, [user_id]))
                listbox_log.insert(tk.END, f"Successfully added {user_id}")
            except PeerFloodError:
                messagebox.showerror("Error", "Too many requests. Please try again later.")
                break
            except Exception as e:
                listbox_log.insert(tk.END, f"Failed to add {user_id}: {e}")

        messagebox.showinfo("Success", "Adding users completed.")
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(add_users())

root = tk.Tk()
root.title("Telegram Scraper and Adder")

root.attributes("-fullscreen", True)
root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))

root.configure(bg="#f5f5f5")

font_title = font.Font(family="Helvetica", size=14, weight="bold")
font_label = font.Font(family="Helvetica", size=12)
font_entry = font.Font(family="Helvetica", size=12)
font_button = font.Font(family="Helvetica", size=12, weight="bold")

frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

label_api_id = tk.Label(frame, text="API ID:", font=font_label, bg="#ffffff")
label_api_id.grid(row=0, column=0, sticky=tk.W, pady=5)
entry_api_id = tk.Entry(frame, font=font_entry, width=30)
entry_api_id.grid(row=0, column=1, pady=5)

label_api_hash = tk.Label(frame, text="API Hash:", font=font_label, bg="#ffffff")
label_api_hash.grid(row=1, column=0, sticky=tk.W, pady=5)
entry_api_hash = tk.Entry(frame, font=font_entry, width=30)
entry_api_hash.grid(row=1, column=1, pady=5)

label_phone_number = tk.Label(frame, text="Phone Number:", font=font_label, bg="#ffffff")
label_phone_number.grid(row=2, column=0, sticky=tk.W, pady=5)
entry_phone_number = tk.Entry(frame, font=font_entry, width=30)
entry_phone_number.grid(row=2, column=1, pady=5)

label_group_or_channel = tk.Label(frame, text="Group or Channel Username:", font=font_label, bg="#ffffff")
label_group_or_channel.grid(row=3, column=0, sticky=tk.W, pady=5)
entry_group_or_channel = tk.Entry(frame, font=font_entry, width=30)
entry_group_or_channel.grid(row=3, column=1, pady=5)

label_group_or_channel_hint = tk.Label(frame, text="Enter username with @ (e.g., @example_channel)", font=font_entry, fg="#888888", bg="#ffffff")
label_group_or_channel_hint.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)

button_scrape = tk.Button(frame, text="Start Scraping", font=font_button, bg="#4CAF50", fg="#ffffff", command=start_scraping)
button_scrape.grid(row=3, column=2, padx=10, pady=5)

label_target_group_or_channel = tk.Label(frame, text="Target Group or Channel Username:", font=font_label, bg="#ffffff")
label_target_group_or_channel.grid(row=5, column=0, sticky=tk.W, pady=5)
entry_target_group_or_channel = tk.Entry(frame, font=font_entry, width=30)
entry_target_group_or_channel.grid(row=5, column=1, pady=5)

button_add = tk.Button(frame, text="Start Adding", font=font_button, bg="#2196F3", fg="#ffffff", command=start_adding)
button_add.grid(row=5, column=2, padx=10, pady=5)

label_users = tk.Label(frame, text="Scraped Users:", font=font_label, bg="#ffffff")
label_users.grid(row=6, column=0, sticky=tk.W, pady=5)
listbox_users = tk.Listbox(frame, font=font_entry, width=50, height=10)
listbox_users.grid(row=7, column=0, columnspan=3, pady=10)

label_log = tk.Label(frame, text="Log:", font=font_label, bg="#ffffff")
label_log.grid(row=8, column=0, sticky=tk.W, pady=5)
listbox_log = tk.Listbox(frame, font=font_entry, width=50, height=10)
listbox_log.grid(row=9, column=0, columnspan=3, pady=10)

root.mainloop()
