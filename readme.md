# XpressGen

## Description
XpressGen is a powerful tool for generating customizable templates and streamlining project initialization. It provides modular, scalable, and easy-to-use components to accelerate development workflows.

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/achrafness/XpressGen.git
   cd XpressGen
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create symbolic links (optional)**:

   If you want to create a symbolic link to easily run `XpressGen` from anywhere, use the following command:

- in Linux , macOs
   ```bash
   ln -s $(pwd)/src/main.py /usr/local/bin/xpressgen
   chmod +x /usr/local/bin/xpressgen
   ```
-  in windaws
   ```bash 
   New-Item -ItemType SymbolicLink -Path "C:\usr\local\bin\xpressgen" -Target "$(Get-Location)\src\main.py"
   ```
   After this, you can run the application using:
   ```bash
   xpressgen
   ```

## Project Structure

```
src/
├── core/               # Core project initialization
├── modules/            # Business logic modules
├── templates/          # Template generators
└── utils/              # Utility functions
```

## Running the Application

```bash
python src/main.py
```

Or, if you have created a symbolic link:

```bash
xpressgen
```

## Contributing

1. **Fork the repository**.
2. **Create your feature branch**:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**:
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**.

<!-- ## License -->

## Contact

Achraf Abdelouadoud - achraf.nessighaoui13@gmail.com     
Project Link: [Link](https://github.com/achrafness/XpressGen.git)



