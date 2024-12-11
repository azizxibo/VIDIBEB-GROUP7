import streamlit as st
from rembg import remove
from PIL import Image
import io


def save_as_pdf(image):
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    c.drawImage(image, 0, 0, image.width, image.height)
    c.save()
    buf.seek(0)
    return buf

def main():
    st.title("VIDIBEB-WEB")
    st.write("Upload an image, remove its background, and download it in your preferred format!")

    uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    format_option = st.selectbox("Select the output format", ["PNG", "JPG", "PDF"])

    if uploaded_file:
        input_image = Image.open(uploaded_file)
        input_image = input_image.convert("RGBA")
        st.image(input_image, caption="Original Image", use_column_width=True)

        with st.spinner("Removing background..."):
            output_image = remove(input_image)

        st.image(output_image, caption="Background Removed", use_column_width=True)

        buf = io.BytesIO()
        if format_option == "PNG":
            output_image.save(buf, format="PNG")
            file_extension = "png"
            mime_type = "image/png"
        elif format_option == "JPG":
            output_image = output_image.convert("RGB")
            output_image.save(buf, format="JPEG")
            file_extension = "jpg"
            mime_type = "image/jpeg"
        elif format_option == "PDF":
            buf = save_as_pdf(output_image)
            file_extension = "pdf"
            mime_type = "application/pdf"

        buf.seek(0)
        st.download_button(
            label="Download Image",
            data=buf,
            file_name=f"output.{file_extension}",
            mime=mime_type,
        )

if __name__ == "__main__":
    main()
