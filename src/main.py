import os
import sys
import shutil
from markdown_blocks import markdown_to_html_node, extract_title


def copy_directory(src, dest, src_root=None):
    if src_root is None:
        src_root = src

    if not os.path.isdir(dest):
        if os.path.exists(dest):
            shutil.rmtree(dest)
        os.mkdir(dest)
    
    if os.path.isfile(src):
        relative_path = os.path.relpath(src, src_root)
        dest_file = os.path.join(dest, relative_path)
        dest_dir = os.path.dirname(dest_file)
        if not os.path.exists(dest_dir):
            print(f"Creating directory: {dest_dir}")
            os.makedirs(dest_dir)
        print(f"Copying file: {src} to {dest_file}")
        shutil.copy(src, dest_file)
        return
    
    if os.path.isdir(src):
        for item in os.listdir(src):
            src_item = os.path.join(src, item)
            copy_directory(src_item, dest, src_root)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    try:
        with open(from_path, "r") as file:
            markdown_content = file.read()
    except FileNotFoundError:
        print(f"Error: The file {from_path} was not found.")
        return
    try:
        with open(template_path, "r") as file:
            template_content = file.read()
    except FileNotFoundError:
        print(f"Error: The file {template_path} was not found.")
        return
    node = markdown_to_html_node(markdown_content)
    html = node.to_html()
    title = extract_title(markdown_content)
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as file:
        file.write(full_html)
        print(f"Page written to {dest_path} successfully!")
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    entries = os.listdir(dir_path_content)
    for entry in entries:
        entry_path = os.path.join(dir_path_content, entry)
        relative_path = os.path.relpath(entry_path, dir_path_content)
        if os.path.isfile(entry_path):
            if entry_path.endswith(".md"):
                html_relative_path = relative_path.replace(".md", ".html")
                dest_file_path = os.path.join(dest_dir_path, html_relative_path)
                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                generate_page(entry_path, template_path, dest_file_path, basepath)
        else:
            new_dest_dir = os.path.join(dest_dir_path, relative_path)
            os.makedirs(new_dest_dir, exist_ok=True)
            generate_pages_recursive(entry_path, template_path, new_dest_dir, basepath)
                


def main():
    src = "static"
    dest = "docs"
    template_path = "template.html"
    dir_path_content = "content"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    copy_directory(src, dest)
    print("Static site copied successfully!")
    generate_pages_recursive(dir_path_content, template_path, dest, basepath)

if __name__ == "__main__":
    main()
