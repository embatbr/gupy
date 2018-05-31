# Desafio Back-end Gupy

Bem vindo ao desafio de back-end da Gupy. Gostaríamos de saber qual o seu ponto de vista para implementação da nossa funcionalidade de inserção manual de candidatos pelos recrutadores, então precisamos que você crie uma api REST utilizando qualquer linguagem (node, python, java, c#...). Esta aplicação deve ter:


## 1 - Inserção de currículos

Este endpoint deve receber, validar e salvar os seguintes campos: Cadastro manual de currículos pelo recrutador:

- nome
- imagem
- data de nascimento
- genero
- email
- telefone
- endereço
- latitude
- longitude
- tags
- lista de experiência profissional
- lista de formações



## 2 - Inserção em lote de currículos

Deve receber um ZIP com vários arquivos JSON dentro. Cada arquivo terá os mesmos Campos descritos acima. Cada arquivo deverá ser cadastrado como um candidato e caso o candidato já exista, os dados deverão ser atualizados.

## BÔNUS (é opcional fazer qualquer um desses, mas se fizer levaremos em consideração)

 - Front-end
 - Internacionalização
 - Outros endpoints do crud
 - Visualização dos candidatos no mapa
 - Deploy no Heroku (ou similar)
 - Continuous deployment no travis (ou similar)