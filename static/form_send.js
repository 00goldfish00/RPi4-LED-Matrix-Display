/**
 * Using javascript to send the post request with form data asynchronously in the background.
 * This prevents:
 * a) the page having to reload to display response data
 * b) getting ridirected to a different endpoint on form submission
 *
 * https://developer.mozilla.org/en-US/docs/Learn/Forms/Sending_forms_through_JavaScript
 */
// Javascript to run when the page loads
window.addEventListener("load", function () {
    function sendData() {
        const XHR = new XMLHttpRequest();

        // Bind the FormData object and the form element
        // form element from constant defined in global scope
        const FD = new FormData(form);

        // Define what happens on successful data submission
        XHR.addEventListener("load", function (event) {
            alert("Color Set!", "success");
        });

        // Define what happens in case of error
        XHR.addEventListener("error", function (event) {
            alert("Oops! Something went wrong.", "danger");
        });

        // Allow the alert popup to live for 2.5 seconds
        setTimeout(function () {
            document.getElementById('submitAlert').remove()
        }, 2500);

        // Set up our request
        XHR.open("POST", "/send_rgb");

        // The data sent is what the user provided in the form
        XHR.send(FD);

        XHR.onload = function() {
            console.log(XHR.response);
        }

    }

    function alert(message, type) {
        var alertElement = document.getElementById("alertPlaceholder");
        if (alertElement) {
            alertElement.innerHTML = '<div id="submitAlert" class="alert alert-' + type + ' alert-dismissible fade show" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
        }
    }

    // Access the form element...
    const form = document.getElementById("form1");

    // ...and take over its submit event.
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        sendData();
    });
});