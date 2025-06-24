import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from pathlib import Path
import re

LANGUAGES = {
    "de": {
        "title": "XMP Cluster Manager",
        "select_folder": "Ordner auswählen",
        "analyze": "Presets analysieren",
        "set_missing": "Leere/fehlende Cluster setzen",
        "rename": "Bestehenden Cluster umbenennen",
        "missing_cluster_name": "Neuer Cluster-Name:",
        "rename_prompt": "Neuer Name für '{old}':",
        "no_selection": "Bitte einen bestehenden Cluster auswählen.",
        "only_existing": "Nur bestehende Cluster können umbenannt werden.",
        "folder_label": "XMP Preset Ordner:",
        "analyze_done": "Analyse abgeschlossen.",
        "set_done": "Leere und fehlende Cluster wurden gesetzt.",
        "rename_done": "Alle Cluster '{old}' wurden zu '{new}' umbenannt.",
        "folder_error": "Ordner existiert nicht.",
        "empty": "Leere Cluster",
        "missing": "Fehlende Cluster",
        "language": "Sprache wechseln"
    },
    "en": {
        "title": "XMP Cluster Manager",
        "select_folder": "Select Folder",
        "analyze": "Analyze Presets",
        "set_missing": "Set Empty/Missing Clusters",
        "rename": "Rename Existing Cluster",
        "missing_cluster_name": "New Cluster Name:",
        "rename_prompt": "New name for '{old}':",
        "no_selection": "Please select an existing cluster.",
        "only_existing": "Only existing clusters can be renamed.",
        "folder_label": "XMP Preset Folder:",
        "analyze_done": "Analysis complete.",
        "set_done": "Empty and missing clusters set.",
        "rename_done": "All clusters '{old}' renamed to '{new}'.",
        "folder_error": "Folder does not exist.",
        "empty": "Empty Clusters",
        "missing": "Missing Clusters",
        "language": "Change Language"
    },
    "es": {
        "title": "Administrador de Clusters XMP",
        "select_folder": "Seleccionar carpeta",
        "analyze": "Analizar Presets",
        "set_missing": "Establecer clusters vacíos/faltantes",
        "rename": "Renombrar cluster existente",
        "missing_cluster_name": "Nuevo nombre del cluster:",
        "rename_prompt": "Nuevo nombre para '{old}':",
        "no_selection": "Por favor selecciona un cluster existente.",
        "only_existing": "Solo se pueden renombrar clusters existentes.",
        "folder_label": "Carpeta de presets XMP:",
        "analyze_done": "Análisis completado.",
        "set_done": "Clusters vacíos y faltantes establecidos.",
        "rename_done": "Todos los clusters '{old}' renombrados a '{new}'.",
        "folder_error": "La carpeta no existe.",
        "empty": "Clusters Vacíos",
        "missing": "Clusters Faltantes",
        "language": "Cambiar idioma"
    }
}

class XMPClusterManager:
    def __init__(self, master):
        self.master = master
        self.language = "de"
        self.folder_path = tk.StringVar()
        self.clusters = {}
        self.empty_clusters = []
        self.missing_clusters = []

        self.setup_ui()

    def t(self, key):
        return LANGUAGES[self.language].get(key, key)

    def setup_ui(self):
        self.master.title(self.t("title"))

        top_frame = tk.Frame(self.master)
        top_frame.pack(pady=5)

        lang_menu = ttk.Combobox(top_frame, values=list(LANGUAGES.keys()), width=5)
        lang_menu.set(self.language)
        lang_menu.pack(side=tk.RIGHT)
        lang_menu.bind("<<ComboboxSelected>>", lambda e: self.change_language(lang_menu.get()))

        tk.Label(self.master, text=self.t("folder_label")).pack(pady=5)
        tk.Entry(self.master, textvariable=self.folder_path, width=60).pack()
        tk.Button(self.master, text=self.t("select_folder"), command=self.choose_folder).pack(pady=5)
        tk.Button(self.master, text=self.t("analyze"), command=self.analyze_presets).pack(pady=10)

        self.cluster_list = tk.Listbox(self.master, width=60, height=10)
        self.cluster_list.pack(pady=5)

        tk.Button(self.master, text=self.t("set_missing"), command=self.set_missing_clusters).pack(pady=5)
        tk.Button(self.master, text=self.t("rename"), command=self.rename_cluster).pack(pady=5)

    def change_language(self, lang):
        self.language = lang
        for widget in self.master.winfo_children():
            widget.destroy()
        self.setup_ui()

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def analyze_presets(self):
        self.clusters = {}
        self.empty_clusters = []
        self.missing_clusters = []
        self.cluster_list.delete(0, tk.END)

        preset_folder = Path(self.folder_path.get())
        if not preset_folder.exists():
            messagebox.showerror("Fehler", self.t("folder_error"))
            return

        cluster_pattern = re.compile(r'crs:Cluster="(.*?)"')

        for file_path in preset_folder.rglob("*.xmp"):
            try:
                content = file_path.read_text(encoding="utf-8")
            except:
                continue

            match = cluster_pattern.search(content)
            if match:
                value = match.group(1)
                if value == "":
                    self.empty_clusters.append((file_path, content))
                else:
                    self.clusters.setdefault(value, []).append((file_path, content))
            else:
                self.missing_clusters.append((file_path, content))

        for name in self.clusters:
            self.cluster_list.insert(tk.END, f"Cluster: {name} ({len(self.clusters[name])} Dateien)")

        self.cluster_list.insert(tk.END, f"{self.t('empty')}: {len(self.empty_clusters)}")
        self.cluster_list.insert(tk.END, f"{self.t('missing')}: {len(self.missing_clusters)}")

        messagebox.showinfo("Info", self.t("analyze_done"))

    def set_missing_clusters(self):
        name = simpledialog.askstring(self.t("set_missing"), self.t("missing_cluster_name"))
        if not name:
            return

        cluster_line = f'crs:Cluster="{name}"'

        for file_path, content in self.empty_clusters:
            new_content = re.sub(r'crs:Cluster=""', cluster_line, content)
            file_path.write_text(new_content, encoding="utf-8")

        for file_path, content in self.missing_clusters:
            insert_before = "</x:xmpmeta>"
            if insert_before in content:
                new_content = content.replace(insert_before, f'    {cluster_line}\n{insert_before}')
                file_path.write_text(new_content, encoding="utf-8")

        messagebox.showinfo("Info", self.t("set_done"))
        self.analyze_presets()

    def rename_cluster(self):
        selected = self.cluster_list.curselection()
        if not selected:
            messagebox.showwarning("Warnung", self.t("no_selection"))
            return

        selected_text = self.cluster_list.get(selected[0])
        if not selected_text.startswith("Cluster: "):
            messagebox.showwarning("Warnung", self.t("only_existing"))
            return

        old_name = selected_text[len("Cluster: "):].split(" (")[0]
        new_name = simpledialog.askstring(self.t("rename"), self.t("rename_prompt").format(old=old_name))
        if not new_name:
            return

        old_line_pattern = re.compile(rf'crs:Cluster="{re.escape(old_name)}"')
        new_line = f'crs:Cluster="{new_name}"'

        for file_path, content in self.clusters[old_name]:
            new_content = old_line_pattern.sub(new_line, content)
            file_path.write_text(new_content, encoding="utf-8")

        messagebox.showinfo("Info", self.t("rename_done").format(old=old_name, new=new_name))
        self.analyze_presets()

if __name__ == "__main__":
    root = tk.Tk()
    app = XMPClusterManager(root)
    root.mainloop()
