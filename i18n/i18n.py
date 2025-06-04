# internationalization

_current_language = 'en'

translations = {
    'en': {
        #? Menu
        'menu.file': ' File ',
        'menu.new_project': 'New Project',
        'menu.save_project': 'Save Project',
        'menu.save_as': 'Save As',
        'menu.open_project': 'Open Project',
        'menu.export_to_excel': 'Export data to Excel',
        'menu.help': 'Help',
        'menu.settings': 'Settings',
        'menu.color_theme': 'Color Theme',
        'menu.language': 'Language',
        'menu.theme_light': 'Light',
        'menu.theme_dark': 'Dark',

        #? Tabs
        'tab.new_project': 'New Project',
        'tab.experiment_parameters': 'Experiment Parameters',
        'tab.data': 'Data',
        'tab.data_visualization': 'Data Visualization',

        #? Dialogs & messages
        'dialog.title': 'Save Project',
        'dialog.open_project': 'Open Project',
        'dialog.save_excel': 'Save Excel File',

        'info.title': 'Information',
        'warning.title': 'Warning',
        'error.title': 'Error',

        'msg.save_prompt': 'Do you want to save the current project before continuing?',
        'msg.new_project_ready': 'New project is ready to be created.',
        'msg.project_not_created': 'Project file has not been created. Go to "New Project" and create a project first.',
        'msg.project_saved': 'Project updated:',
        'msg.project_loaded': 'Project loaded from:',
        'msg.no_data_export': 'There is no data to export. Please process frames first.',
        'msg.excel_saved': 'Excel file saved:',
        'msg.excel_error': 'An error occurred while saving:',

        'error.theme': 'Failed to apply selected theme.',
        'error.error': 'Error',

        #? Help window
        'help.title': 'Dropsli Help',
        'help.tabs.about': 'About',
        'help.tabs.how_to_use': 'How to use',
        'help.tabs.faq': 'FAQ',
        'help.tabs.info': 'Information',
        'help.about_text': (
            "Welcome to Dropsli!\n\n"
            "Dropsli is a scientific tool for processing and analyzing "
            "high-speed video of drops oscillations on substrates."
        ),
        'help.how_to_use_text': (
            """1) Select the directory where the project folder will be created. This folder will store
all files related to the project.

2) Create the project itself. The project data is stored in a JSON file. The "Save Project" option in the File menu updates this JSON file. Later, you will be able to open a previously saved project using the "Open Project" option.

3) Select the folder containing the frames of your experiment. Note that the program will process all frames found in the specified folder.

4) Specify the image scale and frame rate in the "Experiment Parameters" tab. Define the region of interest (the area in which the drop will be located) and the line that marks the boundary of the substrate.

5) Go to the "Data" tab and process the frames. You can save the resulting data in XLSX format, as well as save all processed frames.

6) In the "Data Visualization" tab, you can plot time-dependent graphs of the droplet’s dynamic parameters."""
        ),
        'help.faq_text': (
            """Q: How do I create a new project?
A: Select "New Project" from the File menu. The "New Project" tab will be ready for creating a new project. You can also use Ctrl+N as a shortcut.

Q: How do I save a project?
A: When a project is created, a JSON file is generated to store all data. The "Save Project" option in the File menu updates this data. You can also use Ctrl+S as a shortcut.

Q: How do I open a previously saved project?
A: Select "Open Project" from the File menu and choose the JSON file corresponding to the project you want to open. You can also use Ctrl+O as a shortcut.

Q: How do I change the application language?
A: Select "Settings" from the File menu, then choose "Language". Select the desired option. You can also use Ctrl+L as a shortcut.

Q: How do I change the application's color theme?
A: Select "Settings" from the File menu, then choose "Color Theme". Select the desired option. You can also use Ctrl+T as a shortcut."""
        ),
        'help.info_text': (
            "The program was developed by Michael Slinkin.\n\n"
            "If you have any questions about using the program, "
            "or if you have any ideas for improving it, "
            "feel free to contact the developer by email:\n\n"
            "slinkin.misha2311@gmail.com"
        ),

        #? New Project Tab
        'Project Directory:': 'Project Directory:',
        'Create Project Directory': 'Create Project Directory',
        'Project Name:': 'Project Name:',
        'Create New Project': 'Create New Project',
        'Input folder:': 'Input folder:',
        'Select Input Folder': 'Select Input Folder',
        'Confirm and Next': 'Confirm and Next',
        'Choose directory to create new project': 'Choose directory to create new project',
        'Failed to create project folder': 'Failed to create project folder',
        'Project directory created': 'Project directory created',
        'Error': 'Error',
        'Dropsli Message': 'Dropsli Message',
        'Please create a project directory first.': 'Please create a project directory first.',
        'Save Project As': 'Save Project As',
        'Failed to save project file': 'Failed to save project file',
        'Project file created': 'Project file created',
        'Select the folder that contains the frames of the experiment.': 'Select the folder that contains the frames of the experiment.',
        'The program will process all frames in this folder.': 'The program will process all frames in this folder.',
        'Select input folder': 'Select input folder',
        'Failed to update project file': 'Failed to update project file',
        'Warning': 'Warning',
        'Please create project and select input folder first.': 'Please create project and select input folder first.',
        'Good! All files related to this project will be saved in the appropriate folder.': 'Good! All files related to this project will be saved in the appropriate folder.',
        'Now set up the experiment parameters.': 'Now set up the experiment parameters.',

        #? Experiment Parameters Tab
        "Experiment Parameters": "Experiment Parameters",
        "Scale (pixels per mm):": "Scale (pixels per mm):",
        "Frames per second (fps):": "Frames per second (fps):",
        "Confirm": "Confirm",
        "Edit": "Edit",
        "Image Tools": "Analysis Area Selection",
        "Define baseline": "Define baseline",
        "Define ROI": "Define ROI",
        "Select Image": "Select Image",
        "Confirm and Next": "Confirm and Next",
        "Good! Now everything is ready for data collection!": "Good! Now everything is ready for data collection!",
        "Please enter positive numeric values for Scale and FPS.": "Please enter positive numeric values for Scale and FPS.",
        "No image selected.": "No image selected.",
        "Both baseline and ROI must be drawn before confirming.": "Both baseline and ROI must be drawn before confirming.",
        "Input folder not set.": "Input folder not set.",
        "Select image": "Select image",
        "Failed to load image: {e}": "Failed to load image: {e}",
        "Error": "Error",
        "Warning": "Warning",

        #? Tab Data
        'Process': 'Process',
        'Processed': 'processed',
        'Ready': 'Ready',
        'Export Data to Excel': 'Export Data to Excel',
        'Save Processed Frames': 'Save Processed Frames',
        'Not ready': 'Not ready',
        'Please finish setting experiment parameters before processing.': 'Please finish setting experiment parameters before processing.',
        'Error': 'Error',
        'An error occurred during processing:': 'An error occurred during processing:',
        'Input folder or baseline not set.': 'Input folder or baseline not set.',
        'Could not read FPS and scale.': 'Could not read FPS and scale.',
        'Processing complete': 'Processing complete',
        'Processing completed. All {n} frames were processed.': 'Processing completed. All {n} frames were processed.',
        'Warning': 'Warning',
        'No processed frames found. Please process data first.': 'No processed frames found. Please process data first.',
        "No files": "No files",
        "There are no processed frames to save.": "There are no processed frames to save.",
        "Confirm Save": "Confirm Save",
        "Are you sure you want to save {count} processed frames to the project folder?": "Are you sure you want to save {count} processed frames to the project folder?",
        "Success": "Success",
        "All processed frames saved to:\n{dst}": "All processed frames saved to:\n{dst}",
        "Saving": "Saving",
        "Saving frames...": "Saving frames...",


        #? Tab Diagrams
        'Y axis:': 'Y axis:',
        'X axis:': 'X axis:',
        'Graph style:': 'Graph style:',
        'Plot': 'Plot',
        'Clear': 'Clear',
        'Export as PNG': 'Export as PNG',
        'No data': 'No data',
        "Please process data first on the 'Data' tab.": "Please process data first on the 'Data' tab.",
        'Invalid selection': 'Invalid selection',
        'Selected column not found in data.': 'Selected column not found in data.',
        'Empty plot': 'Empty plot',
        'No valid numeric data available to plot.': 'No valid numeric data available to plot.',
        'No figure': 'No figure',
        'Please plot the diagram first.': 'Please plot the diagram first.',
        'Save Diagram As': 'Save Diagram As',
        'PNG Image': 'PNG Image',
        'Success': 'Success',
        'Diagram saved as:': 'Diagram saved as:',
        'Failed to save diagram:': 'Failed to save diagram:',
        'Time [ms]': 'Time [ms]'


    },

    'ru': {
        #! Menu
        'menu.file': ' Файл ',
        'menu.new_project': 'Новый проект',
        'menu.save_project': 'Сохранить проект',
        'menu.save_as': 'Сохранить как',
        'menu.open_project': 'Открыть проект',
        'menu.export_to_excel': 'Экспорт данных в Excel',
        'menu.help': 'Помощь',
        'menu.settings': 'Настройки',
        'menu.color_theme': 'Цветовая тема',
        'menu.language': 'Язык',
        'menu.theme_light': 'Светлая',
        'menu.theme_dark': 'Тёмная',

        #! Tabs
        'tab.new_project': 'Новый проект',
        'tab.experiment_parameters': 'Параметры эксперимента',
        'tab.data': 'Данные',
        'tab.data_visualization': 'Визуализация данных',

        #! Dialogs & messages
        'dialog.title': 'Сохранение проекта',
        'dialog.open_project': 'Открыть проект',
        'dialog.save_excel': 'Сохранить Excel-файл',

        'info.title': 'Информация',
        'warning.title': 'Предупреждение',
        'error.title': 'Ошибка',

        'msg.save_prompt': 'Сохранить текущий проект перед продолжением?',
        'msg.new_project_ready': 'Новый проект готов к созданию.',
        'msg.project_not_created': 'Файл проекта не был создан. Перейдите во вкладку "Новый проект" и создайте его.',
        'msg.project_saved': 'Проект обновлён:',
        'msg.project_loaded': 'Проект загружен из:',
        'msg.no_data_export': 'Нет данных для экспорта. Сначала обработайте кадры.',
        'msg.excel_saved': 'Excel-файл сохранён:',
        'msg.excel_error': 'Ошибка при сохранении файла:',

        'error.theme': 'Не удалось применить выбранную тему.',
        'error.error': 'Ошибка',

        #! Help window
        'help.title': 'Справка Dropsli',
        'help.tabs.about': 'О программе',
        'help.tabs.how_to_use': 'Как пользоваться',
        'help.tabs.faq': 'Частые вопросы',
        'help.tabs.info': 'Информация',
        'help.about_text': (
            "Добро пожаловать в Dropsli!\n\n"
            "Dropsli — это научный инструмент для обработки и анализа "
            "высокоскоростной видеосъёмки осцилляции капель на подложках."
        ),
        'help.how_to_use_text': (
            """1) Выберите директорию, в которой создастся папка проекта. В ней будут храниться все файлы,
связанные с этим проектом.

2) Создайте сам проект. Сам проект, точнее его данные хранятся в файле формата json. Опция "Сохранить Проект" в меню Файл обновляет этот json файл. В дальнейшем Вы сможете открыть сохраненный ранее проект через опцию "Открыть Файл".

3) Выберете папку, содержащую кадры Вашего эксперимента. Обратите внимание, что программа обработает все кадры, содержащиеся в указанной папке.

4) Укажите масштаб изображения и частоту кадров на вкладке "Экспериментальные параметры". Задайте область интереса (область, внутри которой будет располагаться капля) и линию, определяющую границу подложки.

5) Перейдите на вкладку "Данные" и обработайте кадры. Вы можете сохранить полученные данные в формате xlsx, а так же сохранить все обработанные кадры.

6) На вкладке "Визуализация данных" Вы можете построить временные зависимости динамических параметров капли."""
        ),
        'help.faq_text': (
            """В: Как создать новый проект?
О: Выберите пункт "Новый проект" в меню Файл. Вкладка "Новый проект" будет готова к созданию нового проекта. Вы можете так же воспользоваться сочетанием клавиш Ctrl+N.

В: Как сохранить проект?
О: При создании проекта создается json файл, хранящий все данные. Пункт «Сохранить Проект» в меню Файл обновляет эти данные. Вы можете так же воспользоваться сочетанием клавиш Ctrl+S.

В: Как открыть ранее сохраненный проект?
О: Выберите пункт "Открыть Проект" в меню Файл и выберите JSON файл, относящийся к проекту, который Вы хотите открыть. Вы можете так же воспользоваться сочетанием клавиш Ctrl+O.

В: Как изменить язык приложения?
О: Выберите пункт "Настройки" в меню Файл, затем пункт "Язык". Выберите желаемый вариант. Вы можете так же воспользоваться сочетанием клавиш Ctrl+L.

В: Как изменить цветовую тему приложения?
О: Выберите пункт "Настройки" в меню Файл, затем пункт "Цветовая тема". Выберите желаемый вариант. Вы можете так же воспользоваться сочетанием клавиш Ctrl+T."""
        ),
        'help.info_text': (
            "Программу разработал Михаил Михайлович Слинкин.\n\n"
            "Если у вас остались вопросы по использованию программы или есть идеи по её улучшению, "
            "пишите напрямую разработчику по электронному адресу:\n\n"
            "slinkin.misha2311@gmail.com"
        ),

        #! New Project Tab
        'Project Directory:': 'Папка проекта:',
        'Create Project Directory': 'Создать папку проекта',
        'Project Name:': 'Имя проекта:',
        'Create New Project': 'Создать новый проект',
        'Input folder:': 'Папка с кадрами:',
        'Select Input Folder': 'Выбрать папку с кадрами',
        'Confirm and Next': 'Подтвердить и далее',
        'Choose directory to create new project': 'Выберите папку для создания нового проекта',
        'Failed to create project folder': 'Не удалось создать папку проекта',
        'Project directory created': 'Папка проекта создана',
        'Error': 'Ошибка',
        'Dropsli Message': 'Сообщение Dropsli',
        'Please create a project directory first.': 'Сначала создайте папку проекта.',
        'Save Project As': 'Сохранить проект как',
        'Failed to save project file': 'Не удалось сохранить файл проекта',
        'Project file created': 'Файл проекта создан',
        'Select the folder that contains the frames of the experiment.': 'Выберите папку, содержащую кадры эксперимента.',
        'The program will process all frames in this folder.': 'Программа обработает все изображения из этой папки.',
        'Select input folder': 'Выбрать папку с изображениями',
        'Failed to update project file': 'Не удалось обновить файл проекта',
        'Warning': 'Предупреждение',
        'Please create project and select input folder first.': 'Сначала создайте проект и выберите папку с изображениями.',
        'Good! All files related to this project will be saved in the appropriate folder.': 'Отлично! Все файлы проекта будут сохранены в указанной папке.',
        'Now set up the experiment parameters.': 'Теперь настройте параметры эксперимента.',

        #! Experiment Parameters Tab
        "Experiment Parameters": "Параметры эксперимента",
        "Scale (pixels per mm):": "Масштаб (пикселей на мм):",
        "Frames per second (fps):": "Кадров в секунду (fps):",
        "Confirm": "Подтвердить",
        "Edit": "Редактировать",
        "Image Tools": "Выделение области анализа",
        "Define baseline": "Указать линию подложки",
        "Define ROI": "Выделить область интереса",
        "Select Image": "Выбрать изображение",
        "Confirm and Next": "Подтвердить и далее",
        "Good! Now everything is ready for data collection!": "Отлично! Теперь всё готово для сбора данных!",
        "Please enter positive numeric values for Scale and FPS.": "Введите положительные числовые значения масштаба и fps.",
        "No image selected.": "Изображение не выбрано.",
        "Both baseline and ROI must be drawn before confirming.": "Необходимо указать и линию подложки, и область интереса перед подтверждением.",
        "Input folder not set.": "Не указана папка с изображениями.",
        "Select image": "Выберите изображение",
        "Failed to load image: {e}": "Не удалось загрузить изображение: {e}",
        "Error": "Ошибка",
        "Warning": "Предупреждение",


        #! Tab Data
        'Process': 'Обработать',
        'Processed': 'обработано',
        'Ready': 'Готово',
        'Export Data to Excel': 'Экспорт в Excel',
        'Save Processed Frames': 'Сохранить кадры',
        'Not ready': 'Не готово',
        'Please finish setting experiment parameters before processing.': 'Сначала завершите установку параметров эксперимента.',
        'Error': 'Ошибка',
        'An error occurred during processing:': 'Произошла ошибка при обработке:',
        'Input folder or baseline not set.': 'Не указана папка или базовая линия.',
        'Could not read FPS and scale.': 'Не удалось прочитать FPS и масштаб.',
        'Processing complete': 'Обработка завершена',
        'Processing completed. All {n} frames were processed.': 'Обработка завершена. Обработано кадров: {n}.',

        'Warning': 'Предупреждение',
        'No processed frames found. Please process data first.': 'Нет сохранённых кадров. Сначала выполните обработку.',
        'All processed frames saved to:\n{dst}': 'Все обработанные кадры сохранены в:\n{dst}',
        "No files": "Нет файлов",
        "There are no processed frames to save.": "Нет обработанных кадров для сохранения.",
        "Confirm Save": "Подтверждение сохранения",
        "Are you sure you want to save {count} processed frames to the project folder?": "Вы уверены, что хотите сохранить {count} обработанных кадров в папку проекта?",
        "Success": "Успешно",
        "All processed frames saved to:\n{dst}": "Все обработанные кадры сохранены в:\n{dst}",
        "Saving": "Сохранение",
        "Saving frames...": "Сохранение кадров...",


        #! Tab Diagrams
        'Y axis:': 'Ось Y:',
        'X axis:': 'Ось X:',
        'Graph style:': 'Стиль графика:',
        'Plot': 'Построить',
        'Clear': 'Очистить',
        'Export as PNG': 'Экспорт в PNG',
        'No data': 'Нет данных',
        "Please process data first on the 'Data' tab.": "Сначала обработайте данные на вкладке 'Данные'.",
        'Invalid selection': 'Неверный выбор',
        'Selected column not found in data.': 'Выбранный столбец не найден в данных.',
        'Empty plot': 'Пустой график',
        'No valid numeric data available to plot.': 'Нет числовых данных для построения графика.',
        'No figure': 'Нет изображения',
        'Please plot the diagram first.': 'Сначала постройте график.',
        'Save Diagram As': 'Сохранить график как',
        'PNG Image': 'Изображение PNG',
        'Success': 'Успешно',
        'Diagram saved as:': 'График сохранён как:',
        'Failed to save diagram:': 'Не удалось сохранить график:',
        'Time [ms]': 'Time [ms]'

    }
}


def set_language(lang_code: str):
    global _current_language
    if lang_code in translations:
        _current_language = lang_code
    else:
        raise ValueError(f"Unsupported language: {lang_code}")


def get_language() -> str:
    return _current_language


def t(key: str) -> str:
    translation = translations[_current_language].get(key)
    if translation is None:
        print(f"[i18n WARNING] Missing translation for key '{key}' in language '{_current_language}'")
        return key
    return translation
