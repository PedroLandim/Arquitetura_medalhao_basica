

| Campo              | Regra                                |
| -------------------- | -------------------------------------- |
| `id_venda`         | não pode ser nulo e deve ser único |
| `produto`          | não pode ser vazio                  |
| `quantidade`       | deve ser inteiro e maior que 0       |
| `preco_unitario`   | deve ser numérico e maior que 0     |
| `data_venda`       | deve ser uma data válida            |
| `estado`           | deve ser padronizado                 |
| `metodo_pagamento` | deve estar em uma lista conhecida    |
