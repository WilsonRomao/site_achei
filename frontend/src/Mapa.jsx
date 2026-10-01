import { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { apiService } from "./services/api";

function Mapa({ onSelectUnidade }) {
  const [unidades, setUnidades] = useState([]);
  const [erro, setErro] = useState("");
  const mapElementRef = useRef(null);
  const mapRef = useRef(null);
  const markersRef = useRef(null);

  useEffect(() => {
    let ativo = true;

    apiService.getEstabelecimentos()
      .then((dados) => {
        if (ativo) setUnidades(dados);
      })
      .catch(() => {
        if (ativo) setErro("Não foi possível carregar as unidades de saúde.");
      });

    return () => {
      ativo = false;
    };
  }, []);

  useEffect(() => {
    if (!mapElementRef.current || mapRef.current) return undefined;

    const map = L.map(mapElementRef.current).setView([-20.4697, -54.6201], 13);

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
    }).addTo(map);

    mapRef.current = map;
    markersRef.current = L.layerGroup().addTo(map);

    return () => {
      map.remove();
      mapRef.current = null;
      markersRef.current = null;
    };
  }, []);

  useEffect(() => {
    if (!mapRef.current || !markersRef.current) return;

    markersRef.current.clearLayers();
    const unidadesComCoordenadas = unidades
      .filter((unidade) => Number.isFinite(Number(unidade.latitude)) && Number.isFinite(Number(unidade.longitude)))
      .map((unidade) => {
      const detalhes = [
        `<b>${unidade.nome}</b>`,
        unidade.endereco,
        unidade.telefone,
        unidade.horario ? `Horário: ${unidade.horario}` : null,
      ].filter(Boolean).join("<br>");

      return L.marker([unidade.latitude, unidade.longitude])
        .bindPopup(detalhes)
        .on("click", () => onSelectUnidade(unidade))
        .addTo(markersRef.current);
    });

    if (unidadesComCoordenadas.length > 0) {
      const bounds = L.featureGroup(unidadesComCoordenadas).getBounds();
      mapRef.current.fitBounds(bounds, { padding: [20, 20], maxZoom: 14 });
    }
  }, [unidades, onSelectUnidade]);

  return (
    <div className="map-wrapper">
      <div
        ref={mapElementRef}
        className="leaflet-map"
        style={{
          width: "100%",
          borderRadius: "8px",
        }}
      ></div>
      {erro && <p className="map-message map-error">{erro}</p>}
      {!erro && unidades.length > 0 && !unidades.some((unidade) => unidade.latitude !== null && unidade.longitude !== null) && (
        <p className="map-message">As unidades ainda não possuem coordenadas cadastradas.</p>
      )}
    </div>
  );
}

export default Mapa;