import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

WATCHED_DIR = "/home/vboxuser/Documents"  # Folder to monitor
RECOVERY_DIR = os.path.join(WATCHED_DIR, "Recovery_Storage")  # Recovery storage

# Ensure Recovery Storage Exists
os.makedirs(RECOVERY_DIR, exist_ok=True)


def create_file():
    """Creates a custom file and places a backup in Recovery_Storage."""
    file_name = simpledialog.askstring("Input", "Enter file name (e.g., df.txt):")
    
    if not file_name:
        messagebox.showerror("Error", "No file name entered.")
        return
    
    file_path = os.path.join(WATCHED_DIR, file_name)
    backup_path = os.path.join(RECOVERY_DIR, file_name)  # Backup in Recovery Storage

    with open(file_path, "w") as f:
        f.write("This is a custom test file for recovery.")

    # Create a backup copy in Recovery_Storage
    shutil.copy(file_path, backup_path)

    messagebox.showinfo("Success", f"File created: {file_path}\nBackup saved: {backup_path}")


def delete_file():
    """Moves the selected file to Recovery_Storage instead of deleting it permanently."""
    file_path = filedialog.askopenfilename(initialdir=WATCHED_DIR, title="Select File to Delete",
                                           filetypes=[("All Files", ".")])

    if file_path:
        file_name = os.path.basename(file_path)
        backup_path = os.path.join(RECOVERY_DIR, file_name)

        if os.path.exists(file_path):
            shutil.move(file_path, backup_path)  # Move file to Recovery_Storage
            messagebox.showinfo("Deleted", f"File moved to recovery: {backup_path}")
        else:
            messagebox.showerror("Error", "File not found!")


def recover_file():
    """Restores a file from Recovery_Storage to the original location."""
    file_name = recovery_entry.get().strip()

    if not file_name:
        messagebox.showerror("Error", "Please enter a file name to recover.")
        return

    backup_path = os.path.join(RECOVERY_DIR, file_name)
    restore_path = os.path.join(WATCHED_DIR, file_name)

    if os.path.exists(backup_path):
        shutil.move(backup_path, restore_path)
        messagebox.showinfo("Recovered", f"File successfully restored: {restore_path}")
    else:
        messagebox.showerror("Error", f"File '{file_name}' not found in Recovery_Storage.")


# GUI Setup
root = tk.Tk()
root.title("File Recovery Tool")
root.geometry("400x300")

tk.Label(root, text="File Recovery System", font=("Arial", 14)).pack(pady=10)
tk.Button(root, text="Create Custom File", command=create_file).pack(pady=5)
tk.Button(root, text="Delete File", command=delete_file).pack(pady=5)

tk.Label(root, text="Enter filename to recover:").pack(pady=5)
recovery_entry = tk.Entry(root)
recovery_entry.pack(pady=5)

tk.Button(root, text="Recover File", command=recover_file).pack(pady=10)

root.mainloop()
