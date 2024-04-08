import customtkinter as ctk

def update_label_text():
    # Update the text of the label
    my_label.configure(text="Text Updated!")

app = ctk.CTk()

# Create a CTkLabel without specifying initial text
my_label = ctk.CTkLabel(app, text="Initial Text")
my_label.pack(pady=10)

# Button to trigger text update on the label
update_button = ctk.CTkButton(app, text="Update Label Text", command=update_label_text)
update_button.pack(pady=10)

app.mainloop()