# Window Monitoring

Aplicativo desktop em Python (Tkinter) que monitora o tempo de uso de cada janela/aplicativo ativo no Windows e gera um relatório de uso.

## Funcionalidades

- Monitoramento em tempo real da janela ativa
- Controles de iniciar, pausar e parar
- Duração configurável do monitoramento (em horas)
- Relatório final com o tempo total gasto em cada aplicativo (`relatorio_tempo.txt`)

## Tecnologias

- Python
- Tkinter (interface gráfica)
- psutil
- pywin32 (win32gui)

## Como executar

```bash
pip install psutil pywin32
python script.py
```

## Licença

Este projeto está sob a licença MIT — veja o arquivo [LICENSE](LICENSE) para mais detalhes.
