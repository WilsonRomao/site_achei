const estabelecimentos = [
  {
    nome: "USF JARDIM TARUMÃ DR EMILIO GARBELOTI NETO",
    latitude: -14.606653,
    longitude: -57.492679,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF COOPHAVILA II ALFREDO NEDER",
    latitude: -20.536059,
    longitude: -54.667429,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF VILA FERNANDA MARIA IVONE DE O NASCIMENTO ARAKAKI",
    latitude: -20.515440,
    longitude: -54.686535,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "CF USF MARIA DE LOURDES DOS SANTOS PORTAL CAIOBÁ",
    latitude: -20.523241,
    longitude: -54.679545,
    horario: "segunda a sexta-feira 07h às 19h"
  },
  {
    nome: "UBSF JARDIM BATISTÃO DR HELIO MARTINS COELHO",
    latitude: -20.520999,
    longitude: -54.666013,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF SANTA EMÍLIA JEFERSON RODRIGUES DE SOUZA",
    latitude: -20.500620,
    longitude: -54.685377,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF SAO CONRADO PASTOR ELISEU FEITOSA DE ALENCAR",
    latitude: -20.496931,
    longitude: -54.676639,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF JARDIM ANTÁRTICA DR NELSON ASSEF BUAINAIN",
    latitude: -20.499224,
    longitude: -54.663242,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF JARDIM BONANCA DR HIROSE ADANIA",
    latitude: -20.493816,
    longitude: -54.661208,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF BURITI DR IVAN HIDELBRAND DA COSTA",
    latitude: -20.490328,
    longitude: -54.670963,
    horario: "segunda a sexta-feira 07 às 11h/13 às 17h"
  },
  {
    nome: "USF OLIVEIRA II BENEDITO MARTINS GONCALVES",
    latitude: -20.475358,
    longitude: -54.659982,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF CAIÇARA DR ALBERTO NEDER",
    latitude: -20.481973,
    longitude: -54.646281,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF DOM ANTÔNIO BARBOSA DR EVANDRO M DE ARRUDA",
    latitude: -20.555174,
    longitude: -54.648646,
    horario: "segunda a sexta-feira 07h às 17h"
  },
  {
    nome: "USF PARQUE DO SOL DR BENJAMIM ASATO",
    latitude: -20.549936,
    longitude: -54.651854,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF JARDIM LOS ANGELES SEBASTIÃO LUIZ NOGUEIRA",
    latitude: -20.548959,
    longitude: -54.628597,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "CF DR MAURO R BARROS WANDERLEY IRACY COELHO NETTO",
    latitude: -20.530826,
    longitude: -54.644714,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF JARDIM MACAÚBAS DR SONI LYDIA SOUZA WOLF",
    latitude: -20.548285,
    longitude: -54.619123,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF PAULO COELHO MACHADO",
    latitude: -20.553880,
    longitude: -54.602553,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF MARIO COVAS DR WAGNER JORGE BORTOTTO GARCIA",
    latitude: -20.542916,
    longitude: -54.604309,
    horario: "segunda a sexta-feira 07h às 19h"
  },
  {
    nome: "USF CIDADE MORENA DR VICENTE FRAGELLI",
    latitude: -20.550624,
    longitude: -54.588613,
    horario: "segunda a sexta-feira 07h às 11h/13h às 17h"
  },
  {
    nome: "USF MORENINHA III DR JUDSON TADEU RIBAS",
    latitude: -20.555796,
    longitude: -54.574382,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF COHAB DR OLIMPIO CAVALHEIRO",
    latitude: -20.535526,
    longitude: -54.620048,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF AERO RANCHO DR SEBASTIÃO ELOY PEREIRA",
    latitude: -20.522388,
    longitude: -54.648927,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF AERO RANCHO GRANJA DRA REGIA JUSSARA F DE BARROS",
    latitude: -20.518616,
    longitude: -54.640907,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF JARDIM BOTAFOGO DR ELIZABETH WANDERLE TOBARU",
    latitude: -20.523473,
    longitude: -54.626592,
    horario: "segunda a sexta-feira 07h às 19h"
  },
  {
    nome: "USF AERO RANCHO IV DR NELSON TOKUEI SIMABUKURO",
    latitude: -20.511328,
    longitude: -54.646102,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF NOVA ESPERANCA",
    latitude: -20.493083,
    longitude: -54.623852,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF DONA ΝΕΤΑ GUANANDI ENG ARTHUR HOKAMA",
    latitude: -20.496069,
    longitude: -54.642053,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF JOCKEY CLUB DR JORGE DAVID NASSER",
    latitude: -20.494944,
    longitude: -54.623898,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF VILA CARVALHO",
    latitude: -20.475199,
    longitude: -54.621894,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF INDUBRASIL MANOEL SECCO THOME",
    latitude: -20.478466,
    longitude: -54.753168,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF SERRADINHO DR SUMIE IKEDA RODRIGUES",
    latitude: -20.458452,
    longitude: -54.684399,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF VILA POPULAR DR VESPASIANO BARBOSA MARTINS",
    latitude: -20.452560,
    longitude: -54.704502,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF SILVIA REGINA DRA ELEONORA M QUEVEDO",
    latitude: -20.445933,
    longitude: -54.669165,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF ANA MARIA DO COUTO",
    latitude: -20.442597,
    longitude: -54.677948,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF AERO ITÁLIA HERBERTO CALADO REBELO",
    latitude: -20.442124,
    longitude: -54.686738,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF ZÉ PEREIRA DR JURANDYR DE CASTRO COIMBRA",
    latitude: -20.432295,
    longitude: -54.673081,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF JOSÉ ABRÃO DR ELIAS NASSER NETO",
    latitude: -20.417185,
    longitude: -54.661275,
    horario: "segunda a sexta-feira 07h às 11h/13h às 17h"
  },
  {
    nome: "USF SIRIO LIBANES DR SYRZIL WILSON MAKSOUD",
    latitude: -20.426291,
    longitude: -54.658591,
    horario: "segunda a sexta-feira 07h às 11h/13h às 17h"
  },
  {
    nome: "USF SANTA CARMELIA DR ALBINO COIMBRA",
    latitude: -20.430254,
    longitude: -54.652160,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF LAR DO TRABALHADOR DR NICOLAU FRAGELLI",
    latitude: -20.451862,
    longitude: 54.644425,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF JARDIM AZALEIA DRA ALDA GUEDES GARCIA OLIVEIRA",
    latitude: -20.422257,
    longitude: -54.642814,
    horario: "segunda a sexta-feira 07h às 19h"
  },
  {
    nome: "USF VILA COX",
    latitude: -20.411851,
    longitude: -54.642855,
    horario: "segunda a sexta-feira 07 às 17h"
  },
  {
    nome: "USF VILA NASSER DR MILTON KOJO CHINEN",
    latitude: -20.416206,
    longitude: -54.631574,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF JARDIM PARADISO PEDRO FELIX DE SOUZA",
    latitude: -20.432558,
    longitude: -54.628466,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF JARDIM SEMINARIO MESTRE JOSÉ ALBERTO VERONESE",
    latitude: -20.404650,
    longitude: -54.617632,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF SAO BENEDITO",
    latitude: -20.423920,
    longitude: -54.618850,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF 26 DE AGOSTO JAIR GARCIA DE FREITAS",
    latitude: -20.444161,
    longitude: -54.617225,
    horario: "segunda a sexta-feira 07 às 17h"
  },
  {
    nome: "USF CORONEL ANTONINO DR ARTHUR VASCONCELOS DIAS",
    latitude: -20.430052,
    longitude: -54.599051,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF ESTRELA DO SUL DR WILLIAN MACKSOUD",
    latitude: -20.417602,
    longitude: -54.596288,
    horario: "segunda a sexta-feira 07 às 17h"
  },
  {
    nome: "USF JARDIM MARABÁ DRA MARLY ANΝΑ TATTON BERG G PEREIRA",
    latitude: -20.434434,
    longitude: -54.581553,
    horario: "segunda a sexta-feira 07 às 17h/13h às 16h"
  },
  {
    nome: "USF VIDA NOVA III AQUINO DIAS BEZERRA",
    latitude: -20.377378,
    longitude: -54.571186,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF JOSE TAVARES DO COUTO DR FERNANDO DE ARRUDA TORRES",
    latitude: -20.386292,
    longitude: -54.577795,
    horario: "segunda a sexta-feira 07h às 17h"
  },
  {
    nome: "USF SAO FRANCISCO",
    latitude: -20.384422,
    longitude: -54.559374,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF JARDIM PRESIDENTE DR NASRI SIUFI",
    latitude: -20.401242,
    longitude: -54.587119,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "CF DRA MARCIA DE SA EARP NOVA LIMA",
    latitude: -20.401352,
    longitude: -54.572095,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF NOVA BAHIA CONSELHEIRO DE SAÚDE EDNEY A DE CAMPOS",
    latitude: -20.410101,
    longitude: -54.572431,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF MATA DO JACINTO DR ADEMAR GUEDES DE SOUZA",
    latitude: -20.424660,
    longitude: -54.569344,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF ESTRELA DALVA DR JOÃO MIGUEL BASMAGE",
    latitude: -20.425328,
    longitude: -54.552991,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF MARIA APARECIDA PEDROSSIAN",
    latitude: -20.472676,
    longitude: -54.551286,
    horario: "segunda a sexta-feira 07 às 19h"
  },
  {
    nome: "USF ARNALDO ESTEVÃO DE FIGUEIREDO DR EDGAR PEDRO RS",
    latitude: -20.472387,
    longitude: -54.564361,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF TIRADENTES DR ANTONIO PEREIRA",
    latitude: -20.480649,
    longitude: -54.580547,
    horario: "segunda a sexta-feira 07 às 22h"
  },
  {
    nome: "USF CRISTO REDENTOR DR CARLOS A JURGIELEWCZ",
    latitude: -20.504350,
    longitude: -54.562778,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF CARLOTA DR ASTROGILDO CARMONA",
    latitude: -20.490399,
    longitude: -54.605059,
    horario: "segunda a sexta-feira 07 às 17h"
  },
  {
    nome: "USF JARDIM ITAMARACA EDSON QUINTINO MENDES",
    latitude: -20.517051,
    longitude: -54.577428,
    horario: "segunda a sexta-feira 07h às 19h"
  },
  {
    nome: "USF UNIVERSITÁRIO DR GERMANO BARROS DE SOUZA",
    latitude: -20.519027,
    longitude: -54.598671,
    horario: "segunda a sexta-feira 07h às 17h"
  },
  {
    nome: "USF PIONEIRA DR CELSO LACERDA DE AZEVEDO",
    latitude: -20.514873,
    longitude: -54.609580,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF ALVES PEREIRA DR WALFRIDO AZAMBUJA",
    latitude: -20.526910,
    longitude: -54.602513,
    horario: "segunda a sexta-feira 07h às 11h/13h às 17h"
  },
  {
    nome: "USF ROCHEDINHO DR ROGER BUAINAIN",
    latitude: -20.224502,
    longitude: -54.590556,
    horario: "segunda a sexta-feira 07h às 11h/12h às 16h"
  },
  {
    nome: "USF VILA CORUMBÁ",
    latitude: -20.447169,
    longitude: 54.630277,
    horario: "segunda a sexta-feira 07 às 11h/13h às 17h"
  },
  {
    nome: "USF ANHANDUÍ DR BENTO DE ASSIS MACHADO",
    latitude: -20.986603,
    longitude: -54.509648,
    horario: "segunda a sexta-feira 07 às 12h/13h às 16h"
  },
  {
    nome: "USF JARDIM NOROESTE",
    latitude: -20.459210,
    longitude: -54.530646,
    horario: "segunda a sexta-feira 07h às 19h"
  },
  {
    nome: "USF TRES BARRAS DRA MARIA JOSÉ DE PAULI",
    latitude: -20.626081,
    longitude: -54.531370,
    horario: "segunda a sexta-feira 07 às 12h/13h às 16h"
  },
  {
    nome: "USF AGUAO MANOEL CORDEIRO",
    latitude: -20.241876,
    longitude: -54.789432,
    horario: "segunda a sexta-feira 07 às 12h/13h às 16h"
  },
  {
    nome: "UPA CORONEL ANTONINO",
    latitude: -20.431261,
    longitude: -54.600738,
    horario: "24 horas"
  },
  {
    nome: "UPA VILA ALMEIDA",
    latitude: -20.439850,
    longitude: -54.657575,
    horario: "24 horas"
  },
  {
    nome: "UPA UNIVERSITÁRIO",
    latitude: -20.525394,
    longitude: -54.598441,
    horario: "24 horas"
  },
  {
    nome: "UPA LEBLON",
    latitude: -20.492758,
    longitude: -54.652326,
    horario: "24 horas"
  },
  {
    nome: "UPA MORENINHA",
    latitude: -20.555408,
    longitude: -54.573395,
    horario: "24 horas"
  },
  {
    nome: "UPA SANTA MÔNICA",
    latitude: -20.456087,
    longitude: -54.709952,
    horario: "24 horas"
  },
  {
    nome: "CRS TIRADENTES",
    latitude: -20.480913,
    longitude: -54.580807,
    horario: "24 horas"
  },
  {
    nome: "CRS NOVA BAHIA",
    latitude: -20.410339,
    longitude: -54.572406,
    horario: "24 horas"
  },
  {
    nome: "CRS COOPHAVILA II",
    latitude: -20.535927,
    longitude: -54.670962,
    horario: "24 horas"
  },
  {
    nome: "CRS AERO RANCHO",
    latitude: -20.521966,
    longitude: -54.648404,
    horario: "24 horas"
  }
];

export default estabelecimentos;