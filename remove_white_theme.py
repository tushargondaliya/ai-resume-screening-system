import os

filepath = r"d:\New folder (7)\New folder (4)\ai-resume-screening-system\templates\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. .btn-secondary
content = content.replace("""        .btn-secondary {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 14px 28px;
            background: var(--white);
            color: var(--gray-800);
            border: 1px solid var(--gray-200);""", 
"""        .btn-secondary {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 14px 28px;
            background: var(--bg-card);
            color: var(--white);
            border: 1px solid var(--glass-border);""")

content = content.replace("""        .btn-secondary:hover {
            background: var(--gray-50);
            transform: translateY(-3px);
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.08);
            border-color: var(--gray-300);
        }""",
"""        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.05);
            transform: translateY(-3px);
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
            border-color: rgba(255, 255, 255, 0.2);
        }""")

# 2. .features container
content = content.replace("""        .features {
            padding: 100px 0;
            background: var(--white);
            position: relative;
        }""",
"""        .features {
            padding: 100px 0;
            background: rgba(255, 255, 255, 0.02);
            position: relative;
        }""")

# 3. .feature-icon
content = content.replace("""        .feature-icon {
            width: 60px;
            height: 60px;
            background: var(--white);""",
"""        .feature-icon {
            width: 60px;
            height: 60px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--glass-border);""")

# 4. .step-icon
content = content.replace("""        .step-icon {
            width: 80px;
            height: 80px;
            background: var(--white);""",
"""        .step-icon {
            width: 80px;
            height: 80px;
            background: var(--bg-card);""")

# 5. .cta section
content = content.replace("""        .cta {
            padding: 100px 0;
            text-align: center;
            background: var(--white);
        }""",
"""        .cta {
            padding: 100px 0;
            text-align: center;
            background: transparent;
        }""")

# 6. .btn-white
content = content.replace("""        .btn-white {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 16px 36px;
            background: var(--white);
            color: var(--primary);""",
"""        .btn-white {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 16px 36px;
            background: rgba(255, 255, 255, 0.1);
            color: var(--white);
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);""")

content = content.replace("""        .btn-white:hover {
            transform: translateY(-4px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
            background: var(--gray-50);
        }""",
"""        .btn-white:hover {
            transform: translateY(-4px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
            background: rgba(255, 255, 255, 0.2);
        }""")

# 7. footer
content = content.replace("""        footer {
            background: var(--white);
            padding: 40px 0;
            text-align: center;
            color: var(--gray-400);
            font-size: 14px;
            border-top: 1px solid var(--gray-200);
        }

        footer span {
            color: var(--gray-800);
            font-weight: 600;
        }""",
"""        footer {
            background: #050812;
            padding: 40px 0;
            text-align: center;
            color: var(--gray-400);
            font-size: 14px;
            border-top: 1px solid var(--glass-border);
        }

        footer span {
            color: var(--gray-200);
            font-weight: 600;
        }""")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Remaining white themes removed successfully!")
