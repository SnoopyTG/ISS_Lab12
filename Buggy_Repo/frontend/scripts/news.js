const rssConverter = "https://api.rss2json.com/v1/api.json?rss_url=";
const feeds = [
  { name: "bbc", url: "http://feeds.bbci.co.uk/news/world/rss.xml" },
  { name: "guardian", url: "https://www.theguardian.com/international/rss" }
];
let allArticles = [];

async function loadNews(searchTerm = "", source = "all", reset = false) {
  const list = document.getElementById("newsList");
  const loading = document.getElementById("loading");
  
  if (reset) {
    allArticles = [];
    list.innerHTML = "";
  }
  
  loading.style.display = "block";
  
  try {
    const selectedFeeds = source === "all" ? feeds : feeds.filter(f => f.name === source);
    
    for (const feed of selectedFeeds) {
      try {
        const res = await fetch(`${rssConverter}${encodeURIComponent(feed.url)}`);
        if (!res.ok) {
          console.error(`Failed to fetch ${feed.name}: ${res.status} ${res.statusText}`);
          continue; // Skip this feed but continue with others
        }
        const data = await res.json();
        
        const articles = (data.items || []).map(item => ({
          title: item.title || "No title",
          description: item.description || "No description",
          url: item.link || "#",
          source: feed.name.toUpperCase(),
          pubDate: item.pubDate ? new Date(item.pubDate).toLocaleDateString() : "Unknown"
        }));
        
        allArticles.push(...articles);
      } catch (feedError) {
        console.error(`Error fetching ${feed.name}:`, feedError);
        // Continue with other feeds
      }
    }
    
    const filteredArticles = searchTerm
      ? allArticles.filter(article =>
          article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
          article.description.toLowerCase().includes(searchTerm.toLowerCase())
        )
      : allArticles;
    
    document.getElementById("articleCount").textContent = `Total articles: ${filteredArticles.length}`;
    
    list.innerHTML = "";
    if (filteredArticles.length === 0) {
      list.innerHTML = "<p>No articles found. Try changing your search or source filter.</p>";
    } else {
      filteredArticles.forEach(article => {
        const div = document.createElement("div");
        div.className = "news-item";
        div.innerHTML = `
          <h3><a href="${article.url}" target="_blank">${article.title}</a></h3>
          <p><strong>Source:</strong> ${article.source} | 
             <strong>Date:</strong> ${article.pubDate}</p>
          <p>${article.description}</p>
        `;
        list.appendChild(div);
      });
    }
    
  } catch (err) {
    console.error("Error loading news:", err);
    list.innerHTML = `<p style="color: red;">Error loading news: ${err.message}</p>`;
  } finally {
    loading.style.display = "none";
  }
}

// Add event listeners for search and source filter
document.getElementById("search").addEventListener("input", (e) => {
  const searchTerm = e.target.value;
  const source = document.getElementById("source").value;
  loadNews(searchTerm, source);
});

document.getElementById("source").addEventListener("change", (e) => {
  const source = e.target.value;
  const searchTerm = document.getElementById("search").value;
  loadNews(searchTerm, source, true);
});

// Initial load when the page is ready
document.addEventListener('DOMContentLoaded', () => {
  loadNews();
});