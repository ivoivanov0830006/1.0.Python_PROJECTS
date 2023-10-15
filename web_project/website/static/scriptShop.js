
//---------------- WRAPPER POPUP --------------- //
document.addEventListener('DOMContentLoaded', function() {
    const wrapperContainer = document.querySelector('.profileContent');
    const passwordChangeLink = document.querySelector('.password-change-link');
    const emailChangeLink = document.querySelector('.email-change-link');
    const passwordForm = document.querySelector('.password.form-box');
    const emailForm = document.querySelector('.email.form-box');
    const openPopup = document.querySelector('.editBtn');
    const closePopup = document.querySelector('.btnLoginClose');

    // Handle opening the popup
    openPopup.addEventListener('click', () => {
        wrapperContainer.classList.add('active-popup');
        document.body.style.overflow = 'hidden';
        passwordForm.style.display = 'block';
    });

    // Handle closing the popup
    closePopup.addEventListener('click', () => {
        wrapperContainer.classList.remove('active-popup');
        document.body.style.overflow = 'auto';
        passwordForm.style.display = 'none';
        emailForm.style.display = 'none';
    });

    // Handle switching between "Password Change" and "Email Change" sections
    passwordChangeLink.addEventListener('click', () => {
        passwordForm.style.display = 'block';
        emailForm.style.display = 'none';
    });

    emailChangeLink.addEventListener('click', () => {
        passwordForm.style.display = 'none';
        emailForm.style.display = 'block';
    });
});
