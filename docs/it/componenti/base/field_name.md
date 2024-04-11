### Field Name
Campo di testo preconfigurato con la **Property Name** valorizzata con **rec_name**. Per maggiori info  sulla configurazione vedere *TextField*

### Textfield
Campo di testo input. Oltre alle configurazioni standard bookmark è gestito il mask per tipo d valore che si vuole utilizzare; i valori ammessi sono: **'mac', 'ip', 'date', 'euro', 'numericit', 'sci', 'mail', 'currency', 'euroComplex', 'numeric', 'url'**; è presente un help nel tooltip.

img4

### Button
Pulsante Azione config sezione **Api → Custom Properties**
**btn_action_type** → “post”(default)
**url_action →** url dell’azione che si vuole eseguire 
**leftIcon**  o **rightIcon** → opzionale impostare un icona 

Nel caso si voglia utilizzare il pulsante per aggiungere un record in una tabella integrata
aggiungere le seguenti proprieta’
    **todo**: new_row,
    **default_fields**: {"rec_name":"parent"},
    **open_modal**: y  → apre il form in una modale

Oppure nel caso si voglia aprire un form modale, **modalEdit**: y
Oppure nel caso si voglia esportare dati di una collezzione:
	**export**: y
	**url_action**: /client/export/{nome_model}/{type} - type = xls,csv,json
	**body**: {"query": {"$and": [{"active": true}]}}

IMAGE


#### Number
Implementa le  configurazioni standard 

Di Default un Field Number e’ definito come **Integer**
Se si vuole definire un campo **Float** si deve spuntare il checkbox **Require Decimal** nel TAB
**Data** del configuratore del campo in fase di design.


#### Button Alert
Pulsante Azione con alert configurabile: sezione **Api → Custom Properties**
**modal_title →** titolo della modale 
**modal_message →** messaggio di avviso che si vuole visualizzare
**btn_modal_label →** Testo del pulsante “SI” (valore default)
**btn_action_type →** Post (default)
**url_action →** url dell’azione che si vuole eseguire
