/* SUPABASE */
const supabaseClient = supabase.createClient(
    "https://iywprvavelmmxyxpdyea.supabase.co",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml5d3BydmF2ZWxtbXh5eHBkeWVhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg3NTA5MDQsImV4cCI6MjA4NDMyNjkwNH0.aiPk46MVyHC4VOMjk_f9zIsyMPKu6hTVJmhJpYBqAKU"
);

/* ===================== ADDED ===================== */
/* RESTORE SESSION ON PAGE LOAD */
window.onload = () => {
    const savedUser = sessionStorage.getItem("userId");
    if (savedUser) {
        currentUserId = savedUser;
        console.log("SESSION USER:", currentUserId);
    }
};
/* ================================================= */

/* ELEMENTS */
const signupBtn = document.getElementById("signupTabBtn");
const loginBtn = document.getElementById("loginTabBtn");
const signupSection = document.getElementById("signupSection");
const loginSection = document.getElementById("loginSection");

const askPopup = document.getElementById("askPopup");
const emergencyPopup = document.getElementById("emergencyPopup");
const contactsArea = document.getElementById("contactsArea");

let currentUserId = null;

/* TAB SWITCH */
signupBtn.onclick = () => {
    signupBtn.className = "tab-btn active-signup";
    loginBtn.className = "tab-btn inactive-login";
    signupSection.classList.remove("hidden");
    loginSection.classList.add("hidden");
};

loginBtn.onclick = () => {
    loginBtn.className = "tab-btn active-login";
    signupBtn.className = "tab-btn inactive-signup";
    loginSection.classList.remove("hidden");
    signupSection.classList.add("hidden");
};

/* SIGNUP */
document.getElementById("signupForm").onsubmit = async e => {
    e.preventDefault();

    if (password.value !== confirmPassword.value) {
        alert("Passwords do not match");
        return;
    }

    const { data, error } = await supabaseClient
        .from("users")
        .insert([{
            name: fullName.value,
            gender: gender.value,
            age: age.value,
            email: email.value,
            contact: contact.value,
            password: password.value
        }])
        .select();

    if (error) {
        alert(error.message);
        return;
    }

    currentUserId = data[0].id;
    console.log("USER CREATED ID:", currentUserId);

    loginContact.value = contact.value;
    askPopup.classList.remove("hidden");
};

/* POPUPS */
function openEmergency() {
    askPopup.classList.add("hidden");
    emergencyPopup.classList.remove("hidden");
    contactsArea.innerHTML = "";
    count = 0;
    addContact();
}

function skipEmergency() {
    askPopup.classList.add("hidden");
    loginBtn.click();
}

/* CONTACTS */
let count = 0;

function addContact() {
    if (count >= 5) {
        alert("Max 5 contacts");
        return;
    }

    count++;

    let div = document.createElement("div");
    div.innerHTML = `
        <input class="cname" placeholder="Name">
        <input class="cphone" placeholder="Phone">
    `;
    contactsArea.appendChild(div);
}

/* SAVE CONTACTS */
async function saveEmergency() {

    console.log("USER ID:", currentUserId);

    if (!currentUserId) {
        alert("User ID missing. Signup again.");
        return;
    }

    let names = document.querySelectorAll(".cname");
    let phones = document.querySelectorAll(".cphone");

    let payload = [];

    for (let i = 0; i < names.length; i++) {

        let n = names[i].value.trim();
        let p = phones[i].value.trim();

        if (n && p) {
            payload.push({
                user_id: currentUserId,
                user_contact: loginContact.value, // required
                name: n,
                phone: p
            });
        }
    }

    if (payload.length === 0) {
        alert("Add at least one contact");
        return;
    }

    console.log("SENDING:", payload);

    const { data, error } = await supabaseClient
        .from("emergency_contacts")
        .insert(payload)
        .select();

    if (error) {
        console.error("SAVE ERROR:", error);
        alert(error.message);
        return;
    }

    alert("Emergency contacts saved!");
    emergencyPopup.classList.add("hidden");
    loginBtn.click();
}

/* LOGIN */
document.getElementById("loginForm").onsubmit = async e => {
    e.preventDefault();

    const { data, error } = await supabaseClient
        .from("users")
        .select("*")
        .eq("contact", loginContact.value)
        .eq("password", loginPassword.value)
        .single();

    if (error || !data) {
        alert("Invalid credentials");
        return;
    }

    /* ================= ADDED ================= */
    sessionStorage.setItem("userId", data.id);
    sessionStorage.setItem("userName", data.name);
    currentUserId = data.id;   // keep in JS also
    /* ======================================== */

    console.log("LOGIN USER ID:", data.id);

    alert("Login success!");
    window.location.href = "index.html";
};
