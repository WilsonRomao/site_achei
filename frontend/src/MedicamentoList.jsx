import React from "react"

const MedicamentoList = ({Medicamento}) => {
    return < div>
        <h2>Medicamentos</h2>

        <table>
            <thead>
                <tr>
                    <th>Estabelecimento de Saúde</th>
                    <th>Codigo do Medicamento</th>
                    <th>Medicamento</th>
                    <th>Quantidade</th>
                    <th>Ações</th>
                </tr>

            </thead>

            <tbody>
                {Medicamento.map((item) => (
                    <tr key={item.catmat}>
                        <td>{item.estabelecimentoSaude}</td>
                        <td>{item.catmat}</td>
                        <td>{item.medicamento}</td>
                        <td>{item.quantidade}</td>
                    </tr>
                ))}
                
            </tbody>
        </table>
    
    </div>
}

export default MedicamentoList