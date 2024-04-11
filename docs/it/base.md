# Form Builder Componenti

Tutti i componenti nel builder sono o sono derivati dai componenti di default di [Formio.js](https://formio.github.io/formio.js/app/builder)
Il sistema integra questo tool per la creazione di form Drag&Drop e li rende disponibili all’utente sotto forma di App con [grafica aderente alle linee guida AGID](https://italia.github.io/bootstrap-italia/docs/come-iniziare/introduzione/)

Non tutte le funzionalità di Formio.js sono state gestite ma solo quelle utili al fine del progetto.
Per quanto riguarda le funzionalità di base del progetto vedere la [documentazione generale del applicazione](https://docs.google.com/document/d/1eSXA8a7Gd9tm-iV7kv4eN7dPhJgc4OInUUwxjZ6DXpY/edit#)

## **Metadati**
I metadati sono dati presenti in ogni model (form) e vengono valorizzati in automatico alla creazione/modifica di un record di un form.
L’elenco dei metadati e’ il seguente:

**id, rec_name, owner_uid, owner_name, owner_sector, owner_sector_id, owner_function, update_datetime,create_datetime,owner_function_type, sys, demo, deleted, list_order, owner_personal_type, owner_job_title**

## Funzionalità di base di tutti i componenti:
Nei componenti sono gestite le seguenti proprietà:

**Display**:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Custom CSS Class →** si possono usare classi [Bootstrap 4](https://italia.github.io/bootstrap-italia/1.x/docs/utilities/colori/)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Hidden →** imposta il campo nascosto o no  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Disabled →** disabilita il campo e lo mette in sola lettura e non salva i dati.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Table View →** visualizza o meno il campo nella vista lista

**Validation**:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Required →** rende il campo obbligatorio nel form  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Unique →** controlla che il valore del campo sia univoco del db, rende il campo 
 		 obbligatorio nel form  
**Api**:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Property Name →** è il nome del campo nel database  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Custom Properties →** questa configurazione  dipende dal tipo funzionalità che 
aggiunge il  campo; si veda la documentazione specifica dei componenti  
**Conditional**:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Advanced Conditions Json-logic bookmark  
**Logic**:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Json-logic bookmark  
<font color="red">Nei componenti **non** sono gestite le seguenti proprietà:</font>  
**Display**:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Label Position  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Initial Focus   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hide Label   
**Validation**:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Validate On, Error Label, Custom Error Message, Custom Validation, JSONLogic-Validation  
**API**:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Field Tags  
**Conditional**:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Simple  

### Icone  
Per quanto riguarda le icone e le immagini disponibili nelle interfacce fare riferimento alla [guida ufficiale AGID.](https://italia.github.io/bootstrap-italia/docs/utilities/icone/)




