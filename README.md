# Lightroom XMP Cluster Manager

Manage Lightroom XMP preset clusters with a simple graphical interface.

## Features
- Analyze preset files to detect existing, empty, and missing clusters.
- Rename existing cluster names across multiple files.
- Set a new cluster name for presets missing one.
- Multi‑language interface (German, English, Spanish).

## Installation
1. Ensure you have **Python 3** installed on your system.
2. Clone this repository or download the script.

```bash
pip install tk
```

## Usage
1. Run the application:
   ```bash
   python Lightroom_XMP_Cluster_Manger.py
   ```
2. Use the **Select Folder** button to choose the directory containing your XMP preset files.
3. Click **Analyze Presets** to scan for clusters.
4. Review the list of detected clusters along with empty and missing entries.
5. Use **Set Empty/Missing Clusters** to assign a new cluster name where none exists.
6. Select an existing cluster from the list and choose **Rename Existing Cluster** to change it across all files.

## Languages
Use the drop‑down at the top right of the window to switch between German (`de`), English (`en`), and Spanish (`es`).

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
