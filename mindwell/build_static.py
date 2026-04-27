import os
import re

template_dir = 'templates'
output_dir = 'static_web_prototype'
os.makedirs(output_dir, exist_ok=True)

views = ['index', 'dashboard', 'assessment', 'result', 'rppg', 'chatbot', 'journal', 'resources', 'sos', 'community', 'counsellors']

html_content = ""

# Read base.html
with open(os.path.join(template_dir, 'base.html'), 'r', encoding='utf-8') as f:
    base = f.read()

# Replace url_for in base.html
base = re.sub(r"\{\{ url_for\('static', filename='(.*?)'\) \}\}", r"\1", base)
# Replace other url_for with #hash links for SPA routing
base = re.sub(r"\{\{ url_for\('(.*?)'\) \}\}", r"#\1", base)
base = re.sub(r"\{\{ url_for\('(.*?)', type='(.*?)'\) \}\}", r"#\1-\2", base)

# Split base at {% block content %}
base_parts = base.split('{% block content %}{% endblock %}')
if len(base_parts) != 2:
    base_parts = base.split('{% block content %}\n        {% endblock %}')
if len(base_parts) != 2:
    base_parts = re.split(r'\{%\s*block content\s*%\}.*?\{%\s*endblock\s*%\}', base, flags=re.DOTALL)

head_part = base_parts[0]
tail_part = base_parts[1]

# Inject CSS for views
head_part = head_part.replace('</head>', '''
    <style>
        .view { display: none; }
        .view.active { display: block; }
    </style>
</head>''')

# Replace Jinja includes in base
head_part = re.sub(r"\{\{\s*(.*?)\s*\}\}", r"<span class='data-\1'></span>", head_part)
head_part = head_part.replace('data-user.name', 'data-user-name')

views_html = ""
for view in views:
    try:
        with open(os.path.join(template_dir, f'{view}.html'), 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Remove extends and block content
            content = re.sub(r"\{%\s*extends 'base.html'\s*%\}", '', content)
            content = re.sub(r"\{%\s*block content\s*%\}", '', content)
            content = re.sub(r"\{%\s*endblock\s*%\}", '', content)
            
            # Clean up jinja url_for
            content = re.sub(r"\{\{ url_for\('static', filename='(.*?)'\) \}\}", r"\1", content)
            content = re.sub(r"\{\{ url_for\('(.*?)'\) \}\}", r"#\1", content)
            content = re.sub(r"\{\{ url_for\('(.*?)', type='(.*?)'\) \}\}", r"#\1-\2", content)
            content = re.sub(r"\{\{ url_for\('(.*?)', id=(.*?)\) \}\}", r"#\1", content)
            
            # Replace jinja logic blocks (very naive approach for prototype)
            content = re.sub(r"\{%.*?%\}", "", content)
            
            # Replace jinja variables with spans
            content = re.sub(r"\{\{\s*user\.name\s*\}\}", "<span class='data-user-name'></span>", content)
            content = re.sub(r"\{\{\s*user\.streak\s*\}\}", "<span class='data-user-streak'></span>", content)
            content = re.sub(r"\{\{\s*user\.points\s*\}\}", "<span class='data-user-points'></span>", content)
            content = re.sub(r"\{\{\s*user\.tree_level\s*\}\}", "<span class='data-user-tree-level'></span>", content)
            content = re.sub(r"\{\{\s*user\.current_quest\.title\s*\}\}", "<span class='data-quest-title'></span>", content)
            content = re.sub(r"\{\{\s*user\.current_quest\.description\s*\}\}", "<span class='data-quest-desc'></span>", content)
            
            # Additional variables
            content = re.sub(r"\{\{\s*(.*?)\s*\}\}", r"<span class='data-\1'></span>", content)
            
            views_html += f'\n<div id="view-{view}" class="view">\n{content}\n</div>\n'
    except Exception as e:
        print(f"Error reading {view}: {e}")

# Clean up any leftover forms pointing to Flask endpoints
views_html = views_html.replace('action="#login"', 'id="form-login"')
views_html = views_html.replace('action="#journal"', 'id="form-journal"')

# Inject app.js into tail
tail_part = tail_part.replace('{% block scripts %}{% endblock %}', '<script src="js/app.js"></script>')
tail_part = re.sub(r"\{\{\s*(.*?)\s*\}\}", r"<span class='data-\1'></span>", tail_part)

final_html = head_part + views_html + tail_part

with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Generated static_web_prototype/index.html")
