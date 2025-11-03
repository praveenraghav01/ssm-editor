# 🧩 ssm-editor

A lightweight CLI tool to fetch, edit, and update **AWS SSM Parameter Store** values directly from your favorite text editor (VS Code, Vim, etc).

---

## 🚀 Installation

You can install the package from [PyPI](https://pypi.org/project/ssm-editor/):

```bash
pip3 install ssm-editor
```

Alternatively, install directly from source:

```bash
git clone https://github.com/praveenraghav01/ssm-editor.git
cd ssm-editor
pip3 install -e .
```

---

## 🧠 Usage

To fetch and edit parameters under a specific path:

```bash
ssm-editor --path /dev/pimcore/ --editor code
```

or use `vi`:

```bash
ssm-editor --path /dev/pimcore/ --editor vi
```

The tool will:
1. Fetch all parameters under the given SSM path.
2. Write them to a temporary file as `key=value` pairs.
3. Open that file in your preferred editor.
4. Wait for you to make and save changes.
5. Display a summary of changes in a table.
6. Automatically update changed parameters in SSM.

---

## ⚙️ Requirements

- Python 3.8 or higher
- AWS credentials configured (via environment variables, `~/.aws/credentials`, or IAM role)
- Optional: VS Code CLI (`code`) or Vim

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to open issues or submit pull requests on [GitHub](https://github.com/praveenraghav01/ssm-editor).

---

## 🪪 License

This project is licensed under the [MIT License](LICENSE).  
Copyright (c) 2025 Praveen