import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO

def convert_image(image, format):
    """Convert image to the specified format."""
    img_buffer = BytesIO()
    image.save(img_buffer, format=format)
    img_buffer.seek(0)
    return img_buffer

def main():
    st.title("Background Removal Tool")

    st.write("Upload an image to remove its background and download the result.")

    # File upload
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Display original image
        original_image = Image.open(uploaded_file)
        st.image(original_image, caption="Original Image", use_column_width=True)

        # Process image to remove background
        with st.spinner("Processing image..."):
            image_bytes = uploaded_file.read()
            output_bytes = remove(image_bytes)
            result_image = Image.open(BytesIO(output_bytes)).convert("RGBA")

        st.image(result_image, caption="Image without Background", use_column_width=True)

        # Download options
        st.write("### Download the result:")
        col1, col2, col3 = st.columns(3)

        with col1:
            jpg_buffer = convert_image(result_image.convert("RGB"), "JPEG")
            st.download_button(
                label="Download JPG",
                data=jpg_buffer,
                file_name="no_bg.jpg",
                mime="image/jpeg",
            )

        with col2:
            png_buffer = convert_image(result_image, "PNG")
            st.download_button(
                label="Download PNG",
                data=png_buffer,
                file_name="no_bg.png",
                mime="image/png",
            )

        with col3:
            pdf_buffer = convert_image(result_image.convert("RGB"), "PDF")
            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name="no_bg.pdf",
                mime="application/pdf",
            )

if __name__ == "__main__":
    main()
