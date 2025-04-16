const baseURL = "http://localhost:8000"; // Correct API base URL

async function loadUsers() {
  try {
    const res = await fetch(`${baseURL}/users`);
    const users = await res.json();
    const list = document.getElementById("userList");
    list.innerHTML = "";

    document.getElementById("userCount").textContent = `Total users: ${users.length}`;
    users.forEach(user => {
      const li = document.createElement("li");
      li.textContent = `${user.username}: ${user.bio}`;

      const deleteBtn = document.createElement("button");
      deleteBtn.textContent = "Delete";
      deleteBtn.onclick = async () => {
        try {
          await fetch(`${baseURL}/users/${user._id}`, { method: "DELETE" });
          loadUsers();
        } catch (error) {
          console.error("Error deleting user:", error);
          alert("Failed to delete user. Please try again.");
        }
      };

      li.appendChild(deleteBtn);
      list.appendChild(li);
    });
  } catch (error) {
    console.error("Error loading users:", error);
    document.getElementById("userList").innerHTML = "<li>Error loading users. Please try again later.</li>";
  }
}

document.getElementById("search").addEventListener("input", async (e) => {
  const term = e.target.value.toLowerCase();
  try {
    const res = await fetch(`${baseURL}/users`);
    const users = await res.json();
    const list = document.getElementById("userList");
    list.innerHTML = "";

    const filteredUsers = users.filter(user => user.username.toLowerCase().includes(term));
    document.getElementById("userCount").textContent = `Total users: ${filteredUsers.length}`;

    filteredUsers.forEach(user => {
      const li = document.createElement("li");
      li.textContent = `${user.username}: ${user.bio}`;

      const deleteBtn = document.createElement("button");
      deleteBtn.textContent = "Delete";
      deleteBtn.onclick = async () => {
        try {
          await fetch(`${baseURL}/users/${user._id}`, { method: "DELETE" });
          loadUsers();
        } catch (error) {
          console.error("Error deleting user:", error);
          alert("Failed to delete user. Please try again.");
        }
      };

      li.appendChild(deleteBtn);
      list.appendChild(li);
    });
  } catch (error) {
    console.error("Error searching users:", error);
    document.getElementById("userList").innerHTML = "<li>Error searching users. Please try again later.</li>";
  }
});

// Load users when the page loads
document.addEventListener('DOMContentLoaded', loadUsers);

document.getElementById("userForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const bio = document.getElementById("bio").value;
  try {
    await fetch(`${baseURL}/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, bio })
    });
    e.target.reset();
    loadUsers();
  } catch (error) {
    console.error("Error creating user:", error);
    alert("Failed to create user. Please try again.");
  }
});