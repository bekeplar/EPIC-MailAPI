const password = document.getElementById("password");
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

function login() {

    const url = "https://kepicmail.herokuapp.com/api/v2/auth/login";
    const userCredentials = {
        email: email.value,
        password: password.value
    };

    const submitProgress = document.getElementById("submit_progress");
    submitProgress.style.display = 'block';

    fetch(url, {
        method: "POST",
        headers: {
            "content-type": "application/json",
        },
        body: JSON.stringify(userCredentials),
    })
        .then(response => response.json())
        .then((data) => {
            if (data.status === 401) {

                // Response on invalid user credentials.
                submitProgress.style.display = 'none';
                document.getElementById("success").style.display = "none";
                document.getElementById("error").style.display = "block";
                document.getElementById("error").innerHTML = data.error;
                window.setTimeout(function () {
                    document.getElementById("error").style.display = "none";

                }, 3000);


            } else if (data.status === 200) {

                //on success of user Login.
                submitProgress.style.display = 'none';
                document.getElementById("error").style.display = "none";
                document.getElementById("success").style.display = "block";
                document.getElementById("success").innerHTML = data["data"][0].success;
                token = data.data[0].token;
                localStorage.setItem("token", token);

                window.setTimeout(function () {
                    window.location.replace("../user_dashboard.html");
                }, 1000);

            }


        })
        .catch((error) => console.log(error))

}
function logout() {
    localStorage.removeItem("token");
}