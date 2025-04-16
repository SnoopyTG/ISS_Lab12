const baseURL = "http://localhost:8000";

function showError(message, container) {
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error';
  errorDiv.textContent = message;
  container.innerHTML = '';
  container.appendChild(errorDiv);
}

function showSuccess(message) {
  const successDiv = document.createElement('div');
  successDiv.className = 'success';
  successDiv.textContent = message;
  document.querySelector('.container').insertBefore(successDiv, document.getElementById('itemList'));
  setTimeout(() => successDiv.remove(), 3000);
}

async function loadItems(searchTerm = "") {
  const list = document.getElementById("itemList");
  list.innerHTML = '<div class="loading">Loading items...</div>';
  
  try {
    const res = await fetch(`${baseURL}/items`);
    if (!res.ok) {
      throw new Error(`Server returned ${res.status}: ${res.statusText}`);
    }
    
    const data = await res.json();
    const filteredItems = data.filter(item =>
      item.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    document.getElementById("itemCount").textContent = `Total items: ${filteredItems.length}`;

    if (filteredItems.length === 0) {
      list.innerHTML = "<li>No items found. Try adding some items or changing your search.</li>";
    } else {
      list.innerHTML = '';
      filteredItems.forEach(item => {
        const li = document.createElement("li");
        li.className = 'item-card fade-in';
        li.innerHTML = `
          <div class="item-content">
            <strong>${item.name}</strong>
            <p>${item.description}</p>
          </div>
          <button class="delete-btn">Delete</button>
        `;
        
        const deleteBtn = li.querySelector('.delete-btn');
        deleteBtn.onclick = () => deleteItem(item._id);
        list.appendChild(li);
      });
    }
  } catch (error) {
    console.error("Error loading items:", error);
    showError(`Failed to load items: ${error.message}`, list);
  }
}

async function deleteItem(id) {
  if (!confirm('Are you sure you want to delete this item?')) {
    return;
  }

  try {
    const res = await fetch(`${baseURL}/items/${id}`, { method: "DELETE" });
    if (!res.ok) {
      throw new Error(`Server returned ${res.status}: ${res.statusText}`);
    }
    showSuccess('Item deleted successfully');
    loadItems(document.getElementById("search").value);
  } catch (error) {
    console.error("Error deleting item:", error);
    showError(`Failed to delete item: ${error.message}`, document.getElementById("itemList"));
  }
}

// Add event listeners when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById("search");
  const itemForm = document.getElementById("itemForm");
  
  // Add search event listener with debouncing
  let searchTimeout;
  searchInput.addEventListener("input", (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      loadItems(e.target.value);
    }, 300);
  });

  // Add form submission event listener
  itemForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const nameInput = document.getElementById("name");
    const descInput = document.getElementById("description");
    
    try {
      const res = await fetch(`${baseURL}/items`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          name: nameInput.value.trim(), 
          description: descInput.value.trim() 
        })
      });
      
      if (!res.ok) {
        throw new Error(`Server returned ${res.status}: ${res.statusText}`);
      }
      
      showSuccess('Item created successfully');
      e.target.reset();
      loadItems(searchInput.value);
    } catch (error) {
      console.error("Error creating item:", error);
      showError(`Failed to create item: ${error.message}`, document.getElementById("itemList"));
    }
  });

  // Load items initially
  loadItems();
});

// Chocolate Question : Does React do Server-Side Rendering or Client-Side Rendering?