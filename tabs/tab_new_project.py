import os
import json
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from i18n.i18n import t  # ✅ импорт переводчика

BASE_FOLDER_NAME = "Dropsli_Project"

def generate_unique_folder_name(parent_dir, base_name):
    counter = 1
    while True:
        folder_name = f"{base_name}_{counter}"
        full_path = os.path.join(parent_dir, folder_name)
        if not os.path.exists(full_path):
            return full_path, counter
        counter += 1

class TabNewProject(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        
        self.project_folder = None
        self.project_json_path = None
        self.input_folder = None

        self.grid_columnconfigure(1, weight=1)
        self.create_widgets()
        self.reset()

    def create_widgets(self):
        # Project directory
        self.label_project = ttk.Label(self, text=t("Project Directory:"))
        self.entry_project = ttk.Entry(self, state='readonly')
        self.btn_create_dir = ttk.Button(self, text=t("Create Project Directory"), width=25, command=self.create_project_dir)

        self.label_project.grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.entry_project.grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        self.btn_create_dir.grid(row=0, column=2, padx=10, pady=5)

        # Project JSON file
        self.label_json = ttk.Label(self, text=t("Project Name:"))
        self.entry_json = ttk.Entry(self, state='readonly')
        self.btn_create_json = ttk.Button(self, text=t("Create New Project"), width=25, command=self.create_project_json)

        self.label_json.grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.entry_json.grid(row=1, column=1, sticky='ew', padx=10, pady=5)
        self.btn_create_json.grid(row=1, column=2, padx=10, pady=5)

        # Input folder
        self.label_input = ttk.Label(self, text=t("Input folder:"))
        self.entry_input = ttk.Entry(self, state='readonly')
        self.btn_input = ttk.Button(self, text=t("Select Input Folder"), width=25, command=self.select_input_folder)

        self.label_input.grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.entry_input.grid(row=2, column=1, sticky='ew', padx=10, pady=5)
        self.btn_input.grid(row=2, column=2, padx=10, pady=5)

        # Confirm button
        self.btn_confirm = ttk.Button(self, text=t("Confirm and Next"), width=25, command=self.confirm)
        self.btn_confirm.grid(row=3, column=2, sticky='e', padx=10, pady=20)

    def reset(self):
        self.project_folder = None
        self.project_json_path = None
        self.input_folder = None

        for entry in (self.entry_project, self.entry_json, self.entry_input):
            entry.config(state='normal')
            entry.delete(0, 'end')
            entry.config(state='readonly')

        self.btn_create_dir.config(state='normal')
        self.btn_create_json.config(state='disabled')
        self.btn_input.config(state='disabled')
        self.btn_confirm.config(state='disabled')

    def create_project_dir(self):
        self.reset()

        parent_dir = filedialog.askdirectory(title=t("Choose directory to create new project"))
        if not parent_dir:
            return

        new_folder, index = generate_unique_folder_name(parent_dir, BASE_FOLDER_NAME)
        try:
            os.makedirs(new_folder)
        except Exception as e:
            messagebox.showerror(t("Error"), f"{t('Failed to create project folder')}:\n{e}")
            return

        self.project_folder = new_folder
        self.project_index = index
        self._update_entry(self.entry_project, new_folder)
        self.btn_create_json.config(state='normal')

        messagebox.showinfo(title=t("Dropsli Message"), message=f"{t('Project directory created')}:\n{new_folder}")

    def create_project_json(self):
        if not self.project_folder:
            messagebox.showwarning(t("Warning"), t("Please create a project directory first."))
            return

        default_name = f"dropsli_project_{self.project_index}.json"
        file_path = filedialog.asksaveasfilename(
            title=t("Save Project As"),
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialdir=self.project_folder,
            initialfile=default_name
        )
        if not file_path:
            return

        self.project_json_path = file_path
        self._update_entry(self.entry_json, file_path)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'project_folder': self.project_folder,
                    'input_folder': None
                }, f, indent=4)
        except Exception as e:
            messagebox.showerror(t("Error"), f"{t('Failed to save project file')}:\n{e}")
            return

        self.btn_input.config(state='normal')
        messagebox.showinfo(title=t("Dropsli Message"), message=f"{t('Project file created')}:\n{file_path}")

    def select_input_folder(self):
        msg = (
            t("Select the folder that contains the frames of the experiment.") + "\n\n" +
            t("The program will process all frames in this folder.")
        )
        if not messagebox.askokcancel(title=t('Dropsli Message'), message=msg, icon='info'):
            return

        folder = filedialog.askdirectory(title=t("Select input folder"))
        if not folder:
            return

        self.input_folder = folder
        self._update_entry(self.entry_input, folder)

        if self.project_json_path:
            try:
                with open(self.project_json_path, 'r+', encoding='utf-8') as f:
                    data = json.load(f)
                    data['input_folder'] = folder
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
            except Exception as e:
                messagebox.showerror(t("Error"), f"{t('Failed to update project file')}:\n{e}")

        self.btn_confirm.config(state='normal')

    def confirm(self):
        if not self.project_folder or not self.input_folder:
            messagebox.showwarning(t("Warning"), t("Please create project and select input folder first."))
            return

        self.app.notebook.select(1)
        self.btn_create_dir.config(state='disabled')
        self.btn_create_json.config(state='disabled')
        self.btn_input.config(state='disabled')
        self.btn_confirm.config(state='disabled')

        messagebox.showinfo(title=t('Dropsli Message'), message=(
            t("Good! All files related to this project will be saved in the appropriate folder.") + "\n\n" +
            t("Now set up the experiment parameters.")
        ))

        self.app.tab_exp_param.input_folder = self.input_folder

    def _update_entry(self, entry, text):
        entry.config(state='normal')
        entry.delete(0, 'end')
        entry.insert(0, text)
        entry.config(state='readonly')

    def get_project_data(self):
        return {
            'project_folder': self.project_folder,
            'project_json_path': self.project_json_path,
            'input_folder': self.input_folder
        }

    def load_project_data(self, data):
        self.project_folder = data.get('project_folder')
        self.project_json_path = data.get('project_json_path')
        self.input_folder = data.get('input_folder')

        if self.project_folder:
            self._update_entry(self.entry_project, self.project_folder)
        if self.project_json_path:
            self._update_entry(self.entry_json, self.project_json_path)
        if self.input_folder:
            self._update_entry(self.entry_input, self.input_folder)

        self.btn_create_dir.config(state='disabled')
        self.btn_create_json.config(state='disabled')
        self.btn_input.config(state='disabled')
        self.btn_confirm.config(state='disabled')

    def update_language(self):
        self.label_project.config(text=t("Project Directory:"))
        self.btn_create_dir.config(text=t("Create Project Directory"))
        self.label_json.config(text=t("Project Name:"))
        self.btn_create_json.config(text=t("Create New Project"))
        self.label_input.config(text=t("Input folder:"))
        self.btn_input.config(text=t("Select Input Folder"))
        self.btn_confirm.config(text=t("Confirm and Next"))
