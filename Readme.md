# AraGorilla: Arabic Large Language Model Connected with APIs

![image](https://github.com/Shahad-Mohammed/AraGorilla/assets/74230739/691e81ba-51dc-4eeb-8fe9-717290661435)


https://github.com/Shahad-Mohammed/AraGorilla/assets/74230739/5f9939d7-96d5-421e-a537-f21eb61fa5ea

A minimal Markdown Editor desktop app built on top of Electron.

[![Gitter](https://badges.gitter.im/amitmerchant1990/electron-markdownify.svg)](https://gitter.im/amitmerchant1990/electron-markdownify)


AraGorilla is a fine-tuned LLaMA3-8B model specifically for Arabic instructions-API calls. Inspired by the Gorilla paper's methodology, we employed the self-instruct paradigm to generate {instruction, API} pairs. To adapt LLaMA for our task, we converted these pairs into a structured conversational format, resembling interactions between a user and an agent.




## Key Features

- **LivePreview** - Make changes, See changes: Instantly see what your Markdown documents look like in HTML as you create them.
- **Sync Scrolling**: While you type, LivePreview will automatically scroll to the current location you're editing.
- **GitHub Flavored Markdown**
- **Syntax highlighting**
- **KaTeX Support**
- **Dark/Light mode**
- **Toolbar for basic Markdown formatting**
- **Supports multiple cursors**
- **Save the Markdown preview as PDF**
- **Emoji support in preview** :tada:
- **App will keep alive in tray for quick usage**
- **Full screen mode**: Write distraction-free.
- **Cross-platform**: Windows, macOS, and Linux ready.

## How To Use

To clone and run this application, you'll need Git and Node.js (which comes with npm) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/amitmerchant1990/electron-markdownify

# Go into the repository
$ cd electron-markdownify

# Install dependencies
$ npm install

# Run the app
$ npm start
