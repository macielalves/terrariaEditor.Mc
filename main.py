import tkinter as tk
import os
import subprocess

# Diretórios
android_players_dir = "/storage/emulated/0/Android/data/com.and.games505.TerrariaPaid/Players"
local_get_dir = "./players"
local_push_dir = "./updated_players"

class UpdatePlayerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Terraria Save Manager")
        self.geometry("400x250")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Gerenciar Saves Terraria (Android)").pack(pady=10)

        tk.Button(self, text="📥 Baixar Players do Android", command=self.get_players).pack(pady=5)
        tk.Button(self, text="📤 Enviar Saves Atualizados", command=self.update_players).pack(pady=5)

        self.status_label = tk.Label(self, text="", fg="blue")
        self.status_label.pack(pady=20)

    def get_players(self):
        os.makedirs(local_get_dir, exist_ok=True)
        command = f'adb pull "{android_players_dir}" "{local_get_dir}"'
        result = os.system(command)
        if result == 0:
            self.status_label.config(text="Players baixados com sucesso!", fg="green")
        else:
            self.status_label.config(text="Erro ao baixar os saves!", fg="red")

    def update_players(self):
        if not os.path.exists(local_push_dir):
            self.status_label.config(text="Pasta 'updated_players' não encontrada!", fg="red")
            return

        files = [f for f in os.listdir(local_push_dir) if os.path.isfile(os.path.join(local_push_dir, f))]
        if not files:
            self.status_label.config(text="Nenhum arquivo para enviar.", fg="orange")
            return

        success = 0
        for file in files:
            src = os.path.join(local_push_dir, file)
            command = f'adb push "{src}" "{android_players_dir}/"'
            result = os.system(command)
            if result == 0:
                success += 1

        if success == len(files):
            self.status_label.config(text=f"{success} arquivos enviados com sucesso!", fg="green")
        else:
            self.status_label.config(text=f"{success}/{len(files)} arquivos enviados. Alguns falharam.", fg="red")

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = UpdatePlayerApp()
    app.run()
