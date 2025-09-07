# MC656 - Projeto de Engenharia de Software
Este repositório contém o desenvolvimento de uma API RESTful como parte da disciplina MC656 - Engenharia de Software. O projeto utiliza o framework FastAPI para o back-end e implementa um pipeline de Integração Contínua (CI) com GitHub Actions.
## 🛠️ Tecnologias Utilizadas
- Back-end: Python 3.13
- Framework da API: FastAPI
- Servidor ASGI: Uvicorn
- Testes Automatizados: Pytest
- Qualidade de Código:
  - Flake8 (Linter de Estilo - PEP 8)
  - MyPy (Verificador de Tipos Estáticos)
  - CI/CD: GitHub Actions
## 🚀 Como Executar o Projeto Localmente
Siga os passos abaixo para configurar e executar a aplicação na sua máquina.
**Pré-requisitos**
- Python 3.13 ou superior
- Um gestor de pacotes como o pip
1. Clonar o Repositório
```
git clone https://github.com/felipeverol/MC656-Engenharia-de-Software.git
cd MC656-Engenharia-de-Software
```

2. Criar um Ambiente Virtual (Recomendado)
É uma boa prática isolar as dependências do projeto.
```
# Criar o ambiente virtual
python -m venv .venv

# Ativar o ambiente virtual no Windows:
.\.venv\Scripts\activate
# No macOS/Linux:
source .venv/bin/activate
```

3. Instalar as Dependências
Instale todos os pacotes necessários que estão listados no requirements.txt.
```
pip install -r requirements.txt
```

4. Executar a Aplicação
Com as dependências instaladas, inicie o servidor de desenvolvimento.
```
uvicorn app.main:app --reload
```

A API estará disponível no endereço:  ```http://127.0.0.1:8000```

5. Aceder à Documentação Interativa
O FastAPI gera automaticamente uma documentação interativa (Swagger UI). Pode usá-la para visualizar e testar os endpoints da API:
```http://127.0.0.1:8000/docs```

✅ Testes e Qualidade de Código
O projeto está configurado com um pipeline de CI que executa as seguintes verificações em cada Pull Request para a branch main:
Análise de Estilo (Linting): Garante que o código segue as convenções do PEP 8.
```
flake8 .
```

Verificação de Tipos (Type Checking): Verifica a consistência das anotações de tipo.
```
mypy app
```

Testes Unitários: Executa os testes de lógica da aplicação.
```
pytest
```

Para executar estas verificações localmente, basta rodar os comandos acima no seu terminal.
