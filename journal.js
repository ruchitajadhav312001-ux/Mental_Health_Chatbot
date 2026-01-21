/* SUPABASE */
const supabaseClient = supabase.createClient(
    "https://iywprvavelmmxyxpdyea.supabase.co",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml5d3BydmF2ZWxtbXh5eHBkeWVhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg3NTA5MDQsImV4cCI6MjA4NDMyNjkwNH0.aiPk46MVyHC4VOMjk_f9zIsyMPKu6hTVJmhJpYBqAKU"
);

const datePicker = document.getElementById("datePicker");
const showDate = document.getElementById("showDate");
const showDay = document.getElementById("showDay");
const titleInput = document.getElementById("title");
const contentInput = document.getElementById("content");
const cardsDiv = document.getElementById("cards");

let mood = "😊";

/* DATE */
function formatDate(date) {
    return date.toDateString();
}

function showCurrentDate() {
    let d = datePicker.value ? new Date(datePicker.value) : new Date();
    showDate.innerText = formatDate(d);
    showDay.innerText = d.toLocaleDateString("en-US", { weekday: "long" });
}

datePicker.addEventListener("change", showCurrentDate);
showCurrentDate();

/* MOOD */
function setMood(m) {
    mood = m;
}

/* SAVE */
async function saveEntry() {

    let title = titleInput.value.trim();
    let content = contentInput.value.trim();

    if (!title || !content) {
        alert("Fill title and content");
        return;
    }

    const userId = sessionStorage.getItem("userId");

    if (!userId) {
        alert("Login first");
        return;
    }

    const { error } = await supabaseClient
        .from("journal")
        .insert([{
            user_id: userId,
            title: title,
            content: content,
            mood: mood,
            created_at: new Date()
        }]);

    if (error) {
        console.log("DB ERROR:", error);
        alert(error.message);
        return;
    }

    clearForm();
    loadEntries();
}

/* CLEAR */
function clearForm() {
    titleInput.value = "";
    contentInput.value = "";
}

/* LOAD */
async function loadEntries() {

    const userId = sessionStorage.getItem("userId");
    if (!userId) return;

    const { data, error } = await supabaseClient
        .from("journal")
        .select("*")
        .eq("user_id", userId)
        .order("created_at", { ascending: false });

    if (error) {
        console.log("LOAD ERROR:", error);
        return;
    }

    cardsDiv.innerHTML = "";

    if (!data || data.length === 0) {
        cardsDiv.innerHTML = "<p>No entries yet</p>";
        return;
    }

    data.forEach(e => {
        cardsDiv.innerHTML += `
            <div class="card">
                <h4>${e.title}</h4>
                <p>${e.content}</p>
                <small>${new Date(e.created_at).toDateString()}</small>
            </div>
        `;
    });
}

/* LOAD ON PAGE OPEN */
loadEntries();
