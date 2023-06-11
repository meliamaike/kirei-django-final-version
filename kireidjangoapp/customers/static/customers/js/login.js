
function showRegisterModal() {
  document.getElementById("close-login-modal-btn").click();
  console.log("Show register modal");
}

    // Attach the event listener for the "Registrarte" button
    document.getElementById("register-link").addEventListener("click", showRegisterModal);
  
    // // Function to handle the modal close event
    // function handleLoginModalClose() {
    //   // loginModal.classList.remove("d-none");
    //   console.log("login modal close")
    // }
    // document.getElementById("close-login-modal-btn").addEventListener("click", handleLoginModalClose);

