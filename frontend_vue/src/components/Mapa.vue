<template>
  <div class="mt-4">
    <h3>Mapeamento</h3>

    <div
      ref="mapContainer"
      class="map-container"
    ></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

import estabelecimentos from '../data/estabelecimentos'

// Referência para a div do mapa
const mapContainer = ref(null)

// Guarda a instância do Leaflet
let map = null

// ==========================
// ÍCONES
// ==========================

const pinAzul = new L.Icon({
  iconUrl:
    'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',

  shadowUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',

  iconSize: [25, 41],
  iconAnchor: [12, 41]
})

const pinPreto = new L.Icon({
  iconUrl:
    'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-black.png',

  shadowUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',

  iconSize: [25, 41],
  iconAnchor: [12, 41]
})

// ==========================
// CRIAR MAPA
// ==========================

onMounted(() => {
  map = L.map(mapContainer.value).setView(
    [-20.4697, -54.6201],
    13
  )

  // Mapa OpenStreetMap
  L.tileLayer(
    'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
      attribution: '© OpenStreetMap contributors'
    }
  ).addTo(map)

  // ==========================
  // MARCADORES DAS UBS
  // ==========================

  estabelecimentos.forEach((estabelecimento) => {
    L.marker(
      [
        estabelecimento.latitude,
        estabelecimento.longitude
      ],
      {
        icon: estabelecimento.farmaceutico
          ? pinAzul
          : pinPreto
      }
    )
      .addTo(map)
      .bindPopup(
        `
          <b>${estabelecimento.nome}</b>
          <br>

          Horário: ${estabelecimento.horario}
          <br>

          Farmacêutico:
          ${estabelecimento.farmaceutico ? 'Sim' : 'Não'}
        `,
        {
          offset: [0, -20]
        }
      )
  })
})

// ==========================
// REMOVER MAPA
// ==========================

onUnmounted(() => {
  if (map) {
    map.remove()
    map = null
  }
})
</script>

<style scoped>
.map-container {
  height: 500px;
  width: 100%;
  border-radius: 8px;
}
</style>
