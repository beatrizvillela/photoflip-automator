import streamlit as st
from PIL import Image
import io
import zipfile

st.set_page_config(page_title="PhotoFlip Automator", page_icon="📸")
st.title("📸 PhotoFlip Automator")
st.write("Gire várias imagens com um clique!")

uploaded_files = st.file_uploader("Envie suas fotos aqui", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

rotation_angle = st.selectbox("Escolha o ângulo de rotação", [90, 180, 270])

if st.button("🔁 Girar todas as imagens"):
    if not uploaded_files:
        st.warning("Por favor, envie pelo menos uma imagem.")
    else:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
            for uploaded_file in uploaded_files:
                image = Image.open(uploaded_file)

                # Converte se a imagem tiver canal alfa (transparência)
                if image.mode == "RGBA":
                    image = image.convert("RGB")

                rotated = image.rotate(-rotation_angle, expand=True)

                img_byte_arr = io.BytesIO()
                rotated.save(img_byte_arr, format="JPEG")
                img_byte_arr.seek(0)

                zip_file.writestr(uploaded_file.name, img_byte_arr.read())

        zip_buffer.seek(0)
        st.success("✅ Imagens rotacionadas com sucesso!")
        st.download_button(
            label="📦 Baixar imagens rotacionadas (ZIP)",
            data=zip_buffer,
            file_name="imagens_rotacionadas.zip",
            mime="application/zip"
        )