const toggleBgButtons = document.querySelectorAll(".toggleBgButton");
const backgroundImage1 = "background1.jpg";
const backgroundImage2 = "background3.jpg";
let isBackground1 = true;

const storedBackground = localStorage.getItem("backgroundImage");
if (storedBackground) {
    document.body.style.backgroundImage = `url(${storedBackground})`;
}

toggleBgButtons.forEach((button) => {
    button.addEventListener("click", () => {
        isBackground1 = !isBackground1;
        const newBackgroundImage = isBackground1 ? backgroundImage1 : backgroundImage2;
        document.body.style.backgroundImage = `url(${newBackgroundImage})`;
        localStorage.setItem("backgroundImage", newBackgroundImage);
    });
});
