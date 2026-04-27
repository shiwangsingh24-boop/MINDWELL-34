
import os

root_dir = r"c:\Users\Lenovo\.gemini\antigravity\scratch\mindwell"
output_file = r"c:\Users\Lenovo\.gemini\antigravity\scratch\mindwell_full_source_v20.txt"

files_to_include = [
    'app.py',
    'static/css/style.css',
    'static/js/main.js',
    'static/js/rppg.js',
    'templates/base.html',
    'templates/index.html',
    'templates/dashboard.html',
    'templates/assessment.html',
    'templates/result.html',
    'templates/rppg.html',
    'templates/chatbot.html',
    'templates/journal.html',
    'templates/resources.html',
    'templates/sos.html',
    'templates/community.html',
    'templates/counsellors.html'
]

with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.write("MINDWELL V20 COMPLETE SOURCE CODE\n")
    outfile.write("========================================\n\n")

    for rel_path in files_to_include:
        full_path = os.path.join(root_dir, rel_path)
        if os.path.exists(full_path):
            outfile.write(f"FILE: {rel_path}\n")
            outfile.write("========================================\n")
            try:
                with open(full_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
            except Exception as e:
                outfile.write(f"[Error reading file: {e}]")
            outfile.write("\n\n")
        else:
            outfile.write(f"FILE: {rel_path} (MISSING)\n\n")

print(f"Created {output_file}")
