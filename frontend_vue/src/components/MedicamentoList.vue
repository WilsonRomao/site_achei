<template>
  <div class="mt-5">

    <h4 class="achei-title mb-4">
      Pesquisa de medicamentos disponíveis nas unidades básicas de saúde (UBS)
    </h4>

    <!-- FILTROS -->
    <div class="row g-3 mb-4">

      <!-- Pesquisa por medicamento -->
      <div class="col-12 col-md-8">
        <div class="input-group input-group-lg">

          <input
            name="q"
            class="form-control custom-search-input border-end-0"
            placeholder="O que precisa achar hoje?"
            :value="filtros.q"
            @input="handleChange"
          />

          <span class="input-group-text custom-search-btn bg-white">
            <i class="bi bi-search"></i>
          </span>

        </div>
      </div>

      <!-- Pesquisa por estabelecimento -->
      <div class="col-12 col-md-4">

        <input
          name="estabelecimento"
          list="lista-estabelecimentos"
          class="form-control form-control-lg custom-search-input"
          placeholder="Filtrar por Estabelecimento..."
          :value="filtros.estabelecimento"
          @input="handleChange"
        />

        <datalist id="lista-estabelecimentos">

          <option
            v-for="(estabelecimento, index) in listaEstabelecimentos"
            :key="index"
            :value="estabelecimento"
          />

        </datalist>

      </div>

    </div>


    <!-- TABELA -->
    <div class="card border-0 shadow-sm rounded-4 overflow-hidden">

      <!-- LOADING -->
      <div
        v-if="loading"
        class="text-center p-5 text-muted"
      >

        <div
          class="spinner-border text-info"
          role="status"
        >
          <span class="visually-hidden">
            Carregando...
          </span>
        </div>

        <p class="mt-2">
          Buscando estoques...
        </p>

      </div>


      <!-- RESULTADOS -->
      <template v-else>

        <table class="table table-striped table-hover mb-0 align-middle">

          <thead class="table-light text-muted">
            <tr>

              <th class="ps-4 py-3 fw-normal">
                Medicamento
              </th>

              <th class="py-3 fw-normal">
                Estabelecimento
              </th>

              <th class="py-3 fw-normal text-center">
                Quantidade
              </th>

            </tr>
          </thead>


          <tbody>

            <!-- MEDICAMENTOS -->
            <tr
              v-for="(item, index) in medicamentos"
              :key="`${item.catmat}-${item.estabelecimentoSaude}-${index}`"
            >

              <td class="ps-4 py-3 text-dark">
                {{ item.medicamento }}
              </td>

              <td class="py-3 text-secondary">
                {{ item.estabelecimentoSaude }}
              </td>

              <td class="py-3 text-center">

                <span
                  class="badge rounded-pill"
                  :class="
                    item.quantidade > 0
                      ? 'bg-success'
                      : 'bg-danger'
                  "
                >
                  {{ item.quantidade }}
                </span>

              </td>

            </tr>


            <!-- NENHUM RESULTADO -->
            <tr v-if="medicamentos.length === 0">

              <td
                colspan="3"
                class="text-center py-5 text-muted"
              >
                Nenhum medicamento encontrado para essa busca.
              </td>

            </tr>

          </tbody>

        </table>


        <!-- PAGINAÇÃO -->
        <div
          class="card-footer bg-white border-top-0 d-flex justify-content-between align-items-center py-3 px-4"
        >

          <button
            class="btn btn-outline-secondary rounded-pill px-4"
            :disabled="page === 1"
            @click="paginaAnterior"
          >
            Anterior
          </button>


          <span class="text-muted small">
            Página {{ page }} de {{ totalPages }}
          </span>


          <button
            class="btn btn-outline-secondary rounded-pill px-4"
            :disabled="page === totalPages"
            @click="proximaPagina"
          >
            Próximo
          </button>

        </div>

      </template>

    </div>

  </div>
</template>


<script setup>

const props = defineProps({

  medicamentos: {
    type: Array,
    default: () => []
  },

  listaEstabelecimentos: {
    type: Array,
    default: () => []
  },

  filtros: {
    type: Object,
    required: true
  },

  page: {
    type: Number,
    default: 1
  },

  totalPages: {
    type: Number,
    default: 1
  },

  loading: {
    type: Boolean,
    default: false
  }

})


const emit = defineEmits([
  'filter-change',
  'update:page'
])


// ==========================
// ALTERAÇÃO DOS FILTROS
// ==========================

const handleChange = (event) => {

  const { name, value } = event.target

  emit('filter-change', {
    [name]: value
  })

}


// ==========================
// PAGINAÇÃO
// ==========================

const paginaAnterior = () => {

  if (props.page > 1) {
    emit('update:page', props.page - 1)
  }

}


const proximaPagina = () => {

  if (props.page < props.totalPages) {
    emit('update:page', props.page + 1)
  }

}

</script>