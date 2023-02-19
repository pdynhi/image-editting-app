# Checkout this tutorial
# https://blog.loginradius.com/engineering/guest-post/opencv-web-app-with-streamlit/
# Online deployment:
# https://towardsdatascience.com/3-easy-ways-to-deploy-your-streamlit-web-app-online-7c88bb1024b1
# https://www.youtube.com/watch?v=4SO3CUWPYf0

# Run: streamlit run Image_Filters_Streamlit_app.py

import io
import base64
import cv2
import pyautogui
from PIL import Image
from filters import *


# Generating a link to download a particular image file.
def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format = 'JPEG')
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href

#function to display output
def display():
    ''' This function will display the output image'''
    with output_col:
        st.header('Output')
        st.image(output, channels=color)
        # fromarray convert cv2 image into PIL format for saving it using download link.
        if color == 'BGR':
            result = Image.fromarray(output[:,:,::-1])
        else:
            result = Image.fromarray(output)
        # Display link.
        st.markdown(get_image_download_link(result,'output.png','Download '+'Output'),
                    unsafe_allow_html=True)
        

# Set title.
st.title('美丽 Editing App')
st.text('你好！欢迎你。这是我的第一个应用。我希望你喜欢它。')
st.text('Hello! Welcome. This is my first app. I hope you enjoy.')
# Upload image.
uploaded_file = st.file_uploader('Choose an image file:', type=['png','jpg'])

if uploaded_file is not None:
    # Convert the file to an opencv image.
    raw_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(raw_bytes, cv2.IMREAD_COLOR)
    input_col, output_col = st.columns(2)
    with input_col:
        st.header('Original')
        # Display uploaded image.
        st.image(img, channels='BGR', use_column_width=True)

    st.header('Filters:')
    # Display a selection box for choosing the filter to apply.
    option = st.selectbox('Select a filter:',
                          ( 'None',
                            'Black and White',
                            'Sepia / Vintage',
                            'Pencil Sketch'
                         ))



    # Define columns for thumbnail images.
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.caption('Black and White')
    #     st.image('filter_bw.jpg')
    # with col2:
    #     st.caption('Sepia / Vintage')
    #     st.image('filter_sepia.jpg')
    # with col3:
    #     st.caption('Pencil Sketch')
    #     st.image('filter_pencil_sketch.jpg')


    # Colorspace of output image.
    color = 'BGR'

     # Generate filtered image based on the selected option.
    if option == 'None':
        output = img
    elif option == 'Black and White':
        output = bw_filter(img)
        color = 'GRAY'
    elif option == 'Sepia / Vintage':
        output = sepia(img)
    elif option == 'Pencil Sketch':
        ksize = st.slider('Blur kernel size', 1, 11, 5, step=2)
        output = pencil_sketch(img, ksize)
        color = 'GRAY'
        
    #create the adjust header
    st.header('Adjust:')
    # Display a selection box for choosing the adjustment
    brightness = st.checkbox('Brightness')
    if brightness:
        level = st.slider('level', min_value=-127, max_value=127, step=10,  value=0)
        output = bright(output, level)
        
    contra = st.checkbox('contrast')
    if contra:
        level = st.slider('level', min_value=0.0, max_value=5.0, step=0.1, value=1.0)
        output = contrast(output, level)
        
    vig = st.checkbox('Vignette')
    if vig:
        level = st.slider('level', 0, 10)
        output = vignette(output, level)
        
    #create a restart button
    if st.button('Restart'):
        output = img
        
    display()
    

    