function checkFrequency() {
    const num = document.getElementById("num").value;

    fetch("/frequency", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ number: num })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("result").innerText =
                `Number ${data.number} appeared ${data.frequency} times`;
        });
}

function addNumber() {
    const num = document.getElementById("newNum").value;

    fetch("/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ number: num })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            document.getElementById("newNum").value = "";
        });
}

function bulkAddNumbers() {
    const text = document.getElementById("bulkText").value;

    fetch("/bulk_add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            document.getElementById("bulkText").value = "";
        });
}