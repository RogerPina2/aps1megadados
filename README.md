# Megadados2020-2-Projeto1
Projeto 1 da disciplina Megadados - repositorio para alunos

Para executar o serviço rode

```
Colocar os valores corretos nos arquivos do config

Windows:
    dir principal:
    run -> config.bat
    run -> code .
No VSCode: # ainda no dir principal
    CTRL + SHIFT + P
    Selecionar -> Python: Configure Tests
    Selecionar -> Pytest
    Selecionar -> tasklist
dir scripts:

Windows:
run -> python run_all_migrations.py ../migrations ../../config/config.json ../../config/db_admin_secrets.json

run -> uvicorn tasklist.main:app --reload
```
