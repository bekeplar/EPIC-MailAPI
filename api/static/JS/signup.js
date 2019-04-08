const confirmPassword = document.getElementById("confirm_password");
const password = document.getElementById("password");
const firstName = document.getElementById("firstname");
const lastName = document.getElementById("lastname");
const email = document.getElementById("email");


// Password strength validations
function validatePasswordStrength() {
    const passwordError = document.getElementById("password-error");

    if (/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/.test(password.value)) {
        passwordError.style.display = "none";
        password.setCustomValidity("");

    } else {
        passwordError.style.display = "block";
        passwordError.innerHTML = "Password Must contain a Minimum of 8 characters" +
            " with atleast one upper case letter, atleast on lower case letter and atleast one number.";
        password.setCustomValidity("Weak Password.");

    }

}

password.onkeyup = validatePasswordStrength;
password.onchange = validatePasswordStrength;

function validatePassword() {
    const confirmPasswordError = document.getElementById("confirm_pass-error");
    if (password.value !== confirmPassword.value) {
        confirmPasswordError.style.display = "block";
        confirmPasswordError.innerHTML = "Passwords Do not  match";
    } else {
        confirmPasswordError.style.display = "none";
    }

}

// Validating user password
confirmPassword.onblur = validatePassword;
confirmPassword.onkeyup = validatePassword;


firstName.onkeyup = function () {
    const firstNameError = document.getElementById("firstname-error");

    if (/^[a-zA-Z]{3,}$/.test(firstName.value)) {
        firstNameError.style.display = "none";
        firstName.setCustomValidity("");
    } else {
        firstNameError.style.display = "block";
        firstNameError.innerHTML = "First name must contain atleast three alphabetic characters";
        firstName.setCustomValidity("Invalid First Name.");

    }

};

lastName.onkeyup = function () {
    const lastNameError = document.getElementById("lastname-error");

    if (/^[a-zA-Z]{3,}$/.test(lastName.value)) {
        lastNameError.style.display = "none";
        lastName.setCustomValidity("");

    } else {
        lastNameError.style.display = "block";
        lastNameError.innerHTML = "Last name must contain atleast three alphabetic characters";
        lastName.setCustomValidity("Invalid Last name.");
    }

};


// Displaying the error in form of an array

function displayError(dataArray) {

    for (let key in dataArray) {

        if ({}.hasOwnProperty.call(dataArray, key)) {
            let fieldError = document.getElementById(key + "-error");
            fieldError.style.display = "block";
            fieldError.innerHTML = dataArray[key];
        }
    }
}

// function for signing up a user.
function signUpAccount() {

    const submitProgress = document.getElementById("submit_progress");
    submitProgress.style.display = 'block';

    const url = "https://kepicmail.herokuapp.com/api/v2/auth/signup";
    const newUser = {
        firstname: firstName.value,
        lastname: lastName.value,
        email: email.value,
        password: password.value,
    };


    fetch(url, {
        method: "POST",
        headers: {
            "content-type": "application/json",
        },
        body: JSON.stringify(newUser),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 400) {
                //Bad format data
                submitProgress.style.display = 'none';
                displayError(data.error);


            } else if (data.status === 409) {
                // Checking for an existing user email
                submitProgress.style.display = 'none';

                displayError(data.error);

            } else if (data.status === 201) {
                //on success acceptance of details
                submitProgress.style.display = 'none';

                document.getElementById("message").style.display = "block";
                document.getElementById("message").innerHTML = data["data"][0].success;
                window.setTimeout(function () {
                    window.location.replace("../index.html");
                }, 3000);

            }

        })
        .catch((error) => console.log(error));

}