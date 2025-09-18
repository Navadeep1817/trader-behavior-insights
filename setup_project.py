import os

# Define folder structure
folders = [
    "data",
    "notebooks",
    "src",
    "outputs",
    "outputs/figures",
    "outputs/models"
]

# Define placeholder files
files = {
    "requirements.txt": "",
    "README.md": "# Trader Behavior Insights\n\nProject setup.\n",
    "INSIGHTS.md": "# Insights Report\n\n(To be generated)\n",
    "src/download_data.py": "# Download data script\n",
    "src/prepare_data.py": "# Data preparation script\n",
    "src/eda.py": "# Exploratory Data Analysis script\n",
    "src/stats_and_model.py": "# Statistical tests and modeling script\n",
    "src/generate_report.py": "# Generate report script\n",
    "notebooks/trader_behavior_analysis.ipynb": ""  # Empty notebook
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Project folder structure created successfully!")
