function showLoginModal() {
  var registerModalButton = document.getElementById("register-modal-btn");

  registerModalButton.click();

  console.log("SHow login modal")
  
}

// Attach the event listener for the "Ingresá" link
document.getElementById("login-link").addEventListener("click", function (event) {
  event.preventDefault(); // Prevent the default link behavior
  showLoginModal();
});



    

    

    
        // document.addEventListener("DOMContentLoaded", function() {
        //   var registerForm = document.getElementById("register-form");
        //   var registerModal = document.getElementById("registerModal");
        //   var closeButton = document.querySelector(".close");
        
        //   registerForm.addEventListener("submit", function(event) {
        //     event.preventDefault(); // Prevent default form submission
        
        //     var formData = new FormData(registerForm);
        //     var xhr = new XMLHttpRequest();
        //     xhr.open("POST", "/register/", true);
        //     xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        //     xhr.onreadystatechange = function() {
        //       if (xhr.readyState === XMLHttpRequest.DONE) {
        //         if (xhr.status === 200) {
        //           var response = xhr.responseText;
        //           var parser = new DOMParser();
        //           var responseDoc = parser.parseFromString(response, "text/html");
        //           var newModalContent = responseDoc.getElementById("registerModal");
        
        //           if (newModalContent) {
        //             // Replace the entire modal with the updated content
        //             registerModal.innerHTML = newModalContent.innerHTML;
        //           } else {
        //             // Form is valid, perform desired action (e.g., redirect)
        //             $('#registerModal').modal('hide'); // Hide the modal
        //             window.location.reload(); // Refresh the page
        //           }
        //         } else {
        //           // Handle error case
        //           console.error("Error: " + xhr.status);
        //         }
        //       }
        //     };
        //     xhr.send(formData);
        //   });
        
        // //   closeButton.addEventListener("click", function() {
        // //     registerForm.removeEventListener("submit", handleFormSubmit); 
        // //   });
        // });
        
      
   
  


 