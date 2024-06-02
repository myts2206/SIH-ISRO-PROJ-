import pyshark
import tkinter as tk
from tkinter import scrolledtext

def classify_packets(pcap_file):
    cap = pyshark.FileCapture(pcap_file, keep_packets=False)
    cap.tshark_path = '/home/srihithreddy/sihnet/tshark'  # replace with your tshark path
    results = []

    for pkt in cap:
        try:
            # Check if the packet is ISO/IEC 13818-1 MPEG2-TS
            if pkt.mp2t:
                pid = pkt.mp2t.pid
                transport_scrambling_control = pkt.mp2t.transport_scrambling_control

                if transport_scrambling_control == '0':
                    results.append(f"Packet {pid} is not scrambled.")
                elif transport_scrambling_control == '2' or transport_scrambling_control == '3':
                    results.append(f"Packet {pid} is scrambled.")
                else:
                    results.append(f"Packet {pid} has an unknown scrambling status.")
        except AttributeError:
            continue

    return '\n'.join(results)

def display_results():
    pcap_file = '/home/srihithreddy/sihnet/hi/hi.pcap'  # replace with your pcap file
    results = classify_packets(pcap_file)
    text_area.insert(tk.INSERT, results)

root = tk.Tk()
root.title("Packet Classification Results")

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10, font=("Times New Roman", 15))
text_area.grid(column=0, pady=10, padx=10)

# Move cap.tshark_path assignment here if you want to set it before creating FileCapture
# cap.tshark_path = '/home/srihithreddy/sihnet/tshark'  # replace with your tshark path

process_button = tk.Button(root, text="Process pcap file", command=display_results)
process_button.grid(column=0, pady=10, padx=10)

root.mainloop()
