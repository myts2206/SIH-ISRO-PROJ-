import tkinter as tk
from tkinter import ttk, filedialog
from scapy.all import rdpcap, TCP, UDP
import os

def classify_protocols(packet):
    if UDP in packet and packet[UDP].dport == 5060:
        return "SIP"
    elif TCP in packet and packet[TCP].dport == 80:
        return "HTTP"
    elif TCP in packet and packet[TCP].dport == 443:
        return "HTTPS"
    elif TCP in packet and packet[TCP].dport == 21:
        return "FTP"
    elif TCP in packet and packet[TCP].dport == 22:
        return "SSH"
    elif TCP in packet and packet[TCP].dport == 25:
        return "SMTP"
    elif TCP in packet and packet[TCP].dport == 110:
        return "POP"
    elif UDP in packet and packet[UDP].dport == 161:
        return "SNMP"
    elif packet.haslayer("Raw") and b'\x47' in bytes(packet["Raw"]):
        return "MPEG-TS"
    elif packet.haslayer("Raw") and b'\x47' in bytes(packet["Raw"]) and b'MPE' in bytes(packet["Raw"]):
        return "MPE"
    elif packet.haslayer("Raw") and b'\x47' in bytes(packet["Raw"]) and b'ULE' in bytes(packet["Raw"]):
        return "ULE"
    elif TCP in packet and packet[TCP].dport == 115:
        return "SFTP"
    if packet[2:3] == b'\x47':
        tsc = (packet[3:4][0] & 0xC0) >> 6  # Extract TSC value
        if tsc == 0x3:
            return "Scrambled MPEG-TS"
        else:
            return "MPEG-TS"

def process_folder(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    results = []
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        try:
            capture = rdpcap(file_path)
            protocols = [classify_protocols(packet) for packet in capture]
            results.append((file_name, protocols))
        except Exception as e:
            results.append((file_name, [f"Error processing file: {e}"]))

    return results

def display_gui():
    def upload_folder():
        try:
            folder_path = filedialog.askdirectory()
            if folder_path:
                print(f"Selected folder: {folder_path}")
                information = process_folder(folder_path)
                update_text_widget(information)
            else:
                print("No folder selected.")
        except Exception as e:
            print(f"Error while uploading folder: {e}")

    def update_text_widget(info):
        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
        for file_name, protocols in info:
            text_widget.insert(tk.END, f"File: {file_name}\n")
            for i, protocol in enumerate(protocols, start=1):
                text_widget.insert(tk.END, f"  Packet {i}: Protocol={protocol}\n")
            text_widget.insert(tk.END, "\n")
        text_widget.config(state=tk.DISABLED)

    root = tk.Tk()
    root.title("Wireshark Folder Inspector")

    upload_button = ttk.Button(root, text="Upload Folder", command=upload_folder)
    upload_button.pack(padx=10, pady=10)

    text_widget = tk.Text(root, wrap=tk.WORD, height=20, width=80)
    text_widget.pack(padx=10, pady=10)

    scrollbar = ttk.Scrollbar(root, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget['width'] = 80
    text_widget.config(yscrollcommand=scrollbar.set)

    root.mainloop()

if __name__ == "__main__":
    display_gui()
