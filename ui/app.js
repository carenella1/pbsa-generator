async function createConfig()
{

const name = document.getElementById("entity_name").value
const id = document.getElementById("entity_id").value
const description = document.getElementById("description").value

const res = await fetch("/create-config",
{
method:"POST",
headers:
{
"Content-Type":"application/json"
},
body:JSON.stringify(
{
entity_name:name,
entity_id:id,
description:description
})
})

const data = await res.json()

document.getElementById("status").innerText =
"Config created. Entity type detected: " + data.entity_type

}



async function generateSite()
{

document.getElementById("status").innerText = "Generating site..."

const res = await fetch("/generate",
{
method:"POST"
})

const data = await res.json()

document.getElementById("status").innerText =
"Site generated."

}



async function deploySite()
{

document.getElementById("status").innerText =
"Deploying to GitHub..."

const res = await fetch("/deploy",
{
method:"POST"
})

const data = await res.json()

document.getElementById("status").innerText =
"Deployment complete."

}