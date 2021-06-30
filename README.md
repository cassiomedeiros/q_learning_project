# Pré-requisitos

1. Python >= 3.6.

# Para realizar os testes do algorítmo

1. Clonar reposítorio do git.

2. Acessar a pasta do repositório pelo prompt e criar o ambiente de desenvolvimento.
```
    python -m venv .venv
```

3. Ativar o ambiente.
 ```
    .\.venv\Scripts\activate
```

4. Instalar as dependências.
 ```
    pip install -r .\requirements.txt
```

5. Realizar o build do pojeto.
 ```
    python setup.py bdist_wheel
```

6. Instalar o arquivo ".whl" gerado na pasta dist.
 ```
    pip install .\dist\qlearning-0.0.1-py3-none-any.whl 
```

7. Realizar o teste.

 ```
     python .\tests\teste.py
```

## Observações

Ao realizar o teste, é criada uma imagem na pasta "report" com o resultado da execução algorítimo. A imagem apresenta uma relação de episódios x passos para alcançar o objetivo.