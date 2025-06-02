document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/productos/")
    .then((response) => response.json())
    .then((productos) => {
      const container = document.getElementById("productos-container");

      // Mezclar productos aleatoriamente
      const productosAleatorios = productos
        .sort(() => 0.5 - Math.random())
        .slice(0, 4); // mostrar solo 4 productos

      productosAleatorios.forEach((producto) => {
        const card = document.createElement("div");
        card.className = "col-md-4";

        const precioClp = producto.precio_clp
          ? new Intl.NumberFormat("es-CL", {
              style: "currency",
              currency: "CLP",
              maximumFractionDigits: 0,
            }).format(producto.precio_clp)
          : "No disponible";

        card.innerHTML = `
          <div class="card h-100 shadow-sm">
            <div class="card-body">
              <h5 class="card-title">${producto.nombre}</h5>
              <p class="card-text">
                <strong>Marca:</strong> ${producto.marca}<br>
                <strong>Modelo:</strong> ${producto.modelo}<br>
                <strong>Stock:</strong> ${producto.stock}<br>
                <strong>Precio:</strong> ${precioClp}<br>
                <strong>Tipo:</strong> ${producto.tipo}<br>
              </p>
            </div>
          </div>
        `;

        container.appendChild(card);
      });
    })
    .catch((error) => {
      console.error("Error al obtener productos:", error);
    });
});