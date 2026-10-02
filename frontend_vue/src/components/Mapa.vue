<template>
  <div class="mt-4">
    <h3>Mapeamento</h3>

    <p v-if="loading" class="text-muted">Carregando unidades de saúde...</p>
    <p v-else-if="error" class="alert alert-warning">{{ error }}</p>
    <p v-else-if="markerCount === 0" class="text-muted">
      Nenhuma unidade com coordenadas cadastradas.
    </p>

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
import { apiService } from '../services/api'

// Referência para a div do mapa
const mapContainer = ref(null)
const loading = ref(true)
const error = ref('')
const markerCount = ref(0)

// Guarda a instância do Leaflet
let map = null
let markers = null

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

const criarPopup = (estabelecimento) => {
  const content = document.createElement('div')
  const nome = document.createElement('strong')
  nome.textContent = estabelecimento.nome || 'Unidade de saúde'
  content.append(nome)

  const endereco = estabelecimento.endereco?.trim()
  if (endereco) {
    const linha = document.createElement('p')
    linha.className = 'mb-1'
    linha.textContent = endereco
    content.append(linha)
  }

  const horario = estabelecimento.horario?.trim()
  if (horario) {
    const linha = document.createElement('p')
    linha.className = 'mb-1'
    linha.textContent = `Horário: ${horario}`
    content.append(linha)
  }

  const farmacia = document.createElement('p')
  farmacia.className = 'mb-0'
  farmacia.textContent = estabelecimento.farmaceutico
    ? `Farmacêutico: Sim${estabelecimento.horario_farmaceutico ? ` — ${estabelecimento.horario_farmaceutico}` : ''}`
    : 'Farmacêutico: Não'
  content.append(farmacia)

  return content
}

const carregarEstabelecimentos = async () => {
  loading.value = true
  error.value = ''

  try {
    const estabelecimentos = await apiService.getEstabelecimentos()
    const bounds = []

    estabelecimentos.forEach((estabelecimento) => {
      if (
        estabelecimento.latitude === null ||
        estabelecimento.longitude === null ||
        estabelecimento.latitude === '' ||
        estabelecimento.longitude === ''
      ) return

      const latitude = Number(estabelecimento.latitude)
      const longitude = Number(estabelecimento.longitude)

      if (
        !Number.isFinite(latitude) ||
        !Number.isFinite(longitude) ||
        Math.abs(latitude) > 90 ||
        Math.abs(longitude) > 180
      ) return

      const marker = L.marker([latitude, longitude], {
        icon: estabelecimento.farmaceutico ? pinAzul : pinPreto
      })
        .bindPopup(criarPopup(estabelecimento), { offset: [0, -20] })
        .addTo(markers)

      bounds.push(marker.getLatLng())
    })

    markerCount.value = bounds.length
    if (bounds.length > 1) {
      map.fitBounds(bounds, { padding: [24, 24] })
    } else if (bounds.length === 1) {
      map.setView(bounds[0], 14)
    }
  } catch (requestError) {
    error.value = requestError.message || 'Não foi possível carregar as unidades.'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
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

  markers = L.layerGroup().addTo(map)
  await carregarEstabelecimentos()
})

// ==========================
// REMOVER MAPA
// ==========================

onUnmounted(() => {
  if (map) {
    map.remove()
    map = null
    markers = null
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
