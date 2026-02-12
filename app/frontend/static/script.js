const API_URL = "http://127.0.0.1:8000/websites";

// ---------------------
// Checar status do site
// ---------------------
async function check_site_status(urlParam = null) {
  const urlDigitada =
    urlParam || document.getElementById("urlInput").value;

  const resultDiv = document.getElementById("result-section");
  resultDiv.classList.remove("active");

  if (!urlDigitada) {
    alert("Por favor, digite uma URL.");
    return;
  }

  resultDiv.innerHTML = `
    <div class="loading">
      <span class="spinner"></span>
      <span class="loading-text">Verificando site</span>
    </div>
  `;

  try {
    const response = await fetch(
      `${API_URL}/check-status?url=${encodeURIComponent(urlDigitada)}`
    );

    if (!response.ok) throw new Error("Erro ao consultar API");

    const data = await response.json();
    resultDiv.classList.add("active");

    const siteName = data.site_name || new URL(urlDigitada).hostname;
    const favicon =
      data.favicon ||
      "https://www.google.com/s2/favicons?domain=" + urlDigitada;

    resultDiv.innerHTML = `
      <div class="site-card">
        <div class="absolute-header">
          <div class="site-header">
            <img src="${favicon}" class="favicon" />
            <h3>${siteName}</h3>
          </div>
          <div class="header-options">
            <img 
              src="/app/frontend/static/img/saved.png"
              class="save-website"
              onclick="salvarWebsite('${siteName}', '${data.url}')"
            />
          </div>
        </div>

        <p><strong>Status:</strong> ${data.status}</p>
        <p><strong>HTTP:</strong> ${data.http_status ?? "—"}</p>
        <p><strong>Tempo:</strong> ${data.response_time ?? "—"}s</p>
        <p><strong>URL:</strong> ${data.url}</p>
      </div>
    `;
  } catch (error) {
    resultDiv.innerHTML = "Erro ao verificar o site.";
    console.error(error);
  }
}

// ---------------------
// Listar Websites
// ---------------------
async function listarWebsites() {
  const container = document.getElementById("saved-websites-id");
  container.innerHTML = "";

  try {
    const response = await fetch(API_URL);
    const data = await response.json();

    data.forEach((site) => {
      const favicon =
        "https://www.google.com/s2/favicons?domain=" + site.url;

      container.innerHTML += `
        <div class="template-saved-websites">
          <img src="${favicon}" />

          <div class="saved-info">
            <strong>${site.name}</strong>
            <span>${site.url}</span>
          </div>

          <button 
            class="recheck-btn"
            onclick="check_site_status('${site.url}')"
            title="Verificar novamente"
          >
            ↻
          </button>
        </div>
      `;
    });
  } catch (error) {
    console.error("Erro ao listar websites:", error);
  }
}

// ---------------------
// Salvar Website no Banco
// ---------------------
async function salvarWebsite(nome, urlSite) {
  try {
    const payload = {
      name: nome,
      url: urlSite,
    };

    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (response.status === 201) {
      alert("Website salvo com sucesso!");
      listarWebsites();
    } else {
      alert("Erro ao salvar website");
    }
  } catch (error) {
    console.error("Erro ao salvar:", error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  listarWebsites();
});
