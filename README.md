## 🐍 Python version 3.11.7

## Folder Structure

CLG_PROJECT-MAIN/                     # Root directory of the project
├── .vscode/                         # VSCode-specific settings
│   └── settings.json                # Editor configuration (e.g., linting, formatting)
├── assets/                          # Store images, icons, or static files used in the project
├── myenv/                           # Python virtual environment (should be in .gitignore)
├── sign-to-text/                    # Module for converting sign language to text
│   ├── Data/                        # Contains input data or processed data for model
│   └── Model/                       # Stores trained models or model files
├── text-to-sign/                    # Module for converting text to sign language
│   └── Dataset/                     # Dataset folder for text-to-sign conversion
│       └── simplified_dataset/      # Simplified version of dataset (maybe preprocessed or curated)
├── ui/                              # User Interface code (frontend/backend if applicable)
├── .gitattributes                   # Git file to manage attributes like line endings
├── .gitignore                       # Specifies files and folders Git should ignore
├── combined.avi                     # Combined video file (possibly output or demo)
├── main.py                          # Main script to run the application
├── README.md                        # Project documentation and usage instructions
└── requirements.txt                 # Python dependencies for the project


## 📂 Dataset
   1. ASL dataset used for training and testing<br>
   2. Available on Google Drive 👉 [Download Dataset](https://drive.google.com/drive/folders/1JJAsT6jfaDrJfbAN0opFF_okpy-qUBs6?usp=drive_link)
 
## 🚀 Setup & Run
1. python -m venv myenv<br>
2. myenv\Scripts\activate<br>
3. pip install -r requirements.txt<br>
4. (Set path) Optional<br>
5. python .\main.py

## ▶️ To Run Later
1. myenv\Scripts\activate<br>
2. python .\main.py

## 📽️ Preview
* 🎬 Watch the [demo video](https://github.com/user-attachments/assets/731b240d-5061-43b7-b88b-c1c0719810d9) or try the live version to explore all features in action!<br>

