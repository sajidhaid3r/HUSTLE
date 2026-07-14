import streamlit as st
import requests

st.title("MY AI IMAGE GENERATOR")

st.sidebar.header("SETTINGS")
art_style=st.sidebar.selectbox(
    "Select Desired Art Style",
    ["Photorealistic","Cartoon", "Anime", "Abstract", "Fantasy"])

width=st.sidebar.slider("Image Width", min_value=256, max_value=1024, value=768)
height=st.sidebar.slider("Image Height", min_value=256, max_value=1024, value=768)

user_prompt=st.text_input("Describe the image you want to generate:")

#ADD A BUTTON
if st.button("Generate Image"):
    if user_prompt:
        with st.spinner("Generating Image..."):
            full_prompt=f"{user_prompt}, make the art style: {art_style}"
            url=f"https://image.pollinations.ai/prompt/{full_prompt}?width={width}&height={height}"
            response=requests.get(url)
            if response.status_code==200:
                st.success("Image Generated Successfully!")
                #st.write(response)
                #Convert the binary into pixels or an actual image
                st.image(response.content, caption=full_prompt)
                st.download_button(
                    label="Download Image",
                    data=response.content,
                    file_name="generated_image.png",
                    mime="image/png"
                )
            else:
                st.error("API is not working")
    else:
        st.warning("Please add a image description")

                