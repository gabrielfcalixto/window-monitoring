import time
import psutil
from collections import defaultdict
import win32gui
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext

# Dicionário para armazenar o tempo gasto em cada aplicativo
app_time = defaultdict(int)

# Variáveis globais para controle do monitoramento
monitoring = False
paused = False
start_time = 0
last_app = None
app_start_time = 0

# Função para obter o aplicativo ativo no Windows
def get_active_window():
    window = win32gui.GetForegroundWindow()
    app_name = win32gui.GetWindowText(window)
    return app_name

# Função para converter segundos em horas, minutos e segundos
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours}h {minutes}m {secs}s"

# Função principal para monitorar o tempo
def start_monitoring():
    global monitoring, paused, start_time, last_app, app_start_time

    duration = int(entry_duration.get()) * 3600  # Converte horas para segundos
    monitoring = True
    paused = False
    start_time = time.time()
    last_app = None

    button_start.config(state=tk.DISABLED)
    button_stop.config(state=tk.NORMAL)
    button_pause.config(state=tk.NORMAL)

    while monitoring and time.time() - start_time < duration:
        if not paused:
            current_app = get_active_window()
            if current_app != last_app:
                if last_app:
                    elapsed_time = time.time() - app_start_time
                    app_time[last_app] += elapsed_time
                last_app = current_app
                app_start_time = time.time()
            time.sleep(1)  # Verifica a cada segundo
        root.update()  # Atualiza a interface gráfica

    if monitoring:
        # Adiciona o tempo do último aplicativo
        if last_app:
            elapsed_time = time.time() - app_start_time
            app_time[last_app] += elapsed_time

        # Gera o relatório
        generate_report()
        show_report()
        messagebox.showinfo("Concluído", "Monitoramento concluído! Relatório salvo em 'relatorio_tempo.txt'.")
    
    monitoring = False
    button_start.config(state=tk.NORMAL)
    button_stop.config(state=tk.DISABLED)
    button_pause.config(state=tk.DISABLED)

# Função para parar o monitoramento
def stop_monitoring():
    global monitoring
    monitoring = False
    button_stop.config(state=tk.DISABLED)
    button_pause.config(state=tk.DISABLED)

# Função para pausar/retomar o monitoramento
def pause_monitoring():
    global paused
    paused = not paused
    if paused:
        button_pause.config(text="Retomar")
    else:
        button_pause.config(text="Pausar")

# Função para gerar o relatório e salvar em um arquivo
def generate_report():
    report = "Relatório de Tempo Gasto em Cada Aplicativo:\n"
    for app, time_spent in app_time.items():
        report += f"{app}: {format_time(time_spent)}\n"
    
    # Salva o relatório em um arquivo
    with open("relatorio_tempo.txt", "w", encoding="utf-8") as file:
        file.write(report)

# Função para exibir o relatório em uma nova janela
def show_report():
    report_window = tk.Toplevel(root)
    report_window.title("Relatório de Tempo")
    report_window.geometry("400x300")

    text_area = scrolledtext.ScrolledText(report_window, wrap=tk.WORD, width=50, height=15)
    text_area.pack(padx=10, pady=10)

    with open("relatorio_tempo.txt", "r", encoding="utf-8") as file:
        report = file.read()
        text_area.insert(tk.INSERT, report)
        text_area.config(state=tk.DISABLED)  # Impede a edição do texto

# Interface gráfica
root = tk.Tk()
root.title("Monitor de Aplicativos")
root.geometry("350x200")

# Label e campo de entrada para a duração
label_duration = tk.Label(root, text="Duração (horas):")
label_duration.pack(pady=5)

entry_duration = tk.Entry(root)
entry_duration.pack(pady=5)
entry_duration.insert(0, "6")  # Valor padrão de 6 horas

# Botão para iniciar o monitoramento
button_start = tk.Button(root, text="Iniciar Monitoramento", command=start_monitoring)
button_start.pack(pady=5)

# Botão para parar o monitoramento
button_stop = tk.Button(root, text="Parar", command=stop_monitoring, state=tk.DISABLED)
button_stop.pack(pady=5)

# Botão para pausar/retomar o monitoramento
button_pause = tk.Button(root, text="Pausar", command=pause_monitoring, state=tk.DISABLED)
button_pause.pack(pady=5)

# Inicia a interface gráfica
root.mainloop()