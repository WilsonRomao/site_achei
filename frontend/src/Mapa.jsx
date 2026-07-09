import { useEffect } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import estabelecimentos from "./data/estabelecimentos";

function Mapa() {
  useEffect(() => {
    // Evita criar o mapa duas vezes
    const map = L.map("map").setView([-20.4697, -54.6201], 13);

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
    }).addTo(map);

    estabelecimentos.forEach((e) => {
      L.marker([e.latitude, e.longitude])
        .addTo(map)
        .bindPopup(`
            <b>${e.nome}</b><br>
            Horário: ${e.horario}
            `);
    });

    // Remove o mapa ao desmontar o componente
    return () => {
      map.remove();
    };
  }, []);

  return (
    <div className="mt-4">
      <h3>Mapeamento</h3>

      <div
        id="map"
        style={{
          height: "500px",
          width: "100%",
          borderRadius: "8px",
        }}
      ></div>
    </div>
  );
}

export default Mapa;