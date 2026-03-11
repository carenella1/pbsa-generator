const status = document.getElementById("status");

document.getElementById("createBtn").onclick = async () => {
    const name = document.getElementById("name").value;
    const tagline = document.getElementById("tagline").value;
    const description = document.getElementById("description").value;

    if (!name) {
        status.innerText = "Please enter a name.";
        return;
    }

    const data = {
        entity_id: name.toLowerCase().replace(/\s+/g, "_"),
        site_name: name,
        tagline: tagline,
        description: description,
        projects: []
    };

    status.innerText = "Creating config...";

    try {
        const response = await fetch("http://127.0.0.1:8000/create-config", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        status.innerText = result.status || "Config created.";
        console.log("create-config result:", result);
    } catch (error) {
        console.error("create-config failed:", error);
        status.innerText = "Config creation failed.";
    }
};

document.getElementById("generateBtn").onclick = async () => {
    status.innerText = "Generating PBSA site...";

    try {
        const response = await fetch("http://127.0.0.1:8000/generate", {
            method: "POST"
        });

        const data = await response.json();
        status.innerText = data.status || "Site generated.";
        console.log("generate result:", data);
    } catch (error) {
        console.error("generate failed:", error);
        status.innerText = "Generation failed.";
    }
};

document.getElementById("deployBtn").onclick = async () => {
    status.innerText = "Deploying PBSA site...";

    try {
        const response = await fetch("http://127.0.0.1:8000/deploy", {
            method: "POST"
        });

        const data = await response.json();
        status.innerText = data.status || "Site deployed.";
        console.log("deploy result:", data);
    } catch (error) {
        console.error("deploy failed:", error);
        status.innerText = "Deployment failed.";
    }
};