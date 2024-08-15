# Curso FastAPI

Este é um projeto desenvolvido como parte do curso [FastAPI do Zero ao Deploy](https://fastapidozero.dunossauro.com/) oferecido por Dunossauro. O objetivo deste projeto é explorar as funcionalidades do FastAPI e entender como construir APIs robustas e eficientes utilizando Python.

## Sobre o Projeto

Este projeto foi criado para acompanhar o conteúdo do curso, permitindo ao desenvolvedor aplicar na prática os conceitos aprendidos, incluindo a criação de rotas, tratamento de requisições, e a integração com bibliotecas como `httpx` para testes.

### Funcionalidades

- **FastAPI**: Utilizado para construir a API principal.
- **Testes Automatizados**: Configurado com `pytest` e `pytest-cov` para garantir a qualidade do código.
- **Linting e Formatação**: Configurado com `ruff` para manter o código limpo e consistente.
- **Gerenciamento de Tarefas**: Automatização de tarefas utilizando `Taskipy`.

## Como Executar

### Requisitos

- Python 3.12+
- [Poetry](https://python-poetry.org/) instalado para gerenciamento de dependências.

### Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/curso-fastapi.git
    cd curso-fastapi
    ```

2. Instale as dependências:

    ```bash
    poetry install
    ```

3. Ative o ambiente virtual:

    ```bash
    poetry shell
    ```

### Executando o Projeto

Para iniciar o servidor de desenvolvimento:

```bash
task run
```

A aplicação estará disponível em `http://127.0.0.1:8000`.

### Executando os Testes

Para rodar os testes:

```bash
task test
```

Os resultados da cobertura dos testes podem ser visualizados em `htmlcov/index.html`.

## Estrutura do Projeto

- `app.py`: Arquivo principal contendo a lógica da API.
- `tests/`: Contém os testes automatizados para a API.

## Méritos

Este projeto foi desenvolvido como parte do curso [FastAPI do Zero ao Deploy](https://fastapidozero.dunossauro.com/) oferecido por Dunossauro. Todo o conteúdo técnico e aprendizado aplicado neste repositório são frutos das lições abordadas durante o curso.

## Autor

- **Augusto Bauer Domingos** - [augustobauerdomingos@gmail.com](mailto:augustobauerdomingos@gmail.com)


## Licença

Este projeto está licenciado sob a GNU General Public License - veja o arquivo [LICENSE](LICENSE) para detalhes.

