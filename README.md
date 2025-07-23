# PyShare
Share app local

## Aplicação Desktop
Cria atividades via app desktop, a base de dados e gerado na mesma pasta do arqruivo .exe, após a execução e deve ser salvo e permanecer junto ao .exe, caso mova a aplicação de local ou também para casos de atualização da aplicação, se desejar utilizar a mesma base já salva.

### --> Pode ser acessado pelo pelo main.exe como qualquer aplicação desktop, após o pyinstaller.
### --> Outra opção é pelo terminal com python main.py

<details open>
<summary> **Tecnologias Principais** </summary>
  Python <br/>
  sys <br/>
  Thread <br/>
  SQLite 3 <br/>
  Tkinter <br/>
  <br/>

> **_NOTE:_** SQLite tem limitações para persistir dados simuntaneos, então foi implementada uma fila na aplicação para assim suportar multiplas escritas na base de dados.
