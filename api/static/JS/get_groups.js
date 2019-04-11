function displayError(dataArray) {

    for (let key in dataArray) {

        if ({}.hasOwnProperty.call(dataArray, key)) {
            let fieldError = document.getElementById(key + "-error");
            fieldError.style.display = "block";
            fieldError.innerHTML = dataArray[key];
        }
    }
}

function getGroups() {
    const url = "/api/v2/groups";
    var token = localStorage.getItem("token");
    let output = '';
    fetch(url, {
        method: "GET",
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
    })
        .then((response) => response.json())
        .then((data) => {

            if (data.status === 401) {
                window.setTimeout(function () {
                    window.location.replace("/");
                }, 5000);

            } else if (data.status === 404) {
                submitProgress.style.display = 'hide';
                displayError(data.error);
                document.getElementById("error").style.display = "block";
                document.getElementById("error").innerHTML = "You havent created any group yet.";
                window.setTimeout(function () {
                    window.location.replace("/group.html");
                }, 5000);



            } else if (data.status === 200) {
                //on success
                let Groups = data["data"];
                data.data.forEach(function (groups) {


                    output += `
                    
                    <li>${groups.group_name}</li>
                    <li><a>ViewDetails</a></li>
                                `;

                if (Groups.length === 0) {
                        output += `
                            
                            <section class="flex-col-sp-btn border-radius-30p border-round-lg">
                                    <h2>You dont have any group created yet</h2>
                                  
                            </section>
                        `;
                    }
                
                
    
                    });
                }

                document.getElementById('myUL').innerHTML = output;
        })
        .catch((error) => console.log(error));


}
function logout() {
    localStorage.removeItem("token");
}