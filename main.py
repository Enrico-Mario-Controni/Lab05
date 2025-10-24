import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO
    text=ft.Text("\nAggiungi Nuova Automobile\n", text_align=ft.TextAlign.CENTER,
                 size=25, weight=ft.FontWeight.BOLD)

    marca=ft.TextField(width=300, label="inserisci la marca", text_align=ft.TextAlign.CENTER)
    modello= ft.TextField(width=300,label="inserisci il modello", text_align=ft.TextAlign.CENTER)
    anno=ft.TextField(width=300,label="inserisci l'anno", text_align=ft.TextAlign.CENTER)

    posti = ft.TextField(label="n° posti",width=100, disabled=True, text_align=ft.TextAlign.CENTER)
    posti.value = 0

    def handlerplus(e):
        counter= posti.value
        if posti.value >= 0:
            counter += 1
            posti.value=counter
            page.update()

    def handlerminus(e):
        counter= posti.value
        if posti.value >= 1:
            counter -= 1
            posti.value=counter
            page.update()

    buttonplus = ft.IconButton(icon=ft.Icons.ADD_CIRCLE_ROUNDED, on_click=handlerplus, icon_color="green")
    buttonminus = ft.IconButton(icon=ft.Icons.REMOVE_CIRCLE_ROUNDED, on_click=handlerminus, icon_color="red")
    meccanismo_Posti=ft.Row([buttonplus, posti, buttonminus])
    row=ft.Row( [marca, modello, anno, meccanismo_Posti], spacing=50)

    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO
    def handleradd(e):
        if anno.value.isdigit() and posti.value > 0:
            marca_auto= marca.value.strip()
            modello_auto= modello.value.strip()
            anno_auto= int(anno.value)
            posti_auto= int(posti.value)

            autonoleggio.aggiungi_automobile(marca_auto, modello_auto, anno_auto, posti_auto)
            aggiorna_lista_auto()

            marca.value=""
            modello.value=""
            anno.value=""
            posti.value=0
            page.update()

        else:
            alert.show_alert("❌ Errore: opzione non corretta nel campo anno o  nel campo n°posti")
            marca.value = ""
            modello.value = ""
            anno.value = ""
            posti.value = 0


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    btnadd= ft.ElevatedButton("Aggiungi auto", on_click=handleradd)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        text,
        row,
        btnadd,


        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
