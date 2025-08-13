import customtkinter as ctk
import psutil

def list_clients(port):
    connections = psutil.net_connections(kind='inet')
    clients = set()
    for conn in connections:
        if conn.status == 'ESTABLISHED' and conn.laddr.port == port:
            if conn.raddr:
                clients.add(conn.raddr.ip)
    return clients

def get_clients():
    try:
        port = int(entry_port.get())
        clients = list_clients(port)

        buffer = f"[INFO] Checking port {port}\n"
        buffer += f"Total client: {len(clients)}\n\n"
        for ip in clients:
            buffer += f"{ip}\n"

        output_textbox.configure(state="normal")
        output_textbox.delete(0.0, 'end')
        output_textbox.insert('end', buffer)
        output_textbox.configure(state="disabled")

    except Exception as e:
        output_textbox.configure(state="normal")
        output_textbox.insert('end', f"[ERROR] {str(e)}\n")
        output_textbox.configure(state="disabled")

def clear_output():
    output_textbox.configure(state="normal")
    output_textbox.delete(0.0, 'end')
    output_textbox.insert('end', "[INFO] Output dibersihkan.\n")
    output_textbox.configure(state="disabled")

# UI Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Pratamalabs Port Monitoring")
app.geometry("520x500")

entry_port = ctk.CTkEntry(app, placeholder_text="Port", width=120)
entry_port.pack(pady=10)
entry_port.insert(0, "30120")

frame_btn = ctk.CTkFrame(app)
frame_btn.pack(pady=5)

button_get = ctk.CTkButton(frame_btn, text="Get", command=get_clients)
button_get.pack(side='left', padx=5)

button_clear = ctk.CTkButton(frame_btn, text="Clear", command=clear_output)
button_clear.pack(side='left', padx=5)

output_textbox = ctk.CTkTextbox(app, height=420, width=480)
output_textbox.pack(padx=10, pady=10)
output_textbox.configure(state="disabled")

def on_closing():
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)

app.mainloop()
