<div align="center">

# 🏗️ Teardown Save Editor

**A modern tool to customize your Teardown experience.**  
**Современный редактор сохранений для Teardown.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

[🇬🇧 English](#-english) | [🇷🇺 Русский](#-русский)

</div>

---

## 🇬🇧 English

The **Teardown Save Editor** allows you to modify your game progress, unlock hidden items, and upgrade your tools beyond the game's limits. Built with Python and CustomTkinter, it features a sleek "Industrial" dark design that matches the game's aesthetic.

### ✨ Features

*   **🔫 Weapon & Tool Customization:** Modify ammo, damage, range, power, and cooldowns.
*   **💎 Unlockables:** Instantly unlock all **Valuables**, **Characters**, and **Rank Rewards**.
*   **📂 Auto-Detection:** Automatically finds your `savegame.xml` in `%LOCALAPPDATA%`.
*   **🛡️ Safety First:** Automatically creates a backup of your save file before saving changes.
*   **⚙️ Reset Function:** Messed up your weapon stats? Reset any tool (or all of them) to default values with one click.
*   **🖥️ Modern GUI:** Custom "Industrial Voxel" theme with dark colors and yellow accents.

### 📥 Installation & Usage

#### Option 1: Download the App (Recommended for Gamers)
1.  Go to the **[Releases](../../releases)** page.
2.  Download the `TDSaveEditor.exe`.
3.  Run the program. It will automatically detect your save file.
4.  Edit your stats and click **Save Changes**.

#### Option 2: Run from Source (For Developers)
1.  Clone this repository.
2.  Install the required dependencies:
    ```bash
    pip install customtkinter
    ```
3.  Run the script:
    ```bash
    python TDSaveEditor.py
    ```

### 🚀 How to Use
1.  **File & Info Tab:** Check if your save file is loaded and Teardown is not opened.
2.  **Tools & Weapons:** Use sliders to change ammo count, damage, etc. Toggle "Enabled" to unlock early tools.
3.  **Valuables/Characters:** Click "Unlock All" to get 100% completion in these categories.
4.  **Save:** Click the big "Save Changes" button. Launch Teardown to see the effects!

---

## 🇷🇺 Русский

**Teardown Save Editor** — это инструмент для изменения прогресса в игре, разблокировки скрытых предметов и улучшения инструментов за пределы стандартных ограничений. Программа написана на Python с использованием CustomTkinter и имеет стильный темный дизайн.

### ✨ Возможности

*   **🔫 Настройка Оружия:** Изменяйте количество патронов, урон, дальность, силу и время действия.
*   **💎 Разблокировка:** Мгновенное открытие всех **Ценностей (Valuables)**, **Персонажей** и **Наград за ранг**.
*   **📂 Автопоиск:** Программа сама находит файл `savegame.xml` в папке `%LOCALAPPDATA%`.
*   **🛡️ Безопасность:** Автоматическое создание резервной копии перед каждым сохранением.
*   **⚙️ Сброс настроек:** Испортили характеристики оружия? Сбросьте настройки любого (или всех сразу) инструментов до заводских значений одной кнопкой.
*   **🖥️ Стильный GUI:** Тема "Industrial Voxel" в темных тонах с желтыми акцентами под стиль игры.

### 📥 Установка и Использование

#### Вариант 1: Скачать программу (Для игроков)
1.  Перейдите на вкладку **[Releases](../../releases)**.
2.  Скачайте файл `TDSaveEditor.exe`.
3.  Запустите программу. Она автоматически найдет ваше сохранение.
4.  Внесите изменения и нажмите **Save Changes**.

#### Вариант 2: Запуск из исходного кода (Для разработчиков)
1.  Склонируйте репозиторий.
2.  Установите необходимые библиотеки:
    ```bash
    pip install customtkinter
    ```
3.  Запустите скрипт:
    ```bash
    python TDSaveEditor.py
    ```

### 🚀 Как пользоваться
1.  **File & Info:** Убедитесь, что файл сохранения загружен, а Teardown закрыт.
2.  **Tools & Weapons:** Используйте ползунки для настройки патронов и урона. Включите переключатели "Enabled", чтобы получить инструменты раньше времени.
3.  **Valuables/Characters:** Нажмите "Unlock All", чтобы получить 100% завершение в этих категориях.
4.  **Save:** Нажмите кнопку "Save Changes". Запустите Teardown, чтобы увидеть изменения!

---

<div align="center">
  <p>Made with ❤️ for the Teardown Community</p>
  <p><i>Disclaimer: This tool is not affiliated with Tuxedo Labs. Use at your own risk.</i></p>
</div>
