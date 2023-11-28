import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import rarfile
import shutil

from tools.database import DatabaseManager
from tools.search_elastic import SearchEngine
from tools.elastic import SyncData


def upload_images(uploaded_image):
    """
    Process and upload the provided images to the database.

    Args:
        uploaded_image: List of images uploaded by the user.
    """
    list_image = [[img.name, img] for img in uploaded_image]
    if list_image:
        db_manager = DatabaseManager()
        db_manager.up_data(list_image)
        SyncData().__call__()
        st.write('Done')


def process_rar_file(uploaded_data, paths):
    """
    Processes the uploaded .rar file. Extracts images, renames if necessary,
    and adds them to the database.

    Args:
        uploaded_data: The uploaded .rar file from the user.
        paths (str): The path where the data should be extracted.
    """
    list_image = []
    with rarfile.RarFile(uploaded_data, 'r') as rar:
        rar.extractall(str(paths) + '/search_engine_v1.1/data/cache/')
        a = str(uploaded_data.name).replace('.rar', '')
        try:
            folder = os.listdir(str(paths) + '/search_engine_v1.1/data/cache/')
            new = str(folder[0].replace(' ', '_'))
            old_name = str(paths) + '/search_engine_v1.1/data/cache/' + folder[0]
            new_name = str(paths) + '/search_engine_v1.1/data/cache/' + new
            os.rename(old_name, new_name)
        except Exception as e:
            print(e)

    path_rar = str(paths) + '/search_engine_v1.1/data/cache/' + new + '/'
    list_ima = os.listdir(path_rar)
    for i in list_ima:
        name = i
        path_image = path_rar + str(i)
        list_image.append([name, path_image])

    if list_image:
        db_manager = DatabaseManager()
        db_manager.up_data(list_image)
        SyncData().__call__()
        st.write('Done')

    try:
        shutil.rmtree(path_rar)
    except Exception as e:
        print(e)


def display_search_results(input, precision, pats):
    """
    Searches the database with the provided input and precision.
    Displays the results to the user.

    Args:
        input (str): The search query input by the user.
        precision (float): The precision value set by the user.
        pats (str): Path for locating images in the results.
    """
    search_instance = SearchEngine()
    results = search_instance.main(input, precision)

    for i in results:
        images = Image.open(pats + i[0])
        draw = ImageDraw.Draw(images)
        font = ImageFont.truetype("arial.ttf", 30)
        text = i[1]
        tex = text[:4]
        position = (10, 10)
        text_color = (0, 0, 0)
        draw.text(position, tex, fill=text_color, font=font)
        st.image(images, use_column_width=True, width=300)


def main():
    """
    Main function for the Streamlit app. Provides UI options to upload images,
    upload .rar files containing images, and search the image database.
    """
    st.title("Search Engine Smart")

    # UI select box for user options
    option = st.selectbox(
        'How would you like to proceed?',
        ('Choose option', 'Upload image', 'Upload file rar', 'Search'))

    # If user chooses to upload an image
    if option == "Upload image":
        uploaded_image = st.file_uploader("Upload Image",
                                          type=["jpg", "png", "jpeg"],
                                          accept_multiple_files=True)
        if uploaded_image is not None and len(uploaded_image) > 0:
            upload_images(uploaded_image)

    # If user chooses to upload a .rar file
    elif option == "Upload file rar":
        db_manager = DatabaseManager()
        pats = db_manager.return_path()
        uploaded_data = st.file_uploader('upload file rar', type=['rar'])
        if uploaded_data:
            process_rar_file(uploaded_data, paths)

    # If user chooses to search
    elif option == "Search":
        db_manager = DatabaseManager()
        pats = db_manager.return_path()
        input = st.text_input('Search images')
        st.title("Precision Adjustment Bar")
        precision = st.slider("Accuracy", min_value=0.0, max_value=1.0, value=0.65)
        if st.button("Search"):
            display_search_results(input, precision, pats)

    st.write('You selected:', option)


if __name__ == "__main__":
    main()
