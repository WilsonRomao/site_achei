<template>
  <div class="card border-0 shadow-sm rounded-4">
    <div class="card-body p-4">

      <h5 class="fw-bold mb-3">
        <i class="bi bi-file-earmark-arrow-up me-2"></i>
        Atualizar estoque
      </h5>

      <p class="text-muted small">
        Selecione a planilha Excel contendo os dados atualizados
        do estoque de medicamentos.
      </p>

      <div class="mb-3">
        <input
          ref="fileInput"
          type="file"
          class="form-control"
          accept=".xlsx,.xls"
          @change="handleFileChange"
        />
      </div>

      <!-- Arquivo selecionado -->
      <div
        v-if="arquivo"
        class="alert alert-light border d-flex align-items-center"
      >
        <i class="bi bi-file-earmark-excel me-2"></i>

        <span class="small">
          {{ arquivo.name }}
        </span>
      </div>

      <!-- Mensagem -->
      <div
        v-if="mensagem"
        class="alert"
        :class="erro ? 'alert-danger' : 'alert-success'"
      >
        {{ mensagem }}
      </div>

      <button
        type="button"
        class="btn text-white rounded-pill px-4 fw-bold"
        style="background-color: var(--achei-teal)"
        :disabled="!arquivo || loading"
        @click="handleUpload"
      >
        <span
          v-if="loading"
          class="spinner-border spinner-border-sm me-2"
        ></span>

        {{ loading ? 'Enviando...' : 'Enviar planilha' }}
      </button>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { apiService } from '../services/api'

const emit = defineEmits(['success'])

const arquivo = ref(null)
const loading = ref(false)

const mensagem = ref('')
const erro = ref(false)

const fileInput = ref(null)


// ==========================
// SELECIONAR ARQUIVO
// ==========================

const handleFileChange = (event) => {
  arquivo.value = event.target.files[0]

  mensagem.value = ''
  erro.value = false
}


// ==========================
// ENVIAR ARQUIVO
// ==========================

const handleUpload = async () => {
  if (!arquivo.value) {
    mensagem.value = 'Selecione uma planilha primeiro.'
    erro.value = true
    return
  }

  loading.value = true

  mensagem.value = ''
  erro.value = false

  try {
    const response = await apiService.uploadFile(
      arquivo.value
    )

    mensagem.value =
      response.message || 'Planilha enviada com sucesso!'

    erro.value = false

    // Limpa arquivo selecionado
    arquivo.value = null

    if (fileInput.value) {
      fileInput.value.value = ''
    }

    // Avisa App.vue que o estoque foi atualizado
    emit('success')

  } catch (error) {
    mensagem.value =
      error.message || 'Erro ao enviar a planilha.'

    erro.value = true

  } finally {
    loading.value = false
  }
}
</script>