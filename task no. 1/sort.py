import os
import shutil
import sys
import time
import logging
import concurrent.futures

IMAGE_EXTENSIONS = {'JPEG', 'PNG', 'JPG', 'SVG'}
VIDEO_EXTENSIONS = {'AVI', 'MP4', 'MOV', 'MKV'}
DOCUMENT_EXTENSIONS = {'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'}
AUDIO_EXTENSIONS = {'MP3', 'OGG', 'WAV', 'AMR'}
ARCHIVE_EXTENSIONS = {'ZIP', 'GZ', 'TAR'}


CATEGORIES = {'images', 'video', 'documents', 'audio', 'archives', 'unknown'}


def categorize_file(file_extension):
    '''
    The function takes a file extension and returns the name of the category.
    '''
    if file_extension in IMAGE_EXTENSIONS:
        return 'images'
    elif file_extension in VIDEO_EXTENSIONS:
        return 'video'
    elif file_extension in DOCUMENT_EXTENSIONS:
        return 'documents'
    elif file_extension in AUDIO_EXTENSIONS:
        return 'audio'
    elif file_extension in ARCHIVE_EXTENSIONS:
        return 'archives'
    else:
        return 'unknown'
    

def sort_files(folder_path, sorted_path, ignore_folders):
    '''
    The function sorts all files.
    '''
    start_time = time.time()

    if not os.path.exists(sorted_path):
        os.makedirs(sorted_path)

    for category in CATEGORIES:
        category_path = os.path.join(sorted_path, category)
        os.makedirs(category_path, exist_ok=True)

    for item in os.listdir(folder_path):
        if item.lower() in ignore_folders:
            continue

        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            _, file_extension = os.path.splitext(item)
            file_extension = file_extension[1:].upper()
            category = categorize_file(file_extension)
            shutil.move(item_path, os.path.join(sorted_path, category, item))
            
        elif os.path.isdir(item_path):
            sort_files(item_path, sorted_path, ignore_folders)

    if not os.listdir(folder_path) and folder_path != sorted_path:
        os.rmdir(folder_path)

    end_time = time.time()
    print(f'Done {end_time - start_time}')
    logging.debug(f'Done {end_time - start_time}')

def main():
    if len(sys.argv) > 1:
        main_folder = sys.argv[1]
        sorted_folder = main_folder
        ignore_folders = {'archives', 'video', 'audio', 'documents', 'images', 'unknown'}

        logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(sort_files, main_folder, sorted_folder, ignore_folders)


if __name__ == "__main__":
    main()
