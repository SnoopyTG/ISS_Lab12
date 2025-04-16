const baseURL = "http://localhost:8000";

async function loadAnalytics() {
  try {
    const res = await fetch(`${baseURL}/analytics`);
    const data = await res.json();
    
    document.getElementById("itemCount").textContent = data.stats.item_count;
    document.getElementById("userCount").textContent = data.stats.user_count;
    document.getElementById("avgItemName").textContent = data.stats.avg_item_name_length.toFixed(2);
    document.getElementById("avgUserName").textContent = data.stats.avg_user_username_length.toFixed(2);
    document.getElementById("maxItemName").textContent = data.stats.max_item_name_length;
    document.getElementById("maxUserName").textContent = data.stats.max_user_username_length;
    
    // Update the visualization
    if (data.visualization) {
      document.getElementById("plot").src = `data:image/png;base64,${data.visualization}`;
    } else {
      document.getElementById("plot").style.display = "none";
    }
  } catch (error) {
    console.error("Error loading analytics:", error);
    document.getElementById("stats").innerHTML = "<p>Error loading analytics data. Please try again later.</p>";
  }
}

// Load analytics when the page loads
document.addEventListener('DOMContentLoaded', loadAnalytics);