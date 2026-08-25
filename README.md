# Medico Lab

Sistema web para médicos, desenvolvido em Django, com foco em gerenciamento de prontuários, evoluções clínicas, receituários, pedidos de exames, atestados e anexos de exames.

Projeto derivado e adaptado do [Fisio_lab](https://github.com/celsoleite38/Fisio_lab) para uso médico.

## Funcionalidades principais

- Cadastro e gerenciamento de pacientes
- Prontuário eletrônico com evolução clínica
- Registro de anamnese / dados iniciais do paciente
- Evoluções com possibilidade de anexar imagens
- Emissão de **receituários** (com múltiplos medicamentos)
- Pedidos de exames
- Emissão de atestados
- Anexos de exames (PDF, imagens)
- Geração de PDF para documentos (receituário, pedido, atestado)
- Agenda integrada (herdada do projeto original)
- Autenticação segura com perfil profissional (médico)

## Tecnologias utilizadas

- **Backend**: Django 5.2
- **Frontend**: Bootstrap 4, Font Awesome
- **Banco de dados**: SQLite (desenvolvimento) / PostgreSQL (recomendado produção)
- **Bibliotecas principais**:
  - WeasyPrint (geração de PDF)
  - Pillow (manipulação de imagens)
  - Select2 (busca avançada em selects)
  - jQuery (interatividade)

## Requisitos

- Python 3.11 ou superior
- Git
- Ambiente virtual (venv ou virtualenv)
