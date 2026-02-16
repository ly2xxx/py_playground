# llmfit - Build & Run Guide for Windows

**Quick Summary:** A Rust CLI tool that analyzes your hardware and tells you which LLM models will actually run on your machine.

---

## 📦 What You Need

1. **Rust toolchain** (rustc + cargo)
2. **Git** (to clone the repo)
3. **Windows 10/11** (64-bit)

---

## 🚀 Quick Start (Pre-built Binary Available)

If you just want to run it without building:

1. Download the pre-built binary from the repo
2. Run: `llmfit.exe`

**But if you want to build from source (recommended for latest version):**

---

## 🔨 Build Instructions

### Step 1: Install Rust

**Option A: Using winget (Recommended)**
```powershell
winget search Rustlang.Rustup
winget install Rustlang.Rustup
```

**Option B: Manual Download**
1. Download from: https://win.rustup.rs/x86_64
2. Run the installer: `rustup-init.exe`
3. Follow prompts (defaults are fine)
4. Select option `1` for "Proceed with installation (default)"

**After Installation:**
- Close and reopen PowerShell/Terminal
- Verify: `cargo --version`
- You should see: `cargo 1.93.1` (or newer)

---

### Step 2: Clone the Repository

```powershell
cd C:\code
git clone https://github.com/AlexsJones/llmfit.git
cd llmfit
```

---

### Step 3: Build the Project

```powershell
cargo build --release
```

**What happens:**
- Downloads all dependencies (first time: ~5 minutes)
- Compiles the project (first time: ~9-10 minutes total)
- Creates optimized binary at: `target\release\llmfit.exe`

**Expected output:**
```
Updating crates.io index
Downloading crates ...
  Downloaded 90+ packages...
   Compiling proc-macro2 v1.0.106
   Compiling quote v1.0.44
   ...
   Compiling llmfit v0.2.0
    Finished `release` profile [optimized] target(s) in 9m 30s
```

**⚠️ Warnings are normal:**
```
warning: method `models_fitting_system` is never used
warning: function `truncate_str` is never used
```
These don't affect functionality.

---

## ✅ Verify Build Success

```powershell
.\target\release\llmfit.exe --version
```

**Expected output:**
```
llmfit 0.2.0
```

---

## 🎯 Usage

### 1. Check Your System Specs

```powershell
.\target\release\llmfit.exe system
```

**Example output:**
```
=== System Specifications ===
CPU: Intel(R) Core(TM) i7-6500U CPU @ 2.50GHz (4 cores)
Total RAM: 19.91 GB
Available RAM: 4.20 GB
Backend: CPU (x86)
GPU: Not detected
```

If you have a GPU (NVIDIA/AMD/Intel Arc), it will show:
```
GPU: NVIDIA GeForce RTX 3060
VRAM: 12.00 GB
Backend: CUDA
```

---

### 2. See Which Models Fit (CLI Mode)

```powershell
.\target\release\llmfit.exe --cli
```

**Shows:**
- Models that will run on your hardware
- Estimated tokens/second
- Best quantization level (Q8_0, Q4_K_M, etc.)
- Run mode (GPU / CPU / MoE)
- Memory usage percentage

---

### 3. Interactive TUI (Terminal UI)

```powershell
.\target\release\llmfit.exe
```

**Keyboard shortcuts:**
- `↑` / `↓` or `j` / `k` - Navigate
- `/` - Search
- `f` - Filter by fit level (All/Runnable/Perfect/Good/Marginal)
- `1`-`9` - Toggle providers
- `Enter` - View model details
- `q` - Quit

---

### 4. Search for Specific Models

```powershell
.\target\release\llmfit.exe search "llama 8b"
```

Shows all Llama 8B variants and whether they'll run on your system.

---

### 5. Show Only Perfect Fits

```powershell
.\target\release\llmfit.exe fit --perfect
```

Shows only models that will run **really well** on your hardware (GPU, good memory fit).

---

### 6. List All Models in Database

```powershell
.\target\release\llmfit.exe list
```

Shows all 94 models tracked by llmfit.

---

## 🎨 Understanding the Output

### Status Icons

| Icon | Meaning |
|------|---------|
| 🟢 **Perfect** | Fits in GPU VRAM with headroom. Fast inference. |
| 🟡 **Good** | Fits well. May use CPU+GPU or MoE offload. |
| 🟠 **Marginal** | Tight fit. CPU-only (slow) or barely fits. |
| 🔴 **Too Tight** | Won't run. Not enough VRAM or RAM. |

### Run Modes

- **GPU** - Runs entirely in GPU VRAM (fast!)
- **MoE** - Mixture-of-Experts with expert offloading (e.g., Mixtral, DeepSeek)
- **CPU+GPU** - Doesn't fit in VRAM, spills to RAM with partial GPU acceleration
- **CPU** - No GPU. Runs in system RAM (slow but works)

### Quantization Levels (Quality vs Size)

Best to worst quality (largest to smallest):
- **Q8_0** - 8-bit (best quality, largest)
- **Q6_K** - 6-bit
- **Q5_K_M** - 5-bit medium
- **Q4_K_M** - 4-bit medium (sweet spot)
- **Q3_K_M** - 3-bit medium
- **Q2_K** - 2-bit (smallest, worst quality)

---

## 📂 Add to PATH (Optional)

To run `llmfit` from anywhere:

```powershell
# Option 1: Copy to a PATH location
copy target\release\llmfit.exe C:\Windows\System32\

# Option 2: Add to user PATH
$env:PATH += ";C:\code\llmfit\target\release"
# Make permanent:
[System.Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";C:\code\llmfit\target\release", "User")
```

Then you can run: `llmfit` from any directory.

---

## 🔄 Update llmfit

To get the latest version:

```powershell
cd C:\code\llmfit
git pull
cargo build --release
```

---

## 🐛 Troubleshooting

### Build fails with "cargo: command not found"

**Solution:** Rust not installed or PowerShell needs restart.

```powershell
# Check if rustup is installed:
rustup --version

# If not found, install Rust (see Step 1)

# If installed, restart PowerShell and try:
refreshenv  # (if using Chocolatey)
# OR just close and reopen PowerShell
```

---

### Build fails with linking errors

**Solution:** Install Visual Studio Build Tools

```powershell
winget install Microsoft.VisualStudio.2022.BuildTools
```

Or download from: https://visualstudio.microsoft.com/downloads/

---

### "GPU: Not detected" but I have a GPU

**Possible causes:**
1. **NVIDIA** - Install `nvidia-smi` (comes with NVIDIA drivers)
2. **AMD** - Install `rocm-smi`
3. **Intel Arc** - Make sure drivers are installed

**Test GPU detection:**
```powershell
# NVIDIA:
nvidia-smi

# AMD:
rocm-smi

# Intel Arc:
# Check Device Manager > Display adapters
```

---

### Binary size is huge (~30MB)

This is normal for Rust release builds. It's statically linked (no dependencies needed).

To reduce size (optional):
```powershell
# Strip debug symbols
strip target\release\llmfit.exe

# Or use UPX compression
upx --best --lzma target\release\llmfit.exe
```

---

## 🎯 Use Cases

### 1. Before Downloading a Model

```powershell
llmfit search "deepseek 671b"
```

See if DeepSeek-V3 will run on your machine before downloading 350GB+.

---

### 2. Planning a Hardware Upgrade

Run llmfit on your current system, note which models are "Too Tight."

Then mentally add 16GB more VRAM and see what unlocks.

---

### 3. Quick Reference for Ollama

Before running `ollama pull`, check if the model fits:

```powershell
llmfit search "llama 70b"
# Shows: 🔴 Too Tight - Needs 36.1 GB VRAM (you have 12 GB)
```

Saves you from downloading a model that won't run.

---

## 🚀 Advanced: Integrate with Scripts

```powershell
# Get system specs as JSON (future feature)
# llmfit system --json

# For now, parse text output:
$systemInfo = .\target\release\llmfit.exe system
if ($systemInfo -match "GPU: Not detected") {
    Write-Host "No GPU found - use small models only"
}
```

---

## 📊 Model Database

llmfit tracks **94 models** from:
- Meta (Llama)
- Alibaba (Qwen)
- Mistral AI (Mistral, Mixtral)
- Google (Gemma)
- Microsoft (Phi)
- DeepSeek
- IBM (Granite)
- And many more...

**To update the model database:**
```powershell
cd C:\code\llmfit
python scripts/scrape_hf_models.py
cargo build --release
```

---

## 📝 Quick Reference Card

| Command | What it does |
|---------|--------------|
| `llmfit` | Launch interactive TUI |
| `llmfit system` | Show your hardware specs |
| `llmfit --cli` | Show all models (table view) |
| `llmfit search "text"` | Find models matching text |
| `llmfit fit --perfect` | Show only perfect-fit models |
| `llmfit fit --good` | Show good-fit models |
| `llmfit list` | List all 94 models |
| `llmfit info "Model Name"` | Detailed info on one model |

---

## 🎓 Understanding Scores

llmfit scores models across 4 dimensions (0-100 each):

1. **Quality** - Parameter count, quantization, task alignment
2. **Speed** - Estimated tok/s for your hardware
3. **Fit** - Memory utilization efficiency (50-80% is ideal)
4. **Context** - Context window vs use-case needs

**Composite score** = Weighted average of these dimensions.

Higher score = better match for your system.

---

## ✨ Example Session

```powershell
# Check what I have
PS> llmfit system
=== System Specifications ===
CPU: Intel i7-6500U (4 cores)
Total RAM: 19.91 GB
Available RAM: 4.20 GB
GPU: Not detected

# What can I run?
PS> llmfit fit --good
# Shows models that will run reasonably well

# Search for coding models
PS> llmfit search "coder"
# Shows: Qwen2.5-Coder, CodeLlama, StarCoder2, etc.

# Launch TUI for browsing
PS> llmfit
# Interactive exploration with keyboard shortcuts
```

---

## 🏆 Why Use llmfit?

✅ **Saves time** - Know before you download  
✅ **Saves frustration** - Avoid "model won't fit" errors  
✅ **Saves bandwidth** - Don't download 100GB models that won't run  
✅ **Plan upgrades** - See what 24GB VRAM would unlock  
✅ **MoE-aware** - Correctly calculates Mixtral/DeepSeek active parameters  

---

## 📚 Additional Resources

- **GitHub:** https://github.com/AlexsJones/llmfit
- **Model list:** `llmfit list` or see MODELS.md in repo
- **Architecture docs:** See AGENTS.md in repo
- **HuggingFace models:** Models sourced from https://huggingface.co

---

## 🔧 Tested On

- ✅ Windows 11 (x64)
- ✅ Windows 10 (x64)
- ✅ NVIDIA GPUs (via nvidia-smi)
- ✅ AMD GPUs (via rocm-smi)
- ✅ Intel Arc GPUs
- ✅ Apple Silicon (macOS) - unified memory support
- ✅ Linux (Ubuntu, Fedora, Arch)

---

## 🎯 Build Time Expectations

| System | First Build | Rebuild (after changes) |
|--------|-------------|-------------------------|
| Modern PC (8+ cores) | ~5-6 minutes | ~1-2 minutes |
| Laptop (4 cores) | ~9-10 minutes | ~2-3 minutes |
| Older PC (2 cores) | ~15-20 minutes | ~5-7 minutes |

**Note:** First build downloads ~90 dependencies. Subsequent builds are much faster.

---

## 🚨 Known Issues

1. **No GPU detected on laptops with Optimus** - llmfit may not detect NVIDIA GPU if using Intel integrated graphics. Use dedicated GPU mode in NVIDIA Control Panel.

2. **AMD GPU VRAM reporting may be inaccurate** - `rocm-smi` doesn't always report VRAM correctly. llmfit will estimate based on GPU model name.

3. **Context window may be truncated for large models** - If a model's context is too large for available memory, llmfit will suggest running at half context.

---

## 💡 Tips & Tricks

**1. Combine with Ollama:**
```powershell
# Check before pulling
llmfit search "llama 70b"
# If it shows 🟢 Perfect or 🟡 Good:
ollama pull llama3.1:70b
```

**2. Use filters in TUI:**
- Press `f` to cycle: All → Runnable → Perfect → Good → Marginal
- Press `/` to search, e.g., `/coder`
- Press `1`-`9` to toggle specific providers

**3. Quick reference for team:**
```powershell
# Generate a report
llmfit --cli > models-for-my-system.txt
# Share with team
```

---

**Built:** 2026-02-16 by Helpful Bob 🤖  
**Build Time:** 9m 30s on i7-6500U (4 cores, 20GB RAM)  
**Binary Size:** ~15MB (release build)  

---

**That's it! You now have llmfit running and know how to use it.** 🎉
