function deleteMessage() {
    let messageId = document.getElementById("myDL").value;
    const url = "/api/v2/messages/"+messageId

    var token = localStorage.getItem("token");

    fetch(url, {
        method: "DELETE",
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },

    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 200) {
                document.getElementById('getMessages').innerHTML = data["data"][0].success;

                alert(data["data"][0].success);
                window.location.replace("/user_dashboard.html?type=".concat(message));
            } else if (data.status === 400 || data.status === 404) {
                alert(data.error)
            } else if (data.status === 401) {
                alert(data.error)
            } else if (data.status === 403) {
                alert(data.error)
            }

        });

}