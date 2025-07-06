# VS Code Quick Start for LVGL VPet Demo

## 🚀 **Getting Started**

### **1. Open in VS Code**
```bash
cd "c:\Users\yuxun\Desktop\code\vpet\LVGL_vpet_Demo"
code .
```

### **2. Install Recommended Extensions**
VS Code will prompt you to install recommended extensions. Click "Install All" or:
- **C/C++** (Microsoft) - Essential for C++ development
- **C/C++ Extension Pack** (Microsoft) - Complete toolkit
- **Python** (Microsoft) - For sprite conversion script

### **3. Build and Run**
- **Quick Build**: `Ctrl+Shift+P` → "Tasks: Run Task" → "Build LVGL Demo"
- **Debug**: Press `F5` (builds with debug symbols and runs)
- **Clean**: `Ctrl+Shift+P` → "Tasks: Run Task" → "Clean"

## ⚙️ **Configuration**

### **Compiler Setup**
The project is pre-configured for **MSYS2/MinGW-w64**. If you use a different compiler:

1. **Edit `.vscode/c_cpp_properties.json`**:
   ```json
   "compilerPath": "C:/path/to/your/gcc.exe"
   ```

2. **Edit `.vscode/tasks.json`** and **`.vscode/launch.json`**:
   Update `miDebuggerPath` to your GDB path

### **Common Compiler Paths**
- **MSYS2**: `C:/msys64/mingw64/bin/gcc.exe`
- **TDM-GCC**: `C:/TDM-GCC-64/bin/gcc.exe`
- **Dev-C++**: `C:/Program Files (x86)/Dev-Cpp/MinGW64/bin/gcc.exe`

## 🔨 **Available Tasks**

| Task | Shortcut | Description |
|------|----------|-------------|
| **Build LVGL Demo** | `Ctrl+Shift+P` → Tasks | Release build |
| **Build Debug** | - | Debug build with symbols |
| **Clean** | - | Remove executables |
| **Convert Sprites** | - | Run Python script |
| **Run Demo** | - | Build and execute |

## 🐛 **Debugging**

### **Quick Debug**
1. Press `F5` - automatically builds debug version and starts debugger
2. Set breakpoints by clicking left margin in code
3. Use debug console for variable inspection

### **Debug Configurations**
- **Debug LVGL Demo**: Full debugging with symbols
- **Run LVGL Demo**: Release build execution

## 📁 **File Structure**
```
.vscode/
├── c_cpp_properties.json  # IntelliSense configuration
├── tasks.json            # Build tasks
├── launch.json           # Debug configurations
├── settings.json         # Project settings
└── extensions.json       # Recommended extensions
```

## 🔧 **Troubleshooting**

### **IntelliSense Issues**
- `Ctrl+Shift+P` → "C/C++: Reload IntelliSense Database"
- Check `c_cpp_properties.json` paths are correct

### **Build Errors**
- Verify compiler path in settings
- Check LVGL is extracted to `lvgl/` folder
- Ensure SDL2 development libraries are installed

### **Missing Features**
- Install missing extensions from recommendations
- Check Output panel for detailed error messages

## 💡 **Pro Tips**

1. **Integrated Terminal**: `Ctrl+`` (backtick) for quick commands
2. **Command Palette**: `Ctrl+Shift+P` for all VS Code features
3. **File Explorer**: `Ctrl+Shift+E` to navigate project
4. **Git Integration**: Built-in version control support
5. **Multi-cursor**: `Alt+Click` for multiple cursors

## 🎯 **Next Steps**

1. **Download LVGL**: Extract to `lvgl/` folder
2. **Test Build**: Run "Build LVGL Demo" task
3. **Start Coding**: Modify `lvgl_demo.cpp` for your features

Happy coding! 🚀
